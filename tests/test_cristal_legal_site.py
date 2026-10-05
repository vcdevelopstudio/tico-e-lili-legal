from __future__ import annotations

import unittest
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "cristal-arco-iris"
LANGUAGES = {"pt-BR": "", "en-US": "en", "es-ES": "es"}
DOCUMENTS = {"terms-of-use.html": 9, "privacy-policy.html": 12}


class Page(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.text: list[str] = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class CristalLegalSiteTest(unittest.TestCase):
    def test_documents_are_readable_in_all_three_languages_without_javascript(self):
        for language, folder in LANGUAGES.items():
            for document, sections in DOCUMENTS.items():
                with self.subTest(language=language, document=document):
                    path = BASE / folder / document
                    self.assertTrue(path.is_file(), f"Missing public page: {path}")
                    source = path.read_text(encoding="utf-8")
                    page = Page(source)
                    self.assertIn(("html", {"lang": language}), page.tags)
                    self.assertEqual(sum(tag == "h2" for tag, _ in page.tags), sections)
                    self.assertFalse(any(tag == "script" for tag, _ in page.tags))
                    self.assertFalse(any("hidden" in attrs for _, attrs in page.tags))
                    content = " ".join(page.text)
                    data_name = document.replace("-", "_").replace(".html", ".json")
                    data = json.loads((ROOT / "data" / data_name).read_text(encoding="utf-8"))[language]
                    self.assertIn(data["updated"], content)
                    for section in data["sections"]:
                        self.assertIn(section["body"], content)
                    self.assertIn(("a", {"href": "mailto:vcdevelopstudio@gmail.com"}), page.tags)
                    self.assertIn("vcdevelopstudio@gmail.com", content)
                    self.assertIn("VC Develop Studio", content)
                    self.assertIn("Tico e Lili: Cristal Arco-Íris", content)
                    self.assertNotIn("A proposta de atendimento", content)
                    self.assertNotIn("The proposed support practice", content)
                    self.assertNotIn("La práctica de soporte propuesta", content)

    def test_language_links_and_document_links_keep_readers_in_the_same_game(self):
        for language, folder in LANGUAGES.items():
            for document in DOCUMENTS:
                with self.subTest(language=language, document=document):
                    path = BASE / folder / document
                    self.assertTrue(path.is_file(), f"Missing public page: {path}")
                    page = Page(path.read_text(encoding="utf-8"))
                    languages = [attrs for tag, attrs in page.tags if tag == "a" and "hreflang" in attrs]
                    self.assertEqual({a["hreflang"] for a in languages}, set(LANGUAGES))
                    for link in languages:
                        target = (path.parent / link["href"]).resolve()
                        self.assertEqual(target, (BASE / LANGUAGES[link["hreflang"]] / document).resolve())
                        self.assertEqual(link.get("aria-current") == "page", link["hreflang"] == language)
                    other_document = next(name for name in DOCUMENTS if name != document)
                    targets = [(path.parent / attrs["href"]).resolve() for tag, attrs in page.tags
                               if tag == "a" and attrs.get("href") and not urlsplit(attrs["href"]).scheme]
                    self.assertIn((path.parent / other_document).resolve(), targets)
                    self.assertTrue(all(BASE.resolve() in target.parents for target in targets if target.suffix == ".html"))

    def test_all_local_resources_exist_and_external_web_links_use_https(self):
        for folder in LANGUAGES.values():
            for document in DOCUMENTS:
                path = BASE / folder / document
                self.assertTrue(path.is_file(), f"Missing public page: {path}")
                page = Page(path.read_text(encoding="utf-8"))
                for tag, attrs in page.tags:
                    reference = attrs.get("src") or attrs.get("href")
                    if not reference or reference.startswith("#"):
                        continue
                    url = urlsplit(reference)
                    if url.scheme:
                        self.assertIn(url.scheme, ["https", "mailto"], reference)
                        self.assertNotIn(tag, ["script", "img", "iframe"], reference)
                    else:
                        self.assertTrue((path.parent / url.path).is_file(), reference)


if __name__ == "__main__":
    unittest.main()
