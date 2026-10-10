import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PackageTest(unittest.TestCase):
    def test_package_contains_only_public_files_and_preserves_brasil(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'site'
            module.build(output)
            files = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
            self.assertEqual(len(files), 32)
            self.assertFalse(any(p.startswith(('docs/', 'tests/', 'scripts/', '.github/')) for p in files))
            self.assertFalse(any(p.endswith(('.png', '.py', '.jpg')) for p in files))
            for relative in files:
                self.assertEqual((output / relative).read_bytes(), (ROOT / relative).read_bytes())
            self.assertIn('fauna-flora-brasil/es/privacy-policy.html', files)
            self.assertIn('cristal-arco-iris/en/terms-of-use.html', files)
            for folder in ['', 'en/', 'es/']:
                for document in ['privacy-policy.html', 'terms-of-use.html']:
                    self.assertIn(f'misterios-fundo-do-mar/{folder}{document}', files)
            self.assertIn('misterios-fundo-do-mar/assets/legal.css', files)
