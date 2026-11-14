# Guia de uso — Desafio Onfly com Manus

## Finalidade

Este pacote adapta ao desafio existente os princípios relatados por Fábio Akita: investigar antes de modificar, definir critérios verificáveis, escrever testes de regressão, implementar em incrementos mínimos, revisar a solução e preservar decisões úteis em Markdown. Não é uma reprodução literal de arquivos ou prompts de Akita.

**Este pacote não corrige o código.** Ele fornece instruções, critérios, testes sugeridos, registros e templates para orientar sua implementação no Manus.

## O que entregar, e o que NÃO construir

O objeto do desafio é corrigir o consolidador de reservas de hotéis já escrito em Python 3.11+. Preserve a interface de linha de comando (CLI), o contrato JSON e os testes entregues pela empresa. Não criar frontend, API HTTP, banco de dados, microsserviços, Docker obrigatório ou stack diferente. Não editar os arquivos de dados protegidos.

O projeto original exige um repositório GitHub público com `entrega/README-ENTREGA.md` e, quando usado assistente, `entrega/uso-de-ia/declaracao.md` **e o registro real das sessões**. O material de `entrega/` incluído neste pacote é um MODELO INCOMPLETO: preencha com fatos reais antes de enviar.

## Estrutura dos arquivos de apoio

- `AGENTS.md`: normas duráveis que o Manus deve consultar em cada etapa.
- `MANUS-PROJECT-INSTRUCTIONS.md`: texto conciso para colar nas instruções de um *Project* no Manus.
- `docs/CONTRATO.md`: especificação rastreável, derivada do `README.md` original.
- `docs/DIAGNOSTICO-INICIAL.md`: defeitos observados, baseline, e números independentes para validação.
- `docs/PLANO-TDD.md`: plano de reparo sequencial com checkpoints.
- `docs/MATRIZ-DE-TESTES.md`: cenários necessários além dos 5 testes fornecidos.
- `docs/SEGURANCA-E-ESCOPO.md`: isolamento, confiança nas fontes e limites de autonomia.
- `docs/DECISOES-E-PROGRESSO.md`: memória versionada e log de execução.
- `docs/CHECKLIST-DE-ENTREGA.md`: checklist final e comandos.
- `prompts/01-AUDITORIA.md` a `prompts/05-ENTREGA.md`: comandos prontos para enviar por etapa ao Manus.
- `templates/REGISTRO-SESSAO.md`: referência para registrar conversas REAIS; nunca submeter como se fosse transcrição.
- `entrega/`: modelos para preenchimento, sem alegar implementação realizada.

## Fluxo no Manus (interface web)

1. Crie um **Project** no Manus para este desafio, se o recurso estiver disponível em sua conta. Manus Projects preserva instruções e fontes para novas tarefas; uma conversa antiga não substitui isso.
2. Cole em **Project Instructions** o texto de `MANUS-PROJECT-INSTRUCTIONS.md`. Se não houver Projects, use esse texto no começo da tarefa e carregue os arquivos relevantes.
3. Anexe **o ZIP integrado** `onfly-desafio-com-guia-manus.zip` (preferencial), que inclui o código original e estes Markdown, ou anexe o ZIP original mais o ZIP apenas com Markdown. Se a interface não aceitar ZIP ou não conseguir extraí-lo, descompacte localmente e forneça o diretório/repositório por um meio que o Manus consiga acessar; confirme a raiz antes de executar comandos.
4. Na primeira tarefa, peça para extrair o projeto, confirmar a raiz, ler `README.md`, `AGENTS.md`, `docs/CONTRATO.md`, e executar `prompts/01-AUDITORIA.md`. **Não permitir mudanças de código nesta primeira etapa.**
5. Leia o relatório e execute `prompts/02-PLANO.md`. Autorize uma alteração por vez com `prompts/03-IMPLEMENTACAO-INCREMENTAL.md`, preenchendo o defeito alvo.
6. Ao terminar as correções, use `prompts/04-AUDITORIA-FINAL.md`. Somente depois peça `prompts/05-ENTREGA.md`.
7. Revise pessoalmente o `git diff`, as saídas de testes, o JSON real, a declaração de uso de IA e o histórico das sessões. Faça o envio ao GitHub após aprovação explícita.

## Comandos de referência — terminal Unix/Linux do Manus

```bash
python --version
python -m pip install -r requirements-dev.txt
pytest -q
ruff check src tests
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json --top 5
```

Se o ambiente só dispuser de `python3.11`, use esse executável. `ruff check` é uma verificação complementar; não altere código só para silenciar alertas que não se aplicam. Se não houver `pytest`/`ruff`, configure um ambiente virtual isolado e instale apenas as dependências do projeto; não afirme ter executado verificações inacessíveis.

**Observação de Git:** como o desafio veio em ZIP, pode não conter `.git`. Inicialize um repositório na raiz extraída e registre o baseline antes do primeiro conserto. Verifique o estado do repositório antes de usar comandos Git; nenhuma operação destrutiva sem confirmação.

## Critérios para aprovar cada etapa

O Manus deve entregar, em cada etapa: (1) problema reproduzido; (2) teste que falhava ou evidência equivalente; (3) arquivos alterados; (4) justificativa da menor correção; (5) testes executados e saída real; (6) `git diff` revisável; (7) limitações, quando existirem. Peça nova evidência caso algum item esteja faltando.

## Ordem de autoridade

`README.md` do desafio (regras/entrega) > testes originais imutáveis > código existente para compreender comportamento > documentação auxiliar gerada aqui > sugestões do agente. Em caso de conflito, não inventar semântica; registrar e resolver a partir do enunciado.

## Importante sobre histórico de IA

O enunciado exige exportação de sessões em formato nativo, **ou** log consolidado dos prompts e respostas reais, além de uma declaração do que a IA e o candidato fizeram. O Manus pode não fornecer o mesmo comando `/export` do Claude Code. Se a interface não permitir exportação nativa, guarde cronologicamente as mensagens completas (solicitações e respostas), os artefatos apresentados e as intervenções humanas. Jamais fabrique uma transcrição retrospectiva.
