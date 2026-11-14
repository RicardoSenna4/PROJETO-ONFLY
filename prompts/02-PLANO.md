# PROMPT 02 — Planejamento e estratégia de testes

Copie depois de avaliar a auditoria do PROMPT 01.

---

Com base na auditoria REAL do desafio Onfly, produza um plano de implementação incremental com TDD, respeitando `README.md` e `AGENTS.md`.

1. Classifique cada comportamento errado como bug comprovado ou hipótese; relacione ao teste existente e à regra de negócio.
2. Para cada bug, proponha a menor mudança de produção possível. Se um teste fornecido já está vermelho por esse bug, use-o como RED e evite duplicar testes.
3. Para lacunas dos testes, indique novos arquivos `tests/test_*.py` e critérios de aceitação. Priorize leitura acima de 200, desempate exato, precisão `Decimal`, arredondamento HALF_UP, nenhuma confirmada, virada de ano e código de saída CLI.
4. Estabeleça ordem de implementação, comando de validação e risco de regressão de cada etapa.
5. Apresente explicitamente o que **não** será construído: interface web, APIs, serviços externos, banco de dados, refatoração ampla, novas dependências sem necessidade.
6. Defina como preservar o histórico de uso de IA: prompts + respostas reais e registro de decisões humanas, sem simular transcrição.
7. Se o projeto não tiver Git, proponha `git init`, baseline e commits locais pequenos, sem publicar.

Formato: tabela de etapas, RED esperado, GREEN esperado, arquivos afetados, comando de teste e checkpoint. **Não modifique código nesta tarefa. Aguarde minha autorização para começar o primeiro item.**
