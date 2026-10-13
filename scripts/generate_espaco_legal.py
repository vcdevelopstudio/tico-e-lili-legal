"""Generate the six Space documents; no game or store integration is implied."""
from pathlib import Path
import generate_cristal_legal as renderer

ROOT = Path(__file__).resolve().parents[1]
renderer.BASE = ROOT / 'viagem-pelo-espaco'
renderer.PUBLIC = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/viagem-pelo-espaco/'
renderer.BRAND = 'Tico e Lili : Uma Viagem Pelo Espaço'
renderer.DOCUMENTS = {'privacy-policy.html': 'espaco_privacy_policy',
                      'terms-of-use.html': 'espaco_terms_of_use'}


def generate():
    renderer.generate()
    # English is the explicit public default; retain the requested Portuguese URLs.
    for page in renderer.BASE.rglob('*.html'):
        file = page.name
        html = page.read_text(encoding='utf-8')
        html = html.replace(f'hreflang="x-default" href="{renderer.PUBLIC}{file}"',
                            f'hreflang="x-default" href="{renderer.PUBLIC}en/{file}"')
        page.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    generate()
