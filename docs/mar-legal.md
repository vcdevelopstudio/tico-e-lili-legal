# Documentos legais de Tico e Lili: Mistérios do Fundo do Mar

Preparados em 10/10/2026 a pedido do responsável, para a futura versão com
Google Play Billing: fases 1–3 gratuitas e compra única das fases 4–10,
mantendo progressão por conclusão. Português, inglês e espanhol.

## Estado e publicação

As seis páginas em `misterios-fundo-do-mar/` são **minutas não vigentes**.
Têm aviso localizado e `noindex, nofollow`. A pedido expresso do responsável
em 10/10/2026, foram incluídas na lista de publicação de
`scripts/build_site.py` para disponibilizar os links que serão usados no jogo.
Publicar as minutas não confirma a integração de compras nem sua vigência.
Os textos e URLs dos jogos Cristal e Brasil permanecem preservados.

Após conferir a integração comercial real, revisar as três traduções,
substituir os avisos de minuta por data de vigência e eliminar as pendências
do corpo dos documentos. Remover a inserção de `noindex` no gerador,
gerar novamente. O pacote agora inclui as seis páginas e seu CSS; o teste
de empacotamento confere 32 arquivos públicos, sem documentos internos.
A publicação ocorrerá pelo fluxo Git aprovado para este repositório.

## Fontes e diferenças

- Estrutura e visual: páginas de `cristal-arco-iris/` e
  `fauna-flora-brasil/`, fontes JSON do Cristal e gerador existente.
- Nome completo aprovado: `plan/identidade-jogo.json` e `src/project.godot`
  em `C:/Users/victo/ai-vc-develop/.repo/ticoelilimar`.
  O título de loja abreviado é “Tico e Lili: Mistérios do Mar”.
- Modelo comercial futuro e decisões ainda abertas: `plan/acesso-compra.md`.
  Não há compras integradas no código examinado.
- Dados reais: `src/scripts/game_state.gd`, `settings.gd`, `sound.gd`,
  `bonus_music.gd` e `bonus_music_model.gd` do Mar.
- Progresso: idioma, três volumes, fases concluídas, lembranças reveladas,
  páginas lidas e cópia anterior para recuperação.
- Bônus: notas e tempos, duração até 30 segundos, identificadores e títulos
  opcionais; biblioteca própria com cópia anterior. Não captura microfone.
- Reset preserva preferências e biblioteca musical; não elimina todas as
  cópias anteriores. Apagar uma música retira a lista ativa, mas a cópia
  anterior pode permanecer. Limpar dados remove os arquivos locais.
- Não importar TTS, Play Age Signals ou formatos de cache dos outros jogos
  como se já existissem no Mar.

As fontes externas foram consultadas em 10/10/2026:

- [Integração do Google Play Billing](https://developer.android.com/google/play/billing/integrate)
- [Versões do Google Play Billing](https://developer.android.com/google/play/billing/release-notes)
- [Segurança dos dados e responsabilidade por SDKs](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en)
- [Dados de visitantes do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)
- [Política de Privacidade do Google](https://policies.google.com/privacy)

## Conferir antes da vigência

- Biblioteca e versão realmente exportadas; dados técnicos, identificadores,
  destinatários, finalidades, início da coleta, fila persistente e opção de
  desativação. Não assumir Billing 9.1.0 apenas pelos jogos de referência.
- Produto, preço, estado de compra, reconhecimento e restauração; confirmar
  uso e eventual persistência de tokens, logs e verificação por servidor.
- Cache do direito de acesso: campos e retenção, comportamento no reset,
  limpeza de dados, reinício offline, revogação e reconciliação com a loja.
- Barreira do responsável, controle do acesso 3+7 e progressão; não tratar
  compra pendente ou cancelada como acesso adquirido.
- Quaisquer novos SDKs, permissões, backend, Age Signals ou processamento de
  áudio introduzidos na integração. A minuta não autoriza adicioná-los.
- Correspondência entre AAB final, páginas, ficha de loja e Segurança dos
  dados. A minuta não comprova testes comerciais ou aprovação pelo Google.

## Manutenção e endereços previstos

Fontes editáveis: `data/mar_privacy_policy.json` e
`data/mar_terms_of_use.json`. Gerar com:

```powershell
python scripts/generate_mar_legal.py
python -m unittest discover -s tests -v
```

O gerador reutiliza o renderer do Cristal, com fontes e destino próprios.
O CSS segue o padrão do Brasil e as bandeiras existentes são compartilhadas.

Os endereços em português são:

- https://vcdevelopstudio.github.io/tico-e-lili-legal/misterios-fundo-do-mar/privacy-policy.html
- https://vcdevelopstudio.github.io/tico-e-lili-legal/misterios-fundo-do-mar/terms-of-use.html

Inglês usa `/en/` e espanhol `/es/` antes do nome do arquivo.
Conferir as respostas HTTP e o conteúdo após o deploy antes de entregar os links.
`src/scripts/settings.gd` do jogo tem `terms_url` e `privacy_url` exportados,
atualmente vazios; esta entrega prepara as páginas, sem alterar o jogo.

## Verificação realizada

Em 10/10/2026, os 18 testes existentes passaram. Uma conferência adicional
das seis novas páginas validou idioma, seções, correspondência integral com
os JSONs, nome e contato, aviso de minuta, navegação entre idiomas,
existência dos recursos locais e links externos HTTPS. Gerar novamente
produziu os mesmos bytes. Na preparação inicial, as minutas estavam fora do
pacote público. Na publicação autorizada, o teste passou após incluir as seis
páginas e o CSS no pacote, preservando os documentos dos outros jogos.

O CSS é o mesmo das páginas do Brasil. A inspeção visual no navegador não
foi concluída: o ambiente restringe sockets locais e o navegador não permite
abrir arquivos pelo protocolo `file:`. A validação desta entrega é estrutural
e de conteúdo; revisar a aparência no navegador local antes da publicação.
