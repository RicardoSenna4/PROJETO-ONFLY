# Matriz de testes — entregável, regressão e casos-limite

A matriz identifica verificações recomendadas. Os testes fornecidos são intocáveis. Casos adicionais devem morar em novos arquivos `tests/test_*.py` e observar regras realmente declaradas, sem inventar um produto novo.

| ID | Cenário | Resultado correto/critério | Fonte |
| --- | --- | --- | --- |
| T01 | Testes fornecidos | Cinco testes originais passam sem alterações. | `tests/` original |
| T02 | Exemplo oficial | Sumário 12/9/2/1, 28 noites, `7566.00`, média `270.21`, mês/hotéis exatos. | `README.md` |
| T03 | Dataset real | 300 reservas, 235 CONFIRMED, 31 CANCELLED, 34 NO_SHOW. | CSV + contrato |
| T04 | Dataset real — quantias | 1347 noites, `396170.00`, média `294.11`. | CSV + contrato |
| T05 | Dataset real — agrupamentos | Meses crescentes e top 5 no diagnóstico inicial. | CSV + contrato |
| T06 | Estados não faturáveis | CANCELLED e NO_SHOW aumentam apenas as contagens; nenhum efeito em noites, dinheiro, mês e hotéis. | `README.md` |
| T07 | Sem confirmadas | `total_room_nights=0`, `total_amount_brl="0.00"`, `average_nightly_rate_brl="0.00"`; `by_month=[]`, `top_hotels=[]`. | `README.md` (agregações só CONFIRMED) |
| T08 | Virada de mês | Check-in 2025-01-30, check-out 2025-02-02, 1 quarto = 3 noites, mês `2025-01`. | `README.md` |
| T09 | Virada de ano | Check-in 2024-12-31, check-out 2025-01-02, 2 quartos = 4 noites, mês `2024-12`. | `README.md` |
| T10 | Conversão exata | 100 USD × 5.420000 = 542.00 BRL; 100 EUR × 5.880000 = 588.00. | `README.md` + taxas |
| T11 | Arredondamento HALF_UP | Uma reserva BRL `1.005` é serializada como `"1.01"`. | `README.md` |
| T12 | Acumular antes de arredondar | Duas confirmadas BRL `0.004` cada, uma noite cada → total exato `0.008`, serializado `"0.01"`; não `"0.00"`. | `README.md` |
| T13 | Ranking com empate | Dois hotéis com total exato idêntico ficam em `hotel_id` crescente. | `README.md` |
| T14 | Comparação exata para ordenar | Dois hotéis cuja forma exibida se arredonda igual, mas montantes exatos diferem: ordenar pelo exato antes de formatar. | `README.md` |
| T15 | `--top` | Default 5, `--top 1` retorna 1 item, `--top 20` retorna no máximo hotéis existentes, `--top 0` é erro 2. | CLI |
| T16 | Completo acima de 200 | Um CSV temporário com 201 reservas confirmadas gera `total_reservations=201`; sem truncamento. | Regra de todos os registros |
| T17 | Tipos e schema | Dinheiro sempre string com 2 casas; contagens inteiros; chaves exatas, `report_version=1.0`. | JSON do `README.md` |
| T18 | `generated_at` | Data ISO com timezone `-03:00`; em comparações comparar estrutura ignorando somente valor variável do instante. | `README.md` |
| T19 | CSV com vírgula em aspas | `"Hotel Madrid, Gran Vía"` preserva o nome corretamente. | Dataset e formato CSV |
| T20 | CLI sem argumentos | Código 2, ajuda/erro via argparse; caminho default é `output/report.json`. | Contrato CLI |
| T21 | Arquivo inexistente | Código 2 sem produzir relatório falso. | Contrato CLI |
| T22 | Saída e logging | Cria diretório do output; imprime resumo em stdout, registros de erro em stderr. | README + CLI existente |

## Duas regras importantes de verificação

1. **Não comparar o timestamp literal** porque a data de geração é variável, mas conferir o offset `-03:00`.
2. **Não exigir igualdade entre total geral exibido e soma de subtotais já arredondados**: a regra oficial arredonda independentemente na serialização. O dataset principal apresenta diferença de R$ 0,01 entre essas somas visuais.

## Como produzir evidência

Para cada teste adicionado, registrar o comportamento que o enunciado determina, a razão do teste e, quando for regressão de um defeito original, o erro que ele reproduz no estado anterior. Preferir `run_cli` de `tests/helpers.py` para testes de integração, sem alterar o helper original. Não adicionar dezenas de testes equivalentes somente para elevar contagem.

## Não inventar requisitos

O enunciado diz que os dados fornecidos são consistentes e todas as moedas presentes têm taxa. Pode testar tratamento de arquivo ausente e `--top` inválido (contrato), mas **não criar regras de validação especulativas** para moedas ausentes, nomes duplicados, quartos negativos ou datas inversas sem evidência de exigência.
