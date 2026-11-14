# PROMPT 03 — Execução de UM defeito por vez

Antes de enviar, substitua `[ALVO]` por APENAS um item:

- `D1 — política de status (NO_SHOW não faturável)`
- `D2 — noites de quartos entre datas completas` 
- `D3 — conversão exata de moedas para BRL` 
- `D4 — ordenação do ranking por montante decrescente + desempate por ID` 
- `D5 — leitura integral de 201 ou mais reservas`

Repita este prompt para cada alvo. Mantenha o histórico ou forneça arquivos e memórias atualizados.

---

Autorizo implementar **somente [ALVO]** no repositório Onfly. Leia `README.md`, `AGENTS.md`, `docs/PLANO-TDD.md` e o estado atual de `docs/DECISOES-E-PROGRESSO.md`. Não tocar os demais defeitos, exceto se um bloqueio comprovado exigir minha decisão.

Siga RED → GREEN → REFACTOR:

**RED:** reproduza especificamente o defeito no código atual. Use o teste original quando apropriado; quando o bug não estiver coberto (por exemplo, limite de 200), adicione um teste de regressão em um ARQUIVO NOVO de testes, execute e confirme que falha pelo motivo funcional esperado.

**GREEN:** faça a menor alteração de código de produção necessária, sem renomear interfaces, alterar semântica de saída, mexer em CSVs ou testes fornecidos. Dinheiro deve permanecer `Decimal`. Execute teste alvo, testes relacionados e `pytest -q`. Uma suíte ainda vermelha por OUTROS defeitos esperados pode ocorrer durante o processo; identifique quais exatamente continuam falhando, sem dizer que o projeto já está concluído.

**REFACTOR:** inspecione apenas o código modificado. Refatore se e somente se houver simplificação justificada, mantendo os testes executáveis e sem alterar comportamento externo.

**REGISTRO:** atualize `docs/DECISOES-E-PROGRESSO.md` somente com resultados reais. Preserve evidências de testes, diff, decisões e possíveis mensagens da sessão de IA. Se existir Git, faça commit local pequeno e descritivo após revisar diff, mas não dê push.

**ENTREGUE:** resumo do antes/depois, evidência RED, diff, evidência GREEN (saídas reais), efeitos colaterais, pendências e proposta da próxima etapa. **PARE e aguarde autorização antes de corrigir outro defeito.**
