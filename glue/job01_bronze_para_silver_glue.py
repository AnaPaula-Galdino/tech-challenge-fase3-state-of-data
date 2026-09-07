"""
AWS Glue Job 01: camada Bronze para camada Silver.
Tech Challenge Fase 3, State of Data Brazil.

Script autocontido, pronto para colar no editor de script do AWS Glue.
Nao depende de modulos externos nem de bibliotecas alem do PySpark.

Parametros do job, definidos em Job details > Job parameters:
    --BUCKET   nome do bucket criado no laboratorio, sem o prefixo s3://

Le:     s3://<BUCKET>/bronze/
Grava:  s3://<BUCKET>/silver/   em Parquet, particionado por edicao
"""
import re
import sys
import unicodedata

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F, types as T
from awsglue.context import GlueContext
from awsglue.job import Job

# ---------------------------------------------------------------------------
# 1. Parametros e sessao
# ---------------------------------------------------------------------------
args = getResolvedOptions(sys.argv, ["JOB_NAME", "BUCKET"])
BUCKET = args["BUCKET"]
CAMINHO_BRONZE = f"s3://{BUCKET}/bronze"
CAMINHO_SILVER = f"s3://{BUCKET}/silver"

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# ---------------------------------------------------------------------------
# 2. Arquivos de origem, um por edicao
# ---------------------------------------------------------------------------
EDICOES = {
    "2023-2024": "edicao=2023-2024",
    "2024-2025": "edicao=2024-2025",
    "2025-2026": "edicao=2025-2026",
}

# ---------------------------------------------------------------------------
# 3. Leitura dos cabecalhos
#    As tres edicoes usam tres padroes diferentes de nomenclatura:
#      tupla            ('P1_a ', 'Idade')                     2023-2024
#      numerico com _   1.a.1_faixa_idade                       2024-2025 e 2025-2026
#      numerico com ' ' 3.f.1 Colaboradores usando AI generativa
#    Ha ainda um cabecalho malformado em 2023-2024, sem aspa de fechamento.
# ---------------------------------------------------------------------------
RE_TUPLA = re.compile(r"^\('\s*([^']+?)\s*'\s*,\s*'?(.*?)'?\)?$")
RE_NUM = re.compile(r"^(\d+(?:\.[A-Za-z0-9]+)*)[_ ](.*)$")


def parse_header(h):
    """Devolve (codigo, descricao, padrao) para um cabecalho de coluna."""
    if h.startswith("('"):
        m = RE_TUPLA.match(h)
        if not m:
            return None, h, "nao_reconhecido"
        cod = re.sub(r"^P", "", m.group(1).strip()).replace("_", ".").lower()
        return cod, m.group(2).strip(), "tupla"
    m = RE_NUM.match(h)
    if m:
        return m.group(1).lower(), m.group(2).strip(), "numerico"
    return None, h, "nao_reconhecido"


def normalizar(texto):
    """Minusculas, sem acento e sem pontuacao, para comparar descricoes."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


# ---------------------------------------------------------------------------
# 4. Mapa de conceitos de negocio
#    O codigo da pergunta NAO serve como chave entre edicoes: 145 codigos mudam
#    de significado. Cada conceito aponta para a descricao exata da pergunta.
# ---------------------------------------------------------------------------
CONCEITOS = {
    "idade": {"2023-2024": "idade", "2024-2025": "idade", "2025-2026": "idade"},
    "faixa_idade": {"2023-2024": "faixa_idade", "2024-2025": "faixa_idade", "2025-2026": "faixa_idade"},
    "genero": {"2023-2024": "genero", "2024-2025": "genero", "2025-2026": "genero"},
    "regiao_onde_mora": {"2023-2024": "regiao_onde_mora", "2024-2025": "regiao_onde_mora", "2025-2026": "regiao_onde_mora"},
    "uf_onde_mora": {"2023-2024": "uf_onde_mora", "2024-2025": "uf_onde_mora", "2025-2026": "uf_onde_mora"},
    "nivel_ensino": {"2023-2024": "nivel_de_ensino", "2024-2025": "nivel_de_ensino", "2025-2026": "nivel_de_ensino"},
    "area_formacao": {"2023-2024": "area_de_formacao", "2024-2025": "area_de_formacao", "2025-2026": "area_de_formacao"},
    "situacao_trabalho": {"2023-2024": "qual_sua_situacao_atual_de_trabalho", "2024-2025": "situacao_de_trabalho", "2025-2026": "situacao_de_trabalho"},
    "setor": {"2023-2024": "setor", "2024-2025": "setor", "2025-2026": "setor"},
    "porte_empresa": {"2023-2024": "numero_de_funcionarios", "2024-2025": "numero_de_funcionarios", "2025-2026": "numero_de_funcionarios"},
    "tamanho_time_dados": {"2023-2024": "qual_o_numero_aproximado_de_pessoas_que_atuam_com_dados_na_sua_empresa_hoje", "2024-2025": "numero_de_pessoas_em_dados", "2025-2026": "numero_de_pessoas_em_dados"},
    "cargo": {"2023-2024": "cargo_atual", "2024-2025": "cargo_atual", "2025-2026": "cargo_atual"},
    "nivel": {"2023-2024": "nivel", "2024-2025": "nivel", "2025-2026": "nivel"},
    "faixa_salarial": {"2023-2024": "faixa_salarial", "2024-2025": "faixa_salarial", "2025-2026": "faixa_salarial"},
    "tempo_exp_dados": {"2023-2024": "quanto_tempo_de_experiencia_na_area_de_dados_voce_tem", "2024-2025": "tempo_de_experiencia_em_dados", "2025-2026": "tempo_de_experiencia_em_dados"},
    "atua_como_gestor": {"2023-2024": "gestor", "2024-2025": "atua_como_gestor", "2025-2026": "atua_como_gestor"},
    "modelo_trabalho": {"2023-2024": "atualmente_qual_a_sua_forma_de_trabalho", "2024-2025": "modelo_de_trabalho_atual", "2025-2026": "modelo_de_trabalho_atual"},
    "modelo_trabalho_ideal": {"2023-2024": "qual_a_forma_de_trabalho_ideal_para_voce", "2024-2025": "modelo_de_trabalho_ideal", "2025-2026": "modelo_de_trabalho_ideal"},
    "satisfacao": {"2023-2024": "voce_esta_satisfeito_na_sua_empresa_atual", "2024-2025": "satisfeito_atualmente", "2025-2026": "satisfeito_atualmente"},
    "planos_mudar": {"2023-2024": "voce_pretende_mudar_de_emprego_nos_proximos_6_meses", "2024-2025": "planos_de_mudar_de_emprego_6m", "2025-2026": "planos_de_mudar_de_emprego_6m"},
    "linguagem_preferida": {"2023-2024": "entre_as_linguagens_listadas_abaixo_qual_e_a_sua_preferida", "2024-2025": "linguagem_preferida", "2025-2026": "linguagem_preferida"},
    "cloud_preferida": {"2023-2024": "cloud_preferida", "2024-2025": "cloud_preferida", "2025-2026": "cloud_preferida"},
    "bi_preferida": {"2023-2024": "qual_sua_ferramenta_de_bi_preferida", "2024-2025": "ferramenta_de_bi_preferida", "2025-2026": "ferramenta_de_bi_preferida"},
    "ia_prioridade": {"2023-2024": "ai_generativa_e_uma_prioridade_em_sua_empresa", "2024-2025": "ai_generativa_e_llm_e_uma_prioridade", "2025-2026": "ai_generativa_e_llm_e_uma_prioridade"},
    "ia_resultados": {"2025-2026": "empresa_esta_conseguindo_ter_bons_resultados_com_llms"},
    "ia_barreiras": {"2023-2024": "motivos_que_levam_a_empresa_a_nao_usar_ai_genrativa_e_llms", "2024-2025": "motivos_para_nao_usar_ai_generativa_e_llm", "2025-2026": "motivos_para_nao_usar_ai_generativa_e_llm"},
    "ia_tipo_uso": {"2023-2024": "tipos_de_uso_de_ai_generativa_e_llms_na_empresa", "2024-2025": "tipo_de_uso_de_ai_generativa_e_llm_na_empresa", "2025-2026": "tipo_de_uso_de_ai_generativa_e_llm_na_empresa"},
    "ia_uso_pessoal": {"2023-2024": "utiliza_chatgpt_ou_llms_no_trabalho", "2024-2025": "usa_chatgpt_ou_copilot_no_trabalho", "2025-2026": "usa_chatgpt_ou_copilot_no_trabalho"},
}

# ---------------------------------------------------------------------------
# 5. Regras de harmonizacao, cada uma originada de divergencia observada
# ---------------------------------------------------------------------------
CONCEITOS_BOOLEANOS = ["atua_como_gestor", "satisfacao"]
MAPA_BOOLEANO = {"0": "Nao", "1": "Sim", "false": "Nao", "true": "Sim", "FALSE": "Nao", "TRUE": "Sim"}

CORRECOES_TIPOGRAFICAS = {
    "faixa_salarial": {
        "de R$ 101/mês a R$ 2.000/mês": "de R$ 1.001/mês a R$ 2.000/mês",
        "de R$ 25.001/mês a R$ 3000/mês": "de R$ 25.001/mês a R$ 30.000/mês",
    },
    "porte_empresa": {"de 501 a 100": "de 501 a 1.000"},
}

PADRONIZACAO_CATEGORIAS = {
    "area_formacao": {
        "Outras Engenharias": "Outras Engenharias (não incluir engenharia de software ou TI)",
        "Marketing / Publicidade / Comunicação / Jornalismo": "Marketing / Publicidade / Comunicação / Jornalismo / Ciências Sociais",
        "Ciências Sociais": "Marketing / Publicidade / Comunicação / Jornalismo / Ciências Sociais",
    },
    "cargo": {
        "Engenheiro de Dados/Arquiteto de Dados/Data Engineer/Data Architect": "Engenharia e Arquitetura de Dados",
        "Engenheiro de Dados/Data Engineer/Data Architect": "Engenharia e Arquitetura de Dados",
        "Arquiteto de Dados/Data Architect": "Engenharia e Arquitetura de Dados",
    },
}

AGRUPAMENTOS_SERIE = {
    "tempo_exp_dados": {
        "Não tenho experiência na área de dados": "Sem experiência",
        "Menos de 1 ano": "Até 2 anos",
        "de 1 a 2 anos": "Até 2 anos",
        "de 3 a 4 anos": "De 3 a 6 anos",
        "de 4 a 6 anos": "De 3 a 6 anos",
        "de 5 a 6 anos": "De 3 a 6 anos",
        "de 7 a 10 anos": "De 7 a 10 anos",
        "Mais de 10 anos": "Mais de 10 anos",
    },
}

PONTO_MEDIO_SALARIO = {
    "Menos de R$ 1.000/mês": 500, "de R$ 1.001/mês a R$ 2.000/mês": 1500,
    "de R$ 2.001/mês a R$ 3.000/mês": 2500, "de R$ 3.001/mês a R$ 4.000/mês": 3500,
    "de R$ 4.001/mês a R$ 6.000/mês": 5000, "de R$ 6.001/mês a R$ 8.000/mês": 7000,
    "de R$ 8.001/mês a R$ 12.000/mês": 10000, "de R$ 12.001/mês a R$ 16.000/mês": 14000,
    "de R$ 16.001/mês a R$ 20.000/mês": 18000, "de R$ 20.001/mês a R$ 25.000/mês": 22500,
    "de R$ 25.001/mês a R$ 30.000/mês": 27500, "de R$ 30.001/mês a R$ 40.000/mês": 35000,
    "Acima de R$ 40.001/mês": 40001,
}


def mapa_de_para(coluna, mapa):
    """Aplica um de/para com mapa literal do Spark.

    Encadear when com dezenas de entradas faz a arvore de expressao crescer a
    ponto de estourar a memoria do driver. O mapa literal resolve em uma consulta.
    """
    itens = [F.lit(x) for par in mapa.items() for x in par]
    return F.coalesce(F.create_map(itens)[coluna], coluna)


# ---------------------------------------------------------------------------
# 6. Processamento, uma edicao por vez
# ---------------------------------------------------------------------------
partes = []
relatorio = []

for edicao, prefixo in EDICOES.items():
    bruto = (
        spark.read.option("header", True)
        .option("multiLine", True)
        .option("escape", '"')
        .option("encoding", "UTF-8")
        .csv(f"{CAMINHO_BRONZE}/{prefixo}/")
    )
    linhas_bronze = bruto.count()

    # indice descricao normalizada -> nome real da coluna
    indice = {}
    for h in bruto.columns:
        _cod, descricao, padrao = parse_header(h)
        if padrao == "nao_reconhecido":
            raise ValueError(f"cabecalho nao reconhecido em {edicao}: {h!r}")
        indice.setdefault(normalizar(descricao), h)

    # remocao de duplicatas exatas
    sem_dup = bruto.dropDuplicates()
    linhas_silver = sem_dup.count()

    # selecao das colunas de interesse
    selecao = []
    for conceito, por_edicao in CONCEITOS.items():
        if edicao not in por_edicao:
            continue
        alvo = por_edicao[edicao]
        if alvo not in indice:
            raise ValueError(f"conceito {conceito} nao encontrado em {edicao}, procurado por {alvo!r}")
        selecao.append(F.col("`" + indice[alvo] + "`").alias(conceito))
    df = sem_dup.select(*selecao)

    # limpeza textual
    for c in df.columns:
        df = df.withColumn(c, F.trim(F.col(c)))
        df = df.withColumn(c, F.when(F.col(c) == "", None).otherwise(F.col(c)))

    # booleanos, erros tipograficos e padronizacao de categorias
    for c in CONCEITOS_BOOLEANOS:
        if c in df.columns:
            df = df.withColumn(c, mapa_de_para(F.col(c), MAPA_BOOLEANO))
    for c, mapa in CORRECOES_TIPOGRAFICAS.items():
        if c in df.columns:
            df = df.withColumn(c, mapa_de_para(F.col(c), mapa))
    for c, mapa in PADRONIZACAO_CATEGORIAS.items():
        if c in df.columns:
            df = df.withColumn(c, mapa_de_para(F.col(c), mapa))
    for c, mapa in AGRUPAMENTOS_SERIE.items():
        if c in df.columns:
            df = df.withColumn(f"{c}_serie", mapa_de_para(F.col(c), mapa))

    if "idade" in df.columns:
        df = df.withColumn("idade", F.col("idade").cast(T.IntegerType()))

    if "faixa_salarial" in df.columns:
        itens = [F.lit(x) for par in PONTO_MEDIO_SALARIO.items() for x in par]
        df = df.withColumn(
            "salario_ponto_medio",
            F.create_map(itens)[F.col("faixa_salarial")].cast(T.IntegerType()),
        )

    df = df.withColumn("edicao", F.lit(edicao))
    partes.append(df)
    relatorio.append((edicao, linhas_bronze, linhas_bronze - linhas_silver, linhas_silver))
    print(f"[{edicao}] bronze={linhas_bronze} duplicatas={linhas_bronze - linhas_silver} silver={linhas_silver}")

silver = partes[0]
for p in partes[1:]:
    silver = silver.unionByName(p, allowMissingColumns=True)

total = silver.count()
print(f"camada Silver: {total} linhas, {len(silver.columns)} colunas")

silver.write.mode("overwrite").partitionBy("edicao").parquet(CAMINHO_SILVER)
print(f"gravado em {CAMINHO_SILVER}")

job.commit()
