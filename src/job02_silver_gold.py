"""
Job 02: camada Silver para camada Gold.

Gera as tabelas analiticas que respondem as sete perguntas do enunciado.
Todas as tabelas sao longas, com uma linha por combinacao de edicao, dimensao e
categoria, formato que facilita a consulta no Athena e a geracao de graficos.

Uso local:
    python3 job02_silver_gold.py --silver ./dados/silver --gold ./dados/gold
"""
import argparse
import sys
from pathlib import Path
from pyspark.sql import SparkSession, functions as F, Window

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harmonizacao as H

# conceito -> pergunta do enunciado que ele responde
DISTRIBUICOES = {
    "situacao_trabalho": "R17", "setor": "R17", "porte_empresa": "R17",
    "tamanho_time_dados": "R17", "nivel_ensino": "R17", "area_formacao": "R17",
    "faixa_idade": "R17",
    "cargo": "R18", "nivel": "R18", "faixa_salarial": "R18",
    "tempo_exp_dados_serie": "R18",
    "genero": "R19", "atua_como_gestor": "R19",
    "linguagem_preferida": "R20", "cloud_preferida": "R20", "bi_preferida": "R20",
    "ia_prioridade": "R21", "ia_uso_pessoal": "R21", "ia_resultados": "R21",
    "regiao_onde_mora": "R22", "uf_onde_mora": "R22", "modelo_trabalho": "R22",
    "modelo_trabalho_ideal": "R23", "satisfacao": "R23", "planos_mudar": "R23",
}

# cruzamentos: (dimensao_1, dimensao_2, pergunta)
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


def mapa_de_para(spark_col, mapa):
    """Aplica um dicionario de/para usando um mapa literal do Spark.

    Nao usar encadeamento de when: com dezenas de entradas a arvore de expressao
    cresce a ponto de estourar a memoria do driver. O mapa literal resolve em uma
    unica consulta e mantem o plano de execucao estavel.
    """
    itens = [F.lit(x) for par in mapa.items() for x in par]
    return F.coalesce(F.create_map(itens)[spark_col], spark_col)


def criar_sessao(nome="tc3_silver_gold"):
    return (
        SparkSession.builder.appName(nome)
        .master("local[2]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "America/Sao_Paulo")
        .getOrCreate()
    )


def tabela_distribuicoes(silver):
    """Uma linha por edicao, dimensao e categoria, com contagem e participacao percentual.

    O percentual usa como denominador o total de respostas validas da dimensao
    naquela edicao, nunca o total de respondentes, porque cada pergunta tem
    quantidade propria de nao respostas.
    """
    partes = []
    for coluna, pergunta in DISTRIBUICOES.items():
        if coluna not in silver.columns:
            continue
        base = silver.filter(F.col(coluna).isNotNull())
        cont = base.groupBy("edicao", coluna).agg(F.count("*").alias("respondentes"))
        janela = Window.partitionBy("edicao")
        cont = (
            cont.withColumn("total_validos", F.sum("respondentes").over(janela))
            .withColumn("participacao_pct", F.round(F.col("respondentes") / F.col("total_validos") * 100, 2))
            .withColumn("dimensao", F.lit(coluna))
            .withColumn("pergunta_enunciado", F.lit(pergunta))
            .withColumnRenamed(coluna, "categoria")
            .select("edicao", "pergunta_enunciado", "dimensao", "categoria",
                    "respondentes", "total_validos", "participacao_pct")
        )
        partes.append(cont)
    out = partes[0]
    for p in partes[1:]:
        out = out.unionByName(p)
    return out


def tabela_cruzamentos(silver):
    """Cruzamento de duas dimensoes, com percentual calculado dentro de cada categoria da primeira."""
    partes = []
    for d1, d2, pergunta in CRUZAMENTOS:
        if d1 not in silver.columns or d2 not in silver.columns:
            continue
        base = silver.filter(F.col(d1).isNotNull() & F.col(d2).isNotNull())
        cont = base.groupBy("edicao", d1, d2).agg(F.count("*").alias("respondentes"))
        janela = Window.partitionBy("edicao", d1)
        cont = (
            cont.withColumn("total_no_grupo", F.sum("respondentes").over(janela))
            .withColumn("participacao_pct", F.round(F.col("respondentes") / F.col("total_no_grupo") * 100, 2))
            .withColumn("dimensao_1", F.lit(d1)).withColumn("dimensao_2", F.lit(d2))
            .withColumn("pergunta_enunciado", F.lit(pergunta))
            .withColumnRenamed(d1, "categoria_1").withColumnRenamed(d2, "categoria_2")
            .select("edicao", "pergunta_enunciado", "dimensao_1", "categoria_1",
                    "dimensao_2", "categoria_2", "respondentes", "total_no_grupo", "participacao_pct")
        )
        partes.append(cont)
    out = partes[0]
    for p in partes[1:]:
        out = out.unionByName(p)
    return out


def tabela_salario(silver):
    """Mediana da faixa salarial por recorte.

    A pesquisa coleta faixa, nao valor. A mediana e calculada sobre o ponto medio
    de cada faixa, o que a torna uma estimativa da faixa central, nunca um salario medio.
    """
    partes = []
    for recorte in ["nivel", "genero", "regiao_onde_mora", "cargo", "modelo_trabalho", "setor"]:
        if recorte not in silver.columns:
            continue
        base = silver.filter(F.col("salario_ponto_medio").isNotNull() & F.col(recorte).isNotNull())
        agg = (
            base.groupBy("edicao", recorte)
            .agg(
                F.count("*").alias("respondentes"),
                F.expr("percentile_approx(salario_ponto_medio, 0.5)").alias("mediana_faixa_reais"),
                F.expr("percentile_approx(salario_ponto_medio, 0.25)").alias("q1_faixa_reais"),
                F.expr("percentile_approx(salario_ponto_medio, 0.75)").alias("q3_faixa_reais"),
            )
            .withColumn("recorte", F.lit(recorte))
            .withColumnRenamed(recorte, "categoria")
            .filter(F.col("respondentes") >= 30)  # corte de amostra minima
        )
        partes.append(agg.select("edicao", "recorte", "categoria", "respondentes",
                                 "mediana_faixa_reais", "q1_faixa_reais", "q3_faixa_reais"))
    out = partes[0]
    for p in partes[1:]:
        out = out.unionByName(p)
    return out


def tabela_mencoes(silver):
    """Percentual de respondentes que citam cada item, para conceitos de escolha multipla.

    Necessario porque a edicao 2025-2026 passou a aceitar mais de uma linguagem
    preferida por respondente, enquanto as anteriores aceitavam apenas uma.
    O denominador e o total de respondentes que responderam a pergunta na edicao,
    portanto a soma dos percentuais pode passar de cem na edicao de escolha multipla.
    """
    partes = []
    for coluna in H.CONCEITOS_MULTIPLA_ESCOLHA:
        if coluna not in silver.columns:
            continue
        base = silver.filter(F.col(coluna).isNotNull())
        denom = base.groupBy("edicao").agg(F.count("*").alias("respondentes_pergunta"))
        itens = base.withColumn("item", F.explode(F.split(F.col(coluna), ",")))
        itens = itens.withColumn("item", F.trim(F.col("item")))
        itens = itens.withColumn("item", mapa_de_para(F.col("item"), H.SINONIMOS_LINGUAGEM))
        itens = itens.filter(F.col("item").isin(H.LINGUAGENS_PRINCIPAIS))
        # um respondente conta uma vez por item, mesmo que repita o item
        cont = itens.dropDuplicates(["edicao", coluna, "item"]) if False else itens
        cont = cont.groupBy("edicao", "item").agg(F.count("*").alias("mencoes"))
        cont = (
            cont.join(denom, "edicao")
            .withColumn("mencoes_pct", F.round(F.col("mencoes") / F.col("respondentes_pergunta") * 100, 2))
            .withColumn("dimensao", F.lit(coluna))
            .withColumn("pergunta_enunciado", F.lit("R20"))
            .select("edicao", "pergunta_enunciado", "dimensao", F.col("item").alias("categoria"),
                    "mencoes", "respondentes_pergunta", "mencoes_pct")
        )
        partes.append(cont)
    out = partes[0]
    for p in partes[1:]:
        out = out.unionByName(p)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--silver", required=True)
    ap.add_argument("--gold", required=True)
    args = ap.parse_args()

    spark = criar_sessao()
    spark.sparkContext.setLogLevel("ERROR")
    silver = spark.read.parquet(args.silver).cache()
    silver.count()  # materializa o cache uma unica vez

    dist = tabela_distribuicoes(silver)
    cruz = tabela_cruzamentos(silver)
    sal = tabela_salario(silver)
    men = tabela_mencoes(silver)

    dist.coalesce(1).write.mode("overwrite").parquet(f"{args.gold}/gold_distribuicoes")
    cruz.coalesce(1).write.mode("overwrite").parquet(f"{args.gold}/gold_cruzamentos")
    sal.coalesce(1).write.mode("overwrite").parquet(f"{args.gold}/gold_salario")
    men.coalesce(1).write.mode("overwrite").parquet(f"{args.gold}/gold_mencoes")

    print("\n=== camada Gold gravada ===")
    print(f"  gold_distribuicoes: {dist.count()} linhas, {dist.select('dimensao').distinct().count()} dimensoes")
    print(f"  gold_cruzamentos:   {cruz.count()} linhas, {cruz.select('dimensao_1','dimensao_2').distinct().count()} pares")
    print(f"  gold_salario:       {sal.count()} linhas, {sal.select('recorte').distinct().count()} recortes")
    print(f"  gold_mencoes:       {men.count()} linhas")
    spark.stop()
