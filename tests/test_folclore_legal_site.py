import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit
from test_cristal_legal_site import Page

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'encantos-do-folclore'
PUBLIC = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/encantos-do-folclore/'


class FolcloreLegalTest(unittest.TestCase):
    def test_six_public_documents_match_approved_sources_and_all_links_resolve(self):
        for lang, folder in {'pt-BR': '', 'en-US': 'en', 'es-ES': 'es'}.items():
            for filename, data_name in [('privacy-policy.html', 'privacy_policy'),
                                        ('terms-of-use.html', 'terms_of_use')]:
                with self.subTest(lang=lang, filename=filename):
                    path = BASE / folder / filename
                    page = Page(path.read_text(encoding='utf-8'))
                    doc = json.loads((ROOT / 'data' / f'folclore_{data_name}.json').read_text(encoding='utf-8'))[lang]
                    text = ' '.join(page.text)
                    self.assertIn(('html', {'lang': lang}), page.tags)
                    self.assertIn('Tico e Lili : Encantos do Folclore', text)
                    self.assertIn(doc['updated'], text)
                    for section in doc['sections']:
                        self.assertIn(section['body'], text)
                    self.assertFalse(any(tag in ('script', 'iframe') for tag, _ in page.tags))
                    self.assertEqual({a['hreflang'] for tag, a in page.tags if tag == 'a' and 'hreflang' in a},
                                     {'pt-BR', 'en-US', 'es-ES'})
                    default = [a for tag, a in page.tags if tag == 'link' and a.get('hreflang') == 'x-default']
                    self.assertEqual(default[0]['href'], PUBLIC + 'en/' + filename)
                    for tag, attrs in page.tags:
                        ref = attrs.get('href') or attrs.get('src')
                        if not ref or ref.startswith('#'):
                            continue
                        parts = urlsplit(ref)
                        if parts.scheme:
                            self.assertIn(parts.scheme, ('https', 'mailto'))
                        else:
                            self.assertTrue((path.parent / parts.path).is_file(), ref)

    def test_disclosures_are_folclore_specific_and_do_not_publish_private_evidence(self):
        for lang in ('pt-BR', 'en-US', 'es-ES'):
            data = json.loads((ROOT / 'data/folclore_privacy_policy.json').read_text(encoding='utf-8'))[lang]
            text = json.dumps(data, ensure_ascii=False)
            for term in ['com.engvcdevelop.ticoelili.folclore', '1–3', '4–10', 'DataTransport/CCT',
                         '3.3.0', '9.1.0', 'token', 'AAID', 'Google']:
                self.assertIn(term, text)
            for private in ['C:/', 'C:\\', 'BEGIN PUBLIC KEY', '131561382', '.local/', 'signing.json']:
                self.assertNotIn(private, text)
            self.assertEqual(len(data['sections']), 7)
