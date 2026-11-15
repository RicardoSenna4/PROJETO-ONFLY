# Memória versionada — decisões e progresso

> Documento de trabalho; atualizar somente com evidências observadas. Campos `PENDENTE` são tarefas, não fatos.

## Estado atual

- Estado do ZIP original: inspecionado; baseline externo `5 failed` (2026-11-13).
- Estado da implementação: **Tarefas 3–10 integradas à `main` pelo PR #11 e sincronizadas com `feature/onfly-correcoes`; T11 documentada nesta branch de entrega.**
- Tarefa 02 — plano técnico concluído em 2026-11-14, versionado em `docs/PLANO-TECNICO-TAREFA-02.md`; nenhuma alteração de código da aplicação.
- Status das correções: **D1–D5 concluídas e validadas localmente; Tarefa 8 concluída (16 testes novos de cobertura)**.
- Testes após T10: **33 passed** (`python -m pytest -q`, Python 3.13.5; 20.45 s após revisão da formatação dos testes). CLI da amostra validado na D4 (12 reservas, 28 diárias, BRL 7566.00). CLI no CSV principal após D7/D8: **300 reservas, 235 CONFIRMED, 31 CANCELLED, 34 NO_SHOW, 1347 diárias, BRL 396170.00, média BRL 294.11**. **Ruff não executado** (binário ausente; instalação de ruff==0.8.4 indisponível no índice); execução em **Python 3.11 não realizada** (somente 3.13 disponível).
- GitHub: código e testes das Tarefas 2–10 integrados à `main` por PR #11 (merge `7ef467b`), autoria rastreável em commits individuais. `feature/onfly-correcoes` foi sincronizada. A Tarefa 11 é desenvolvida em `feature/onfly-entrega`, com Issue #12.

## Decisões duráveis

| ID | Decisão | Razão | Evidência/status |
| --- | --- | --- | --- |
| ADR-001 | Preservar Python/CLI e arquitetura existente | Enunciado é de manutenção, não reconstrução. | `README.md` e `src/`. |
| ADR-002 | Usar `Decimal`, somar sem arredondar e aplicar HALF_UP só na serialização | Regra financeira do desafio. | `README.md`. |
| ADR-003 | Executar correções pequenas com testes de regressão | Reduz risco e permite auditoria, adaptando XP/TDD. | Processo escolhido, ainda não executado. |
| ADR-004 | Manter registro auditável de uso de IA | Entrega exige transparência. | Seção Entrega do README. |

Adicione novas decisões apenas quando ocorrerem e explique alternativas descartadas por motivo concreto.

## Log por iteração (preencher com saídas REAIS)

| Etapa | Data | Teste RED | Mudança | Teste GREEN | Diff revisado | Intervenção humana | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline | 2026-11-14 (reexecução) | `python -m pytest -q`: 5 falhas | Nenhuma | N/A | N/A | Auditoria, issue #1 e commit `8886887` | Concluído |
| Planejamento | 2026-11-14 | Sem mudança nos testes | `docs/PLANO-TECNICO-TAREFA-02.md` | N/A | Documento e commit `b533e6f` | Issue #2 | Concluído |
| D1 Status | 2026-11-15 | 2 falhas (`tests/test_status_rules.py`, `tests/test_status_exclusions.py`) | `is_billable` exige `CONFIRMED` e foi criado teste de regressão para agregações | 2 passed; suíte 2 passed/4 failed (D2–D4 ainda pendentes) | Sim: alteração de uma condição e um novo teste | Solicitação para implementar Tarefas 3 e 4 | Concluído localmente; commit registrado no GitHub |
| D2 Noites | 2026-11-15 | 3 falhas (`tests/test_nights.py`, `tests/test_stay_boundaries.py`) | Subtrair datas completas e multiplicar por quartos; dois testes de regressão | 3 passed; suíte 5 passed/3 failed (D3/D4 ainda pendentes) | Sim: expressão de cálculo alterada sem mudar API | Solicitação para implementar Tarefas 3 e 4 | Concluído localmente; commit registrado no GitHub |
| D3 Câmbio | 2026-11-15 | 4 failed, 2 passed em `tests/test_currency.py tests/test_currency_precision.py` | `convert_to_brl` passa a retornar `amount * rate` com `Decimal`; cinco testes novos de precisão e serialização | 6 passed específicos; suíte 12 passed/1 failed (D4 pendente) | Sim: uma operação alterada e novos testes | Solicitação para implementar Tarefas 5 e 6; issue #5 | Concluído e publicado na branch de trabalho |
| D4 Ranking | 2026-11-15 | 3 failed (`tests/test_top_hotels.py tests/test_ranking_tiebreakers.py`) | Chave de ordenação `(-amount, hotel_id)` preserva `Decimal` exato; dois testes novos | 3 passed específicos; suíte 15 passed; amostra do CLI validada | Sim: chave de ordenação alterada sem mudar schema | Solicitação para implementar Tarefas 5 e 6; issue #6 | Concluído e publicado na branch de trabalho |
| D5 Limite 200 | 2026-11-15 | `test_csv_full_read.py`: 2 failed (205 e 300 linhas lidas como 200) | Removido apenas `break` artificial; adicionados dois testes de regressão | 2 passed específicos; 17 passed na suíte; CLI principal com 300/300 reservas e valores esperados | Sim: nenhuma mudança no parsing, schema, CSVs ou testes originais | Solicitação para Tarefas 7 e 8; issue #7 | Concluído e publicado na branch de trabalho |
| Testes ampliados (T8) | 2026-11-15 | Suíte anterior: 17 passed; cenários adicionais não cobertos | 16 novos testes de contrato JSON, CLI, status, datas, CSV e 300 reservas; sem mudanças em produção | 16 passed direcionados; suíte completa 33 passed; compileall OK; amostra e CSV completo validados | Sim: validação de requisitos reais e hashes dos 8 arquivos originais protegidos | Issue #8; instrução para executar Tarefas 7 e 8 | Concluído e publicado na branch de trabalho |
| Validação E2E T9 | 2026-11-15 | Baseline: 33 testes e registros prévios de amostra; relatório integral ainda não comparado campo a campo | Executado CLI em amostra e dataset completo (`--top` 1, 5 e 12); comparado com oráculo independente em `csv`, `datetime.date` e `Decimal` | 4/4 execuções PASS; resumo, todos os meses, top N, schema, duas casas e timezone -03:00 | Sim: comparação completa e divergências de arredondamento explicadas | Issue #9 e `docs/VALIDACAO-PONTA-A-PONTA-T09.md` | Concluído; sem mudanças no código produtivo |
| Auditoria técnica T10 | 2026-11-15 | Código e testes da T9; 33 passed | Revisão manual dos 5 defeitos, contrato do CLI, JSON, segurança, dependências e integridade; correção exclusivamente de formatação em teste; remoção de whitespace do relatório T9 | Suíte **33 passed em 20.45s**; compileall OK; 8 arquivos originais protegidos idênticos; 29 módulos .py analisados por AST; linhas src/tests <=120 | Verificação de arquivos e diff; Ruff/Python3.11 ausentes | Issue #10; `docs/AUDITORIA-FINAL-T10.md` | Revisão feita; dois gates NÃO EXECUTADOS e entrega T11/T12 pendente |
| Documentação de entrega T11 | 2026-11-15 | Templates originais incompletos, incluindo declaração incorreta de Manus como uso confirmado | README-ENTREGA preenchido, declaração factual de ChatGPT/GPT-6, índice parcial de solicitações e aviso de exportação pendente | Verificação textual e conformidade com o README; não substitui exportação integral | Documentos sem alegar sessões fictícias | Issue #12; PR #11 já integrado | Conteúdo preparado; exportação nativa integral pendente |
| Revisão de prontidão T12 | 2026-11-15 | CI inicial apresentou três I001 de imports | Ajustes de estilo somente nos testes novos; CI Python 3.11, pytest, Ruff e CLI; checklist e relatório final | GitHub Actions #43759288991: SUCCESS; 33 passed, Ruff sem falhas, dois datasets validados | Integridade de dados originais preservada; docs revisados | Issue #13 | Qualidade técnica aprovada; exportação integral e envio do formulário pendentes |

## Problemas descobertos / registro de kaizen

Registre apenas falhas realmente vistas: data, teste/log, hipótese confirmada, aprendizado reutilizável e arquivo atualizado. **Não preencher preventivamente uma lista de bugs imaginários.**

## Regra para atualização do `AGENTS.md`

Atualizar somente se uma falha real revelar uma regra durável e aplicável a sessões futuras. Decisões pontuais permanecem aqui; instruções universais já existentes não devem ser duplicadas.

## Verificação de integridade após Tarefas 7 e 8

- Comparação byte a byte com o ZIP original: `data/reservas_hoteis.csv`, `data/taxas_cambio.csv`, `data/exemplo-validacao.csv` e os cinco testes originais sem alterações.
- `python -m pytest -q`: **33 passed in 21.74s**.
- `python -m compileall -q src tests`: **sucesso**.
- CLI `data/exemplo-validacao.csv`: **12 reservas, 9 confirmadas, 28 diárias, BRL 7566.00, média BRL 270.21**; ranking H01, H02, H12, H10, H09.
- CLI `data/reservas_hoteis.csv`: **300 reservas, 235 confirmadas, 31 canceladas, 34 no-show, 1347 diárias, BRL 396170.00, média BRL 294.11**.
- Ruff não foi executado (não disponível). Revisão final, registro das sessões de IA e validação em Python 3.11 ainda pendentes.

## Tarefa 10 — pendências de prontidão

- Ruff 0.8.4 (`ruff check src tests`) não pôde ser instalado/executado neste ambiente; não presumir PASS.
- Python 3.11 e dependências exatas do `requirements-dev.txt` não disponíveis; testar no ambiente adequado antes da submissão.
- `git diff --cached --check` de uma importação **integral** do diretório (sem baseline Git) sinalizou três espaços em `prompts/03-IMPLEMENTACAO-INCREMENTAL.md` e uma linha em branco final no `README.md` original; esses trechos eram preexistentes, não parte das correções. O diff isolado da revisão do teste passou na checagem de whitespace. O relatório T9 teve seus espaços finais removidos durante T10.
- `entrega/README-ENTREGA.md` e `entrega/uso-de-ia/declaracao.md` permanecem templates; preencher com resultados reais e a participação efetiva do ChatGPT e de quaisquer outros agentes comprovadamente utilizados, além da exportação de sessões, nas Tarefas 11 e 12.
- Nenhum merge da branch na `main`, alteração de visibilidade do repositório ou envio à Onfly foi executado.

## Integração e validação de entrega (15/11/2026)

- Pull Request #11 integrou as Tarefas 2–10 em main sem conflito. Em seguida, main e feature/onfly-correcoes foram sincronizadas.
- Documentação da Tarefa 11 registrada no commit defb573; declaração de IA identifica ChatGPT/GPT-6, sem inventar sessões do Manus.
- CI inicialmente falhou somente no Ruff (três I001 em testes adicionais), e os imports foram organizados no commit b0ca7eb.
- CI verificado: https://github.com/RicardoSenna4/PROJETO-ONFLY/actions/runs/43759288991 — CPython 3.11.18, pytest 8.3.4, Ruff 0.8.4, 33 passed, lint PASS e CLI PASS em amostra e dataset completo.
- Não foi possível anexar a exportação integral da conversa pelo assistente; é necessária ação do titular antes da submissão. Não afirmar que formulário da Onfly foi enviado.
