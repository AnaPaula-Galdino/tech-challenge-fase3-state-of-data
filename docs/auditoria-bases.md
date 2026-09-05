# Auditoria de Recebimento das Bases, Fase 3

**Data:** 05/09/2026
**Objetivo:** verificar se os arquivos enviados correspondem ao que o PDF da Fase 3 exige, antes de qualquer processamento.

## 1. Conferência contra o requisito R01 do PDF

O enunciado pede, na página 3, o "Histórico das 3 últimas pesquisas disponíveis no Data Hackers". As três últimas edições publicadas no perfil oficial `datahackers` no Kaggle são 2023-2024, 2024-2025 e 2025-2026. Os três arquivos recebidos correspondem exatamente a essas edições.

| Arquivo recebido | Edição | Dataset de origem | Registros | Colunas |
|------------------|--------|-------------------|-----------|---------|
| `State_of_data_BR_2023_Kaggle - df_survey_2023.csv` | 2023-2024 | `datahackers/state-of-data-brazil-2023` | 5.293 | 399 |
| `Final Dataset - State of Data 2024 - Kaggle - df_survey_2024.csv` | 2024-2025 | `datahackers/state-of-data-brazil-20242025` | 5.217 | 403 |
| `Final Dataset - State of Data 2025-2026 - Kaggle.csv` | 2025-2026 | `datahackers/state-of-data-brazil-2025-2026` | 3.495 | 388 |

**Conclusão:** requisito R01 atendido quanto ao insumo. Nenhuma edição faltando, nenhuma edição a mais, nenhum arquivo repetido, os três somas de verificação MD5 são distintos.

## 2. Verificação de integridade

| Verificação | Resultado |
|-------------|-----------|
| Codificação | UTF-8 válido nos três arquivos, sem marca de ordem de byte |
| Acentuação nos cabeçalhos | Íntegra, exemplo: "1.e.1_Não acredito que minha experiência profissional seja afetada" |
| Delimitador | Vírgula, conforme padrão do Kaggle e conforme orientação do professor para o ETL |
| Consistência de largura | Todas as linhas com o mesmo número de campos do cabeçalho, nos três arquivos |
| Sinal de edição em Excel | Nenhum. Os arquivos preservam o formato original de origem |

**Conclusão:** as bases estão cruas e fiéis à fonte, condição necessária para a camada Bronze.

## 3. Achados que exigem tratamento documentado

| Achado | Onde | Efeito | Tratamento previsto |
|--------|------|--------|---------------------|
| Identificadores duplicados | 2 ocorrências em 2024-2025 e 1 em 2025-2026 | Contagem inflada e risco de dupla contagem em agregações | Remoção na camada Silver, com registro do volume removido |
| Padrão de cabeçalho divergente | 2023-2024 usa o formato de tupla `('P1_a ', 'Idade')`; 2024-2025 e 2025-2026 usam `1.a_idade` | Impede união direta das três edições | Mapa de equivalência de perguntas, construído coluna a coluna |
| Espaços residuais em códigos de pergunta | 2023-2024, exemplo `'P1_a '` | Falha em junções por chave textual | Normalização de nomes na Silver |
| Número de colunas diferente entre edições | 399, 403 e 388 | Perguntas entram e saem a cada edição | Série histórica restrita às perguntas com equivalência confirmada nas três |
| Queda de volume em 2025-2026 | 3.495 respondentes, contra 5.217 e 5.293 | Comparação absoluta entre anos fica enviesada | Toda comparação entre edições em base percentual, com a limitação declarada |

## 4. Achado crítico: o código da pergunta não é chave confiável entre edições

Ao validar os domínios de valores coluna a coluna, ficou provado que o código da pergunta muda de significado entre edições. O caso mais grave:

| Código | 2023-2024 | 2024-2025 | 2025-2026 |
|--------|-----------|-----------|-----------|
| `2.q` | Ocorrência de layoffs na empresa | Ocorrência de layoffs na empresa | Modelo de trabalho atual |
| `2.r` | Modelo de trabalho atual | Modelo de trabalho atual | Modelo de trabalho ideal |

Uma análise que confiasse no código teria comparado layoffs de 2023 e 2024 com trabalho remoto de 2025, no mesmo gráfico, sem nenhum erro visível de execução. O resultado pareceria correto e estaria errado.

Levantamento completo do problema, com os números já corrigidos pelo triple check:

- 330 códigos existem nas três edições, mas 145 deles carregam pergunta diferente em pelo menos uma edição.
- 237 perguntas foram casadas por descrição nas três edições, e 92 delas mudaram de código entre uma edição e outra.

**Regra adotada:** nenhuma coluna entra na análise por código. Cada coluna usada é confirmada por três critérios simultâneos, código, texto da pergunta e conjunto de categorias observadas nos dados. Só entra na série histórica a coluna aprovada nos três critérios. O mapa completo está em `mapa_equivalencia_edicoes.csv`.

Mapeamento correto já confirmado para o modelo de trabalho, com as mesmas quatro categorias nas três edições, o que torna a comparação válida:

| Edição | Coluna correta |
|--------|----------------|
| 2023-2024 | `P2_r`, "Atualmente qual a sua forma de trabalho?" |
| 2024-2025 | `2.r_modelo_de_trabalho_atual` |
| 2025-2026 | `2.q_modelo_de_trabalho_atual` |

## 5. Segundo achado: quebra de série na senioridade

A pergunta de nível profissional ganhou uma categoria nova em 2025-2026:

| Edição | Categorias |
|--------|-----------|
| 2023-2024 | Júnior, Pleno, Sênior |
| 2024-2025 | Júnior, Pleno, Sênior |
| 2025-2026 | Júnior, Pleno, Sênior, Especialista/Staff+ |

São 349 respondentes na categoria nova, o que representa parcela relevante da edição. Comparar a proporção de Sênior entre 2024 e 2025 sem tratar isso produz queda artificial. Tratamento previsto: apresentar a série com a categoria nova destacada e, para a comparação direta entre anos, informar as duas leituras, com e sem a nova categoria, sempre com a premissa declarada no gráfico.

## 6. Terceiro achado: três padrões de nomenclatura, não dois

A primeira leitura identificou dois padrões de cabeçalho. O triple check revelou um terceiro, que estava sendo lido de forma errada e silenciosa:

| Padrão | Exemplo | Onde aparece |
|--------|---------|--------------|
| Tupla | `('P1_a ', 'Idade')` | 2023-2024 |
| Numérico com sublinhado | `1.a.1_faixa_idade` | 2024-2025 e 2025-2026 |
| Numérico com espaço | `3.f.1 Colaboradores usando AI generativa` | 2024-2025 e 2025-2026 |

O terceiro padrão concentra justamente os blocos de inteligência artificial generativa, que respondem à pergunta do enunciado sobre adoção de IA. A leitura inicial cortava o código em `3.f` e agrupava oito colunas distintas sob o mesmo identificador. Havia ainda um cabeçalho malformado em 2023-2024, `('P6_b_16 ', 'SQL Server Integration Services (SSIS))`, sem a aspa de fechamento, que era descartado sem aviso.

O leitor de cabeçalhos foi reescrito para cobrir os três padrões e o caso malformado. Prova de correção: o número de códigos únicos extraídos passou a ser exatamente igual ao número de colunas de cada arquivo, 399, 403 e 388, e nenhuma coluna ficou sem reconhecimento nas três edições.

## 7. Status

Bases aprovadas para ingestão na camada Bronze, sem qualquer alteração prévia. Os cinco achados acima entram no dicionário de dados e no mapa de equivalência, com justificativa de cada decisão de tratamento.
