"""Family feed (FAM-28): one stable list read by every app that trusts the publisher prefix.

Launching a family game means adding it here once its Play page is public; no app update.
Mar still reads its own strict feed (closed package list) until it adopts FAM-28.
"""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
FEED = ROOT / 'catalogo/familia/v1/jogos.json'
PREFIX = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/'
BRASIL = 'com.engvcdevelop.ticoelilibrasil'
CRISTAL = 'com.engvcdevelop.ticoelili.cristalarcoiris'


def refresh_module():
    spec = importlib.util.spec_from_file_location('refresh_catalog', ROOT / 'scripts/refresh_catalog.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FamiliaCatalogTest(unittest.TestCase):
    def feed(self):
        raw = FEED.read_bytes()
        self.assertLessEqual(len(raw), 65536)
        return json.loads(raw)

    def test_offers_cristal_and_fauna_flora_in_production_with_purchase_disclosure(self):
        feed = self.feed()
        self.assertEqual(feed['schema_version'], 1)
        self.assertIs(type(feed['revision']), int)
        self.assertEqual([g['package_id'] for g in feed['games']], [CRISTAL, BRASIL])
        self.assertNotIn('com.engvcdevelop.ticoelili.folclore', {g['package_id'] for g in feed['games']})
        for game in feed['games']:
            self.assertIs(game['enabled'], True)
            self.assertEqual(game['release_state'], 'production')
            self.assertIs(game['has_in_app_purchases'], True)
            self.assertEqual(set(game['listing']), {'pt-BR', 'en-US', 'es-ES'})
            for copy in game['listing'].values():
                self.assertTrue(0 < len(copy['title']) <= 80)
                self.assertTrue(0 < len(copy['description']) <= 180)
            self.assertTrue(game['icon_url'].startswith(PREFIX + 'catalogo/v1/icons/'))
            icon = (ROOT / game['icon_url'].removeprefix(PREFIX)).read_bytes()
            self.assertLessEqual(len(icon), 524288)
            self.assertEqual(hashlib.sha256(icon).hexdigest(), game['icon_sha256'])

    def test_cristal_offer_is_identical_to_mar_and_brasil_matches_its_legal_page(self):
        feed = self.feed()
        mar = json.loads((ROOT / 'catalogo/mar/v1/jogos.json').read_bytes())
        self.assertEqual(feed['games'][0], mar['games'][0])
        brasil = feed['games'][1]
        self.assertEqual(brasil['listing']['pt-BR']['title'], 'Tico e Lili: Descobrindo a Fauna e Flora do Brasil')
        self.assertIn('Fases 1 a 3 gratuitas', brasil['listing']['pt-BR']['description'])
        self.assertIn('fases 4 a 10', brasil['listing']['pt-BR']['description'])
        self.assertIn('Stages 1–3 are free', brasil['listing']['en-US']['description'])
        self.assertIn('Fases 1 a 3 gratis', brasil['listing']['es-ES']['description'])
        policy = (ROOT / 'fauna-flora-brasil/privacy-policy.html').read_text(encoding='utf-8')
        self.assertIn('As fases 1 a 3 são gratuitas', policy)
        self.assertIn('fases 4 a 10', policy)

    def test_every_offer_is_a_public_family_package(self):
        for game in self.feed()['games']:
            self.assertTrue(game['package_id'].startswith('com.engvcdevelop.'))
            self.assertFalse(game['package_id'].endswith(('.hml', '.prototype')))
        self.assertFalse((ROOT / 'catalogo/folclore').exists(), 'one family list, never one per game')

    def test_mar_feed_still_offers_only_cristal(self):
        mar = json.loads((ROOT / 'catalogo/mar/v1/jogos.json').read_bytes())
        self.assertEqual([g['package_id'] for g in mar['games']], [CRISTAL])

    def test_refresh_uses_the_family_public_url_and_keeps_offers(self):
        module = refresh_module()
        self.assertEqual(module.public_url('catalogo/familia/v1/jogos.json'),
                         PREFIX + 'catalogo/familia/v1/jogos.json')
        self.assertEqual(module.public_url('catalogo/mar/v1/jogos.json'), PREFIX + 'catalogo/mar/v1/jogos.json')
        with self.assertRaises(ValueError):
            module.public_url('catalogo/desconhecido/jogos.json')
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'jogos.json'
            target.write_bytes(FEED.read_bytes())
            now = datetime(2026, 11, 12, 12, tzinfo=timezone.utc)
            result = module.refresh(target, now=now, previous_revision=2_000_000_000)
            self.assertEqual(result['revision'], 2_000_000_001)
            self.assertEqual(result['valid_until'], '2026-11-13T11:00:00Z')
            self.assertEqual(result['games'], self.feed()['games'])

    def test_workflow_renews_both_feeds_with_separate_bootstrap(self):
        workflow = (ROOT / '.github/workflows/deploy-pages.yml').read_text(encoding='utf-8')
        self.assertIn('scripts/refresh_catalog.py catalogo/familia/v1/jogos.json', workflow)
        self.assertIn('bootstrap_familia_catalog', workflow)
        self.assertIn('bootstrap_mar_catalog', workflow)

    def test_family_bootstrap_only_accepts_404_when_explicit(self):
        module = refresh_module()
        from urllib.error import HTTPError
        error = HTTPError(PREFIX + 'catalogo/familia/v1/jogos.json', 404, 'Not Found', {}, None)
        with patch.object(module, 'urlopen', side_effect=error):
            self.assertEqual(module.published_revision(PREFIX + 'catalogo/familia/v1/jogos.json', allow_bootstrap=True), 0)
            with self.assertRaises(HTTPError):
                module.published_revision(PREFIX + 'catalogo/familia/v1/jogos.json')


if __name__ == '__main__':
    unittest.main()
