from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ["pt-BR", "en-US", "es-ES"]
CONTACT_EMAIL = "vcdevelopstudio@gmail.com"
SITE_FILES = [
    "index.html",
    "privacy-policy.html",
    "terms-of-use.html",
    "assets/site.css",
    "assets/site.js",
    "data/privacy_policy.json",
    "data/terms_of_use.json",
    ".github/workflows/deploy-pages.yml",
    ".gitignore",
    ".nojekyll",
]


def load_document(name: str) -> dict[str, dict[str, object]]:
    path = ROOT / "data" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


class LegalSiteContractTest(unittest.TestCase):
    def test_public_site_includes_the_required_documents_and_deployment_files(self) -> None:
        """A missing legal page or Pages workflow leaves the public requirement incomplete."""
        for relative_path in SITE_FILES:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_privacy_policy_keeps_all_required_sections_and_support_contact(self) -> None:
        """Dropping a privacy topic would make the public policy diverge from the game."""
        policy = load_document("privacy_policy")
        expected_sections = [
            "overview",
            "local_data",
            "billing",
            "tts",
            "children",
            "sharing",
            "security",
            "retention",
            "deletion",
            "changes",
            "website",
            "contact",
            "age_signals",
            "access_cache",
            "sdk_diagnostics",
        ]
        expected_back_labels = {
            "pt-BR": "Voltar",
            "en-US": "Back",
            "es-ES": "Volver",
        }
        self.assertEqual(list(policy), LANGUAGES)
        for language, document in policy.items():
            self.assertEqual(document["contact"], CONTACT_EMAIL, language)
            self.assertIn("VC Develop Studio", document.get("publisher", ""), language)
            self.assertEqual(document["back"], expected_back_labels[language], language)
            sections = document["sections"]
            self.assertEqual([section["id"] for section in sections], expected_sections, language)

    def test_terms_cover_the_required_rules_in_every_supported_language(self) -> None:
        """A missing commercial rule could leave a family without essential legal information."""
        terms = load_document("terms_of_use")
        expected_sections = [
            "personal_use",
            "one_time_purchase",
            "no_subscription",
            "google_play",
            "adult_responsibility",
            "intellectual_property",
            "support",
            "updates",
            "consumer_rights",
            "access_cache",
            "age_signals",
        ]
        self.assertEqual(list(terms), LANGUAGES)
        for language, document in terms.items():
            self.assertEqual(document["contact"], CONTACT_EMAIL, language)
            self.assertIn("VC Develop Studio", document.get("publisher", ""), language)
            sections = document["sections"]
            self.assertEqual([section["id"] for section in sections], expected_sections, language)

    def test_billing_disclosure_includes_the_transaction_token_and_separates_support_and_website(self) -> None:
        """Purchase acknowledgment and contacting support have different data practices from playing."""
        policy = load_document("privacy_policy")
        for language, document in policy.items():
            sections = {section["id"]: section for section in document["sections"]}
            self.assertIn("token", sections["billing"]["body"].lower(), language)
            self.assertIn("GitHub Pages", sections["website"]["body"], language)
            self.assertIn("IP", sections["website"]["body"], language)
            self.assertIn(CONTACT_EMAIL, sections["contact"]["body"], language)
            for section in sections.values():
                for link in section.get("links", []):
                    self.assertTrue(link["url"].startswith("https://"), link)
                    self.assertTrue(link["label"].strip(), link)

    def test_public_code_has_no_placeholder_or_tracking_integration(self) -> None:
        """A tracking or placeholder endpoint would contradict the site's privacy promises."""
        source_paths = [
            ROOT / "index.html",
            ROOT / "privacy-policy.html",
            ROOT / "terms-of-use.html",
            ROOT / "assets/site.css",
            ROOT / "assets/site.js",
        ]
        public_source = "\n".join(path.read_text(encoding="utf-8") for path in source_paths).lower()
        for forbidden in [
            "example.com",
            "googletagmanager",
            "document.cookie",
            "localstorage",
            "sessionstorage",
            "sendbeacon",
        ]:
            self.assertNotIn(forbidden, public_source)

    def test_pages_workflow_packages_only_the_static_site_root(self) -> None:
        """Deploying another path could accidentally expose unrelated material."""
        workflow = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
        for fragment in [
            "actions/configure-pages@v5",
            "actions/upload-pages-artifact@v3",
            "actions/deploy-pages@v4",
            "path: '_site'",
        ]:
            self.assertIn(fragment, workflow)


if __name__ == "__main__":
    unittest.main()
