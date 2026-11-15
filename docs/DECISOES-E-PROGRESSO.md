# Memória versionada — decisões e progresso

> Documento de trabalho; atualizar somente com evidências observadas. Campos `PENDENTE` são tarefas, não fatos.

## Estado atual

- Estado do ZIP original: inspecionado; baseline externo `5 failed` (2026-11-13).
- Estado da implementação: **Tarefa 01 — auditoria inicial realizada neste ambiente em 2026-11-14; nenhuma correção de código.**
- Tarefa 02 — plano técnico concluído em 2026-11-14, versionado em `docs/PLANO-TECNICO-TAREFA-02.md`; nenhuma alteração de código da aplicação.
- Status das correções: **D1 concluída e validada localmente; D2–D5 pendentes**.
- Testes finais / Ruff / amostra final / dataset final: **NÃO EXECUTADOS APÓS CORREÇÕES**.
- GitHub: **projeto-base publicado na `main`** (`8886887`) e plano técnico da Tarefa 02 na branch `feature/onfly-correcoes` (`b533e6f`). Issue #1 concluída; Issue #2 documenta o planejamento.

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
| D2 Noites | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| D3 Câmbio | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| D4 Ranking | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| D5 Limite 200 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| Integração | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| Entrega | PENDENTE | N/A | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

## Problemas descobertos / registro de kaizen

Registre apenas falhas realmente vistas: data, teste/log, hipótese confirmada, aprendizado reutilizável e arquivo atualizado. **Não preencher preventivamente uma lista de bugs imaginários.**

## Regra para atualização do `AGENTS.md`

Atualizar somente se uma falha real revelar uma regra durável e aplicável a sessões futuras. Decisões pontuais permanecem aqui; instruções universais já existentes não devem ser duplicadas.
