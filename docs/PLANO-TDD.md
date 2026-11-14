# Plano TDD incremental — condução com o Manus

## Princípios

Não fazer uma correção gigantesca. O teste fornecido pode servir como fase RED se comprovar o comportamento errado; só escrever teste novo onde houver lacuna. Uma iteração é: **problema reproduzido → teste vermelho → menor correção → teste verde → suíte → revisão do diff → checkpoint humano**.

## Sequência sugerida

| Etapa | Alvo | Evidência RED | Mudança mínima esperada (a confirmar na investigação) | Testes de aceitação |
| --- | --- | --- | --- | --- |
| 0 | Baseline e Git | 5 testes falhando no original | Não editar código | Log do baseline + commit inicial. |
| 1 | Status (`D1`) | `tests/test_status_rules.py` | Permitir apenas `CONFIRMED`. | Teste de status e nenhuma regressão nova. |
| 2 | Noites (`D2`) | `tests/test_nights.py` | Subtrair objetos `date`. | Viradas de mês e ano, múltiplos quartos. |
| 3 | Câmbio (`D3`) | `tests/test_currency.py` | Multiplicar `Decimal` por taxa `Decimal`. | USD, EUR, BRL; precisão e half-up. |
| 4 | Ranking (`D4`) | `tests/test_top_hotels.py` | Ordenação decrescente pelo montante exato, segundo critério ID crescente. | Ranking original, desempates, `--top`. |
| 5 | Leitura completa (`D5`) | Escrever `tests/test_reader_full_input.py`, mais de 200 reservas | Remover limitação artificial da leitura. | 201+ entradas e relatório real de 300. |
| 6 | Integração | Exemplo e dataset real | Ajustes apenas se surgirem defeitos confirmados. | Sample 12, dataset 300, schema, CLI, erros. |
| 7 | Revisão | `git diff` e qualidade | Apenas refatoração justificada. | `pytest -q`, `ruff check`, 2 CLIs e oráculos. |
| 8 | Entrega | Evidências concluídas | Preencher templates com fatos e exportar sessões. | Checklist de entrega sem TODOs. |

A ordem 1–5 organiza dependências, mas pode ser ajustada se a investigação demonstrar custo/risco menor. Não usar o valor da taxa de câmbio como número mágico no código: ler arquivo de taxas existente.

## Como usar `prompts/03-IMPLEMENTACAO-INCREMENTAL.md`

Cole o prompt em uma tarefa do Manus e preencha **apenas um alvo** como, por exemplo, `D3 — currency_converter.py`. Diga explicitamente para parar ao terminar. Não disparar todos os alvos em paralelo; mudanças simultâneas no mesmo repositório tornam regressões e auditoria mais difíceis.

## Testes por comportamento, não por implementação

- Asserts de saída devem validar números, campos e ordenação, preferencialmente lendo o JSON gerado pelo CLI real.
- Evitar mocks que confirmam argumentos internos enquanto o cálculo real está errado.
- Testar CSV com nomes que contêm vírgulas, incluindo `Hotel Lisboa, Centro`.
- Um bug deve produzir teste vermelho por falha funcional concreta, não por importação faltante ou ambiente mal configurado.
- Não alterar um teste válido para adaptá-lo ao código defeituoso.
- Não introduzir testes artificiais sobre políticas que o enunciado não define.

## Checkpoint de cada etapa

```text
ETAPA: D?
ANTES: comportamento incorreto e comando/saída real.
RED: teste e falha observada.
DEPOIS: resumo do ajuste mínimo.
GREEN: teste alvo, suíte completa e resultados exatos.
ARQUIVOS: lista e diff revisável.
CONTRATO: invariantes preservados.
REGISTRO: atualização em docs/DECISOES-E-PROGRESSO.md.
PRÓXIMA: proposta, sem executá-la automaticamente.
```

## Quando refatorar

Depois de uma alteração localizada, revise as áreas modificadas. Se estiverem simples e claras, **não refatore por estética**. Se houver duplicação ou cálculo incoerente, faça uma refatoração pequena e independente, com os testes antes e depois. Nenhum novo framework, gestor de dependências ou pipeline CI é obrigatório para este desafio.
