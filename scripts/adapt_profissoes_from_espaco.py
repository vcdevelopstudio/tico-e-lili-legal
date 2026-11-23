"""One-off adaptation (2026-11-23): Profissões adopts the Espaço commercial texts.

The guardian asked for the same model as the other family games: one-time Google Play
purchase and the "Mais jogos" family catalog. Version numbers of the SDK stay out because
the Profissões build with billing does not exist yet; the price stays undecided.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'com.engvcdevelop.ticoelili.profissoes'
UPDATED = {'pt-BR': ('Atualizada em 23 de novembro de 2026', 'Atualizados em 23 de novembro de 2026'),
           'en-US': ('Updated on November 23, 2026', 'Updated on November 23, 2026'),
           'es-ES': ('Actualizada el 23 de noviembre de 2026', 'Actualizados el 23 de noviembre de 2026')}
PRIVACY_SCOPE = {
    'pt-BR': f'Esta política é destinada aos responsáveis por crianças que utilizam Tico e Lili: Profissões, jogo sobre as profissões da cidade para Android, pacote {PACKAGE}, pensado para crianças de 3–5 anos. Ela descreve a versão comercial, com a compra pelo Google Play e a área “Mais jogos”, no mesmo modelo dos outros jogos da família Tico e Lili. Publicar esta política não anuncia disponibilidade do aplicativo nem aprovação da Google, e não altera versões já instaladas.',
    'en-US': f'This policy is for the parents and guardians of children who use Tico e Lili: Profissões, a game about the jobs people do in town, for Android, package {PACKAGE}, designed for children aged 3–5. It describes the commercial version, with purchasing through Google Play and the “More games” area, following the same model as the other Tico e Lili family games. Publishing this policy does not announce the app’s availability or Google’s approval, and does not change versions already installed.',
    'es-ES': f'Esta política está dirigida a los responsables de los niños que usan Tico e Lili: Profissões, juego sobre las profesiones de la ciudad para Android, paquete {PACKAGE}, pensado para niños de 3–5 años. Describe la versión comercial, con la compra a través de Google Play y el área “Más juegos”, con el mismo modelo de los demás juegos de la familia Tico e Lili. Publicar esta política no anuncia la disponibilidad de la aplicación ni la aprobación de Google, y no modifica versiones ya instaladas.',
}
TERMS_SCOPE = {
    'pt-BR': f'Estes termos regem Tico e Lili: Profissões, jogo infantil sobre as profissões da cidade para celulares e tablets Android, pacote {PACKAGE}, em orientação vertical, com português, inglês e espanhol. É pensado para crianças de 3–5 anos, com acompanhamento de uma pessoa responsável. VCDevelopStudio é o responsável pelo produto. A versão comercial integra a compra pelo Google Play com GodotGooglePlayBilling e a Google Play Billing Library, como os outros jogos da família; estes documentos não anunciam lançamento nem aprovação da Google.',
    'en-US': f'These terms govern Tico e Lili: Profissões, a children’s game about the jobs people do in town, for Android phones and tablets, package {PACKAGE}, in portrait orientation, in Portuguese, English and Spanish. It is designed for children aged 3–5, with a guardian’s supervision. VCDevelopStudio is responsible for the product. The commercial version integrates purchasing through Google Play with GodotGooglePlayBilling and the Google Play Billing Library, like the other family games; these documents do not announce a launch or Google’s approval.',
    'es-ES': f'Estos términos rigen Tico e Lili: Profissões, juego infantil sobre las profesiones de la ciudad para teléfonos y tabletas Android, paquete {PACKAGE}, en orientación vertical, en portugués, inglés y español. Está pensado para niños de 3–5 años, con el acompañamiento de un responsable. VCDevelopStudio es el responsable del producto. La versión comercial integra la compra a través de Google Play con GodotGooglePlayBilling y la Google Play Billing Library, como los demás juegos de la familia; estos documentos no anuncian lanzamiento ni aprobación de Google.',
}
SWAPS = [('continuar a viagem', 'continuar o jogo'), ('continue the journey', 'continue the game'),
         ('continuar el viaje', 'continuar el juego'), ('As páginas do Espaço', 'As páginas de Profissões'),
         ('The Space pages', 'The Profissões pages'), ('Las páginas del Espacio', 'Las páginas de Profissões'),
         ('A viagem tem', 'O jogo tem'), ('The journey has', 'The game has'), ('El viaje tiene', 'El juego tiene')]


def adapt(text):
    for old, new in SWAPS:
        text = text.replace(old, new)
    return re.sub(r' (3\.3\.0|9\.1\.0)', '', text)


def build(kind, scope, keep_price):
    espaco = json.loads((ROOT / f'data/espaco_{kind}.json').read_text(encoding='utf-8'))
    current = json.loads((ROOT / f'data/profissoes_{kind}.json').read_text(encoding='utf-8'))
    for lang, doc in espaco.items():
        doc['updated'] = UPDATED[lang][0 if kind == 'privacy_policy' else 1]
        for section in doc['sections']:
            section['body'] = adapt(section['body'])
            if section['id'] == 'scope':
                section['body'] = scope[lang]
            if keep_price and section['id'] == 'price':
                section.update(next(s for s in current[lang]['sections'] if s['id'] == 'price'))
    (ROOT / f'data/profissoes_{kind}.json').write_text(json.dumps(espaco, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    build('privacy_policy', PRIVACY_SCOPE, keep_price=False)
    build('terms_of_use', TERMS_SCOPE, keep_price=True)
