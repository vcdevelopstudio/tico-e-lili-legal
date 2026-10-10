"""Generate draft Mar pages with the shared Cristal renderer.

Run: python scripts/generate_mar_legal.py
Sources: data/mar_privacy_policy.json and data/mar_terms_of_use.json.
Published drafts retain their notice and noindex until the purchase integration is reviewed.
"""
import generate_cristal_legal as renderer

renderer.BASE = renderer.ROOT / 'misterios-fundo-do-mar'
renderer.PUBLIC = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/misterios-fundo-do-mar/'
renderer.BRAND = 'Tico e Lili: Mistérios do Fundo do Mar'
renderer.DOCUMENTS = {
    'privacy-policy.html': 'mar_privacy_policy',
    'terms-of-use.html': 'mar_terms_of_use',
}


def generate():
    renderer.generate()
    for folder in renderer.LANGUAGES.values():
        for document in renderer.DOCUMENTS:
            path = renderer.BASE / folder / document
            html = path.read_text(encoding='utf-8')
            html = html.replace('  <head>\n', '  <head>\n    <meta name="robots" content="noindex, nofollow">\n', 1)
            path.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    generate()
