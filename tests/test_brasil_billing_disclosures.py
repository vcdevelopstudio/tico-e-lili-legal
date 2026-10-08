"""Prevent stale purchase/diagnostic claims in any Brasil legal translation."""
from datetime import date
import unittest

from test_brasil_legal_site import BASE, DOCUMENTS, LANGUAGES, Page


PURCHASE = {
    "": ["fases 1 a 3 são gratuitas", "não consumível", "fases 4 a 10",
         "não há assinatura nem cobrança recorrente", "não pula a progressão",
         "consulta e restauração", "confirmação das transações", "desafio numérico",
         "verificação jurídica de idade ou identidade", "não cancela a compra"],
    "en": ["stages 1–3 are free", "non-consumable", "stages 4–10",
           "no subscription or recurring charge", "does not skip progression",
           "querying and restoring", "acknowledging transactions", "numeric challenge",
           "legal age or identity verification", "does not cancel the purchase"],
    "es": ["fases 1 a 3 son gratuitas", "no consumible", "fases 4 a 10",
           "no hay suscripción ni cobro recurrente", "no omite la progresión",
           "consulta y restauración", "confirmación de las transacciones", "desafío numérico",
           "verificación jurídica de edad o identidad", "no cancela la compra"],
}
PRIVACY = {
    "": ["9.1.0", "identificador temporário de sessão", "fila persistente local",
         "não efêmero", "não há opção no jogo para desativar", "inclusive quando ninguém realiza uma compra",
         "não grava tokens ou dados bancários", "encaminha o token ao google play",
         "produto, pacote do aplicativo e estado", "interpretação fundamentada",
         "não uma confirmação específica", "prazo de retenção confirmado",
         "não foi comprovada anonimização completa", "já enviados ao google"],
    "en": ["9.1.0", "temporary library session identifier", "persistent local queue",
           "non-ephemeral", "no option to disable", "even when no one makes a purchase",
           "does not store tokens or banking data", "sends the token to google play",
           "product, app package and access-entitlement state", "reasoned interpretation",
           "not a specific confirmation", "no confirmed retention period",
           "complete anonymization of these records has not been established", "already sent to google"],
    "es": ["9.1.0", "identificador temporal de sesión", "cola persistente local",
           "no es efímero", "no ofrece una opción para desactivar", "incluso cuando nadie realiza una compra",
           "no guarda tokens ni datos bancarios", "envía el token a google play",
           "producto, el paquete de la aplicación y el estado", "interpretación fundamentada",
           "no una confirmación específica", "plazo de conservación confirmado",
           "no se ha comprobado la anonimización completa", "ya enviados a google"],
}
STALE = [
    "compra planejada", "compra prevista", "planned purchase",
    "a integração ainda não foi implementada", "this integration has not been implemented",
    "esta integración todavía no se ha implementado", "sem bloqueio de pagamento",
    "without a payment restriction", "sin bloqueo de pago",
    "não utiliza análise de uso", "does not require its own account, show ads or use usage analytics",
    "no muestra anuncios ni utiliza análisis de uso", "2026-10-02",
]


class BrasilBillingDisclosureTest(unittest.TestCase):
    def text(self, folder, document):
        page = Page((BASE / folder / document).read_text(encoding="utf-8"))
        return page, " ".join(" ".join(page.text).split()).lower()

    def test_all_six_pages_disclose_implemented_purchase_without_stale_promises(self):
        for folder in LANGUAGES.values():
            for document in DOCUMENTS:
                with self.subTest(folder=folder, document=document):
                    page, text = self.text(folder, document)
                    for phrase in PURCHASE[folder] + ["datatransport/cct", "vcdevelopstudio@gmail.com"]:
                        self.assertIn(phrase, text)
                    for phrase in STALE:
                        self.assertNotIn(phrase, text)
                    dates = [attrs["datetime"] for tag, attrs in page.tags if tag == "time"]
                    self.assertEqual(len(dates), 1)
                    self.assertGreaterEqual(date.fromisoformat(dates[0]), date(2026, 10, 8))

    def test_privacy_separates_purchase_tokens_cache_and_automatic_diagnostics(self):
        for folder in LANGUAGES.values():
            with self.subTest(folder=folder):
                page, text = self.text(folder, "privacy-policy.html")
                for phrase in PRIVACY[folder] + ["https", "github pages"]:
                    self.assertIn(phrase, text)
                self.assertTrue(any(tag == "a" and attrs.get("href") == "https://policies.google.com/privacy"
                                    for tag, attrs in page.tags))


if __name__ == "__main__":
    unittest.main()
