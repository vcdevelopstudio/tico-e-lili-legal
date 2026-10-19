"""Disclosure regression for the approved PROD catalog in Brasil0.2.8+."""
import unittest
from test_brasil_legal_site import BASE, LANGUAGES, Page

WORDS={
 "":("antes do bloqueio parental","24 horas","mesma revisão","registra e armazena","não dispomos de prazo específico confirmado","mais jogos"),
 "en":("before the parental gate","24 hours","same revision","logs and stores","no confirmed specific retention period","more games"),
 "es":("antes de la barrera parental","24 horas","misma revisión","registra y almacena","no disponemos de un plazo específico confirmado","más juegos"),
}
class BrasilCatalogDisclosures(unittest.TestCase):
 def test_all_pages_identify_the_version_and_have_no_draft_banner(self):
  for folder in LANGUAGES.values():
   for document in ("privacy-policy.html","terms-of-use.html"):
    with self.subTest(folder=folder,document=document):
     page=Page((BASE/folder/document).read_text(encoding="utf8"));text=" ".join(page.text).lower()
     self.assertIn("0.2.8",text)
     self.assertNotIn("minuta",text);self.assertNotIn("draft —",text);self.assertNotIn("borrador",text)
     self.assertEqual([a.get("datetime") for t,a in page.tags if t=="time"],["2026-10-19"])
 def test_privacy_explains_actual_network_cache_and_host_limits(self):
  for folder in LANGUAGES.values():
   with self.subTest(folder=folder):
    page=Page((BASE/folder/"privacy-policy.html").read_text(encoding="utf8"));text=" ".join(page.text).lower()
    for word in WORDS[folder]+("vcdevelopstudio.github.io","github pages","https","ip"):
     self.assertTrue(word in text, "Missing disclosure: "+word)
    links=[a.get("href","") for t,a in page.tags if t=="a"]
    self.assertTrue(any(x.startswith("https://docs.github.com/") and "privacy" in x for x in links))
