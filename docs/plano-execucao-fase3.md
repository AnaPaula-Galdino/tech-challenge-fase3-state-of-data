# Plano de Execução: Tech Challenge Fase 3

**Versão:** v2.0, de 05/09/2026
**Prazo:** controlado pela Ana. Este plano organiza a ordem técnica das etapas, não datas.
**Documentos irmãos:** `fase3-matriz-rastreabilidade.md` e `fase3-diretrizes-docentes.md`

**Hierarquia de fontes:** o PDF oficial da Fase 3 é a única fonte da verdade da entrega. O consolidado do Discord é fonte de apoio operacional, usada para destravar erro técnico no ambiente AWS e para entender o que a banca observa. Ele não cria requisito, não substitui exigência e não autoriza reduzir escopo. Quando as duas fontes divergirem, prevalece o PDF, e a divergência fica registrada na matriz. Contribuição de aluno no canal não é considerada orientação.

---

## 1. Problema de negócio

Instituição financeira de grande porte pretende expandir sua área de Dados, Analytics e IA e precisa de evidências sobre o mercado brasileiro para decidir contratação, capacitação e investimento em tecnologia. Toda a análise responde a essas três decisões, que são o fio condutor da narrativa executiva.

## 2. Fontes de dados

Edições utilizadas, confirmadas no perfil oficial `datahackers` no Kaggle:

| Edição | Referência no Kaggle | Última atualização |
|--------|----------------------|--------------------|
| 2023-2024 | `datahackers/state-of-data-brazil-2023` | 20/06/2024 |
| 2024-2025 | `datahackers/state-of-data-brazil-20242025` | 09/05/2025 |
| 2025-2026 | `datahackers/state-of-data-brazil-2025-2026` | 09/07/2026 |

O corpo docente esclareceu que qualquer janela de três edições consecutivas é aceita nesta turma, dada a sazonalidade da pesquisa. Mantém-se a janela mais recente, que é a leitura literal do enunciado.

Os arquivos devem ser os originais baixados do Kaggle, em CSV, sem qualquer tratamento prévio. Converter para Excel ou corrigir acentuação antes do upload descaracteriza a camada Bronze e foi explicitamente desaconselhado pelo professor.

## 3. Arquitetura da solução

```
Kaggle (3 CSVs originais)
   | upload pelo console
   v
S3, bucket unico na regiao us-east-1
   +-- bronze/   dados brutos, particionados por edicao, formato original
   +-- silver/   dados harmonizados e tratados, Parquet
   +-- gold/     tabelas analiticas por pergunta de negocio, Parquet
   |
   +-- Glue Job 01 (PySpark)   bronze -> silver: encoding, tipagem, de/para de colunas, nulos e outliers
   +-- Glue Job 02 (PySpark)   silver -> gold: agregacoes por pergunta de negocio
   +-- Glue Data Catalog       registro das tabelas das tres camadas
   +-- Amazon Athena           consultas analiticas em SQL sobre a Gold
   |
   v
Python com matplotlib -> graficos em alta resolucao -> material executivo
```

Diagrama oficial no Draw.io, exportado em PNG e embutido no material executivo. O professor confirmou que o diagrama é do fluxo de dados de ponta a ponta, não da modelagem de tabelas.

## 4. Divisão de trabalho

Decisão registrada em 30/08/2026 e reforçada pela orientação docente de que o provisionamento pelo console visual é aceito:

1. **Claude:** desenvolve e testa todo o pipeline em PySpark neste ambiente, com o mesmo código que roda no Glue, e depois executa a solução no AWS Academy Lab operando o console pelo navegador da Ana.
2. **Ana:** inicia o laboratório e faz o login. A partir daí, acompanha a execução.

A rede deste ambiente de execução bloqueia o acesso direto aos serviços da AWS por política da organização, verificado em 05/09/2026, portanto a automação por linha de comando com credenciais temporárias não é possível. O caminho é o console, operado pelo navegador.

Regra de economia de créditos: nada é testado dentro do laboratório. Todo o processamento é validado aqui, com os mesmos dados e o mesmo código, e o lab recebe apenas a execução final já conferida.

O roteiro será dividido em blocos de menos de uma hora, porque as credenciais do Learner Lab expiram nesse intervalo, e cada bloco terá ponto de retomada.

## 5. Entregáveis

| # | Arquivo | Requisitos atendidos |
|---|---------|----------------------|
| 1 | `TechChallenge_Fase3_MaterialExecutivo.pptx` e PDF | R24, R25, R27, R31, R32 |
| 2 | `arquitetura_aws.drawio` e `arquitetura_aws.png` | R03, R26, R33 |
| 3 | Notebooks 01 a 05, de ingestão a gráficos | R05 a R10, R28 a R30 |
| 4 | `glue_jobs/job01_bronze_silver.py` e `job02_silver_gold.py` | R06, R07, R09 |
| 5 | `sql/consultas_athena.sql` | R08 |
| 6 | `dicionario_de_dados.md` e `mapa_equivalencia_edicoes.md` | R12 e rastreabilidade do tratamento |
| 7 | `roteiro_execucao_aws.md` | R02 |
| 8 | `roteiro_pitch_4min.md` | B01 |
| 9 | Repositório GitHub com README e artefatos | B03 |
| 10 | Matriz atualizada e relatório das quatro auditorias | Protocolo do projeto |

## 6. Ordem de execução

A sequência abaixo é encadeada por dependência técnica, não por calendário. Cada etapa começa quando a anterior está validada.

| Etapa | Descrição | Responsável | Depende de |
|-------|-----------|-------------|------------|
| 1 | Recepção das três bases originais e do material da Fase 2 | Ana | Nada |
| 2 | Dicionário de dados e mapa de equivalência entre edições | Claude | Etapa 1 |
| 3 | Pipeline Bronze, Silver e Gold em PySpark, testado ponta a ponta, scripts do Glue e roteiro de execução | Claude | Etapa 2 |
| 4 | Execução no AWS Academy Lab pelo navegador, com captura das evidências | Claude, com o lab iniciado pela Ana | Etapa 3 |
| 5 | Consultas no Athena e apuração dos indicadores das sete perguntas | Claude | Etapa 4 |
| 6 | Gráficos padronizados e diagrama no Draw.io | Claude | Etapa 5 |
| 7 | Material executivo em PowerPoint e PDF | Claude | Etapa 6 |
| 8 | Repositório GitHub e roteiro do pitch de 4 minutos | Claude | Etapa 7 |
| 9 | Quatro auditorias, correções e checklist final | Claude | Etapa 8 |
| 10 | Gravação do vídeo e entrega | Ana | Etapa 9 |

## 7. Riscos e limitações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Esquemas divergentes entre as três edições | Comparação histórica inválida | Mapa de equivalência explícito, só entram na série histórica as perguntas com equivalência confirmada |
| Bases com mais de 300 colunas | Processamento pesado e leitura difícil | Seleção das colunas de interesse já na Silver, documentada |
| Amostra autosselecionada, pesquisa voluntária | Conclusões não generalizáveis para todo o mercado | Limitação declarada no material executivo, leitura sempre relativa |
| Faixas de remuneração categóricas, não valores | Média salarial não é calculável diretamente | Uso da mediana da faixa, com a premissa declarada |
| Credenciais do lab expiram em cerca de uma hora | Interrupção no meio da execução | Roteiro em blocos curtos, com ponto de retomada |
| Teto de créditos do lab | Conta desativada | Pipeline testado fora do lab, sem reprocessamento desnecessário |

## 8. Decisões registradas

| Tema | Decisão |
|------|---------|
| Execução na AWS | Claude executa no console pelo navegador da Ana, após validar tudo fora do lab |
| Região | us-east-1, Norte da Virgínia, em todas as operações |
| Formato das camadas tratadas | Parquet na Silver e na Gold |
| Dados | Arquivos originais em CSV, baixados do Kaggle, sem tratamento prévio |
| Material executivo | PowerPoint editável e PDF final |
| Identidade visual | Sistema visual da Fase 2 preservado. Paleta final: `#4E8098` primária, `#8FBCD4` secundária, `#C1642F` destaque, no lugar do vinho da Fase 2 |
| Redação | Sem travessões, tom executivo e formal |
| Bônus | Roteiro de pitch de 4 minutos escrito por Claude, vídeo gravado pela Ana |
| GitHub | Repositório público com os artefatos, link citado no material executivo, como diferencial |
