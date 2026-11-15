# Entrega — Desafio técnico Onfly

## Resumo da solução

Foi mantido o consolidador original em Python, executado por linha de comando, e corrigidos cinco defeitos que produziam números incorretos. O contrato de argumentos, o schema JSON, os três CSVs fornecidos e os cinco testes originais foram preservados. Foram acrescentados testes de regressão e documentos de auditoria; não foram introduzidos frontend, API, banco de dados ou dependências de produção.

**Repositório público:** https://github.com/RicardoSenna4/PROJETO-ONFLY
**Integração do código:** PR #11, merge em `main`.
**Escopo da entrega:** código, testes e documentação. **O envio do formulário da Onfly ainda é uma etapa separada.**

## Defeitos corrigidos e causa raiz

| Defeito | Causa raiz (uma frase) | Correção e arquivos | Evidências |
| --- | --- | --- | --- |
| D1 — Política de status | O predicado `status != "CANCELLED"` incluía indevidamente `NO_SHOW` nas métricas financeiras. | `src/onfly_report/services/status_policy.py`: somente `CONFIRMED` é faturável. | `tests/test_status_rules.py` e `tests/test_status_exclusions.py` |
| D2 — Diárias | O cálculo subtraía apenas o número do dia, ignorando mudanças de mês e ano. | `src/onfly_report/services/stay_calculator.py`: `(checkout - checkin).days * rooms`. | `tests/test_nights.py` e `tests/test_stay_boundaries.py` |
| D3 — Conversão monetária | O cálculo dividia pela taxa `rate_to_brl` e convertia os operandos para `float`, perdendo precisão. | `src/onfly_report/services/currency_converter.py`: `amount * rate` com `Decimal` sem arredondamento intermediário. | `tests/test_currency.py`, `tests/test_currency_precision.py` e teste de regressão |
| D4 — Ranking de hotéis | A ordenação usava total crescente em vez de decrescente. | `src/onfly_report/services/report_builder.py`: ordenação por `(-total_exato, hotel_id)`. | `tests/test_top_hotels.py` e `tests/test_ranking_tiebreakers.py` |
| D5 — Leitura integral | Um `break` encerrava a leitura da exportação depois de 200 reservas. | `src/onfly_report/repositories/csv_reservation_repository.py`: remoção do corte artificial. | `tests/test_csv_full_read.py` e `tests/test_full_dataset_contract.py` |

O arredondamento monetário continua sendo efetuado somente na serialização para duas casas, com `ROUND_HALF_UP`. Reservas `CANCELLED` e `NO_SHOW` permanecem nas contagens por status, mas não integram valores, noites, meses nem ranking.

## Investigação e implementação

1. Foi inspecionado o README original, incluindo o contrato do CLI e as regras de negócio, sem substituir o enunciado por suposições.
2. O baseline reproduziu **5 testes falhando**. Cada problema foi isolado com o teste fornecido e, quando adequado, com casos de regressão novos, executados antes da correção (RED).
3. As cinco correções foram aplicadas em commits separados, com foco na menor mudança funcional (GREEN), revisando o impacto e evitando refatorações desnecessárias.
4. A cobertura foi ampliada para datas com virada de mês/ano, precisão decimal, empate no ranking, arquivos maiores que 200 registros, ausência de confirmadas, JSON, erros de argumentos e processamento do CSV original.
5. Foram executados relatórios ponta a ponta, comparados campo a campo com um **oráculo independente** baseado em `csv.DictReader`, `date` e `Decimal`, que não importava funções da implementação.

**Rastreamento:** Issues #1–#10 e relatórios em `docs/DIAGNOSTICO-INICIAL.md`, `docs/DECISOES-E-PROGRESSO.md`, `docs/VALIDACAO-PONTA-A-PONTA-T09.md` e `docs/AUDITORIA-FINAL-T10.md`.

## Como executar

Requer Python **3.11 ou superior**. Na raiz do repositório, em bash/zsh:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
ruff check src tests

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json \
  --top 5

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json \
  --top 5
```

No Windows PowerShell, defina `$env:PYTHONPATH = "src"` antes de `python -m onfly_report ...`. O diretório de saída é criado automaticamente. Os parâmetros `--input` e `--rates` são obrigatórios; `--output` usa `output/report.json` por padrão e `--top` usa 5.

## Resultados observados

Na reexecução local de **15/11/2026**, com **Python 3.13.5** e **pytest 9.0.2**, o comando `python -m pytest -q` retornou:

```text
.................................                                        [100%]
33 passed in 21.24s
```

`python -m compileall -q src tests` também passou. Os **cinco testes fornecidos** e os **três CSVs originais** permaneceram idênticos aos arquivos entregues, conforme verificação byte a byte. Os cinco módulos alterados conferiram com os blobs Git da branch remota após a auditoria.

| Indicador | Amostra de validação | Arquivo completo |
| --- | ---: | ---: |
| Reservas totais | 12 | 300 |
| CONFIRMED | 9 | 235 |
| CANCELLED | 2 | 31 |
| NO_SHOW | 1 | 34 |
| Diárias | 28 | 1347 |
| Total BRL | 7566.00 | 396170.00 |
| Média por diária BRL | 270.21 | 294.11 |

Os meses, o ranking `--top 5`, o formato monetário e o fuso fixo `-03:00` também passaram nas comparações independentes. Foram verificadas ainda saídas `--top 1` e `--top 12`. Diferenças de um centavo entre a soma de subtotais **já arredondados** e o total arredondado separadamente são esperadas pelo contrato.

**Limitações de verificação:** Ruff 0.8.4 e Python 3.11 não estavam disponíveis no ambiente local utilizado nas Tarefas 1–10; portanto, **não se afirma que essas duas verificações passaram**. A automação de CI, se habilitada, é a fonte de evidência adicional em Python 3.11. Seu resultado deve ser consultado antes da submissão.

## Validação adicional no GitHub Actions (Python 3.11)

A execução real [#43759288991](https://github.com/RicardoSenna4/PROJETO-ONFLY/actions/runs/43759288991), concluída com SUCCESS em 15/11/2026, utilizou **CPython 3.11.18**, **pytest 8.3.4** e **Ruff 0.8.4**, instalados de requirements-dev.txt. Resultados: **33 passed in 1.89s**, **All checks passed!** no comando Ruff, execução do CLI na amostra com **12 reservas/28 diárias/BRL 7566.00** e na base principal com **300 reservas/1347 diárias/BRL 396170.00**. A correção dos três blocos de importação de testes adicionais foi exclusivamente de estilo, sem mudar as regras do programa. A limitação de ambiente citada acima refere-se apenas às primeiras execuções locais, não ao CI aprovado.

## Uso de inteligência artificial e pendências da submissão

Foi usado **ChatGPT (GPT-6)** para investigação, implementação, testes, documentação e ações autorizadas no GitHub. O candidato definiu as solicitações, o repositório e a sequência das tarefas. A atribuição dos commits ao perfil `RicardoSenna4` não substitui a declaração de uso de IA. Os detalhes estão em `entrega/uso-de-ia/declaracao.md`.

**Manus:** foram preparados documentos e prompts para eventual utilização, mas **não há comprovação neste histórico de execução de código pelo Manus**. Caso tenham existido sessões separadas, o candidato deve acrescentar suas exportações e identificar o modelo e as atividades conforme registros reais.

**Pendência documental obrigatória:** anexar a **exportação completa e fiel** das sessões de IA (ChatGPT e outras efetivamente usadas) em `entrega/uso-de-ia/`. O arquivo `indice-de-interacoes.md` é um índice factual parcial, **não é uma exportação integral**. Confirmar essa etapa e os demais itens de `docs/CHECKLIST-DE-ENTREGA.md` antes de enviar o link ao formulário da Onfly.
