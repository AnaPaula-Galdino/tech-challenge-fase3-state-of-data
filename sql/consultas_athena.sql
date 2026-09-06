-- ============================================================================
-- Tech Challenge Fase 3, consultas analiticas no Amazon Athena
--
-- Base: State of Data Brazil, edicoes 2023-2024, 2024-2025 e 2025-2026.
-- Todas as consultas leem a camada Gold, registrada no Glue Data Catalog.
--
-- Convencao: cada consulta responde a uma pergunta do enunciado, identificada
-- por um codigo Rxx e pelo texto da pergunta no comentario que a antecede.
--
-- Antes da primeira execucao, definir em Athena > Configuracoes o local de
-- armazenamento dos resultados, e criar o banco de dados com:
--     CREATE DATABASE IF NOT EXISTS workspace;
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 0. Registro das tabelas da camada Gold no catalogo
--    Executar uma unica vez, apos a gravacao das tabelas pelo Glue Job 02.
--    Substituir <bucket> pelo nome do bucket criado no laboratorio.
-- ----------------------------------------------------------------------------
CREATE EXTERNAL TABLE IF NOT EXISTS workspace.gold_distribuicoes (
    edicao              string,
    pergunta_enunciado  string,
    dimensao            string,
    categoria           string,
    respondentes        bigint,
    total_validos       bigint,
    participacao_pct    double
)
STORED AS PARQUET
LOCATION 's3://<bucket>/gold/gold_distribuicoes/';

CREATE EXTERNAL TABLE IF NOT EXISTS workspace.gold_cruzamentos (
    edicao              string,
    pergunta_enunciado  string,
    dimensao_1          string,
    categoria_1         string,
    dimensao_2          string,
    categoria_2         string,
    respondentes        bigint,
    total_no_grupo      bigint,
    participacao_pct    double
)
STORED AS PARQUET
LOCATION 's3://<bucket>/gold/gold_cruzamentos/';

CREATE EXTERNAL TABLE IF NOT EXISTS workspace.gold_salario (
    edicao               string,
    recorte              string,
    categoria            string,
    respondentes         bigint,
    mediana_faixa_reais  int,
    q1_faixa_reais       int,
    q3_faixa_reais       int
)
STORED AS PARQUET
LOCATION 's3://<bucket>/gold/gold_salario/';

CREATE EXTERNAL TABLE IF NOT EXISTS workspace.gold_mencoes (
    edicao                 string,
    pergunta_enunciado     string,
    dimensao               string,
    categoria              string,
    mencoes                bigint,
    respondentes_pergunta  bigint,
    mencoes_pct            double
)
STORED AS PARQUET
LOCATION 's3://<bucket>/gold/gold_mencoes/';


-- ----------------------------------------------------------------------------
-- R17. Como esta estruturado o mercado brasileiro de dados?
--      Setores que mais empregam, na edicao mais recente.
-- ----------------------------------------------------------------------------
SELECT categoria AS setor,
       respondentes,
       participacao_pct
FROM workspace.gold_distribuicoes
WHERE dimensao = 'setor'
  AND edicao = '2025-2026'
ORDER BY participacao_pct DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- R18. Quais perfis profissionais sao mais valorizados pelo mercado?
--      Faixa salarial mediana por nivel, com a evolucao entre as edicoes.
-- ----------------------------------------------------------------------------
SELECT categoria AS nivel,
       MAX(CASE WHEN edicao = '2023-2024' THEN mediana_faixa_reais END) AS mediana_2023_2024,
       MAX(CASE WHEN edicao = '2024-2025' THEN mediana_faixa_reais END) AS mediana_2024_2025,
       MAX(CASE WHEN edicao = '2025-2026' THEN mediana_faixa_reais END) AS mediana_2025_2026
FROM workspace.gold_salario
WHERE recorte = 'nivel'
GROUP BY categoria
ORDER BY mediana_2025_2026;


-- R18, complemento. Faixa salarial mediana por cargo na edicao mais recente.
--      Responde a pergunta no nivel do cargo, e nao apenas da senioridade.
--      Cargos com menos de 30 respostas sao omitidos, por instabilidade da mediana.
SELECT categoria AS cargo,
       respondentes,
       mediana_faixa_reais,
       q1_faixa_reais,
       q3_faixa_reais
FROM workspace.gold_salario
WHERE recorte = 'cargo'
  AND edicao = '2025-2026'
  AND respondentes >= 30
ORDER BY mediana_faixa_reais DESC, respondentes DESC;


-- ----------------------------------------------------------------------------
-- R19. Qual e o cenario de diversidade de genero nas carreiras de dados?
--      Participacao feminina por edicao e variacao acumulada.
-- ----------------------------------------------------------------------------
WITH feminino AS (
    SELECT edicao, participacao_pct
    FROM workspace.gold_distribuicoes
    WHERE dimensao = 'genero' AND categoria = 'Feminino'
)
SELECT edicao,
       participacao_pct,
       ROUND(participacao_pct - FIRST_VALUE(participacao_pct) OVER (ORDER BY edicao), 2)
           AS variacao_em_pontos_desde_a_primeira_edicao
FROM feminino
ORDER BY edicao;


-- ----------------------------------------------------------------------------
-- R20. Quais tecnologias apresentam maior adocao entre os profissionais?
--      Mencoes por linguagem preferida. Atencao: em 2025-2026 a pergunta passou
--      a aceitar mais de uma resposta, por isso a metrica e a mencao e a soma
--      dos percentuais pode ultrapassar cem naquela edicao.
-- ----------------------------------------------------------------------------
SELECT categoria AS linguagem,
       MAX(CASE WHEN edicao = '2023-2024' THEN mencoes_pct END) AS pct_2023_2024,
       MAX(CASE WHEN edicao = '2024-2025' THEN mencoes_pct END) AS pct_2024_2025,
       MAX(CASE WHEN edicao = '2025-2026' THEN mencoes_pct END) AS pct_2025_2026
FROM workspace.gold_mencoes
WHERE dimensao = 'linguagem_preferida'
GROUP BY categoria
ORDER BY pct_2025_2026 DESC;


-- R20, complemento. Preferencia declarada de nuvem e de ferramenta de BI na
--      edicao mais recente. As respostas sem preferencia sao mantidas na base do
--      percentual e apenas excluidas da leitura no material executivo.
SELECT dimensao AS categoria_de_ferramenta,
       categoria AS ferramenta,
       respondentes,
       total_validos,
       participacao_pct
FROM workspace.gold_distribuicoes
WHERE dimensao IN ('cloud_preferida', 'bi_preferida')
  AND edicao = '2025-2026'
  AND participacao_pct >= 1
ORDER BY dimensao, participacao_pct DESC;


-- ----------------------------------------------------------------------------
-- R21. Qual e o indice de adocao de inteligencia artificial e seu impacto?
--      Consolidacao das respostas em duas posicoes: prioridade e nao prioridade.
-- ----------------------------------------------------------------------------
SELECT edicao,
       ROUND(SUM(CASE WHEN categoria LIKE 'Sim,%' THEN participacao_pct ELSE 0 END), 2)
           AS pct_ia_e_prioridade,
       ROUND(SUM(CASE WHEN categoria LIKE 'Não é uma iniciativa%' THEN participacao_pct ELSE 0 END), 2)
           AS pct_ia_nao_e_prioridade
FROM workspace.gold_distribuicoes
WHERE dimensao = 'ia_prioridade'
GROUP BY edicao
ORDER BY edicao;


-- R21, segunda parte. O enunciado pede o indice de adocao E SEU IMPACTO.
--      A pergunta de estagio dos projetos existe apenas na edicao 2025-2026,
--      com 646 respostas validas, e por isso nao entra em serie historica.
SELECT categoria AS estagio_declarado,
       respondentes,
       total_validos,
       participacao_pct
FROM workspace.gold_distribuicoes
WHERE dimensao = 'ia_resultados'
  AND edicao = '2025-2026'
ORDER BY participacao_pct DESC;


-- ----------------------------------------------------------------------------
-- R22. Existem diferencas relevantes entre regioes, senioridades ou modelos
--      de trabalho? Modelo de trabalho por edicao.
-- ----------------------------------------------------------------------------
SELECT categoria AS modelo_de_trabalho,
       MAX(CASE WHEN edicao = '2023-2024' THEN participacao_pct END) AS pct_2023_2024,
       MAX(CASE WHEN edicao = '2024-2025' THEN participacao_pct END) AS pct_2024_2025,
       MAX(CASE WHEN edicao = '2025-2026' THEN participacao_pct END) AS pct_2025_2026
FROM workspace.gold_distribuicoes
WHERE dimensao = 'modelo_trabalho'
GROUP BY categoria
ORDER BY pct_2025_2026 DESC;


-- R22, complemento. Faixa salarial mediana por regiao, na edicao mais recente.
SELECT categoria AS regiao,
       respondentes,
       mediana_faixa_reais,
       q1_faixa_reais,
       q3_faixa_reais
FROM workspace.gold_salario
WHERE recorte = 'regiao_onde_mora'
  AND edicao = '2025-2026'
ORDER BY mediana_faixa_reais DESC;


-- ----------------------------------------------------------------------------
-- R23. Quais oportunidades e desafios para empresas que desejam investir em
--      dados e IA? Satisfacao declarada dentro de cada modelo de trabalho.
-- ----------------------------------------------------------------------------
SELECT categoria_1 AS modelo_de_trabalho,
       ROUND(MAX(CASE WHEN categoria_2 = 'Sim' THEN participacao_pct END), 2) AS pct_satisfeitos,
       MAX(total_no_grupo) AS respondentes_no_modelo
FROM workspace.gold_cruzamentos
WHERE dimensao_1 = 'modelo_trabalho'
  AND dimensao_2 = 'satisfacao'
  AND edicao = '2025-2026'
GROUP BY categoria_1
ORDER BY pct_satisfeitos DESC;


-- R23, complemento. Intencao de mudar de emprego nos proximos seis meses,
-- indicador direto de risco de retencao para o cliente do caso.
SELECT edicao,
       categoria AS intencao,
       participacao_pct
FROM workspace.gold_distribuicoes
WHERE dimensao = 'planos_mudar'
ORDER BY edicao, participacao_pct DESC;
