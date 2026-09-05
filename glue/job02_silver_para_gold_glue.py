"""
AWS Glue Job 02: camada Silver para camada Gold.
Tech Challenge Fase 3, State of Data Brazil.

Script autocontido, pronto para colar no editor de script do AWS Glue.

Parametros do job, definidos em Job details > Job parameters:
    --BUCKET   nome do bucket criado no laboratorio, sem o prefixo s3://

Le:     s3://<BUCKET>/silver/
Grava:  s3://<BUCKET>/gold/gold_distribuicoes/
        s3://<BUCKET>/gold/gold_cruzamentos/
        s3://<BUCKET>/gold/gold_salario/
        s3://<BUCKET>/gold/gold_mencoes/
"""
import sys

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F, Window
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME", "BUCKET"])
BUCKET = args["BUCKET"]
CAMINHO_SILVER = f"s3://{BUCKET}/silver"
CAMINHO_GOLD = f"s3://{BUCKET}/gold"

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# ---------------------------------------------------------------------------
# Conceito -> pergunta do enunciado que ele responde
# ---------------------------------------------------------------------------
DISTRIBUICOES = {
    "situacao_trabalho": "R17", "setor": "R17", "porte_empresa": "R17",
    "tamanho_time_dados": "R17", "nivel_ensino": "R17", "area_formacao": "R17",
    "faixa_idade": "R17",
    "cargo": "R18", "nivel": "R18", "faixa_salarial": "R18", "tempo_exp_dados_serie": "R18",
    "genero": "R19", "atua_como_gestor": "R19",
    "linguagem_preferida": "R20", "cloud_preferida": "R20", "bi_preferida": "R20",
    "ia_prioridade": "R21", "ia_uso_pessoal": "R21", "ia_resultados": "R21",
    "regiao_onde_mora": "R22", "uf_onde_mora": "R22", "modelo_trabalho": "R22",
    "modelo_trabalho_ideal": "R23", "satisfacao": "R23", "planos_mudar": "R23",
}

CRUZAMENTOS = [
    ("genero", "nivel", "R19"),
    ("genero", "faixa_salarial", "R19"),
    ("genero", "atua_como_gestor", "R19"),
    ("nivel", "faixa_salarial", "R18"),
    ("regiao_onde_mora", "faixa_salarial", "R22"),
    ("regiao_onde_mora", "modelo_trabalho", "R22"),
    ("nivel", "modelo_trabalho", "R22"),
    ("modelo_trabalho", "satisfacao", "R23"),
    ("setor", "ia_prioridade", "R21"),
    ("porte_empresa", "ia_prioridade", "R21"),
]

RECORTES_SALARIO = ["nivel", "genero", "regiao_onde_mora", "cargo", "modelo_trabalho", "setor"]

CONCEITOS_MULTIPLA_ESCOLHA = ["linguagem_preferida"]

SINONIMOS_LINGUAGEM = {
    "sql": "SQL", "Sql": "SQL", "python": "Python", "Pyhton": "Python",
    "pyspark": "PySpark", "Pyspark": "PySpark", "GO": "Go", "Golang": "Go", "golang": "Go",
    "javascript": "JavaScript", "Javascript": "JavaScript",
    "dax": "DAX/M", "Dax": "DAX/M", "DAX": "DAX/M", "M": "DAX/M",
    "M/DAX": "DAX/M", "M e Dax": "DAX/M", "Linguagem M": "DAX/M",
    "sas": "SAS", "kotli": "Kotlin", "Kotli": "Kotlin",
}

LINGUAGENS_PRINCIPAIS = ["Python", "SQL", "R", "Scala", "C/C++/C#", "Java", "JavaScript", "Go", "Rust", "DAX/M"]


def mapa_de_para(coluna, mapa):
    itens = [F.lit(x) for par in mapa.items() for x in par]
    return F.coalesce(F.create_map(itens)[coluna], coluna)


silver = spark.read.parquet(CAMINHO_SILVER).cache()
print(f"camada Silver: {silver.count()} linhas")

# ---------------------------------------------------------------------------
# Tabela 1, distribuicoes
# O denominador e o total de respostas validas da dimensao naquela edicao,
# nunca o total de respondentes, porque cada pergunta tem seu proprio volume
# de nao respostas.
# ---------------------------------------------------------------------------
partes = []
for coluna, pergunta in DISTRIBUICOES.items():
    if coluna not in silver.columns:
        continue
    base = silver.filter(F.col(coluna).isNotNull())
    cont = base.groupBy("edicao", coluna).agg(F.count("*").alias("respondentes"))
    janela = Window.partitionBy("edicao")
    partes.append(
        cont.withColumn("total_validos", F.sum("respondentes").over(janela))
        .withColumn("participacao_pct", F.round(F.col("respondentes") / F.col("total_validos") * 100, 2))
        .withColumn("dimensao", F.lit(coluna))
        .withColumn("pergunta_enunciado", F.lit(pergunta))
        .withColumnRenamed(coluna, "categoria")
        .select("edicao", "pergunta_enunciado", "dimensao", "categoria",
                "respondentes", "total_validos", "participacao_pct")
    )
distribuicoes = partes[0]
for p in partes[1:]:
    distribuicoes = distribuicoes.unionByName(p)

# ---------------------------------------------------------------------------
# Tabela 2, cruzamentos
# ---------------------------------------------------------------------------
partes = []
for d1, d2, pergunta in CRUZAMENTOS:
    if d1 not in silver.columns or d2 not in silver.columns:
        continue
    base = silver.filter(F.col(d1).isNotNull() & F.col(d2).isNotNull())
    cont = base.groupBy("edicao", d1, d2).agg(F.count("*").alias("respondentes"))
    janela = Window.partitionBy("edicao", d1)
    partes.append(
        cont.withColumn("total_no_grupo", F.sum("respondentes").over(janela))
        .withColumn("participacao_pct", F.round(F.col("respondentes") / F.col("total_no_grupo") * 100, 2))
        .withColumn("dimensao_1", F.lit(d1)).withColumn("dimensao_2", F.lit(d2))
        .withColumn("pergunta_enunciado", F.lit(pergunta))
        .withColumnRenamed(d1, "categoria_1").withColumnRenamed(d2, "categoria_2")
        .select("edicao", "pergunta_enunciado", "dimensao_1", "categoria_1",
                "dimensao_2", "categoria_2", "respondentes", "total_no_grupo", "participacao_pct")
    )
cruzamentos = partes[0]
for p in partes[1:]:
    cruzamentos = cruzamentos.unionByName(p)

# ---------------------------------------------------------------------------
# Tabela 3, estatistica salarial
# A pesquisa coleta faixa, nao valor. A mediana e calculada sobre o ponto medio
# de cada faixa, o que a torna estimativa da faixa central, nunca salario medio.
# ---------------------------------------------------------------------------
partes = []
for recorte in RECORTES_SALARIO:
    if recorte not in silver.columns:
        continue
    base = silver.filter(F.col("salario_ponto_medio").isNotNull() & F.col(recorte).isNotNull())
    partes.append(
        base.groupBy("edicao", recorte)
        .agg(
            F.count("*").alias("respondentes"),
            F.expr("percentile_approx(salario_ponto_medio, 0.5)").alias("mediana_faixa_reais"),
            F.expr("percentile_approx(salario_ponto_medio, 0.25)").alias("q1_faixa_reais"),
            F.expr("percentile_approx(salario_ponto_medio, 0.75)").alias("q3_faixa_reais"),
        )
        .withColumn("recorte", F.lit(recorte))
        .withColumnRenamed(recorte, "categoria")
        .filter(F.col("respondentes") >= 30)
        .select("edicao", "recorte", "categoria", "respondentes",
                "mediana_faixa_reais", "q1_faixa_reais", "q3_faixa_reais")
    )
salario = partes[0]
for p in partes[1:]:
    salario = salario.unionByName(p)

# ---------------------------------------------------------------------------
# Tabela 4, mencoes
# Necessaria porque a edicao 2025-2026 passou a aceitar mais de uma linguagem
# preferida por respondente, enquanto as anteriores aceitavam apenas uma.
# ---------------------------------------------------------------------------
partes = []
for coluna in CONCEITOS_MULTIPLA_ESCOLHA:
    if coluna not in silver.columns:
        continue
    base = silver.filter(F.col(coluna).isNotNull())
    denom = base.groupBy("edicao").agg(F.count("*").alias("respondentes_pergunta"))
    itens = base.withColumn("item", F.explode(F.split(F.col(coluna), ",")))
    itens = itens.withColumn("item", F.trim(F.col("item")))
    itens = itens.withColumn("item", mapa_de_para(F.col("item"), SINONIMOS_LINGUAGEM))
    itens = itens.filter(F.col("item").isin(LINGUAGENS_PRINCIPAIS))
    cont = itens.groupBy("edicao", "item").agg(F.count("*").alias("mencoes"))
    partes.append(
        cont.join(denom, "edicao")
        .withColumn("mencoes_pct", F.round(F.col("mencoes") / F.col("respondentes_pergunta") * 100, 2))
        .withColumn("dimensao", F.lit(coluna))
        .withColumn("pergunta_enunciado", F.lit("R20"))
        .select("edicao", "pergunta_enunciado", "dimensao", F.col("item").alias("categoria"),
                "mencoes", "respondentes_pergunta", "mencoes_pct")
    )
mencoes = partes[0]
for p in partes[1:]:
    mencoes = mencoes.unionByName(p)

# ---------------------------------------------------------------------------
# Gravacao
# ---------------------------------------------------------------------------
for nome, df in [("gold_distribuicoes", distribuicoes), ("gold_cruzamentos", cruzamentos),
                 ("gold_salario", salario), ("gold_mencoes", mencoes)]:
    df.coalesce(1).write.mode("overwrite").parquet(f"{CAMINHO_GOLD}/{nome}")
    print(f"gravada {nome}: {df.count()} linhas")

job.commit()
