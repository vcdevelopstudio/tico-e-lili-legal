"""Build the Pages artifact from an explicit public-file allowlist."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def public_files():
    files = [ROOT / name for name in ['index.html', 'privacy-policy.html', 'terms-of-use.html', '.nojekyll', 'assets/site.css', 'assets/site.js', 'data/privacy_policy.json', 'data/terms_of_use.json']]
    for game in ['cristal-arco-iris', 'fauna-flora-brasil']:
        for folder in ['', 'en', 'es']:
            files.extend(ROOT / game / folder / name for name in ['privacy-policy.html', 'terms-of-use.html'])
        files.append(ROOT / game / 'assets/legal.css')
    files.extend(ROOT / 'fauna-flora-brasil/assets' / name for name in ['br.svg', 'us.svg', 'es.svg'])
    return files


def build(destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Use a new empty destination to prevent stale files in the artifact')
    destination.mkdir(parents=True)
    for source in public_files():
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


if __name__ == '__main__':
    import sys
    build(sys.argv[1])
