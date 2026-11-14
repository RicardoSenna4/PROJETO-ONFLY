# Checklist de auditoria e entrega — Onfly

Marcar somente depois de executar e conferir. O Manus pode preparar arquivos, mas a revisão e autorização final são do candidato.

## Funcional

- [ ] `pytest -q` passa com os 5 testes fornecidos, intactos.
- [ ] Testes adicionados cobrem status, noites em fronteiras, moeda exata, desempate, leitura 201+ e serialização.
- [ ] Amostra de 12 reservas confere integralmente com o README original.
- [ ] Dataset principal confere com `docs/DIAGNOSTICO-INICIAL.md`: 300 reservas; 235 confirmadas; 31 canceladas; 34 no-show; 1347 noites; R$ 396170.00; média 294.11; meses e top 5.
- [ ] Relatório JSON tem chaves/tipos/nome de campos exatos, valores monetários string com duas casas.
- [ ] Não há `float` no fluxo financeiro; arredondamento somente ao serializar com `ROUND_HALF_UP`.
- [ ] Ranking usa valor exato decrescente, desempate ID ascendente; meses crescentes pelo check-in.
- [ ] `generated_at` tem offset `-03:00`.
- [ ] CLI funciona com `--input`, `--rates`, `--output`, `--top`; defaults e retornos 0/2/1.
- [ ] CLI cria o diretório `output/`, imprime resumo no stdout, erros no stderr quando apropriado.

## Qualidade

- [ ] `ruff check src tests` executado e resultado verificado (sem alterar testes fornecidos para corrigir lint).
- [ ] `git diff --check` executado, saída verificada.
- [ ] Diff final contém somente alterações necessárias.
- [ ] Nenhum CSV ou teste original foi modificado; conferir contra arquivos originais.
- [ ] `.gitignore` evita commitar output temporário, ambiente virtual, caches e segredos.
- [ ] Requisitos e arquitetura mantidos, sem dependências novas desnecessárias.

## Entrega exigida

- [ ] `entrega/README-ENTREGA.md` descreve cada defeito corrigido, causa raiz em uma frase, processo de investigação, validação e resultado VERDADEIRO de `pytest`.
- [ ] `entrega/uso-de-ia/declaracao.md` preenchido porque houve uso de Manus; registra ferramentas/modelos verificáveis e divisão real de trabalho.
- [ ] `entrega/uso-de-ia/` contém exportação de sessão(ões) REAL(REAIS) ou log fiel e completo das solicitações e respostas; não deixar somente template.
- [ ] Nenhum `PENDENTE`, `TODO`, exemplo de resposta ou afirmação não verificada nos arquivos de entrega.
- [ ] Repositório público GitHub contém o projeto completo e está livre de credenciais ou arquivos pessoais.
- [ ] Link enviado ao canal/forms solicitado pela empresa.

## Últimos comandos orientativos

```bash
pytest -q
ruff check src tests
git diff --check
git status --short
git diff -- README.md data/reservas_hoteis.csv data/taxas_cambio.csv tests/
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json --top 5
```

Ao auditar integridade dos arquivos originais, comparar hashes SHA-256 ou `git diff` a partir do commit baseline, conforme o repositório. O comando `git diff -- tests/` só cobre alterações rastreadas; use `git status` para localizar também arquivos novos.
