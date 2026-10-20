"""Exercise deployed metadata renewal without changing curated offers."""
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]


class CatalogRefreshTest(unittest.TestCase):
    def refresh_module(self):
        script = ROOT / 'scripts/refresh_catalog.py'
        self.assertTrue(script.is_file(), 'Published catalog needs bounded validity renewal')
        spec = importlib.util.spec_from_file_location('refresh_catalog', script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_renewal_preserves_offers_and_expires_within_24_hours(self):
        module = self.refresh_module()
        original = json.loads((ROOT / 'catalogo/v1/jogos.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'feed.json'
            path.write_text(json.dumps(original), encoding='utf-8')
            now = datetime(2026, 10, 20, 12, tzinfo=timezone.utc)
            result = module.refresh(path, now=now, previous_revision=original['revision'])
            self.assertEqual(result['games'], original['games'])
            self.assertEqual(result['schema_version'], original['schema_version'])
            expiry = datetime.strptime(result['valid_until'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            self.assertEqual((expiry - now).total_seconds(), 23 * 3600)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), result)

    def test_same_clock_and_higher_published_revision_never_reuse_revision(self):
        module = self.refresh_module()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'feed.json'
            path.write_text((ROOT / 'catalogo/v1/jogos.json').read_text(encoding='utf-8'), encoding='utf-8')
            now = datetime(2026, 10, 20, 12, tzinfo=timezone.utc)
            first = module.refresh(path, now=now, previous_revision=2_000_000_000)
            second = module.refresh(path, now=now, previous_revision=first['revision'])
            self.assertEqual(first['revision'], 2_000_000_001)
            self.assertEqual(second['revision'], 2_000_000_002)
            self.assertLess(second['revision'], 2**31)

    def test_invalid_revision_is_rejected_without_overwriting_feed(self):
        module = self.refresh_module()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'feed.json'
            content = (ROOT / 'catalogo/v1/jogos.json').read_bytes()
            path.write_bytes(content)
            with self.assertRaises(ValueError):
                module.refresh(path, previous_revision=2**53)
            self.assertEqual(path.read_bytes(), content)

    def test_missing_published_feed_requires_explicit_first_publication(self):
        module = self.refresh_module()
        error = HTTPError(module.PUBLIC, 404, 'Not Found', {}, None)
        with patch.object(module, 'urlopen', side_effect=error):
            with self.assertRaises(HTTPError):
                module.published_revision()
            self.assertEqual(module.published_revision(allow_bootstrap=True), 0)
