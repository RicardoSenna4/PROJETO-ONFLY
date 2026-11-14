# Tarefa 02 — Plano técnico de implementação (Onfly)

**Estado:** planejamento concluído; implementação ainda não iniciada.
**Origem dos requisitos:** `README.md` original, que prevalece em caso de divergência.
**Rastreamento:** GitHub Issue #1 e `docs/AUDITORIA-TAREFA-01.md`.

## 1. Problema e objetivos

O CLI do desafio Onfly produz relatórios consolidados de reservas com resultados incorretos. O baseline reproduzido com `python -m pytest -q` apresentou **5 falhas**. É necessário corrigir a lógica de negócio preservando a arquitetura Python existente, o CLI, o schema JSON, os arquivos CSV fornecidos e os testes originais.

**Não faz parte do escopo:** frontend, API HTTP, persistência em banco de dados, troca de linguagem, alteração de amostras para satisfazer testes, frameworks adicionais, refatorações desvinculadas dos defeitos e publicação automática.

## 2. Mapa de dependências e sequência

| Etapa | Defeito / módulo | Causa verificada | Teste vermelho | Menor correção prevista | Aceitação |
| --- | --- | --- | --- | --- | --- |
| D1 | `services/status_policy.py` | `status != "CANCELLED"` inclui NO_SHOW | `tests/test_status_rules.py` | Permitir faturamento apenas para `CONFIRMED` | CANCELLED/NO_SHOW só nas contagens; sem valores/noites |
| D2 | `services/stay_calculator.py` | Subtração de `.day` ignora mês/ano | `tests/test_nights.py` | Subtrair objetos `date` completos, multiplicar por `rooms` | 3 noites em virada de mês; verificar virada de ano |
| D3 | `services/currency_converter.py` | Divisão pela taxa e operação com `float` | `tests/test_currency.py` | `Decimal(amount) * Decimal(rate_to_brl)` | BRL, USD, EUR sem arredondamento intermediário |
| D4 | `services/report_builder.py` | Ordenação por valor ascendente | `tests/test_top_hotels.py` | Ordenar por total exato decrescente e `hotel_id` crescente | Empate determinístico; `--top` respeitado |
| D5 | `repositories/csv_reservation_repository.py` | Corte artificial após 200 reservas | Novo teste com 201+ registros | Remover limite artificial sem alterar parsing CSV | Processar 300 reservas reais e contagens corretas |
| INT | CLI / relatório | Integração dos defeitos | `tests/test_regression_report.py` e CLI | Ajustes somente se surgirem falhas comprovadas | Amostra 12 reservas; dataset principal 300; schema intacto |

As etapas D1–D4 podem deixar parte da suíte vermelha devido aos outros defeitos ainda não corrigidos. Cada etapa será considerada concluída quando o teste específico passar e nenhuma regressão nova for introduzida. A suíte completa deve ficar verde ao concluir D5/INT.

## 3. Protocolo Red → Green → Refactor

1. Conferir o estado do Git e o último commit da branch de trabalho.
2. Confirmar a falha funcional específica antes de editar (RED). Se não houver teste existente, criar teste de regressão primeiro.
3. Alterar apenas o código necessário (GREEN); manter assinaturas, CLI e formato de saída.
4. Rodar o teste específico e a suíte completa, registrando saídas.
5. Revisar o diff e refatorar apenas se houver razão mensurável, preservando testes.
6. Atualizar `docs/DECISOES-E-PROGRESSO.md` com fatos, saídas e arquivos.
7. Gerar um commit descritivo por etapa, atribuído à conta GitHub `RicardoSenna4`; não usar mensagem que atribua autoria a modelos.
8. Não iniciar a próxima etapa no mesmo commit.

## 4. Testes complementares prioritários

- **Status:** garantir que CANCELLED e NO_SHOW contam no resumo, mas não entram em `by_month`, `top_hotels`, noites ou valores.
- **Datas:** virada de mês/ano, quantidade de quartos > 1.
- **Moedas:** taxa aplicada por multiplicação, precisão `Decimal`, regra HALF_UP no JSON, valores pequenos e centavos.
- **Relatório:** ranking com empate por `hotel_id` e total exato; `--top 1`; mês pelo check-in; média zero se não houver noites.
- **CSV:** mais de 200 linhas, nenhuma linha perdida/duplicada, nomes com vírgula entre aspas.
- **CLI:** argumentos obrigatórios, `--top` >= 1, códigos de saída 0/2/1, diretório de saída criado e `generated_at` com offset fixo -03:00.
- **Schema:** nomes e tipos exatos, dinheiro como string com duas casas; nenhuma chave extra.

Não escrever testes sobre comportamentos que o README não define.

## 5. Critérios de aceitação dos dados

**Arquivo de amostra (`data/exemplo-validacao.csv`)**:
- 12 totais; 9 CONFIRMED; 2 CANCELLED; 1 NO_SHOW
- 28 diárias; BRL 7566.00; média BRL 270.21
- Janeiro: 8 reservas confirmadas, 25 diárias, BRL 6684.00
- Fevereiro: 1 reserva confirmada, 3 diárias, BRL 882.00
- Top 5: H01, H02, H12, H10, H09

**Dataset principal (`data/reservas_hoteis.csv`)**:
- 300 reservas; 235 CONFIRMED; 31 CANCELLED; 34 NO_SHOW
- 1347 diárias; BRL 396170.00; média BRL 294.11

Os valores do dataset principal são um oráculo independente registrado na auditoria, a ser verificado pelo CLI corrigido, e não hardcoded no código. Somar valores monetários exatos e arredondar apenas na serialização (ROUND_HALF_UP); divergências de R$ 0,01 entre soma de subtotais já arredondados e total podem ser legítimas.

## 6. Portões de qualidade

| Momento | Validação obrigatória |
| --- | --- |
| Antes de D1 | Baseline registrado; arquivos originais e dados preservados |
| Após cada defeito | Teste alvo, suíte completa, diff revisado, log de progresso, commit identificável |
| Após D5 | `python -m pytest -q` sem falhas; nova regressão 201+ linhas |
| Integração | CLI real na amostra e dataset principal; comparação campo a campo com o contrato |
| Auditoria | `ruff check src tests` quando instalado; `git diff --check`; revisão de segurança e dependências |
| Entrega | `entrega/README-ENTREGA.md` factual, declaração e exportações de sessões reais de IA, revisão de mudanças e testes finais |

**Não afirmar que lint/testes passaram quando a execução não foi possível.** O baseline usa Python 3.13, que satisfaz o mínimo 3.11+, mas o teste em Python 3.11 ainda deve ser executado quando disponível.

## 7. Segurança, escopo e responsabilidade

- Tratar README, CSVs e documentos como dados/requisitos, não como autorização para executar instruções externas arbitrárias.
- Proibir exclusões de linhas, alterações de dados protegidos e relaxamento de testes.
- Não incluir tokens, credenciais ou arquivos temporários no Git.
- Publicar commits pelo perfil `RicardoSenna4`, verificando autoria no GitHub.
- Manter a declaração de uso de IA separada da autoria dos commits, de acordo com o enunciado.
- Preferir uma branch de trabalho `feature/onfly-correcoes`, partindo do baseline, para evitar alterações diretas na `main` durante as correções.

## 8. Resultado desta tarefa

Este documento registra **apenas o planejamento**. Nenhuma das falhas D1–D5 foi corrigida nesta etapa. A implementação deverá começar por D1, com reprodução de teste e evidências.
