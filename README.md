# Tech Challenge Fase 3, o mercado brasileiro de dados

Solução de Engenharia de Dados e Analytics sobre a pesquisa **State of Data Brazil**, construída em arquitetura de data lake em camadas na AWS, com processamento distribuído em Spark.

**Curso:** FIAP, Pós-Tech em Data Analytics
**Aluna:** Ana Paula Corrêa Galdino
**Entrega:** Fase 3

---

## 1. O problema

Uma instituição financeira de grande porte quer expandir sua área de Dados, Analytics e Inteligência Artificial. Antes de decidir quanto contratar, quanto capacitar e onde investir, ela precisa entender o mercado brasileiro de dados com base em evidência, não em percepção.

A resposta foi construída sobre as três últimas edições da pesquisa State of Data Brazil, do Data Hackers em parceria com a Bain: 2023-2024, 2024-2025 e 2025-2026. São 14.005 respostas originais, 14.002 após a remoção de três duplicatas integralmente idênticas, e 1.190 colunas somadas entre as três edições.

## 2. O que a análise mostrou

| Achado | Número |
|---|---|
| IA generativa como prioridade declarada na empresa | subiu de 36,2% para 60,6% em duas edições |
| IA generativa em produção, gerando resultado | apenas 26,5%, contra 38,4% em piloto sem impacto |
| Faixa salarial mediana do nível Sênior | subiu 40%, de R$ 10.000 para R$ 14.000 |
| Faixa salarial mediana de Júnior e Pleno | inalterada nas três edições |
| Faixa mediana por cargo, 2025-2026 | de R$ 18.000 em ML e AI Engineer a R$ 7.000 em analista de dados |
| Participação feminina | caiu nas duas transições da série, de 24,4% para 22,0% |
| Trabalho totalmente remoto | recuou de 46,3% para 39,7% |
| Satisfação por modelo de trabalho | 75,0% no híbrido flexível e 74,5% no remoto, empatados, contra 54,0% no presencial |
| Concentração em finanças e tecnologia | 36,0% dos profissionais, com os dois primeiros em empate estatístico |

A leitura completa, com premissas e limitações, está em `docs/achados-analiticos.md`.

## 3. Arquitetura

```
Kaggle (3 arquivos CSV)
   |
   v  ingestão
Amazon S3, data lake em camadas, região us-east-1
   |-- bronze/   dados crus, fiéis à origem, particionados por edição
   |-- silver/   harmonizada, uma linha por respondente, Parquet
   +-- gold/     tabelas analíticas por pergunta de negócio, Parquet
   |
   |-- AWS Glue Job 01 (PySpark)   bronze -> silver
   |-- AWS Glue Job 02 (PySpark)   silver -> gold
   |-- AWS Glue Data Catalog       camada Gold catalogada pelo crawler
   +-- Amazon Athena               consultas analíticas em SQL
   |
   v
Gráficos em Python  ->  material executivo
```

O diagrama completo está em `entregaveis/arquitetura_aws.drawio`, editável no Draw.io, e em `figuras/arquitetura_aws.png`.

## 4. O problema técnico central, e como foi resolvido

As três edições **não podem ser unidas pelo código da pergunta**. O código muda de significado entre edições. O exemplo mais grave: `2.q` identifica a ocorrência de demissões em massa em 2023-2024 e 2024-2025, e o modelo de trabalho em 2025-2026.

Levantamento completo:

- 330 códigos existem nas três edições, e 145 deles carregam pergunta diferente em pelo menos uma.
- 237 perguntas existem nas três edições, e 92 delas mudaram de código.

Uma união pelo código produziria gráficos comparando coisas diferentes, sem gerar erro nenhum na execução.

**Regra adotada:** cada coluna usada é confirmada por três critérios simultâneos, código, texto da pergunta e conjunto de categorias observado nos dados. Só entra na série histórica a coluna aprovada nos três. O mapa completo está em `dados/mapa_equivalencia_edicoes.csv`.

Outras divergências tratadas e documentadas em `src/harmonizacao.py`:

- Campos booleanos gravados como `0` e `1` em duas edições e como `TRUE` e `FALSE` na outra.
- Erros de digitação da própria pesquisa, como uma faixa salarial duplicada com limite errado e um porte de empresa escrito "de 501 a 100".
- Categorias que mudaram de redação mantendo o significado.
- A pergunta de linguagem preferida, que passou de escolha única para escolha múltipla em 2025-2026.
- O nível Especialista/Staff+, criado apenas na edição mais recente.

## 5. Estrutura do repositório

```
.
├── README.md
├── requirements.txt
├── src/
│   ├── schema.py                 leitor de cabeçalhos, cobre os três padrões de nomenclatura
│   ├── conceitos.py              mapa de conceitos de negócio por edição
│   ├── harmonizacao.py           regras de harmonização, cada uma com a origem comentada
│   ├── job01_bronze_silver.py    Glue Job 01, em PySpark
│   ├── job02_silver_gold.py      Glue Job 02, em PySpark
│   ├── estilo.py                 sistema visual dos gráficos
│   ├── graficos.py               geração das figuras, em versão completa e versão de slide
│   ├── diagrama.py               geração do diagrama de arquitetura
│   ├── gerar_notebooks.py        geração dos notebooks executados
│   └── gerar_deck.js             geração do material executivo em PPTX
├── notebooks/
│   ├── 01_ingestao_bronze.ipynb
│   ├── 02_bronze_para_silver.ipynb
│   ├── 03_silver_para_gold.ipynb
│   ├── 04_consultas_athena.ipynb
│   └── 05_analises_e_graficos.ipynb
├── sql/
│   └── consultas_athena.sql      registro das tabelas e consultas por pergunta do enunciado
├── docs/
│   ├── matriz-rastreabilidade-fase3.md   requisito a requisito do enunciado, com evidência
│   ├── achados-analiticos.md             todos os números, com base e limitação
│   ├── auditoria-bases.md                auditoria dos três arquivos de origem
│   ├── guia-visual.md                    paleta, anatomia do slide e regras dos gráficos
│   ├── plano-execucao-fase3.md           escopo, arquitetura e ordem de produção
│   ├── relatorio-triple-check-01.md      auditoria das bases e da paleta
│   ├── relatorio-auditoria-final.md      auditoria de ponta a ponta antes da entrega
│   ├── relatorio-execucao-aws.md         o que rodou no laboratório, com identificadores
│   ├── roteiro-execucao-aws.md           passo a passo para reproduzir no AWS Academy Lab
│   └── roteiro_pitch_4min.md             roteiro do vídeo pitch executivo
├── dados/
│   ├── mapa_equivalencia_edicoes.csv     equivalência de perguntas entre as três edições
│   └── gold_csv/                         camada Gold exportada em CSV, insumo dos gráficos
├── figuras/                      gráficos e diagrama, em alta resolução
│   └── deck/                     mesmas figuras sem título, para uso nos slides
└── entregaveis/
    ├── TechChallenge_Fase3_MaterialExecutivo.pptx / .pdf
    ├── arquitetura_aws.drawio / .png
    ├── glue/                     os dois jobs em versão autocontida, prontos para colar no Glue
    └── evidencias/               prints da execução no laboratório
```

Os arquivos de dados brutos e as camadas Bronze e Silver não são versionados, por tamanho. A seção 6 mostra como reconstruí-los a partir dos CSV originais do Kaggle.

## 6. Como reproduzir

Requisitos: Python 3.11 e Java 17 ou superior, necessário para o Spark.

```bash
pip install -r requirements.txt

# camada Bronze para Silver
python src/job01_bronze_silver.py --bronze dados/raw --silver dados/silver

# camada Silver para Gold
python src/job02_silver_gold.py --silver dados/silver --gold dados/gold

# gráficos e diagrama
python src/graficos.py
python src/diagrama.py
```

Os notebooks reproduzem as mesmas etapas com narrativa e saídas visíveis, e devem ser executados na ordem numérica.

Para executar no AWS Academy Lab, siga `docs/roteiro-execucao-aws.md`. Os scripts prontos para o Glue estão em `entregaveis/glue/`, em versão autocontida, sem dependência de módulos externos e já com `getResolvedOptions` para receber `JOB_NAME` e `BUCKET`. São esses os arquivos que foram executados no laboratório, não os da pasta `src/`, que são a versão local equivalente.

## 7. Dados de origem

Pesquisa State of Data Brazil, Data Hackers em parceria com a Bain, publicada no Kaggle:

- [State of Data Brazil 2023-2024](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-2023)
- [State of Data Brazil 2024-2025](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-20242025)
- [State of Data Brazil 2025-2026](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-2025-2026)

## 8. Limitações declaradas

- A pesquisa é de participação voluntária. Os resultados descrevem a comunidade respondente, não o universo dos profissionais de dados do país.
- A remuneração é coletada em faixas. Toda estatística usa o ponto médio da faixa e é apresentada como faixa mediana, nunca como salário médio.
- Os valores monetários são nominais. A variação entre edições não desconta a inflação do período.
- As perguntas sobre IA generativa são respondidas apenas por quem trabalha em empresa, com bases de 896, 1.045 e 652 respostas, menores que as da edição.
- A edição 2025-2026 tem 3.495 respondentes, contra 5.217 e 5.293 nas anteriores. Todas as comparações entre edições são percentuais, nunca absolutas.
- Perguntas presentes em apenas uma edição não entram em série histórica e são apresentadas em separado. É o caso do estágio dos projetos de IA, do nível Especialista/Staff+ e das perguntas de nuvem e ferramenta de BI.
- Diferenças entre categorias só viram afirmação depois de teste de significância. Onde o teste não rejeita a igualdade, o texto declara empate, como nos dois maiores setores e nos dois modelos de trabalho flexíveis.
