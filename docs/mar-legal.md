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

## Atualização Mais jogos de 20/10/2026

O responsável confirmou nesta conversa que endpoint, hospedagem e tratamento
de dados devem seguir o que foi feito no Brasil. A referência foi conferida
nos documentos Brasil publicados pelo commit 021ca8c e nas fontes do GitHub.
Essa confirmação resolve a adoção documental da hospedagem para o Mar;
não altera a configuração nem ativa o aplicativo.

| Fato | Tratamento adotado nos documentos do Mar |
| --- | --- |
| Conteúdo e endpoint | VC Develop Studio; https://vcdevelopstudio.github.io/tico-e-lili-legal/catalogo/v1/jogos.json |
| Operador e imagens | GitHub Pages, infraestrutura de entrega do GitHub; host vcdevelopstudio.github.io, ícones sob /tico-e-lili-legal/catalogo/v1/icons/ |
| IP e logs | IP, caminho e cabeçalhos técnicos para entrega e segurança; Pages registra e armazena IP mesmo sem login. Sem garantia de anonimato, efemeridade ou exclusão imediata |
| Retenção | Sem prazo específico confirmado para os logs do Pages. A declaração geral do GitHub usa finalidades e obrigações aplicáveis como critérios; não inventar dias nem confundir TTL das ofertas com retenção remota |
| Ativação | Catálogo real do Mar continua enabled=false, endpoint e allowlists vazios, conforme leitura em 20/10/2026. Textos delimitam a condição de habilitação e não anunciam uma versão ativa |
| Ofertas | Só pacotes com publicação pública comprovada podem ser exibidos; não inserir ofertas ou pacotes no Mar por esta entrega |

As seis páginas recebem nova seção: 12 na privacidade e 8 nos termos. Os
encerramentos passam a 13 e 9. Data de revisão: 20/10/2026. Escopo mantém
explícito o catálogo desativado; o fluxo de downloads e saída para a loja só
se aplica quando habilitado. A redação distingue promoção própria opcional
de publicidade de terceiros, preservando os fatos de Billing.

Preservadas as seções de compra, SDK/diagnósticos, cache comercial, reset,
restauração, áudio e suporte. Não copiar do Brasil a versão 0.2.8, o TTS
parental ou a regra específica de primeira aceitação por revisão. No Mar,
o código examinado guarda accepted_at, invalidated e ícones por hash; a
validade é limitada por valid_until e 24h desde a aceitação local, sem
afirmar lista offline homologada. A voz parental examinada usa arquivos
locais e prefer_native_voice=false. Nenhum código do jogo foi alterado.

Fontes reconferidas em 20/10/2026:

- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection
- https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement

A minuta de 19/10/2026 em docs/minutas permanece um registro de trabalho
fora do pacote público. As confirmações e o escopo condicional acima
substituem suas pendências de publicação dos documentos. Configuração,
ativação e validação física do catálogo pertencem à entrega do aplicativo.

Verificação local desta atualização: os 24 testes existentes passaram. Uma
comparação com HEAD confirmou a preservação integral das seções Billing,
diagnósticos, cache comercial, retenção/reset, áudio, dados locais e suporte
da política, além de compra/restauração, dados locais e direitos nos termos.
Conferidos os seis HTML, PT/EN/ES, numeração 13/9, links e data; a geração
foi determinística. Feed e ícone públicos responderam diretamente por HTTPS;
o JSON correspondeu ao arquivo local e o ícone ao hash declarado. O pacote
e os documentos dos outros jogos não foram alterados.

## Ativação solicitada em 20/10/2026

O responsável pediu habilitar o recurso para preparar o lançamento. A
configuração real do Mar foi ligada para a próxima build, com apenas o
Cristal público na allowlist e o Mar fechado excluído. Instalações anteriores
não mudam por atualizar documentos ou configuração-fonte.

O smoke test isolado reproduziu quatro falhas: recurso desligado,
endpoint/hosts vazios, pacotes vazios e feed incompatível. A revisão detectou
que o Brasil exige exatamente os campos do schema original; acrescentar
has_in_app_purchases ao feed compartilhado quebraria esse cliente. Por isso
foi criada a variante https://vcdevelopstudio.github.io/tico-e-lili-legal/catalogo/mar/v1/jogos.json
com o campo de compra exigido pelo Mar, preservando integralmente o feed
catalogo/v1/jogos.json do Brasil e os mesmos ícones aprovados.

O workflow Pages renova somente revision e valid_until dessa variante em
cada deploy e a cada 6 horas. Usa revisão maior que a fonte, a publicação
anterior e o relógio UTC em segundos, dentro do limite inteiro suportado.
A validade é de 23 horas, respeitando o teto de 24h do cliente. O JSON
versionado é uma semente de curadoria; os metadados do artefato publicado
são derivados no build, sem commits automáticos ou mudanças de ofertas.
Nenhum cron é garantia de execução: atraso ou falha podem tornar a lista
indisponível. O cliente continua recusando dados expirados ou regressivos.

Os seis documentos descrevem o catálogo habilitado na configuração da
próxima versão, sem alegar que um APK/AAB antigo no teste fechado foi
atualizado. Os trechos Billing permanecem preservados. Ativação de fonte,
teste desktop, build Android, instalação, escuta e upload Play são resultados
distintos e devem ser comunicados separadamente.

Verificação da ativação: 28 testes Python e 193 verificações isoladas Godot
passaram (32 policy, 16 service, 8 integrity, 15 flow, 122 runtime). O teste
HTTPS real será registrado após servir a variante Mar. Revisão independente
confirmou preservação do schema Brasil e bootstrap restrito: HTTP 404 falha
normalmente; apenas workflow_dispatch com bootstrap_mar_catalog=true permite
a primeira publicação. Renovações futuras usam a revisão pública anterior
e falham em vez de reiniciar a sequência se o endpoint estiver ausente.
