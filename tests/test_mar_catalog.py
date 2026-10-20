"""Check the Mar-specific public offer without changing Brasil's schema."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MarCatalogTest(unittest.TestCase):
    def test_mar_offer_is_only_public_crystal_with_localized_purchase_disclosure(self):
        raw = (ROOT / 'catalogo/mar/v1/jogos.json').read_bytes()
        self.assertLessEqual(len(raw), 65536)
        feed = json.loads(raw)
        self.assertEqual(feed['schema_version'], 1)
        self.assertIs(type(feed['revision']), int)
        self.assertEqual(len(feed['games']), 1)
        game = feed['games'][0]
        self.assertEqual(game['package_id'], 'com.engvcdevelop.ticoelili.cristalarcoiris')
        self.assertIs(game['enabled'], True)
        self.assertEqual(game['release_state'], 'production')
        self.assertIs(game['has_in_app_purchases'], True)
        self.assertEqual(set(game['listing']), {'pt-BR', 'en-US', 'es-ES'})
        for copy in game['listing'].values():
            self.assertTrue(copy['title'].strip())
            self.assertTrue(copy['description'].strip())
        prefix = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/'
        self.assertTrue(game['icon_url'].startswith(prefix + 'catalogo/v1/icons/'))
        icon = ROOT / game['icon_url'].removeprefix(prefix)
        self.assertEqual(hashlib.sha256(icon.read_bytes()).hexdigest(), game['icon_sha256'])
        brasil = json.loads((ROOT / 'catalogo/v1/jogos.json').read_bytes())
        original_game = brasil['games'][0]
        self.assertNotIn('has_in_app_purchases', original_game)
        self.assertEqual({k: v for k, v in game.items() if k != 'has_in_app_purchases'}, original_game)

    def test_mar_seed_is_renewed_for_23_hours_without_altering_the_offer(self):
        spec = importlib.util.spec_from_file_location('refresh_catalog', ROOT / 'scripts/refresh_catalog.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        source = (ROOT / 'catalogo/mar/v1/jogos.json').read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'jogos.json'
            target.write_bytes(source)
            now = datetime(2026, 10, 20, 12, tzinfo=timezone.utc)
            result = module.refresh(target, now=now, previous_revision=2_000_000_000)
            self.assertEqual(result['revision'], 2_000_000_001)
            self.assertEqual(result['valid_until'], '2026-10-21T11:00:00Z')
            self.assertEqual(result['games'], json.loads(source)['games'])
            self.assertLessEqual(target.stat().st_size, 65536)
