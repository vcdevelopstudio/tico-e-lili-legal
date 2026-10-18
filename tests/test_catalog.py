"""Publisher contract checks for the prepared v1 catalog, not app runtime approval."""
import hashlib
import json
import struct
import unittest
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class CatalogTest(unittest.TestCase):
    def test_reviewed_crystal_entry_and_localized_copy(self):
        raw = (ROOT / 'catalogo/v1/jogos.json').read_bytes()
        feed = json.loads(raw.decode('utf-8'))
        self.assertLessEqual(len(raw), 65536)
        self.assertEqual(set(feed), {'schema_version', 'revision', 'valid_until', 'games'})
        self.assertEqual(feed['schema_version'], 1)
        self.assertIs(type(feed['revision']), int)
        self.assertGreaterEqual(feed['revision'], 1)
        self.assertEqual(datetime.strptime(feed['valid_until'], '%Y-%m-%dT%H:%M:%SZ').year, 2026)
        self.assertEqual(len(feed['games']), 1)
        game = feed['games'][0]
        self.assertEqual(set(game), {'id', 'package_id', 'enabled', 'release_state', 'listing', 'icon_url', 'icon_sha256'})
        self.assertEqual(game['package_id'], 'com.engvcdevelop.ticoelili.cristalarcoiris')
        self.assertIs(game['enabled'], True)
        self.assertEqual(game['release_state'], 'production')
        expected = {
            'pt-BR': 'Conheça Tico e Lili: Cristal Arco-Íris. Fases 1 a 3 gratuitas; compra única para acesso às fases 4 a 10.',
            'en-US': 'Discover Tico e Lili: Cristal Arco-Íris. Stages 1–3 are free; a one-time purchase grants access to stages 4–10.',
            'es-ES': 'Descubre Tico e Lili: Cristal Arco-Íris. Fases 1 a 3 gratis; compra única para acceder a las fases 4 a 10.'}
        self.assertEqual(set(game['listing']), set(expected))
        for lang, text in expected.items():
            entry = game['listing'][lang]
            self.assertEqual(entry, {'title': 'Tico e Lili: Cristal Arco-Íris', 'description': text})
            self.assertLessEqual(len(entry['title']), 80)
            self.assertLessEqual(len(text), 180)
            self.assertFalse(any(c in text for c in '<>[]'))

    def test_icon_matches_trusted_host_digest_and_png_limits(self):
        game = json.loads((ROOT / 'catalogo/v1/jogos.json').read_text(encoding='utf-8'))['games'][0]
        url = urlsplit(game['icon_url'])
        self.assertEqual((url.scheme, url.netloc, url.query, url.fragment), ('https', 'vcdevelopstudio.github.io', '', ''))
        self.assertEqual(url.path, '/tico-e-lili-legal/catalogo/v1/icons/cristal-arco-iris-v2.png')
        icon = (ROOT / 'catalogo/v1/icons/cristal-arco-iris-v2.png').read_bytes()
        self.assertLessEqual(len(icon), 524288)
        self.assertEqual(icon[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack('>II', icon[16:24]), (512, 512))
        self.assertEqual(hashlib.sha256(icon).hexdigest(), game['icon_sha256'])
        self.assertEqual(game['icon_sha256'], '3ede99424e81bbd2c339e405245b220f922c8cf2dbe34f9c250cf5df2956c115')
