# Tarefa 10 — Auditoria técnica de qualidade e conformidade

**Data:** 2026-11-15. **Issue:** #10. **Branch:** `feature/onfly-correcoes`.
**Escopo:** revisão técnica e evidências reais, sem reconstrução da aplicação, sem alterar regras de domínio, dados protegidos ou os testes originais.

## Resultado executivo

**Contrato funcional: PASS.** Não foram encontrados defeitos funcionais novos nos cenários definidos pelo README original e nos testes executados.
**Prontidão de entrega: PARCIAL.** Permanecem pendentes **Ruff 0.8.4**, execução explícita em **Python 3.11** e documentação/exportações reais das sessões de IA (Tarefas 11 e 12). Não declarar entrega 100% pronta.

## Evidências da execução

| Verificação | Comando/abordagem | Resultado |
| --- | --- | --- |
| Testes automatizados completos | `python -m pytest -q` | **PASS — 33 passed in 20.45s**, Python 3.13.5 |
| Integridade sintática | `python -m compileall -q src tests` | PASS |
| Parse do Python | `ast.parse` dos 29 arquivos Python de src/ e tests/ | PASS — 29/29 |
| Arquivos fornecidos intactos | SHA-256 byte a byte com ZIP original | PASS — 3 CSVs + 5 testes originais |
| Funções alteradas | diff entre ZIP original e worktree | PASS — somente 5 módulos originais de domínio/persistência foram modificados |
| Precisão monetária | rastreamento de `Decimal`, verificação de ausência de `float` nos cálculos | PASS |
| CLI oficial: amostra e base | 4 execuções + oráculo independente da T9 | PASS |
| Linhas de código acima de 120 caracteres | inspeção de `src/**/*.py` e `tests/**/*.py` após ajuste | PASS — zero linhas acima de 120 |
| Whitespace da alteração do teste | `git diff --no-index --check` para arquivo antes/depois | PASS |
| Ruff | `ruff check src tests` / `uvx --offline ruff` / tentativa `pip install ruff==0.8.4` | **NOT RUN** — Ruff não instalado; não encontrado no cache/índice disponível |
| Ambiente Python 3.11 | `python3.11 --version`, lista de Python instalados | **NOT RUN** — somente Python 3.13.5 instalado |
| Testes com versões pinadas | `requirements-dev.txt` fixa pytest 8.3.4 e Ruff 0.8.4 | **NOT RUN** nesse ambiente; pytest executado foi 9.0.2 |

O teste integral foi repetido **depois** de ajustar a formatação de `tests/test_status_exclusions.py` para respeitar o limite de linha. O conteúdo e o comportamento do teste não mudaram.

## Revisão por área

| Área auditada | Situação | Evidência |
| --- | --- | --- |
| Política de status | PASS | `is_billable(status)` exige apenas `CONFIRMED`; outras categorias continuam contabilizadas |
| Noites civis | PASS | `(checkout - checkin).days * rooms` preserva viradas de mês/ano e check-out exclusivo |
| Câmbio e exatidão | PASS | `Decimal` para valores e taxas, conversão por multiplicação, somas exatas e HALF_UP apenas na serialização |
| Mês e hotéis | PASS | Agrupa pelo check-in, ordena meses crescente; hotéis por total exato decrescente, ID crescente nos empates |
| CSV e persistência | PASS | `csv.DictReader` processa 300/300 registros; não há corte em 200 linhas |
| Contrato HTTP/API | NÃO APLICÁVEL | O desafio é uma aplicação CLI, não uma API |
| Interface CLI | PASS | Parâmetros esperados, `--top >= 1`, códigos 0/2/1 e diretórios de saída testados |
| Formato JSON | PASS | Chaves, tipos e strings monetárias conferidos; timestamp com -03:00 |
| Dependências/complexidade | PASS | Código de produção usa apenas biblioteca padrão; nenhuma arquitetura adicional introduzida |
| Segurança básica | PASS (revisão estática) | Ausência de `eval`, `exec`, `os.system`, `shell=True` e marcadores comuns de credenciais no código inspecionado |
| Testes originais e dados | PASS | Oito arquivos protegidos byte a byte idênticos ao ZIP original |
| Revisão de código | PASS | Somente correções D1–D5 e testes/documentação de regressão; sem alterações nas interfaces públicas |
| Entrega/documentação | PENDENTE | `entrega/README-ENTREGA.md`, `declaracao.md` e registros reais de IA ainda não preenchidos |

## Achados, gravidade e decisão

**A10-01 — Sem defeitos funcionais adicionais identificados** (**informativo**). Os 33 testes e comparações independentes passam. Não adicionar refatorações desnecessárias ou novas tecnologias.

**A10-02 — Ruff não disponível** (**pendência de validação**). O executável não está instalado, `uvx --offline` não o encontrou em cache e a tentativa de instalação de `ruff==0.8.4` não encontrou uma distribuição. Executar `ruff check src tests` em ambiente conectado antes da entrega. **Não equiparar análise manual a Ruff**.

**A10-03 — Python 3.11 não disponível** (**pendência de compatibilidade**). O projeto declara Python >=3.11 e foi testado aqui apenas com 3.13.5 / pytest 9.0.2, não com Python 3.11 / pytest 8.3.4. Validar as versões prescritas antes da submissão.

**A10-04 — Linhas de teste além de 120 caracteres** (**baixo, corrigido**). Reformatadas três linhas de `tests/test_status_exclusions.py`, sem alterar asserts ou dados. Teste específico e 33 testes gerais voltaram a passar.

**A10-05 — Whitespace preexistente na documentação** (**baixo, não funcional**). A verificação `git diff --cached --check` após inicializar do zero um repositório local sobre o **diretório completo** reportou três espaços finais em `prompts/03-IMPLEMENTACAO-INCREMENTAL.md` e uma linha em branco ao final do `README.md` original. São textos anteriores a estas tarefas; não representam defeito do CLI. Os espaços finais introduzidos no relatório da T9 foram corrigidos na T10. A checagem específica do diff do teste revisado passou; **não alegar um `git diff --check` global da comparação remota**.

**A10-06 — Documentos de entrega ainda são modelos** (**bloqueador de submissão**). A declaração em `entrega/uso-de-ia/declaracao.md` não identifica de forma completa os modelos/assistentes efetivamente usados. O `README-ENTREGA.md` tem marcadores `[PREENCHER]`. As sessões reais de IA devem ser exportadas e atribuídas fielmente. Estas alterações pertencem às Tarefas 11–12, e não devem ser simuladas nem omitidas.

## Próximos critérios de aceitação

1. Rodar `python3.11 -m pip install -r requirements-dev.txt`, `python3.11 -m pytest -q` e `ruff check src tests` em ambiente que disponha das versões pinadas.
2. Validar novamente a amostra e o arquivo integral caso haja ajustes do lint.
3. Completar `entrega/README-ENTREGA.md`, `entrega/uso-de-ia/declaracao.md` e exportações genuínas de sessões, incluindo ChatGPT e quaisquer outros agentes usados de fato.
4. Conferir o diff final e então autorizar, separadamente, merge/publicação e submissão.

**Nota de escopo:** não houve necessidade de modificar código de produção na Tarefa 10. `main` deve permanecer inalterada até revisão e aprovação da entrega.
