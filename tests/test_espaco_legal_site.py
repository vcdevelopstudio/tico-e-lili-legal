import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit
from test_cristal_legal_site import Page

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'viagem-pelo-espaco'
LANGUAGES = {'pt-BR': '', 'en-US': 'en', 'es-ES': 'es'}


class EspacoLegalTest(unittest.TestCase):
    def test_six_pages_match_sources_and_keep_language_and_document_navigation(self):
        for lang, folder in LANGUAGES.items():
            for name, data_name in [('privacy-policy.html', 'espaco_privacy_policy'),
                                    ('terms-of-use.html', 'espaco_terms_of_use')]:
                with self.subTest(lang=lang, name=name):
                    path = BASE / folder / name
                    page = Page(path.read_text(encoding='utf-8'))
                    text = ' '.join(page.text)
                    data = json.loads((ROOT / 'data' / (data_name + '.json')).read_text(encoding='utf-8'))[lang]
                    self.assertIn(('html', {'lang': lang}), page.tags)
                    self.assertIn(data['title'], text)
                    self.assertIn(data['updated'], text)
                    self.assertIn('Tico e Lili : Uma Viagem Pelo Espaço', text)
                    self.assertEqual(sum(tag == 'h2' for tag, _ in page.tags), 9)
                    for section in data['sections']:
                        self.assertIn(section['body'], text)
                    self.assertFalse(any(tag == 'script' for tag, _ in page.tags))
                    switches = [a for tag, a in page.tags if tag == 'a' and 'hreflang' in a]
                    self.assertEqual({a['hreflang'] for a in switches}, set(LANGUAGES))
                    for a in switches:
                        self.assertEqual((path.parent / a['href']).resolve(),
                                         (BASE / LANGUAGES[a['hreflang']] / name).resolve())
                        self.assertEqual(a.get('aria-current') == 'page', a['hreflang'] == lang)
                    other = 'terms-of-use.html' if name == 'privacy-policy.html' else 'privacy-policy.html'
                    self.assertTrue(any(tag == 'a' and a.get('href') == other for tag, a in page.tags))
                    default = [a for tag, a in page.tags if tag == 'link' and a.get('hreflang') == 'x-default']
                    self.assertEqual(default[0]['href'], 'https://vcdevelopstudio.github.io/tico-e-lili-legal/viagem-pelo-espaco/en/' + name)
                    for tag, a in page.tags:
                        ref = a.get('src') or a.get('href')
                        if not ref or ref.startswith('#'):
                            continue
                        url = urlsplit(ref)
                        if url.scheme:
                            self.assertIn(url.scheme, ['https', 'mailto'])
                            self.assertNotIn(tag, ['script', 'iframe', 'img'])
                        else:
                            self.assertTrue((path.parent / url.path).is_file(), ref)

    def test_final_model_prices_and_no_inherited_sdk_claims(self):
        for lang in LANGUAGES:
            terms = json.loads((ROOT / 'data/espaco_terms_of_use.json').read_text(encoding='utf-8'))[lang]
            privacy = json.loads((ROOT / 'data/espaco_privacy_policy.json').read_text(encoding='utf-8'))[lang]
            combined = json.dumps([terms, privacy], ensure_ascii=False)
            self.assertIn('1–3', combined)
            self.assertIn('4–10', combined)
            self.assertIn('US$1.00' if lang == 'en-US' else 'US$1,00', combined)
            self.assertIn('R$2.99' if lang == 'en-US' else 'R$2,99', combined)
            for unverified in ['9.1.0', '3.3.0', 'DataTransport', 'PLAY_BILLING_LIBRARY',
                               'allowBackup=false', 'US-003', 'C:/', 'C:\\']:
                self.assertNotIn(unverified, combined)
            self.assertEqual([s['id'] for s in privacy['sections']],
                             ['scope', 'children', 'local', 'billing', 'offline', 'deletion', 'support', 'website', 'security'])
