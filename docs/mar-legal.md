# Documentos legais de Tico e Lili: Mistérios do Fundo do Mar

Atualizados em 12/10/2026 para a versão comercial 0.1.0, código 5,
preparada para teste fechado. A integração implementada usa
GodotGooglePlayBilling 3.3.0 e Google Play Billing Library 9.1.0.

## Escopo e publicação

As seis páginas PT/EN/ES mantêm as URLs originais. A revisão remove os
avisos de minuta, integração futura e ausência de compras, além do
`noindex, nofollow` inserido pelo gerador inicial. O pacote público continua
com 32 arquivos. Somente dados, páginas, gerador e documentação do Mar
foram alterados; os documentos dos outros jogos são preservados.

A publicação usa o workflow existente, acionado por push em main. Após
o deploy, conferir o conteúdo integral servido, sem login, nas seis URLs.
HTTP 200 sozinho não comprova que os textos novos estejam disponíveis.

## Fonte técnica

Contexto completo fornecido pelo responsável:

`C:/Users/victo/ai-vc-develop/.repo/ticoelilimar/tasks/us/US-017-google-play-billing/evidencias/ciclos/CICLO-005/prompt-paginas-legais.txt`

Conferidos também os scripts `billing_service.gd`, `billing_policy.gd`
e o reset em `settings.gd` do projeto Mar. A caracterização do SDK/DEX
é a inspeção estática relatada no contexto, não uma captura de tráfego
realizada nesta entrega nem auditoria dos servidores Google.

## Comportamento descrito

- Fases 1–3 gratuitas; compra única permanente, não consumível, para acesso
  às fases 4–10, sem assinatura. A progressão por conclusão é preservada.
  O bônus musical exige concluir a fase 10. Preço localizado consultado da
  Play, sem preço universal fixado no texto.
- Produto configurado: `tico_lili_mar_full_game`, opção `full-game`.
  Pacote comercial: `com.engvcdevelop.ticoelilimar`.
- Startup comercial inicia Billing e consulta catálogo/propriedade; retorno
  ao app reconsulta; Restaurar consulta Play. Tokens/estado tratados em
  memória para consulta e ACK; sem backend de validação do estúdio.
- Cache próprio separado: produto, package, ambiente e booleano owned.
  Não persiste token, conta/e-mail, cartão ou pedido.
- Reset preserva compra, idioma, volumes e biblioteca musical; pode deixar
  cópia anterior do progresso. Restaurar compra recupera direito de acesso,
  não progresso nem músicas. Limpar dados remove arquivos/cache/filas locais,
  sem cancelar a compra ou excluir registros Google.
- Progresso, preferências, livro e músicas locais. Bônus registra notas,
  tempos e títulos, sem microfone. Sem conta própria, chat, anúncios,
  analytics de gameplay, câmera ou localização. Narração local, sem TTS
  online. Release desativa backup automático do app (`allowBackup=false`).
- SDK: logger PLAY_BILLING_LIBRARY, DataTransport/CCT; ID aleatório de
  instância/sessão, package/versão SDK, Android, marca/modelo/fabricante,
  memória e Build.FINGERPRINT. Não confundir com Build.SERIAL,
  AAID/IMEI/Android ID persistente, Firebase Analytics ou Crashlytics.
- DataTransport 3.1.8 usa fila SQLite persistente. Diagnósticos automáticos
  operam antes da área parental e sem compra, sem opt-out implementado.
  Não prometer anonimato, efemeridade ou retenção/exclusão Google.
- Conta matemática é barreira de navegação, não verificação legal de
  idade/identidade/consentimento nem neutral age screen.

## Limites preservados

Transação, ACK, restauração e reinício offline físicos ainda não
homologados no contexto de 12/10/2026. Cache implementado não comprova
acesso offline após reinício em aparelho. Compra, preço e restauração
exigem rede. A publicação dos documentos não anuncia aprovação,
lançamento ou disponibilidade do jogo na Play.

Categorias/finalidades de Segurança dos dados são interpretação
fundamentada das regras gerais, não confirmação específica Google.
A exceção de compartilhamento esperado de uma ação iniciada pelo usuário
não é aplicada automaticamente aos diagnósticos, nem eles são tratados
automaticamente como prestador em nome do estúdio.

## Fontes externas conferidas em 12/10/2026

- [Segurança dos dados](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en)
- [Políticas para famílias](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en)
- [Versões do Google Play Billing](https://developer.android.com/google/play/billing/release-notes)
- [Testes do Google Play Billing](https://developer.android.com/google/play/billing/test)

## Manutenção e verificação

Fontes: `data/mar_privacy_policy.json` e `data/mar_terms_of_use.json`.
Gerador próprio reutiliza o renderer do Cristal sem alterar os textos dele.

```powershell
python scripts/generate_mar_legal.py
python -m unittest discover -s tests -v
```

Verificar correspondência entre JSONs e HTML, navegação PT/EN/ES, recursos
locais, remoção de afirmações antigas, data, limites comerciais e
reprodução determinística. Após o deploy, ler e comparar os seis corpos
públicos com os arquivos gerados; registrar o SHA e o resultado do workflow
na entrega. Suporte e privacidade: VC Develop Studio,
vcdevelopstudio@gmail.com. Atendimento por e-mail e visitas ao
GitHub Pages/IPs continuam descritos separadamente.

Verificação local de 12/10/2026: 18 testes existentes passaram. As seis
páginas corresponderam integralmente às fontes JSON, com versão/data,
seções coerentes, links entre idiomas e recursos válidos, sem avisos antigos
ou noindex. Gerar novamente preservou o conteúdo dos seis arquivos.
