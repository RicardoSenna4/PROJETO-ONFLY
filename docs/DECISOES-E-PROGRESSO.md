# Memória versionada — decisões e progresso

> Documento de trabalho; atualizar somente com evidências observadas. Campos `PENDENTE` são tarefas, não fatos.

## Estado atual

- Estado do ZIP original: inspecionado; baseline externo `5 failed` (2026-11-13).
- Estado da implementação: **Tarefas 3–6 concluídas e testadas localmente em 2026-11-15, commits separados na branch de trabalho.**
- Tarefa 02 — plano técnico concluído em 2026-11-14, versionado em `docs/PLANO-TECNICO-TAREFA-02.md`; nenhuma alteração de código da aplicação.
- Status das correções: **D1–D5 concluídas e validadas localmente; Tarefa 8 (ampliação dos testes) pendente**.
- Testes após D7: **17 passed** (`python -m pytest -q`, Python 3.13.5). CLI da amostra validado na D4 (12 reservas, 28 diárias, BRL 7566.00). CLI no CSV principal após D7: **300 reservas, 235 CONFIRMED, 31 CANCELLED, 34 NO_SHOW, 1347 diárias, BRL 396170.00, média BRL 294.11**. **Ruff ainda não executado** no ambiente; validação final em Python 3.11 pendente.
- GitHub: baseline na `main` (`8886887`, inalterada); correções D1 (`cfca5d9`), D2 (`e9c575f`), D3 (`78fbc00`) e D4 (commit desta etapa) na branch `feature/onfly-correcoes`. Issues #3–#6 rastreiam as correções.

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
| Integração | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| Entrega | PENDENTE | N/A | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

## Problemas descobertos / registro de kaizen

Registre apenas falhas realmente vistas: data, teste/log, hipótese confirmada, aprendizado reutilizável e arquivo atualizado. **Não preencher preventivamente uma lista de bugs imaginários.**

## Regra para atualização do `AGENTS.md`

Atualizar somente se uma falha real revelar uma regra durável e aplicável a sessões futuras. Decisões pontuais permanecem aqui; instruções universais já existentes não devem ser duplicadas.
