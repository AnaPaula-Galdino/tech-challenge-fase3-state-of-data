# Roteiro de execução no AWS Academy Lab

**Objetivo:** reproduzir o pipeline completo no laboratório, gerando as evidências exigidas pela Matriz de Rastreabilidade.

**Princípio de economia de créditos:** nada é testado dentro do laboratório. Todo o processamento já foi validado fora dele, com os mesmos dados e o mesmo código. O laboratório recebe apenas a execução final conferida.

**Regra de ouro:** confirme a região **us-east-1, Norte da Virgínia**, no seletor no alto à direita do console, antes de qualquer operação. Erros de permissão que parecem falta de acesso quase sempre são região errada.

**Sobre o tempo:** as credenciais do Learner Lab expiram em cerca de uma hora. O roteiro está dividido em blocos curtos, cada um com ponto de retomada.

**Scripts prontos para colar:** os dois jobs estão em `entregaveis/glue/`, em versão autocontida, sem dependência de arquivos externos. Ambos foram executados fora do laboratório, com os mesmos dados, e produziram exatamente os mesmos números do pipeline de referência: 14.002 linhas na Silver e as quatro tabelas Gold com 1.008, 982, 135 e 29 linhas. Nada será descoberto dentro do laboratório.

**Antes de começar, tenha em mãos:** os três arquivos CSV originais, extraídos dos arquivos baixados do Kaggle. Eles precisam estar na sua máquina para o upload no S3.

---

## Mapa das evidências

São sete capturas de tela. Cada uma comprova um requisito da Matriz de Rastreabilidade. Eu aviso na hora de cada uma.

| Print | O que capturar | Requisito que comprova |
|-------|----------------|------------------------|
| 1 | Bucket criado, com os quatro prefixos, e a região visível no topo | R02, R05 |
| 2 | Um dos prefixos de edição com o CSV dentro e o tamanho do arquivo | R05 |
| 3 | Athena com o local de resultados configurado e o banco `workspace` criado | R08 |
| 4 | Glue Job 01 com status Succeeded, e o prefixo `silver/` populado | R06, R07, R09 |
| 5 | Glue Job 02 com status Succeeded, e as quatro tabelas em `gold/` | R06, R07, R09 |
| 6 | Glue Data Catalog listando as tabelas registradas | R06 |
| 7 | Resultado de pelo menos três consultas no Athena, incluindo a de adoção de IA | R08, R21 |

Guarde os arquivos em `evidencias/` com nomes sequenciais, por exemplo `print1-bucket.png`, para que a matriz possa referenciar cada um.

---

## Bloco 1. Preparação do bucket, cerca de 10 minutos

1. Inicie o laboratório e aguarde o indicador ficar verde.
2. Abra o console da AWS e confirme a região us-east-1.
3. Vá em S3 e crie um bucket com nome único, por exemplo `tc3-state-of-data-<seu-identificador>`.
4. Dentro do bucket, crie os prefixos `bronze/`, `silver/`, `gold/` e `athena-results/`.

**Evidência a capturar:** print do bucket com os quatro prefixos visíveis e a região no canto superior.

## Bloco 2. Ingestão na camada Bronze, cerca de 10 minutos

1. Entre no prefixo `bronze/` e crie três subpastas, uma por edição: `edicao=2023-2024`, `edicao=2024-2025` e `edicao=2025-2026`.
2. Faça o upload de cada CSV original na subpasta correspondente.

**Atenção:** suba os arquivos exatamente como foram baixados do Kaggle. Não abra e salve no Excel antes. Isso alteraria codificação e separador, e descaracterizaria a camada Bronze, que precisa ser fiel à origem.

**Evidência a capturar:** print de uma das subpastas mostrando o arquivo e o tamanho.

## Bloco 3. Configuração do Athena, cerca de 5 minutos

1. Abra o Amazon Athena.
2. Em Configurações, defina o local de armazenamento dos resultados como `s3://<seu-bucket>/athena-results/`. Sem esse passo, o banco de dados padrão não aparece e as consultas falham.
3. No editor, execute:

```sql
CREATE DATABASE IF NOT EXISTS workspace;
```

**Evidência a capturar:** print da configuração salva e do banco `workspace` na lista.

## Bloco 4. Glue Job 01, Bronze para Silver, cerca de 15 minutos

1. Abra o AWS Glue e vá em ETL jobs, criando um job do tipo Script editor com Spark.
2. Cole o conteúdo de `entregaveis/glue/job01_bronze_para_silver_glue.py`, sem alterar nada. O script já está no formato do Glue e lê o nome do bucket por parâmetro.
3. Em Job details:
   - IAM Role: `LabRole`, a role padrão do laboratório;
   - Requested number of workers: o mínimo disponível, porque o volume é pequeno e isso economiza crédito;
   - Job parameters: adicione a chave `--BUCKET` com o nome do seu bucket, sem o prefixo `s3://`.
4. Salve e execute.

**Ponto de atenção:** se o job falhar por permissão, confira a região antes de qualquer outra hipótese.

**Evidência a capturar:** print do job com status Succeeded e print do prefixo `silver/` populado.

## Bloco 5. Glue Job 02, Silver para Gold, cerca de 10 minutos

1. Repita o processo do bloco anterior com `entregaveis/glue/job02_silver_para_gold_glue.py`.
2. Mesma role, mesmo número mínimo de workers e o mesmo parâmetro `--BUCKET`.

**Evidência a capturar:** print do job com status Succeeded e print das quatro tabelas em `gold/`.

## Bloco 6. Catalogação, cerca de 10 minutos

Há dois caminhos, ambos válidos.

**Caminho A, por crawler.** Em Glue, crie um crawler apontando para `s3://<seu-bucket>/gold/`, com destino no banco `workspace`, e execute.

**Caminho B, por SQL no Athena.** Execute a seção 0 do arquivo `sql/consultas_athena.sql`, substituindo `<bucket>` pelo nome do seu bucket. São quatro instruções `CREATE EXTERNAL TABLE`.

Se preferir montar o ETL pela interface visual do Glue, lembre-se de preencher **database e nome da tabela** no nó Target. Sem isso, a tabela não é registrada no catálogo e não aparece no Athena.

**Evidência a capturar:** print do Glue Data Catalog com as quatro tabelas listadas.

## Bloco 7. Consultas analíticas, cerca de 10 minutos

Execute, no Athena, as consultas do arquivo `sql/consultas_athena.sql`, na ordem. Cada uma responde a uma pergunta do enunciado e está identificada pelo código da Matriz de Rastreabilidade.

**Evidência a capturar:** print do resultado de pelo menos três consultas, incluindo a de adoção de inteligência artificial, que sustenta o principal achado do trabalho.

## Bloco 8. Encerramento

1. Baixe os resultados que quiser guardar. O acesso ao laboratório termina algumas semanas após o fim da fase.
2. Encerre o laboratório para não consumir crédito à toa.

---

## Se algo der errado

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Erro de permissão ao criar bucket ou role | região errada | trocar para us-east-1, Norte da Virgínia |
| Banco de dados padrão não aparece no Glue ou no Athena | local de resultados do Athena não configurado | configurar o local e executar `CREATE DATABASE workspace` |
| Tabela não aparece no Athena após o ETL | nome da tabela não preenchido no nó Target | refazer o nó Target informando database e nome da tabela |
| Tabela aparece só com cabeçalho | formato ou delimitador errados na origem | conferir formato CSV e delimitador vírgula, e testar a opção Recursive na URL do S3 |
| Aviso de limite de saída excedido no Athena | efeito das mais de 300 colunas do dataset | é aviso, não falha, pode prosseguir |
| Script local perde conexão com a AWS | credenciais temporárias expiradas | copiar novamente as três chaves em AWS Details e atualizar as credenciais |
| Conta desativada | teto de créditos atingido | solicitar reativação à coordenação, informando o e-mail cadastrado |
