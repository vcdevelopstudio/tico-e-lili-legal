"""Generate additive language URLs without modifying the legacy pages.

Run: python scripts/generate_cristal_legal.py
Source of truth: data/privacy_policy.json and data/terms_of_use.json.
Commit the generated HTML alongside future legal text changes.
"""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'cristal-arco-iris'
PUBLIC = 'https://vcdevelopstudio.github.io/tico-e-lili-legal/cristal-arco-iris/'
BRAND = 'Tico e Lili: Cristal Arco-Íris'
LANGUAGES = {'pt-BR': '', 'en-US': 'en', 'es-ES': 'es'}
LABELS = {'pt-BR': ('Português', 'br', 'Pular para o conteúdo', 'Idioma', 'Documentos legais'),
          'en-US': ('English', 'us', 'Skip to content', 'Language', 'Legal documents'),
          'es-ES': ('Español', 'es', 'Saltar al contenido', 'Idioma', 'Documentos legales')}
DOCUMENTS = {'privacy-policy.html': 'privacy_policy', 'terms-of-use.html': 'terms_of_use'}


def generate():
    data = {file: json.loads((ROOT / 'data' / (name + '.json')).read_text(encoding='utf-8'))
            for file, name in DOCUMENTS.items()}
    for lang, folder in LANGUAGES.items():
        prefix = '../' if folder else ''
        root_prefix = '../../' if folder else '../'
        for file in DOCUMENTS:
            doc = data[file][lang]
            title = escape(doc['title'])
            relative = (folder + '/' if folder else '') + file
            alternates, switches = [], []
            for other, subdir in LANGUAGES.items():
                target = (subdir + '/' if subdir else '') + file
                label, flag, *_ = LABELS[other]
                current = ' aria-current="page"' if other == lang else ''
                alternates.append(f'    <link rel="alternate" hreflang="{other}" href="{PUBLIC}{target}">')
                switches.append(f'        <a href="{prefix}{target}" hreflang="{other}" lang="{other}"{current}><img src="{root_prefix}fauna-flora-brasil/assets/{flag}.svg" alt="" width="28" height="20">{label}</a>')
            nav = []
            for target in DOCUMENTS:
                current = ' aria-current="page"' if target == file else ''
                nav.append(f'        <a href="{target}"{current}>{escape(data[target][lang]["title"])}</a>')
            sections = []
            for section in doc['sections']:
                links = []
                for link in section.get('links', []):
                    if not link['url'].startswith('https://'):
                        raise ValueError('Expected HTTPS policy link')
                    links.append(f'          <p class="policy-link"><a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a></p>')
                sections.append('\n'.join([
                    f'        <section id="{escape(section["id"], quote=True)}">',
                    f'          <h2>{escape(section["title"])}</h2>',
                    f'          <p>{escape(section["body"])}</p>', *links, '        </section>']))
            _, _, skip, language_label, nav_label = LABELS[lang]
            html = '\n'.join([
                '<!doctype html>', f'<html lang="{lang}">', '  <head>',
                '    <meta charset="utf-8">',
                '    <meta name="viewport" content="width=device-width, initial-scale=1">',
                f'    <meta name="description" content="{title} — {BRAND}.">',
                f'    <title>{title} | {BRAND}</title>',
                f'    <link rel="canonical" href="{PUBLIC}{relative}">', *alternates,
                f'    <link rel="alternate" hreflang="x-default" href="{PUBLIC}{file}">',
                f'    <link rel="stylesheet" href="{root_prefix}assets/site.css">',
                f'    <link rel="stylesheet" href="{prefix}assets/legal.css">',
                '  </head>', '  <body>',
                f'    <a class="skip-link" href="#document-content">{skip}</a>',
                '    <header class="site-header">',
                '      <p class="eyebrow">VC Develop Studio</p>',
                f'      <p class="game-name">{BRAND}</p>',
                f'      <nav class="language-switcher" aria-label="{language_label}">',
                *switches, '      </nav>',
                f'      <nav class="document-nav" aria-label="{nav_label}">',
                *nav, '      </nav>', '    </header>',
                '    <main id="legal-document">',
                '      <article id="document-content" class="legal-content" tabindex="-1">',
                f'        <h1>{title}</h1>',
                f'        <p class="updated">{escape(doc["updated"])}</p>',
                f'        <p class="publisher">{escape(doc["publisher"])}</p>',
                *sections,
                f'        <p class="policy-link"><a href="mailto:{escape(doc["contact"], quote=True)}">{escape(doc["contact"])}</a></p>',
                '      </article>', '    </main>', '  </body>', '</html>', ''])
            path = BASE / folder / file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    generate()
