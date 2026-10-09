import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class DiagnosticsDisclosureTest(unittest.TestCase):
 def test_complete_diagnostic_and_voice_claims_in_each_language(self):
  claims={
   'pt-BR': ['Os registros são encaminhados aos serviços do Google e podem permanecer em uma fila local persistente em disco para envio posterior.', 'Não comprar não equivale a desativar esses diagnósticos.', 'Não foi confirmado um prazo de retenção, anonimização ou exclusão desses registros nos servidores do Google; não prometemos essas condições.'],
   'en-US': ['Records are forwarded to Google services and may remain in a persistent local disk queue for later transmission.', 'Not buying does not mean disabling these diagnostics.', 'No retention period, anonymization or deletion of these records on Google servers has been confirmed; we do not promise these conditions.'],
   'es-ES': ['Los registros se envían a los servicios de Google y pueden permanecer en una cola local persistente en disco para su envío posterior.', 'No comprar no equivale a desactivar estos diagnósticos.', 'No se ha confirmado un plazo de conservación, anonimización o eliminación de estos registros en los servidores de Google; no prometemos esas condiciones.']}
  voice={
   'pt-BR':'A voz é usada para chamar os pais ou responsáveis na barreira de compra; não há narração das fases nem gravação da voz das crianças.',
   'en-US':'Voice is used to call parents or guardians at the purchase gate; there is no stage narration or recording of children’s voices.',
   'es-ES':'La voz se utiliza para llamar a los padres o responsables en la barrera de compra; no hay narración de las fases ni grabación de las voces de los niños.'}
  policy=json.loads((ROOT/'data/privacy_policy.json').read_text(encoding='utf-8'))
  terms=json.loads((ROOT/'data/terms_of_use.json').read_text(encoding='utf-8'))
  for lang,sentences in claims.items():
   ps={s['id']:s for s in policy[lang]['sections']};ts={s['id']:s for s in terms[lang]['sections']}
   for sentence in sentences:self.assertIn(sentence,ps['sdk_diagnostics']['body'])
   self.assertIn(voice[lang],ps['tts']['body'])
   for key in ['overview','billing','sharing','retention']:self.assertIn('15',ps[key]['body'])
   self.assertIn('15',ts['google_play']['body'])
   self.assertTrue(ps['sdk_diagnostics']['title'].startswith('15.'))
   self.assertIn('1.0.2',ps['overview']['body'])
   self.assertIn('1.0.2',ts['personal_use']['body'])
