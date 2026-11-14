# Diagnóstico inicial — evidências antes da implementação

## Proveniência

Inspeção estática e execução dos 5 testes fornecidos sobre os arquivos **originais do ZIP Onfly**, realizada em 2026-11-13. Os resultados seguintes se referem **somente ao baseline original**, não demonstram correção da solução. O Manus deve reproduzi-los no próprio ambiente e registrar suas saídas.

## Baseline de testes

Comando executado na raiz extraída: `pytest -q`.

**Resultado observado: `5 failed`** — falham os seguintes testes fornecidos:

| Teste | Saída/causa observada |
| --- | --- |
| `test_currency_conversion_to_brl` | Obteve `118.45` em vez de `642.00`; conversão dividiu pela taxa. |
| `test_nights_across_month_boundary` | Obteve `-28` em vez de `3`; usou `checkout.day - checkin.day`. |
| `test_regression_report_on_sample` | Total `1018.45` em vez de `1542.00`; média `203.69` em vez de `308.40`; defeito de câmbio contaminou agregação. |
| `test_status_rules_exclude_cancelled_and_no_show` | Obteve `120.00` em vez de `100.00`; `NO_SHOW` foi incluído indevidamente. |
| `test_top_hotels_are_ranked_descending` | Obteve `H04,H03,H02` em vez de `H01,H02,H03`; ranking crescente. |

## Cinco defeitos observáveis e candidatos a testes de regressão

| Código | Arquivo/função | Evidência no original | Impacto esperado | Ação mais econômica a INVESTIGAR |
| --- | --- | --- | --- | --- |
| D1 | `src/onfly_report/services/status_policy.py` / `is_billable` | `status != "CANCELLED"` | `NO_SHOW` erroneamente contabilizado | Faturável somente se `status == "CONFIRMED"`. |
| D2 | `src/onfly_report/services/stay_calculator.py` / `calculate_room_nights` | `checkout.day - checkin.day` | Negativos ou valores errados na mudança de mês/ano | Diferença entre objetos `date`. |
| D3 | `src/onfly_report/services/currency_converter.py` / `convert_to_brl` | `float(amount) / float(rate)` | Direção errada do câmbio e perda de precisão | Multiplicação de `Decimal` sem conversão para float. |
| D4 | `src/onfly_report/services/report_builder.py` / ranking | Ordenação crescente por `amount` | Ranking invertido | Ordenar pelo valor exato decrescente e `hotel_id` ascendente. |
| D5 | `src/onfly_report/repositories/csv_reservation_repository.py` / `read` | `if len(rows) == 200: break` | Ignora as últimas 100 reservas do dataset principal | Ler todas as linhas; novo teste com mais de 200. |

**Nota:** o teste de regressão geral falha por uma combinação de problemas já listados; `5 failed` não implica exatamente cinco testes isolando cinco defeitos. O limite de 200 reservas não é detectado pelos testes fornecidos.

## Dados do CSV, confirmados independentemente

| Arquivo | Reservas | Confirmadas | Canceladas | No-show |
| --- | ---: | ---: | ---: | ---: |
| `data/exemplo-validacao.csv` | 12 | 9 | 2 | 1 |
| `data/reservas_hoteis.csv` | 300 | 235 | 31 | 34 |

As 300 reservas do dataset principal se distribuem em 12 hotéis; as moedas são BRL, USD e EUR. A tabela de câmbio original contém BRL=1.000000, USD=5.420000, EUR=5.880000.

## Oráculo INDEPENDENTE do dataset principal

Calculado em script de inspeção externo ao projeto, usando a especificação do README, `datetime.date`, `Decimal`, agregação sem arredondar e `ROUND_HALF_UP` apenas na formatação. Use como conferência do relatório final do Manus, e não como substituto de testes independentes no projeto.

**Summary esperado** (exceto `generated_at`):

```json
{
  "total_reservations": 300,
  "confirmed_reservations": 235,
  "cancelled_reservations": 31,
  "no_show_reservations": 34,
  "total_room_nights": 1347,
  "total_amount_brl": "396170.00",
  "average_nightly_rate_brl": "294.11"
}
```

**by_month esperado**:

| month | reservations | room_nights | total_brl |
| --- | ---: | ---: | ---: |
| 2024-12 | 35 | 174 | 61335.80 |
| 2025-01 | 37 | 235 | 64662.89 |
| 2025-02 | 26 | 138 | 45991.09 |
| 2025-03 | 39 | 215 | 65984.99 |
| 2025-04 | 21 | 146 | 31335.97 |
| 2025-05 | 39 | 196 | 63507.98 |
| 2025-06 | 38 | 243 | 63351.29 |

**top_hotels esperado** com `--top 5`:

| hotel_id | hotel_name | room_nights | total_brl |
| --- | --- | ---: | ---: |
| H06 | Hotel Salvador Centro | 160 | 45165.46 |
| H10 | Hotel Madrid, Gran Vía | 120 | 45041.69 |
| H12 | Hotel Miami Beach | 106 | 41647.69 |
| H07 | Hotel Brasília Tower | 148 | 39920.52 |
| H11 | Hotel Buenos Aires | 102 | 37455.69 |

**Atenção às casas decimais:** pela regra de arredondar cada subtotal só na serialização, a soma dos valores mensais *já apresentados* pode diferir do total geral em R$ 0,01. Neste dataset, os totais mensais apresentados somam R$ 396170.01, e os valores apresentados dos 12 hotéis somam R$ 396169.99. O total geral correto continua `"396170.00"`. Não introduza ajustes artificiais para forçar a soma de valores previamente arredondados. A mesma regra vale para classificação: utilize os valores exatos, não strings já arredondadas.

## Limites do diagnóstico

Não existe evidência de outros defeitos além dos identificados sem testes específicos. Verificações adicionais são prudentes para a exatidão e o contrato, mas NÃO devem ser apresentadas como bugs comprovados antes de reproduzi-los. Não inferir sistema de detecção de IA a partir do enunciado; ele exige divulgação e sessões reais.
