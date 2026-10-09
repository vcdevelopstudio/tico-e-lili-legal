"""Regression checks for reviewed claims, not merely feature-name presence.

Semantic equivalence still requires human/editorial review against the game code.
These sentences protect specific decisions from accidental removal or inversion.
"""
import json
import re
import unittest
from pathlib import Path
from test_cristal_legal_site import Page, LANGUAGES

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = {
 'pt-BR': {
  'cache': ['Nas versões que incorporam esse recurso, o aplicativo armazena localmente o identificador do produto, a versão do formato e um indicador de acesso previamente confirmado pelo Google Play.', 'Esse cache não contém dados de cartão, token de compra nem identificador de pedido.', 'O Google Play pode levar tempo para atualizar suas informações e uma revogação não é detectada enquanto o aparelho está offline.'],
  'age': ['Ausência de sinal, recusa de compartilhamento ou erro não comprova maioridade.', 'Sem bloqueio explícito conhecido, o fluxo de compra pode continuar com a barreira adulta e os controles do Google Play.'],
  'memory': 'No código examinado, esses sinais ficam somente em memória, sem gravação em arquivos, logs ou envio a servidor do estúdio.',
  'adult': 'A conta matemática separa a decisão de compra da brincadeira; não verifica idade, identidade ou consentimento legal.',
  'scope': 'As descrições de cache local de acesso comprado e Play Age Signals aplicam-se somente às versões que incorporam essas funcionalidades; não descrevem automaticamente versões anteriores ainda instaladas.',
  'date': '9 de outubro de 2026',
 },
 'en-US': {
  'cache': ['In versions that include this feature, the app stores the product identifier, format version and a flag indicating access previously confirmed by Google Play locally.', 'This cache contains no card details, purchase token or order identifier.', 'Google Play may take time to update its information, and revocation is not detected while the device is offline.'],
  'age': ['A missing signal, refusal to share or error does not prove adulthood.', 'Without a known explicit block, the purchase flow may continue with the adult gate and Google Play controls.'],
  'memory': 'In the code examined, these signals are held only in memory, without files, logs or transmission to a studio server.',
  'adult': 'The arithmetic question separates the purchase decision from play; it does not verify age, identity or legal consent.',
  'scope': 'The descriptions of the local purchased-access cache and Play Age Signals apply only to versions that include these features; they do not automatically describe earlier versions that remain installed.',
  'date': 'October 9, 2026',
 },
 'es-ES': {
  'cache': ['En las versiones que incorporan esta función, la aplicación guarda localmente el identificador del producto, la versión del formato y un indicador de acceso previamente confirmado por Google Play.', 'Esta caché no contiene datos de tarjeta, token de compra ni identificador de pedido.', 'Google Play puede tardar en actualizar su información y no se detecta una revocación mientras el dispositivo está sin conexión.'],
  'age': ['La ausencia de señal, la negativa a compartirla o un error no demuestra la mayoría de edad.', 'Sin un bloqueo explícito conocido, el flujo de compra puede continuar con la barrera para adultos y los controles de Google Play.'],
  'memory': 'En el código examinado, estas señales se mantienen solo en memoria, sin archivos, logs ni envío a un servidor del estudio.',
  'adult': 'La operación matemática separa la decisión de compra del juego; no verifica edad, identidad ni consentimiento legal.',
  'scope': 'Las descripciones de la caché local del acceso comprado y Play Age Signals se aplican solo a las versiones que incorporan estas funciones; no describen automáticamente versiones anteriores que sigan instaladas.',
  'date': '9 de octubre de 2026',
 },
}


class AgeCacheLegalTest(unittest.TestCase):
 def test_reviewed_claims_and_cross_references_in_all_languages(self):
  for lang,claims in CLAIMS.items():
   documents={name:json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))[lang] for name in ['privacy_policy','terms_of_use']}
   sections={name:{s['id']:s for s in doc['sections']} for name,doc in documents.items()}
   policy,terms=sections['privacy_policy'],sections['terms_of_use']
   self.assertIn(claims['memory'],policy['age_signals']['body'])
   for sentence in claims['cache']:self.assertIn(sentence,policy['access_cache']['body'])
   for sentence in claims['age']:
    for document in [policy,terms]:self.assertIn(sentence,document['age_signals']['body'])
   self.assertIn(claims['adult'],policy['children']['body'])
   self.assertIn(claims['adult'],terms['adult_responsibility']['body'])
   for name,key in [('privacy_policy','overview'),('terms_of_use','personal_use')]:
    self.assertIn(claims['scope'],sections[name][key]['body'])
    doc=documents[name]
    self.assertIn(claims['date'],doc['updated'])
    self.assertEqual(doc['contact'],'vcdevelopstudio@gmail.com')
    self.assertEqual([int(s['title'].split('.')[0]) for s in doc['sections']],list(range(1,len(doc['sections'])+1)))
    self.assertEqual(len({s['id'] for s in doc['sections']}),len(doc['sections']))
   # Explicit targets: age=13/cache=14 in privacy, age=11 in terms.
   self.assertTrue(policy['age_signals']['title'].startswith('13.'))
   self.assertTrue(policy['access_cache']['title'].startswith('14.'))
   self.assertTrue(terms['age_signals']['title'].startswith('11.'))
   for sid,numbers in [('children',[3,12,13,14]),('local_data',[14]),('retention',[13,14,15]),('sharing',[3,4,11,12,13,15])]:
    self.assertEqual(set(map(int,re.findall(r'\b\d+\b',policy[sid]['body']))),set(numbers))
   self.assertEqual(re.findall(r'\b\d+\b',terms['adult_responsibility']['body']),['11'])
   self.assertEqual(re.findall(r'\b\d+\b',terms['age_signals']['body']),['13'])
   self.assertEqual(re.findall(r'\b\d+\b',terms['access_cache']['body']),['14'])

 def test_static_sections_exactly_match_json_order_and_content(self):
  for lang,folder in LANGUAGES.items():
   for filename,data_name in [('privacy-policy.html','privacy_policy'),('terms-of-use.html','terms_of_use')]:
    doc=json.loads((ROOT/'data'/f'{data_name}.json').read_text(encoding='utf-8'))[lang]
    source=(ROOT/'cristal-arco-iris'/folder/filename).read_text(encoding='utf-8')
    blocks=re.findall(r'<section id="([^"]+)">(.*?)</section>',source,re.S)
    self.assertEqual([sid for sid,_ in blocks],[s['id'] for s in doc['sections']])
    for (_,block),section in zip(blocks,doc['sections']):
     actual=[text.strip() for text in Page(block).text if text.strip()]
     self.assertEqual(actual,[section['title'],section['body']]+[link['label'] for link in section.get('links',[])])
    self.assertNotIn('\ufffd',source)
