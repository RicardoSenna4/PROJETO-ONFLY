# Índice factual de interações — NÃO é exportação completa

**Objetivo:** facilitar rastreabilidade das solicitações conhecidas e das evidências de desenvolvimento.
**Limite:** as solicitações abaixo foram transcritas literalmente do histórico disponível nesta conversa. Os resultados citados são **referências a commits e issues**, não transcrições integrais das respostas do assistente. Este documento **não cumpre sozinho** o requisito da Onfly de exportação das sessões ou log completo de prompts/respostas.

## Solicitações registradas (ordem de ocorrência)

| Ordem | Solicitação do candidato (literal) | Evidência verificável |
| --- | --- | --- |
| 1 | "aplique as instruções do akita para como desenvolver esse projeto, respeitando o que é aplicável e cabível nas especificações do projeto. me retorne tudo de orientação e .md que será necessário. leve em consideração que vou desenvolver no manus" | `AGENTS.md`, `docs/`, `prompts/` |
| 2 | "me retorne um .zip com todos os arquivos" | Pacote ZIP gerado na conversa, não versionado como artefato independente |
| 3 | "em texto, quebre as tarefas que eu devo mandar para o manus, levando em consideração que ja forneci os .md de orientações e o link do github do projeto." | Roteiro de 12 tarefas apresentado na conversa |
| 4 | "vamos começar nosso desenvolvimento. todos os progressos de cada tarefa deverão ser salvos nesse repositório do github https://github.com/RicardoSenna4/PROJETO-ONFLY. não quero que os commits tenham nome de ia, mas tenham nome do meu perfil de usuário" | Issues #1, #2 e commits do projeto-base |
| 5 | "faça" (em resposta ao próximo passo de publicar projeto-base e planejar) | `docs/PLANO-TECNICO-TAREFA-02.md`, Issue #2 |
| 6 | "agora implemente as tarefas 3 e 4" | Issues #3 e #4; commits `cfca5d9`, `e9c575f` |
| 7 | "implemente as tarefas 5 e 6" | Issues #5 e #6; commits `78fbc00`, `09cf3b5` |
| 8 | "execute as tarefas 7 e 8" | Issues #7 e #8; commits `459d1ba`, `aecf6ca` |
| 9 | "implemente as tarefas 9 e 10" | Issues #9 e #10; commits `5dbfb21`, `5627a1d`, `2b14c39` |
| 10 | "faça um merge em todas as branchs de forma correta e que funcione corretamente. logo após, implemente as tarefas 11 e 12" | PR #11 (merge das correções) e Issues #12/#13 (entrega e revisão) |

## Respostas e evidências de execução

A descrição verificável das respostas práticas está nos diffs dos commits, nas Issues #1–#10 e em `docs/DECISOES-E-PROGRESSO.md`. Não foram copiados aqui trechos supostamente literais de respostas que não puderam ser integralmente extraídos. Para uma auditoria fiel de prompts **e respostas**, o titular deve anexar a exportação real, incluindo mensagens do assistente, resultados de ferramentas quando exportados e as eventuais sessões adicionais.

## Como completar corretamente

1. Exportar esta conversa de ChatGPT pelo mecanismo disponibilizado pela plataforma/conta, conservando as mensagens completas. Salvar a exportação em `entrega/uso-de-ia/` (ou em vários arquivos se houver divisão nativa por sessões).
2. Se a plataforma não oferecer exportação de uma conversa isolada, recuperar fielmente todas as mensagens e respostas ou uma exportação de dados correspondente e montar um log completo sem inventar conteúdo.
3. Caso o Manus tenha sido usado, exportar também as sessões **reais** de Manus, com mensagens, resultados e identificação do modelo se mostrada.
4. Revisar apenas dados sensíveis eventualmente presentes, registrar tarjas, e atualizar `declaracao.md` para refletir **somente** sessões realmente anexadas.

**Situação neste commit:** registro parcial de rastreabilidade; exportação integral **PENDENTE**.
