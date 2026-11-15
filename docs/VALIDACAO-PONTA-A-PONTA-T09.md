# Tarefa 09 — Validação real ponta a ponta do CLI

**Status: PASS** — quatro execuções do CLI comparadas com cálculos independentes sobre os CSVs originais.
**Data:** 2026-11-15. **Branch:** `feature/onfly-correcoes`. **Issue:** #9.
**Ponto de partida:** commit `aecf6ca` (Tarefa 8). **Ambiente:** Python 3.13.5.

## Comandos reproduzíveis

Executar a partir da raiz do repositório, com Python 3.11+:

```bash
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json --top 5
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json --top 5
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/top1.json --top 1
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/top12.json --top 12
```

Na validação os caminhos de saída estavam em diretórios temporários, para não versionar relatórios gerados. Foram usados `sys.executable`, `PYTHONPATH=src` e os mesmos argumentos. Todos retornaram exit code 0, criaram JSON válido e imprimiram o resumo no stdout.

## Oráculo independente

Uma rotina de verificação externa ao código de `src/` leu os arquivos com `csv.DictReader`, datas com `date.fromisoformat` e valores/taxas diretamente como `Decimal`. Contou todos os status, filtrou `CONFIRMED` para valores e noites, calculou `(checkout - checkin).days * rooms` e `amount * rate_to_brl`. Acumulou sem arredondar, aplicou `ROUND_HALF_UP` a duas casas apenas ao serializar e ordenou hotéis por valor exato decrescente, com `hotel_id` crescente em empate. O oráculo **não importou módulos da implementação**.

Comparou por igualdade estrutural os objetos `summary`, `by_month` e `top_hotels` completos. Verificou ainda a lista exata de chaves de topo, `report_version=1.0`, os valores monetários como strings de duas casas e `generated_at` como data ISO com deslocamento `-03:00`, sem comparar o horário variável.

## Resumos encontrados

| Campo | Amostra oficial | Base completa |
| --- | ---: | ---: |
| `total_reservations` | 12 | 300 |
| `confirmed_reservations` | 9 | 235 |
| `cancelled_reservations` | 2 | 31 |
| `no_show_reservations` | 1 | 34 |
| `total_room_nights` | 28 | 1347 |
| `total_amount_brl` | "7566.00" | "396170.00" |
| `average_nightly_rate_brl` | "270.21" | "294.11" |

Todos os sete campos conferiram com o contrato do README, o oráculo independente e a saída real.

## Resultado mensal — amostra

| Mês | Reservas confirmadas | Noites | Total BRL |
| --- | ---: | ---: | ---: |
| 2025-01 | 8 | 25 | 6684.00 |
| 2025-02 | 1 | 3 | 882.00 |

## Ranking — amostra (`--top 5`)

| Hotel ID | Nome | Noites | BRL |
| --- | --- | ---: | ---: |
| H01 | Hotel Aurora Paulista | 3 | 1200.00 |
| H02 | Hotel Mirante | 2 | 1084.00 |
| H12 | Hotel Miami Beach | 1 | 1000.00 |
| H10 | Hotel Madrid, Gran Vía | 4 | 900.00 |
| H09 | Hotel Lisboa, Centro | 3 | 882.00 |

## Resultado mensal — arquivo integral

| Mês | Reservas confirmadas | Noites | Total BRL |
| --- | ---: | ---: | ---: |
| 2024-12 | 35 | 174 | 61335.80 |
| 2025-01 | 37 | 235 | 64662.89 |
| 2025-02 | 26 | 138 | 45991.09 |
| 2025-03 | 39 | 215 | 65984.99 |
| 2025-04 | 21 | 146 | 31335.97 |
| 2025-05 | 39 | 196 | 63507.98 |
| 2025-06 | 38 | 243 | 63351.29 |

## Ranking — arquivo integral (`--top 5`)

| Hotel ID | Nome | Noites | BRL |
| --- | --- | ---: | ---: |
| H06 | Hotel Salvador Centro | 160 | 45165.46 |
| H10 | Hotel Madrid, Gran Vía | 120 | 45041.69 |
| H12 | Hotel Miami Beach | 106 | 41647.69 |
| H07 | Hotel Brasília Tower | 148 | 39920.52 |
| H11 | Hotel Buenos Aires | 102 | 37455.69 |

Os relatórios `--top 1` e `--top 12` também foram integralmente comparados, incluindo a quantidade e a ordem dos hotéis.

**Nota sobre arredondamento:** somar os valores mensais **já arredondados** da base completa resulta em R$ 396170.01, diferente em R$ 0.01 do total exato global serializado (R$ 396170.00). Isso é esperado pelo contrato: acumular com precisão e arredondar cada campo apenas na serialização. Não deve haver ajuste artificial.

## Matriz da execução

| Verificação | Resultado |
| --- | --- |
| Executar CLI na amostra com `--top 5` | PASS |
| Executar CLI na base completa com `--top 5` | PASS |
| Executar CLI na base completa com `--top 1` | PASS |
| Executar CLI na base completa com `--top 12` | PASS |
| Comparar os sete campos de `summary` | PASS |
| Comparar **todos** os registros de `by_month` | PASS |
| Comparar **todos** os registros de `top_hotels` | PASS |
| Tipos, duas casas e formato do schema JSON | PASS |
| `generated_at` com offset fixo -03:00 | PASS |
| Resultado funcional do programa | PASS |

Não foram necessárias correções de código nesta tarefa. Auditoria técnica, Ruff e Python 3.11 são tratados na Tarefa 10.
