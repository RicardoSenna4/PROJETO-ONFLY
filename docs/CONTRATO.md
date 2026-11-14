# Contrato funcional — Onfly

> Resumo para trabalho de engenharia derivado do `README.md` ORIGINAL. Havendo divergência, prevalece o README original. Não substituir nem editar o enunciado.

## Comando obrigatório

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json \
  --top 5
```

Argumentos: `--input` e `--rates` obrigatórios. `--output` opcional, default `output/report.json`. `--top` opcional, default 5, inteiro ≥ 1. Código de saída: `0` sucesso, `2` entrada ou argumentos inválidos, `1` erro inesperado. Resumo no stdout, logs no stderr, caminho de output criado quando necessário.

## Pipeline de negócio

**ler integralmente → converter tipos → contar status → filtrar CONFIRMED → agregar → serializar**.

- Datas civis ISO `YYYY-MM-DD` com cálculo não inclusivo: `(checkout - checkin).days * rooms`.
- `total_reservations` = todas as linhas de reserva.
- `confirmed_reservations`, `cancelled_reservations`, `no_show_reservations`: contagens por status, sem misturar com filtros financeiros.
- Só `CONFIRMED` contribui para noites, dinheiro, mensal e hotéis. `CANCELLED` e `NO_SHOW` continuam nas contagens.
- `amount` é na `currency` de origem. BRL = `Decimal(amount) * Decimal(rate_to_brl)`, usando CSV de taxas; sem `float` e sem arredondamentos intermediários.
- Total/medida média são calculados com valores exatos; arredondar HALF_UP somente na serialização, para 2 casas decimais.
- A média é `total_amount_brl / total_room_nights`; quando o denominador é zero, `"0.00"`.
- `by_month` agrupa apenas confirmadas pelo mês do **check-in**; ordena `YYYY-MM` crescente.
- `top_hotels` agrupa apenas confirmadas por `hotel_id` e usa `hotel_name`; ordena por **montante exato decrescente**, desempate por `hotel_id` ascendente; aplica `--top`.
- `report_version` é `"1.0"`; `generated_at` deve ter `-03:00` fixo, e seu valor específico não é comparado.
- O JSON não pode ter campos extras nem mudar nome, tipo, ordem semântica, unidade ou valor de qualquer campo do contrato.

## Shape exato do relatório

```json
{
  "report_version": "1.0",
  "generated_at": "2025-07-01T10:00:00-03:00",
  "summary": {
    "total_reservations": 0,
    "confirmed_reservations": 0,
    "cancelled_reservations": 0,
    "no_show_reservations": 0,
    "total_room_nights": 0,
    "total_amount_brl": "0.00",
    "average_nightly_rate_brl": "0.00"
  },
  "by_month": [
    {"month": "2025-01", "reservations": 0, "room_nights": 0, "total_brl": "0.00"}
  ],
  "top_hotels": [
    {"hotel_id": "H01", "hotel_name": "Hotel Exemplo", "room_nights": 0, "total_brl": "0.00"}
  ]
}
```

O exemplo ilustra a **estrutura**, não exige que uma execução vazia tenha linha mensal ou hotel fictício. Para nenhuma reserva confirmada, coleções de agregação devem estar vazias.

## Conjunto de validação publicado

`data/exemplo-validacao.csv` deve produzir: total=12, confirmadas=9, canceladas=2, no-show=1, noites=28, BRL=`"7566.00"`, média=`"270.21"`.

`by_month`:
- `2025-01`: 8 reservas, 25 noites, `"6684.00"`.
- `2025-02`: 1 reserva, 3 noites, `"882.00"`.

`top_hotels` (`--top 5`):
1. H01, Hotel Aurora Paulista, 3 noites, `"1200.00"`.
2. H02, Hotel Mirante, 2 noites, `"1084.00"`.
3. H12, Hotel Miami Beach, 1 noite, `"1000.00"`.
4. H10, Hotel Madrid, Gran Vía, 4 noites, `"900.00"`.
5. H09, Hotel Lisboa, Centro, 3 noites, `"882.00"`.

## Restrições de entrega

Não modificar os testes fornecidos nem os CSVs protegidos. Pode mudar código interno, acrescentar testes e documentação. Exigir `entrega/README-ENTREGA.md` com defeitos, causas raiz, investigação, como executar e resultado real de `pytest`. Ao utilizar IA, incluir registro fiel das sessões e `entrega/uso-de-ia/declaracao.md`, com ferramentas/modelos e divisão de trabalho. Projeto em repositório GitHub público e link via forms conforme orientações recebidas.
