# Checklist de entrega — evidências em 15/11/2026

## Funcionalidade: aprovado

- [x] Cinco defeitos de status, diárias, câmbio, ranking e limite CSV corrigidos.
- [x] Cinco testes fornecidos preservados; 28 testes adicionais completam uma suíte de 33.
- [x] Python 3.11.18 com pytest 8.3.4: 33 testes passaram no GitHub Actions.
- [x] Ruff 0.8.4: análise estática aprovada no GitHub Actions.
- [x] Amostra oficial: 12 reservas, 28 diárias, total 7566.00 BRL.
- [x] Dataset original: 300 reservas, 235 confirmadas, 1347 diárias, total 396170.00 BRL.
- [x] JSON, valores como string, timezone -03:00, meses, ranking e CLI verificados.
- [x] Cálculo monetário com Decimal e arredondamento HALF_UP apenas na serialização.
- [x] Os três CSVs originais e os cinco testes fornecidos permaneceram byte a byte intactos.
- [x] PR #11 integrado sem conflito e histórico das correções preservado.
- [x] Dependências de produção não ampliadas e arquivos temporários ignorados.

## Qualidade e controle de versão

- [x] GitHub Actions: https://github.com/RicardoSenna4/PROJETO-ONFLY/actions/runs/43759288991 — sucesso.
- [x] Compilação Python verificada localmente.
- [x] Arquivos de entrega preenchidos com informações factual e limitadamente verificáveis.
- [x] CI na main após PR #14: execução #43759841195 concluída com sucesso no commit 897e1a6.
- [ ] Revisão humana final de cada diff e da declaração de uso de IA.
- [x] Checagem de whitespace concluída com sucesso no CI do merge PR #14.

## Documentação e envio: pendente

- [x] README-ENTREGA.md descreve cinco defeitos, causas, testes e como executar.
- [x] declaracao.md registra uso de ChatGPT/GPT-6 e distingue autoria Git de uso de IA.
- [x] indice-de-interacoes.md fornece rastreabilidade factual parcial.
- [ ] Anexar a exportação completa das interações ChatGPT ou log fiel e completo de prompts e respostas.
- [ ] Se Manus ou outro assistente também foi usado, anexar suas sessões reais e revisar a declaração.
- [ ] Enviar o link do repositório no formulário solicitado pela Onfly (não realizado).

**Resultado:** aprovação técnica comprovada; submissão ainda condicionada ao histórico integral de IA e confirmação humana.

## Verificações reproduzíveis

Em um ambiente Python 3.11 ou superior, a partir da raiz:

- python -m pip install -r requirements-dev.txt
- python -m pytest -q
- ruff check src tests
- PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json --top 5
- PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json --top 5
- git diff --check
