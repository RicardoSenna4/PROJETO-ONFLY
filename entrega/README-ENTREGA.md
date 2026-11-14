# Entrega — Desafio Onfly

> **TEMPLATE NÃO PREENCHIDO.** Não submeter sem substituir os campos pendentes por evidências REAIS e remover esta observação. Este pacote contém apenas a orientação, não a correção do código.

## Resumo da solução

[PREENCHER após implementação: o que foi corrigido no CLI existente e como o contrato foi preservado.]

## Defeitos corrigidos e causa raiz

| Defeito | Causa raiz (uma frase) | Arquivos modificados | Evidência/teste |
| --- | --- | --- | --- |
| Status de reservas | [PREENCHER com causa confirmada] | [PREENCHER] | [PREENCHER] |
| Noites de quarto | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Câmbio/precisão | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Ranking de hotéis | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Leitura integral | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Outros (se existirem) | [PREENCHER ou REMOVER ESTA LINHA] | [PREENCHER] | [PREENCHER] |

## Investigação e abordagem

[PREENCHER como se reproduziram bugs, que testes RED os demonstraram, mudanças mínimas feitas e decisões reais de revisão/refatoração. Não alegar TDD para um defeito se o processo não foi seguido.]

## Como executar

Requer Python 3.11+.

```bash
python -m pip install -r requirements-dev.txt
pytest -q
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json --top 5
```

## Resultados efetivamente observados

- Ambiente usado: [PREENCHER: versão Python e ambiente real].
- Resultado FINAL de `pytest -q`: [PREENCHER com comando, contagem e resultado reais; NÃO repetir o baseline como final].
- Resultado de análise estática: [PREENCHER com resultado real ou informar não executado].
- Exemplo oficial: [PREENCHER com resultado real].
- Relatório principal: [PREENCHER com resultado real].
- Limitações conhecidas: [PREENCHER ou declarar nenhuma identificada após testes, se verdadeiro].

## Uso de IA

Foi usado Manus como agente de apoio ao desenvolvimento, com detalhes e registro de sessões reais em `entrega/uso-de-ia/`. [VALIDAR QUE OS ARQUIVOS EXISTEM E REFLETEM A VERDADE.]
