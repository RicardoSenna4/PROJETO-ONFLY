# PROMPT 04 — Auditoria técnica final e oráculos

Copie apenas após todos os defeitos específicos terem sido implementados.

---

Realize uma auditoria integral do projeto Onfly como revisor independente, sem começar por refatoração. Leia o README original e os arquivos `AGENTS.md`, `docs/CONTRATO.md`, `docs/DIAGNOSTICO-INICIAL.md`, `docs/MATRIZ-DE-TESTES.md`, `docs/CHECKLIST-DE-ENTREGA.md`. Não confie nas afirmações de sessões anteriores: execute comandos e examine arquivos atuais.

1. Execute `pytest -q` e reporte contagem exata de testes e resultado. Verifique que os testes fornecidos estão preservados e que os CSVs protegidos não mudaram.
2. Execute `ruff check src tests` (ou reporte limitação) e `git diff --check` (se houver Git).
3. Execute o CLI na `data/exemplo-validacao.csv`; leia o JSON e compare cada campo relevante à tabela do README original.
4. Execute o CLI na `data/reservas_hoteis.csv` com `--top 5`; compare summary, meses, ranking e ordenações com os números em `docs/DIAGNOSTICO-INICIAL.md`.
5. Examine tipos JSON, 2 casas monetárias, `-03:00`, relatórios sem confirmadas, precisão Decimal, teste com 201+ linhas, `--top 0` e entrada inexistente.
6. Verifique o arredondamento antes de comparar totais: **não force** que a soma de subtotais já arredondados seja idêntica ao total geral; o README exige arredondamento na serialização.
7. Revise segurança, simplicidade e diff: código morto, duplicação real, mudanças fora do escopo, dados/segredos acidentais, mocks enganosos e alterações de interface.
8. Para qualquer problema, apresente reprodução e proposta de correção localizada. Não edite testes originais ou dados para mascará-lo.

Saída: tabela PASS/FAIL/NOT RUN por categoria, evidência de cada comando, discrepâncias reais, riscos residuais, arquivos alterados e parecer objetivo de prontidão. Se algum teste falhar, **não** declarar pronto para entrega. Não publicar sem autorização.
