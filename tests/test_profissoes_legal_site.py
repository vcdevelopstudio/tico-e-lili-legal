import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit
from test_cristal_legal_site import Page

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'profissoes'
LANGUAGES = {'pt-BR': '', 'en-US': 'en', 'es-ES': 'es'}


class ProfissoesLegalTest(unittest.TestCase):
    def test_six_pages_match_sources_and_keep_language_and_document_navigation(self):
        for lang, folder in LANGUAGES.items():
            for name, data_name in [('privacy-policy.html', 'profissoes_privacy_policy'),
                                    ('terms-of-use.html', 'profissoes_terms_of_use')]:
                with self.subTest(lang=lang, name=name):
                    path = BASE / folder / name
                    page = Page(path.read_text(encoding='utf-8'))
                    text = ' '.join(page.text)
                    data = json.loads((ROOT / 'data' / (data_name + '.json')).read_text(encoding='utf-8'))[lang]
                    self.assertIn(('html', {'lang': lang}), page.tags)
                    self.assertIn(data['title'], text)
                    self.assertIn(data['updated'], text)
                    self.assertIn('Tico e Lili: Profissões', text)
                    self.assertEqual(sum(tag == 'h2' for tag, _ in page.tags), len(data['sections']))
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
                    self.assertEqual(default[0]['href'], 'https://vcdevelopstudio.github.io/tico-e-lili-legal/profissoes/en/' + name)
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

    def test_family_commercial_model_with_catalog_and_undecided_price(self):
        # Pedido do responsável (23/11): igual aos outros jogos, com compra e a lista "Mais jogos".
        stale = ['em desenvolvimento', 'ainda não foi confirmad', 'ainda não estão confirmad', 'in development',
                 'not yet confirmed', 'not been confirmed', 'en desarrollo', 'aún no se ha confirmado', 'aún no están confirmad']
        for lang in LANGUAGES:
            terms = json.loads((ROOT / 'data/profissoes_terms_of_use.json').read_text(encoding='utf-8'))[lang]
            privacy = json.loads((ROOT / 'data/profissoes_privacy_policy.json').read_text(encoding='utf-8'))[lang]
            combined = json.dumps([terms, privacy], ensure_ascii=False)
            with self.subTest(lang=lang):
                self.assertIn('1–3', combined)
                self.assertIn('4–10', combined)
                for fact in ['com.engvcdevelop.ticoelili.profissoes', 'GodotGooglePlayBilling', 'Google Play Billing Library',
                             'DataTransport', 'https://vcdevelopstudio.github.io/tico-e-lili-legal/catalogo/familia/v1/jogos.json']:
                    self.assertIn(fact, combined)
                # Preço e versões do SDK só depois do build comercial do Profissões.
                for wrong in stale + ['US$', 'R$', '3.3.0', '9.1.0', '0.9.0', '.hml', 'ticoeliliespaco', 'US-0', 'C:/', 'C:\\']:
                    self.assertNotIn(wrong, combined)
                for outro_jogo in ['Sabores', 'comida', 'food', 'Espaço', 'Space', 'Espacio', 'foguete', 'rocket',
                                   'viagem', 'journey', 'viaje']:
                    self.assertNotIn(outro_jogo, combined)
                self.assertEqual([s['id'] for s in privacy['sections']],
                                 ['scope', 'children', 'local', 'billing', 'diagnostics', 'offline',
                                  'catalog', 'deletion', 'support', 'website', 'security'])


if __name__ == '__main__':
    unittest.main()
