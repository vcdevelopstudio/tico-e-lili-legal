"""Generate the six Folclore pages from their own approved source data."""
import generate_cristal_legal as renderer

renderer.BASE = renderer.ROOT / 'encantos-do-folclore'
renderer.PUBLIC = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/encantos-do-folclore/'
renderer.BRAND = 'Tico e Lili : Encantos do Folclore'
renderer.DOCUMENTS = {'privacy-policy.html': 'folclore_privacy_policy',
                      'terms-of-use.html': 'folclore_terms_of_use'}


def generate():
    renderer.generate()
    for page in renderer.BASE.rglob('*.html'):
        text = page.read_text(encoding='utf-8')
        text = text.replace(f'hreflang="x-default" href="{renderer.PUBLIC}{page.name}"',
                            f'hreflang="x-default" href="{renderer.PUBLIC}en/{page.name}"')
        page.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    generate()
