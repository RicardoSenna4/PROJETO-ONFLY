# Tarefa 01 — Auditoria inicial e baseline

Data: 2026-11-14. Auditoria executada no pacote original, sem correções no código.

## Ambiente

- Python 3.13.5 (compatível com requisito de Python 3.11+).
- pytest 9.0.2.
- Ruff não disponível nesta execução; nenhum resultado de lint foi presumido.
- Repositório GitHub de destino: `RicardoSenna4/PROJETO-ONFLY`, inicialmente vazio.
- Total de linhas de dados: 12 na amostra e 300 no dataset principal.

## Reproduções

`python -m pytest -q`: **5 failed in 3.60s**.

| Teste | Esperado | Obtido |
|---|---|---|
| `test_currency_conversion_to_brl` | `642.00` | `118.45` |
| `test_nights_across_month_boundary` | `3` | `-28` |
| `test_regression_report_on_sample` | `1542.00` | `1018.45` |
| `test_status_rules_exclude_cancelled_and_no_show` | `100.00` | `120.00` |
| `test_top_hotels_are_ranked_descending` | `H01,H02,H03` | `H04,H03,H02` |

Execução real do CLI com `PYTHONPATH=src python -m onfly_report`:

- Amostra (`data/exemplo-validacao.csv`): 12 reservas, 9 confirmadas, **-33** diárias, **5962.41 BRL**. Contrato: 28 diárias, 7566.00 BRL.
- Dataset (`data/reservas_hoteis.csv`): **200** reservas, 153 confirmadas, **-1393** diárias, **193218.53 BRL**. Arquivo físico tem 300 reservas.

## Defeitos confirmados por inspeção

1. `src/onfly_report/services/status_policy.py:8`: `status != "CANCELLED"` inclui indevidamente NO_SHOW.
2. `src/onfly_report/services/stay_calculator.py:10`: diferença apenas de `.day`, ignorando mês/ano.
3. `src/onfly_report/services/currency_converter.py:11`: conversão usa float e divisão, não multiplicação Decimal.
4. `src/onfly_report/services/report_builder.py:91`: ranking em valor crescente.
5. `src/onfly_report/repositories/csv_reservation_repository.py:47-48`: `break` após 200 reservas.

## Contratos a preservar

- Parâmetros `--input`, `--rates`, `--output`, `--top`; códigos de saída e schema JSON.
- Somente CONFIRMED faturável; `Decimal` em dinheiro; arredondamento HALF_UP apenas ao serializar.
- Não modificar testes fornecidos, `data/reservas_hoteis.csv` ou `data/taxas_cambio.csv`.
- A declaração e os registros de uso de IA previstos no README original são obrigatórios na entrega.

## Decisão de versionamento

O repositório remoto foi criado sem commits. A integração GitHub disponível não expõe parâmetros para garantir explicitamente a identidade Git `author`/`committer` do usuário. Portanto, nenhum commit remoto será criado com identidade não confirmada. O progresso foi documentado na issue [#1](https://github.com/RicardoSenna4/PROJETO-ONFLY/issues/1). A publicação do primeiro commit deve usar credenciais Git do próprio usuário e identidade configurada explicitamente.

## Próximo incremento

Planejamento e correção D1 (`status_policy.py`) com teste pré-existente de regressão, após publicar o baseline com identidade Git comprovada.
