# Termos e privacidade — Uma Viagem Pelo Espaço

Edição de 13/10/2026. Escopo: seis páginas no diretório
`viagem-pelo-espaco`, CSS próprio, fontes JSON, gerador e allowlist.
Os documentos das outras aventuras não são modificados.

## Fontes e limite da revisão

Consultados no projeto Espaço, somente para leitura:

- `tasks/us/US-003-godot-telas-terra/prompt-projeto-legal.md`
- `plan/monetizacao.md`, incluindo REQ-COM-07 / DEC-IMP-004
- `plan/configuracoes.md` e `plan/perfil-inicial.md`
- `tasks/us/US-003-godot-telas-terra/_status.md`

Raiz consultada:
`C:/Users/victo/ai-vc-develop/.repo/ticoeliliespaco`.
Busca por código Godot, project.godot, export_presets, Gradle e plugins
não encontrou implementação ou pacote comercial disponível nessa raiz.
O status da US-003 descreve implementação futura. Monetização confirma
produto/SDK, compra/restauração/cache e validação comercial como futuros.
Não existe evidência suficiente para declarar versão de SDK, campos,
diagnósticos, opt-out, retenção, backup Android ou reinício offline.
Não foi realizada captura de tráfego nem auditoria de servidores.

Os documentos descrevem o produto final aprovado, e não a primeira fatia:
dez fases, 1–3 gratuitas, compra definitiva 4–10, US$1,00 internacional /
equivalente local e R$2,99 Brasil, preço localizado da loja na oferta,
sem assinatura/anúncios, progresso separado do acesso, reset preservando
preferências e direitos. A ausência de integração comercial confirmada é
expressa nas páginas; não se afirma ausência universal de coleta.
Revisão desta política e da build comercial é necessária antes de sua
distribuição, especialmente para serviços, diagnósticos e cache.

Contato confirmado no prompt: VCDevelopStudio / vcdevelopstudio@gmail.com.
Atendimento por Gmail e hospedagem GitHub Pages são descritos separadamente.
Páginas estáticas sem scripts, cookies ou armazenamento do navegador.
Inglês é x-default; as URLs raiz solicitadas continuam em português.

## Fluxo de publicação e fontes externas

Fluxo existente: commit e push em main, workflow Deploy GitHub Pages;
somente allowlist pública é enviada ao Pages. A allowlist cresce de 32
para 39 arquivos: seis HTML e um CSS. JSONs internos, docs, testes e
scripts do Espaço não são publicados.

Fontes oficiais consultadas em 13/10/2026:

- [Privacidade Google](https://policies.google.com/privacy)
- [Reembolsos Google Play](https://support.google.com/googleplay/answer/2479637?hl=pt-BR)
- [Dados do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)
- [Segurança Billing](https://developer.android.com/google/play/billing/security)

Essas fontes descrevem os provedores e não comprovam integração no Espaço.
Direitos obrigatórios do consumidor e licenças de terceiros são preservados.

## Verificações reproduzíveis

```powershell
python scripts/generate_espaco_legal.py
python -m unittest discover -s tests -v
```

Testes: conteúdo integral HTML/JSON por idioma, títulos, datas, seções,
navegação entre idiomas/documentos, x-default inglês, recursos locais,
HTTPS e ausência de scripts; preços e ausência de declarações de SDK
herdadas; pacote de 39 arquivos e exclusão de fontes internas.
Conferir geração determinística, diff sem alterações dos outros jogos,
layout móvel/desktop e conteúdo integral servido nas seis URLs após deploy.
Commit e resultado de deploy são registrados na entrega ao responsável.
Nenhuma alteração ou publicação do aplicativo faz parte desta tarefa.
