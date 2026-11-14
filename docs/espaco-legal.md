# Termos e privacidade — Uma Viagem Pelo Espaço

Primeira edição em 13/10/2026; revisada em 14/11/2026. Escopo: seis páginas no diretório
`viagem-pelo-espaco`, CSS próprio, fontes JSON, gerador e allowlist.
Os documentos das outras aventuras não são modificados.

## Edição de 14/11/2026 — versão comercial 0.9.0

Revisão feita após a integração do Google Play Billing no jogo. Fatos lidos no
código do jogo e no AAB de produção 0.9.0 (código 53), assinado e ainda não
enviado à Play:

- Pacote `com.vcdevelopstudio.ticoeliliespaco`; fases 1–3 gratuitas e compra
  única não consumível para 4–10, US$1,00 / R$2,99, preço localizado na oferta.
- GodotGooglePlayBilling 3.3.0 e Billing Library 9.1.0 (`billing.properties`
  do AAB); DataTransport/CCT presente no dex. Billing inicia ao abrir o app e
  reconsulta ao voltar ao app, ao abrir o mapa e em Restaurar.
- Cache próprio da compra: só produto, pacote, ambiente e acesso; sem token
  nem pedido. Falha de consulta não revoga; consulta concluída sem a compra
  (reembolso) revoga. Pendente não libera. ACK único.
- Bloqueio parental com voz que chama um adulto; Comprar/Restaurar só depois.
  Compra reconhecida na oferta entra na fase escolhida.
- Manifesto mesclado com `allowBackup="false"`. Redefinir progresso conserva a
  compra e o cache do catálogo.
- "Mais jogos": feed `catalogo/familia/v1/jogos.json`, downloads só ao abrir a
  lista ou Atualizar (antes do bloqueio da loja), validade máxima de 24 h.

A política passou de nove para onze seções (diagnósticos e catálogo). Os
termos mantêm as nove seções; mudaram produto, preço, compra pelo responsável,
uso offline, redefinição e privacidade. Não houve captura de tráfego.

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
HTTPS e ausência de scripts; preços, pacote, versões do Billing, DataTransport,
feed do catálogo e ausência de frases de "em desenvolvimento"; pacote de 39 arquivos e exclusão de fontes internas.
Conferir geração determinística, diff sem alterações dos outros jogos,
layout móvel/desktop e conteúdo integral servido nas seis URLs após deploy.
Commit e resultado de deploy são registrados na entrega ao responsável.
Nenhuma alteração ou publicação do aplicativo faz parte desta tarefa.
