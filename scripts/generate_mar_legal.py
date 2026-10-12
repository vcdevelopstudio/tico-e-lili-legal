"""Generate Mar legal pages with the shared Cristal renderer.

Run: python scripts/generate_mar_legal.py
Sources: data/mar_privacy_policy.json and data/mar_terms_of_use.json.
The JSON sources describe the commercial integration and its validation limits.
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


if __name__ == '__main__':
    generate()
