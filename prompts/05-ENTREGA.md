# PROMPT 05 — Preparar documentação de entrega sem falsificar evidências

Copie apenas depois da auditoria final passar, ou peça que marque pendências explicitamente.

---

Prepare a entrega do desafio Onfly preservando o projeto, seus testes originais, dados e contrato de CLI. Leia `README.md` (seção Entrega), `AGENTS.md`, `docs/DECISOES-E-PROGRESSO.md` e `docs/CHECKLIST-DE-ENTREGA.md`.

1. Preencha `entrega/README-ENTREGA.md` com defeitos efetivamente corrigidos, **uma frase de causa raiz por defeito**, como cada defeito foi investigado, estratégia RED/GREEN/REFACTOR, comandos de validação e resultado literalmente observado do `pytest -q` final (incluindo contagem de testes). Não declare sucesso se algum comando não tiver sido executado.
2. Preencha `entrega/uso-de-ia/declaracao.md`: identifique Manus como ferramenta, o(s) modelo(s) **somente se confirmado(s)** pela interface ou logs, tarefas específicas feitas pela IA e tarefas realmente feitas pelo candidato. Se o modelo não for verificável, escreva `modelo não disponibilizado/confirmado pela interface`.
3. Organize o histórico REAL da(s) sessão(ões) em `entrega/uso-de-ia/` na exportação nativa disponível ou log consolidado cronológico com **prompts e respostas**, sem resumir seletivamente nem simular exportações. Se não puder acessar o histórico completo, avise o candidato; não fabrique o conteúdo.
4. Execute verificações finais pertinentes e confira que os templates não deixam `TODO`, `PENDENTE` ou resultados exemplificativos no texto de entrega.
5. Revise `git status`, diff e `.gitignore`, garantindo que não existem credenciais, ambientes virtuais, caches, outputs temporários ou mudanças nos arquivos proibidos. O repositório público não deve conter segredos extraídos das sessões.
6. Entregue um relatório final de prontidão, arquivos a commitar, comandos Git sugeridos e pendências humanas. **Não crie repositório remoto, não faça push, não altere a visibilidade e não envie forms sem minha autorização explícita.**
