"""
Job 01: camada Bronze para camada Silver.

Le os CSV crus das tres edicoes do State of Data Brazil, harmoniza esquema e
categorias, e grava a camada Silver em Parquet, particionada por edicao.

O mesmo codigo roda localmente e no AWS Glue. A unica diferenca sao os caminhos,
recebidos por parametro.

Uso local:
    python3 job01_bronze_silver.py --bronze ./dados/raw --silver ./dados/silver
"""
import argparse
import sys
from pathlib import Path
from pyspark.sql import SparkSession, functions as F, types as T

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import ler_cabecalhos, EDICOES
from conceitos import CONCEITOS
import harmonizacao as H


def criar_sessao(nome="tc3_bronze_silver"):
    return (
        SparkSession.builder.appName(nome)
        .master("local[2]")
        .config("spark.driver.memory", "3g")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "America/Sao_Paulo")
        .getOrCreate()
    )


def mapa_de_para(spark_col, mapa):
    """Aplica um dicionario de/para usando um mapa literal do Spark.

    Nao usar encadeamento de when: com dezenas de entradas a arvore de expressao
    cresce a ponto de estourar a memoria do driver. O mapa literal resolve em uma
    unica consulta e mantem o plano de execucao estavel.
    """
    itens = [F.lit(x) for par in mapa.items() for x in par]
    return F.coalesce(F.create_map(itens)[spark_col], spark_col)


def processar(spark, bronze_dir, silver_dir):
    cabecalhos = ler_cabecalhos(bronze_dir)
    indice = {ed: {dn: h for c, d, dn, h in linhas} for ed, linhas in cabecalhos.items()}
    relatorio = []
    partes = []

    for edicao, arquivo in EDICOES.items():
        bruto = (
            spark.read.option("header", True)
            .option("multiLine", True)
            .option("escape", '"')
            .option("encoding", "UTF-8")
            .csv(f"{bronze_dir}/{arquivo}")
        )
        linhas_bronze = bruto.count()

        # 1. remocao de duplicatas exatas, verificadas como linhas integralmente identicas
        sem_dup = bruto.dropDuplicates()
        removidas = linhas_bronze - sem_dup.count()

        # 2. selecao das colunas de interesse, resolvidas pela descricao da pergunta
        selecao = []
        for conceito, cfg in CONCEITOS.items():
            if edicao not in cfg["desc"]:
                continue
            coluna_origem = indice[edicao][cfg["desc"][edicao]]
            selecao.append(F.col(f"`{coluna_origem}`").alias(conceito))
        df = sem_dup.select(*selecao)

        # 3. limpeza textual: espacos das pontas e vazio convertido em nulo
        for c in df.columns:
            df = df.withColumn(c, F.trim(F.col(c)))
            df = df.withColumn(c, F.when(F.col(c) == "", None).otherwise(F.col(c)))

        # 4. booleanos com codificacao divergente entre edicoes
        for c in H.CONCEITOS_BOOLEANOS:
            if c in df.columns:
                df = df.withColumn(c, mapa_de_para(F.col(c), H.MAPA_BOOLEANO))

        # 5. correcao de erros de digitacao da pesquisa de origem
        for c, mapa in H.CORRECOES_TIPOGRAFICAS.items():
            if c in df.columns:
                df = df.withColumn(c, mapa_de_para(F.col(c), mapa))

        # 6. padronizacao de categorias que mudaram de redacao
        for c, mapa in H.PADRONIZACAO_CATEGORIAS.items():
            if c in df.columns:
                df = df.withColumn(c, mapa_de_para(F.col(c), mapa))

        # 7. agrupamento para serie historica, em coluna separada da original
        for c, mapa in H.AGRUPAMENTOS_SERIE.items():
            if c in df.columns:
                df = df.withColumn(f"{c}_serie", mapa_de_para(F.col(c), mapa))

        # 8. tipagem numerica de idade
        if "idade" in df.columns:
            df = df.withColumn("idade", F.col("idade").cast(T.IntegerType()))

        # 9. ponto medio da faixa salarial, para calculo de mediana
        if "faixa_salarial" in df.columns:
            itens = [F.lit(x) for par in H.PONTO_MEDIO_SALARIO.items() for x in par]
            df = df.withColumn("salario_ponto_medio",
                               F.create_map(itens)[F.col("faixa_salarial")].cast(T.IntegerType()))

        df = df.withColumn("edicao", F.lit(edicao))
        partes.append(df)
        relatorio.append(
            {"edicao": edicao, "linhas_bronze": linhas_bronze,
             "duplicatas_removidas": removidas, "linhas_silver": sem_dup.count(),
             "colunas_silver": len(df.columns)}
        )

    # uniao das tres edicoes pelo nome da coluna, tolerando ausencias
    silver = partes[0]
    for p in partes[1:]:
        silver = silver.unionByName(p, allowMissingColumns=True)

    silver.write.mode("overwrite").partitionBy("edicao").parquet(silver_dir)
    return silver, relatorio


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bronze", required=True)
    ap.add_argument("--silver", required=True)
    args = ap.parse_args()

    spark = criar_sessao()
    spark.sparkContext.setLogLevel("ERROR")
    silver, rel = processar(spark, args.bronze, args.silver)

    print("\n=== camada Silver gravada ===")
    for r in rel:
        print(f"  {r['edicao']}: bronze={r['linhas_bronze']} duplicatas={r['duplicatas_removidas']} "
              f"silver={r['linhas_silver']} colunas={r['colunas_silver']}")
    print(f"  total Silver: {silver.count()} linhas, {len(silver.columns)} colunas")
    spark.stop()
