# Matriz de Rastreabilidade de Requisitos: Tech Challenge Fase 3

**Curso:** FIAP, Pós-Tech em Data Analytics (turma 13DTAT)
**Aluna:** Ana Galdino (trabalho individual)
**Fonte da verdade, única:** `DTAT, Tech Challenge, Fase 3.pdf` (6 páginas)
**Fonte de apoio operacional:** respostas do corpo docente no canal de dúvidas do Discord, consolidadas em `fase3-diretrizes-docentes.md`. Serve para destravar erro técnico e entender o que a banca avalia. Não cria, não substitui e não flexibiliza requisito. Em qualquer divergência, prevalece o PDF.
**Prazo:** controlado pela Ana
**Versão da matriz:** v6.0, de 05/09/2026
**Status permitidos:** `Atendido`, `Parcial`, `Pendente`, `Bloqueado (depende de decisão da Ana)`

---

## 1. Requisitos obrigatórios de insumo e ferramentas

| ID | Requisito (transcrição literal do PDF) | Página/seção | Entregável que atende | Evidência | Status |
|----|----------------------------------------|--------------|-----------------------|-----------|--------|
| R01 | "Histórico das 3 últimas pesquisas disponíveis no Data Hackers" | p. 3 | Camada Bronze | `docs/auditoria-bases.md`, seção 1. Confirmado por consulta ao catálogo do Kaggle em 05/09/2026 | Atendido |
| R02 | "Serviços da AWS através do ambiente AWS Academy Lab" | p. 3 | Pipeline executado no laboratório | Executado em 05/09/2026 na conta 857646333550, região us-east-1. `docs/relatorio-execucao-aws.md` e prints 1 a 4 | Atendido |
| R03 | "Draw.io para o desenho do diagrama da arquitetura da solução." | p. 3 | Diagrama da arquitetura | `entregaveis/arquitetura_aws.drawio`, editável no Draw.io, e `entregaveis/arquitetura_aws.png` | Atendido |
| R04 | "Link da base de dados do Data Hackers: https://www.kaggle.com/datahackers/datasets" | p. 3 | Bases brutas na camada Bronze | Três arquivos originais recebidos e auditados, `docs/auditoria-bases.md`, seção 2 | Atendido |

## 2. Etapas obrigatórias do pipeline

| ID | Requisito (transcrição literal do PDF) | Página/seção | Entregável que atende | Evidência | Status |
|----|----------------------------------------|--------------|-----------------------|-----------|--------|
| R05 | "Ingestão e organização das bases de dados no S3" | p. 3 | Camada Bronze no S3 | Bucket `tc3-state-of-data-857646333550`, três arquivos em prefixos por edição, tamanhos conferidos byte a byte contra a origem. Prints 1 e 2 | Atendido |
| R06 | "ETL/ELT e catalogação das tabelas com o Glue Jobs" | p. 3 | Glue Jobs 01 e 02, mais crawler | `tc3-job01-bronze-silver` SUCCEEDED em 134 s e `tc3-job02-silver-gold` SUCCEEDED em 142 s. Crawler `tc3-crawler-gold` SUCCEEDED, quatro tabelas no banco `workspace`. Prints 3 e 4 | Atendido |
| R07 | "Organização das camadas de dados (Bronze, Silver e Gold)" | p. 3 | Três camadas no S3 | Bronze com os CSV originais, Silver em Parquet particionada por edição, Gold com quatro tabelas. Estrutura visível nos prints 2 e 3 | Atendido |
| R08 | "Tratamento e consultas analíticas utilizando o Glue Notebook ou Athena" | p. 3 | Consultas no Athena | Consulta `33ab51b7-bd13-49eb-96ae-c8ae980fdad0` SUCCEEDED no Athena sobre a Gold catalogada, resultado idêntico ao do material executivo. Mais 9 consultas em `sql/consultas_athena.sql`. Print 4 | Atendido |
| R09 | "Utilização do Spark no processamento dos dados" | p. 3 | Processamento em PySpark | Executado no AWS Glue 4.0, que roda Spark. Os dois jobs são PySpark puro. Localmente validado em Spark 3.5.3, notebooks 02 e 03 | Atendido |
| R10 | "Geração de gráficos para as análises" | p. 3 | Treze gráficos e um diagrama | `figuras/`, gerados por `src/graficos.py`, a 200 pontos por polegada, em duas versões, completa e para slide. Notebook 05 | Atendido |

## 3. Requisitos de Applied Analytics

| ID | Requisito (transcrição literal do PDF) | Página/seção | Entregável que atende | Evidência | Status |
|----|----------------------------------------|--------------|-----------------------|-----------|--------|
| R11 | "aplicar conceitos de Applied Analytics para transformar os dados da pesquisa em informações úteis para a tomada de decisão" | p. 3 | Camada Gold orientada a indicadores de negócio | Quatro tabelas Gold organizadas por pergunta de negócio, `dados/gold/` | Atendido |
| R12 | "explorar, tratar e analisar os dados com o objetivo de compreender o perfil dos profissionais de tecnologia e dados no Brasil" | p. 3 e 4 | Análise exploratória e seção de perfil do material executivo | `docs/achados-analiticos.md` e slides 3, 4, 7 e 8 do material executivo | Atendido |
| R13 | "identificar tendências de mercado" | p. 4 | Série histórica das três edições | Todas as tabelas Gold têm a coluna edicao. Séries nos gráficos 1, 3, 4, 5, 6, 7 e 9 | Atendido |
| R14 | "mapear competências e tecnologias mais demandadas" | p. 4 | Análise de stack tecnológico | `figuras/fig07_linguagens.png`, sobre a tabela `gold_mencoes`, e `figuras/fig13_ferramentas.png`, sobre nuvem e ferramenta de BI preferidas. Slides 13 e 14 | Atendido |
| R15 | "avaliar diferenças por senioridade, região, modelo de trabalho e remuneração" | p. 4 | Quatro recortes segmentados | Tabela `gold_salario` com seis recortes e `gold_cruzamentos` com dez pares | Atendido |
| R16 | "propor recomendações estratégicas para empresas que desejam contratar, capacitar e investir em Dados, Analytics e Inteligência Artificial" | p. 4 | Seção de recomendações do material executivo | Slide 20 do material executivo, com as três decisões amarradas a números apresentados antes | Atendido |

## 4. Perguntas que a apresentação deve responder

| ID | Requisito (transcrição literal do PDF) | Página/seção | Entregável que atende | Evidência | Status |
|----|----------------------------------------|--------------|-----------------------|-----------|--------|
| R17 | "Como está estruturado o mercado brasileiro de Dados?" | p. 4 | Bloco 1 da apresentação | Slides 7 e 8, setor e região, com teste de significância na diferença entre os dois maiores setores | Atendido |
| R18 | "Quais perfis profissionais são mais valorizados pelo mercado?" | p. 4 | Bloco 2 | Slide 9, faixa salarial mediana por nível nas três edições, e slide 10, mediana por cargo na edição 2025-2026, com o número de respostas por cargo | Atendido |
| R19 | "Qual é o cenário de diversidade de gênero nas carreiras de dados?" | p. 4 | Bloco 3 | Slides 11 e 12, série da participação feminina e distribuição por nível dentro de cada gênero | Atendido |
| R20 | "Quais tecnologias apresentam maior adoção entre os profissionais?" | p. 4 | Bloco 4 | Slide 13, menções por linguagem preferida, com a mudança de formato declarada, e slide 14, nuvem e ferramenta de BI preferidas | Atendido |
| R21 | "Qual é o índice de adoção de Inteligência Artificial e seu impacto?" | p. 4 | Bloco 5 | Índice de adoção nos slides 15 e 16, série e detalhe por posição declarada. Impacto no slide 17, estágio dos projetos de IA generativa, com 26,5% em produção gerando resultado contra 38,4% em piloto sem impacto | Atendido |
| R22 | "Existem diferenças relevantes entre regiões, senioridades ou modelos de trabalho?" | p. 4 | Bloco 6 | Slides 8, 9, 18 e 19, região, senioridade, modelo de trabalho e satisfação e remuneração por modelo | Atendido |
| R23 | "Quais oportunidades e desafios podem ser identificados para empresas que desejam investir em Dados e Inteligência Artificial?" | p. 4 | Bloco 7 | Slides 17, 19 e 20, lacuna entre prioridade e resultado em IA, satisfação por modelo e recomendações | Atendido |

## 5. Entregáveis formais

| ID | Requisito (transcrição literal do PDF) | Página/seção | Entregável que atende | Evidência | Status |
|----|----------------------------------------|--------------|-----------------------|-----------|--------|
| R24 | "material executivo em PowerPoint ou PDF, apresentando os principais indicadores, análises, insights e recomendações" | p. 4, Entrega 1 | `TechChallenge_Fase3_MaterialExecutivo.pptx` e PDF | 22 slides, validação estrutural aprovada e três rodadas de inspeção visual, a última sobre o PDF renderizado página a página | Atendido |
| R25 | "deve construir uma narrativa clara sobre o perfil dos profissionais [...] tendências de mercado, uso de tecnologias, remuneração, senioridade, modelos de trabalho e oportunidades estratégicas" | p. 4, Entrega 1 | Storytelling em sete blocos | Sequência situação, complicação, resolução, evidências e recomendações, slides 2 a 20 | Atendido |
| R26 | "diagrama da arquitetura da solução AWS, preferencialmente construído no Draw.io, evidenciando os serviços utilizados e o fluxo dos dados desde a ingestão até o consumo analítico" | p. 4, Entrega 2 | Diagrama da arquitetura | `entregaveis/arquitetura_aws.drawio` e PNG. Fluxo de ponta a ponta, da ingestão ao consumo | Atendido |
| R27 | "O desenho deve estar contido no material executivo." | p. 4, Entrega 2 | Slide de arquitetura | Slide 5 do material executivo | Atendido |
| R28 | "entregar os scripts, notebooks e códigos utilizados, de forma organizada e consolidada" | p. 5, Entrega 3 | Pacote único de códigos | `entregaveis/TechChallenge_Fase3_Codigos.zip`, com src, notebooks, sql, glue, docs, figuras, dados de apoio, README e requirements | Atendido |
| R29 | "Os códigos devem estar preferencialmente em arquivos de Notebook, com o uso de Spark/PySpark e/ou SQL" | p. 5, Entrega 3 | Notebooks executados e SQL | Cinco notebooks, 29 células de código, todas executadas na ordem e com saída visível, zero erros. Doze consultas SQL, todas executadas contra a camada Gold, zero falhas | Atendido |
| R30 | "demonstrando as etapas de ingestão, tratamento, transformação, catalogação, consultas analíticas e geração dos dados utilizados nas análises e gráficos" | p. 5, Entrega 3 | Notebooks 01 a 05, na ordem do pipeline | Ingestão, tratamento, transformação, catalogação, consultas e gráficos, um notebook por etapa | Atendido |

## 6. Requisitos de contexto, restrições e implícitos

| ID | Requisito (transcrição literal do PDF) | Página/seção | Entregável que atende | Evidência | Status |
|----|----------------------------------------|--------------|-----------------------|-----------|--------|
| R31 | "conectando arquitetura de dados, processamento em ambiente AWS, análise exploratória, DataViz e Storytelling para responder ao problema de negócio proposto" | p. 4, Expectativas | Coerência entre os três entregáveis | O diagrama do slide 5 descreve o pipeline dos notebooks, que produz os números dos slides 7 a 19 | Atendido |
| R32 | Cliente é "uma Instituição Financeira de grande porte" que precisa "definir suas estratégias de contratação, capacitação de profissionais e investimentos em tecnologia" | p. 2 | Enquadramento do problema e das recomendações | Slide 3, contexto, e slide 20, recomendações dirigidas às três decisões do cliente | Atendido |
| R33 | "o desafio simula uma arquitetura moderna de Big Data & Analytics em ambiente Cloud [...] Data Lake, processamento distribuído, organização em camadas, transformação de dados, catalogação, consultas analíticas e visualização executiva" | p. 3 | Slide de arquitetura e narrativa técnica | Data lake em camadas, processamento distribuído, catalogação e consulta, slides 5 e 6 | Atendido |
| R34 | "NÃO será oferecida nenhuma ferramenta de DataViz e sua adoção é opcional [...] não são exigidos Dashboards na entrega final" | p. 3 | Decisão registrada | Gráficos gerados em Python, nenhum dashboard entregue, conforme a restrição do enunciado | Atendido |
| R35 | "este é um entregável obrigatório da fase", com pontuação equivalente a 90% da nota final, e atenção ao prazo | p. 2 e p. 5 | Controle de prazo | Gerido pela Ana | Pendente |
| R36 | "Lembre-se de que você poderá apresentar a evolução do projeto durante as lives com os docentes." | p. 5 | Material parcial disponível para as lives | Documentação e material executivo prontos e versionados no projeto | Atendido |

## 7. Diretrizes operacionais do corpo docente (apoio, não requisito)

Origem: canal de dúvidas do Discord da turma 13DTAT, extração de 04/09/2026. A consolidação completa fica em `docs/fase3-diretrizes-docentes.md`, material de apoio interno que **não é publicado no repositório**, por reproduzir mensagens de terceiros do canal da turma. Estas linhas não são requisitos e não entram na contagem de conformidade. Só entra aqui o que foi escrito por professor ou coordenação, nunca contribuição de aluno. Onde a orientação flexibiliza o enunciado, o projeto segue a leitura literal do PDF, registrada na coluna de efeito.

| ID | Diretriz | Autoria | Efeito no projeto | Status |
|----|----------|---------|-------------------|--------|
| D01 | Toda operação na AWS deve ocorrer na região us-east-1 (Norte da Virgínia). Região de São Paulo gera erros de permissão | Prof. Thiago Generoso | Primeiro item do roteiro de execução | Aplicado |
| D02 | Não tratar os dados no Excel antes de subir ao S3, sob pena de descaracterizar a camada Bronze | Prof. Rafael Moura | Os arquivos originais do Kaggle sobem crus, em CSV | Aplicado |
| D03 | Criar a infraestrutura pelo console visual é aceito, não é exigido script de AWS CLI para provisionamento | Prof. Thiago Generoso | Reduz escopo: entregam-se apenas scripts de criação de tabelas e consultas | Aplicado |
| D04 | No Athena, configurar o local de resultados e criar o database antes de tudo (`CREATE DATABASE WORKSPACE;`) | Prof. Rafael Moura | Passo 3 do roteiro de execução | Aplicado |
| D05 | No nó Target do Visual ETL é obrigatório preencher database e nome da tabela, senão a tabela não aparece no Athena | Prof. Rafael Moura | Ponto de checagem no roteiro | Aplicado |
| D06 | Redshift não funciona no AWS Academy, o conteúdo é conceitual | Coordenação | Fora do escopo da solução | Aplicado |
| D07 | Camadas tratadas devem ser gravadas em Parquet | Aulas e canal | Silver e Gold em Parquet | Aplicado |
| D08 | Aviso de "output limit exceeded" no Athena é normal, efeito das mais de 300 colunas | Prof. Rafael Moura | Não tratar como falha | Aplicado |
| D09 | Credenciais do Learner Lab expiram em cerca de uma hora | Prof. Rafael Moura | Roteiro dividido em blocos curtos, com ponto de retomada | Aplicado |
| D10 | GitHub não é obrigatório, mas é diferencial, e o link pode ser citado no material executivo | Prof. Rafael Moura | Decisão da Ana: fazer o repositório e citar o link no material executivo | Aplicado |
| D11 | Qualquer janela de três edições consecutivas é aceita nesta turma, dada a sazonalidade da pesquisa | Prof. Rafael Moura | Flexibilização não aproveitada. O PDF pede as três últimas disponíveis e é o que será entregue: 2023-2024, 2024-2025 e 2025-2026 | Aplicado |
| D12 | O lab tem teto de créditos e pode ser desativado, evitar reprocessamento desnecessário | Coordenação | Pipeline roteirizado, sem retrabalho no lab | Aplicado |

## 8. Itens fora do enunciado, definidos pela Ana

| ID | Item | Entregável | Evidência | Status |
|----|------|------------|-----------|--------|
| B01 | Roteiro do pitch executivo de 4 minutos | `entregaveis/roteiro_pitch_4min.md` | Seis blocos cronometrados, 568 palavras faladas, tempo estimado de 3 minutos e 55 segundos a 145 palavras por minuto | Atendido |
| B02 | Vídeo pitch executivo de até 4 minutos | Gravação feita pela Ana a partir do roteiro | (pendente) | Pendente |
| B03 | Repositório GitHub com os artefatos, citado no material executivo | Repositório público [github.com/AnaPaula-Galdino/tech-challenge-fase3-state-of-data](https://github.com/AnaPaula-Galdino/tech-challenge-fase3-state-of-data) | 71 arquivos em 12 commits: código, notebooks executados, SQL, jobs Glue, documentação, camada Gold em CSV, figuras e entregáveis. Link citado nos slides 21 e 22 do material executivo | Atendido |

> **Nota 1:** a apresentação executiva não é bônus, ela é a Entrega 1 obrigatória (R24 e R25). O diferencial perante o avaliador é o par roteiro e vídeo pitch, mais o repositório GitHub, que o próprio professor classificou como diferencial.
>
> **Nota 2:** os itens B01 a B03 são adicionais e nunca podem competir com os requisitos do PDF por tempo ou atenção. Se o prazo apertar, a ordem de sacrifício é B02, depois B03, depois B01. Nenhum requisito de R01 a R36 pode ser reduzido para viabilizar um bônus.

---

## 9. Situação da matriz

| Status | Quantidade |
|--------|-----------|
| Atendido | 37 |
| Pendente | 2 |

**Os 35 requisitos verificáveis do enunciado estão atendidos e evidenciados.** O trigésimo sexto, R35, é o controle de prazo, que não é entregável e permanece sob responsabilidade da Ana. A pendência restante é um item adicional, fora do enunciado:

| ID | O que falta | Natureza |
|----|-------------|----------|
| R35 | Controle de prazo | Sob responsabilidade da Ana |
| B02 | Gravação do vídeo pitch | Item adicional, roteiro entregue e cronometrado em 3 minutos e 55 segundos |

A auditoria de ponta a ponta executada em 05/09/2026, antes da publicação, encontrou e corrigiu 19 não conformidades, entre erros factuais, imprecisões estatísticas e lacunas de conformidade com o enunciado. O relatório completo, camada por camada, está em `docs/relatorio-auditoria-final.md`.

A execução na AWS, realizada em 05/09/2026, fechou os requisitos R02, R05, R06 e R08, que eram os últimos pendentes do enunciado. O relatório completo, com identificadores de recurso, tempos de execução e resultado das consultas, está em `docs/relatorio-execucao-aws.md`.
