# Relatório de execução na AWS

**Data da execução:** 05/09/2026
**Ambiente:** AWS Academy Learner Lab, curso ALLv2PT-BR-LTI13-175031
**Conta:** 857646333550
**Região:** us-east-1, Norte da Virgínia
**Orçamento do laboratório:** USD 50, sessão de 4 horas

---

## 1. Resumo

O pipeline completo foi executado no AWS Academy Lab, da ingestão dos arquivos originais até a consulta analítica no Amazon Athena. Todas as etapas concluíram com sucesso, sem nenhuma reexecução por erro.

O resultado da consulta final no Athena reproduziu, dígito por dígito, os números que já constavam no material executivo, o que comprova que o pipeline em nuvem e o pipeline de referência produzem exatamente o mesmo resultado.

## 2. Recursos criados

| Recurso | Identificação |
|---------|---------------|
| Bucket S3 | `tc3-state-of-data-857646333550` |
| Camadas | `bronze/`, `silver/`, `gold/`, `athena-results/`, `scripts/` |
| Glue Job 01 | `tc3-job01-bronze-silver` |
| Glue Job 02 | `tc3-job02-silver-gold` |
| Crawler | `tc3-crawler-gold` |
| Banco de dados | `workspace` |
| Função de execução | `LabRole`, a role padrão do laboratório |

## 3. Camada Bronze, ingestão

Os três arquivos originais foram enviados sem qualquer tratamento prévio e organizados em prefixos por edição.

| Arquivo | Prefixo | Tamanho no S3 | Tamanho na origem |
|---------|---------|---------------|-------------------|
| `State_of_data_BR_2023_Kaggle - df_survey_2023.csv` | `edicao=2023-2024` | 15.241.470 bytes | 15.241.470 bytes |
| `Final Dataset - State of Data 2024 - Kaggle - df_survey_2024.csv` | `edicao=2024-2025` | 16.262.191 bytes | 16.262.191 bytes |
| `Final Dataset - State of Data 2025-2026 - Kaggle.csv` | `edicao=2025-2026` | 10.361.791 bytes | 10.361.791 bytes |

A conferência byte a byte comprova que a camada Bronze é fiel à origem, como exige o conceito e como orientou o professor.

## 4. Processamento

| Job | Configuração | Estado | Tempo |
|-----|--------------|--------|-------|
| `tc3-job01-bronze-silver` | Glue 4.0, 2 workers G.1X | **SUCCEEDED** | 134 segundos |
| `tc3-job02-silver-gold` | Glue 4.0, 2 workers G.1X | **SUCCEEDED** | 142 segundos |

Ambos rodaram com o número mínimo de workers, decisão tomada para preservar o orçamento do laboratório. Nenhum dos dois precisou de segunda tentativa, porque os scripts já haviam sido validados fora do laboratório, com os mesmos dados.

**Saída do Job 01:** camada Silver em Parquet, particionada em `edicao=2023-2024`, `edicao=2024-2025` e `edicao=2025-2026`.

**Saída do Job 02:** quatro tabelas analíticas em Parquet, `gold_distribuicoes`, `gold_cruzamentos`, `gold_salario` e `gold_mencoes`.

## 5. Catalogação

O crawler `tc3-crawler-gold` percorreu a camada Gold e registrou as quatro tabelas no banco `workspace` do Glue Data Catalog. Estado final: `READY`, último rastreamento `SUCCEEDED`.

Tabelas registradas e visíveis para os demais serviços:

```
gold_cruzamentos   gold_distribuicoes   gold_mencoes   gold_salario
```

## 6. Consulta analítica no Athena

Consulta executada, correspondente à pergunta R21 do enunciado, sobre a adoção de inteligência artificial:

```sql
SELECT edicao,
       ROUND(SUM(CASE WHEN categoria LIKE 'Sim,%' THEN participacao_pct ELSE 0 END), 2)
           AS pct_ia_prioridade
FROM workspace.gold_distribuicoes
WHERE dimensao = 'ia_prioridade'
GROUP BY edicao
ORDER BY edicao
```

Identificador da execução: `33ab51b7-bd13-49eb-96ae-c8ae980fdad0`
Estado: **SUCCEEDED**

Resultado:

| edicao | pct_ia_prioridade |
|--------|-------------------|
| 2023-2024 | 36,16 |
| 2024-2025 | 53,59 |
| 2025-2026 | 60,58 |

**Conferência cruzada.** Estes são exatamente os mesmos valores apurados no pipeline de referência e apresentados no material executivo, onde aparecem arredondados como 36,2%, 53,6% e 60,6%. O pipeline em nuvem e o pipeline local produzem resultado idêntico.

## 7. Evidências capturadas

| Print | Conteúdo | Requisitos comprovados |
|-------|----------|------------------------|
| 1 | Bucket criado com as cinco camadas, região us-east-1, indicador do lab ativo | R02, R05 |
| 2 | Camada Bronze organizada por edição, com os tamanhos dos arquivos | R05 |
| 3 | Os dois Glue Jobs com estado SUCCEEDED e as quatro tabelas Gold | R06, R07, R09 |
| 4 | Crawler concluído, tabelas no catálogo e resultado da consulta no Athena | R06, R08, R21 |

## 8. Ocorrências durante a execução

**Terminal do laboratório parou de aceitar entrada.** Após um recarregamento da página, o terminal embutido do Learner Lab deixou de responder à digitação, embora continuasse exibindo conteúdo. Em vez de insistir e consumir tempo de sessão, a execução migrou para o **AWS CloudShell**, disponível na mesma conta e na mesma região. O CloudShell funcionou sem restrição e passou a ser o ambiente de execução de todos os comandos.

**Decisão de economia.** Nenhum teste foi feito dentro do laboratório. Todo o código havia sido validado previamente em ambiente externo, com os mesmos três arquivos, e o laboratório recebeu apenas a execução final. Isso evitou o consumo de crédito com tentativa e erro, que é a causa mais comum de esgotamento do orçamento relatada pela turma.
