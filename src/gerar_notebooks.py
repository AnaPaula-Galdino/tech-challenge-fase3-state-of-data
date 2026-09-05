"""Gera os notebooks entregaveis a partir de blocos de codigo ja validados."""
import nbformat as nbf

SPARK_CFG = '''import sys, os
os.environ.pop("JAVA_TOOL_OPTIONS", None)
sys.path.insert(0, "../src")

from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder.appName("tc3")
    .master("local[2]")                      # no AWS Glue esta linha nao existe
    .config("spark.driver.memory", "3g")
    .config("spark.sql.shuffle.partitions", "4")
    .config("spark.sql.session.timeZone", "America/Sao_Paulo")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
print("Spark", spark.version)'''


def md(texto):
    return nbf.v4.new_markdown_cell(texto)


def code(texto):
    return nbf.v4.new_code_cell(texto)


CABECALHO = """# {titulo}

**Tech Challenge Fase 3** · Pós-Tech em Data Analytics, FIAP
**Base:** State of Data Brazil, edições 2023-2024, 2024-2025 e 2025-2026
**Etapa do pipeline:** {etapa}

{intro}"""

NOTEBOOKS = {
"01_ingestao_bronze.ipynb": dict(
  titulo="Ingestão e camada Bronze",
  etapa="ingestão dos arquivos de origem no data lake",
  intro="A camada Bronze recebe os arquivos exatamente como saíram do Kaggle, sem nenhuma alteração. "
        "Qualquer correção de acentuação, tipo ou formato feita antes deste ponto descaracterizaria a camada, "
        "que existe justamente para ser fiel à origem.",
  celulas=[
    md("## 1. Configuração da sessão Spark\n\nA sessão local reproduz o mesmo comportamento do AWS Glue. "
       "Ao portar o código para o Glue, apenas a linha `.master(...)` é removida e os caminhos locais passam a apontar para o S3."),
    code(SPARK_CFG),
    md("## 2. Conferência dos arquivos recebidos\n\nAntes de qualquer processamento, a estrutura de cada arquivo é verificada. "
       "Os três correspondem às três últimas edições publicadas pelo Data Hackers, exigência da página 3 do enunciado."),
    code('''from schema import ler_cabecalhos, EDICOES

cabecalhos = ler_cabecalhos("../dados/raw")
for edicao, linhas in cabecalhos.items():
    print(f"{edicao}: {len(linhas)} colunas")'''),
    md("## 3. Leitura dos dados brutos\n\nA leitura usa `multiLine` e `escape` porque várias respostas abertas contêm quebras de linha e aspas."),
    code('''bronze = {}
for edicao, arquivo in EDICOES.items():
    df = (
        spark.read.option("header", True)
        .option("multiLine", True)
        .option("escape", '"')
        .option("encoding", "UTF-8")
        .csv(f"../dados/raw/{arquivo}")
    )
    bronze[edicao] = df
    print(f"{edicao}: {df.count()} linhas, {len(df.columns)} colunas")'''),
    md("## 4. Organização no data lake\n\nNo AWS Academy Lab, os arquivos são enviados ao S3 na estrutura abaixo, "
       "particionada por edição, o que permite consultar uma edição isolada sem varrer as demais.\n\n"
       "```\ns3://<bucket>/bronze/edicao=2023-2024/\ns3://<bucket>/bronze/edicao=2024-2025/\ns3://<bucket>/bronze/edicao=2025-2026/\n```"),
    code('''# verificacao de integridade antes de seguir para a camada Silver
for edicao, df in bronze.items():
    total = df.count()
    distintas = df.dropDuplicates().count()
    print(f"{edicao}: {total} linhas, {total - distintas} duplicata(s) exata(s)")'''),
    md("**Leitura do resultado.** As edições 2024-2025 e 2025-2026 trazem, respectivamente, duas e uma linha "
       "integralmente duplicadas. São duplicações reais de registro, não colisão de identificador, "
       "portanto podem ser removidas com segurança na camada Silver."),
  ]),

"02_bronze_para_silver.ipynb": dict(
  titulo="Transformação da camada Bronze para a camada Silver",
  etapa="harmonização das três edições",
  intro="Esta é a etapa mais delicada do projeto. As três edições usam padrões de nomenclatura diferentes, "
        "e o código da pergunta muda de significado entre elas, o que torna impossível unir as bases pelo código.",
  celulas=[
    md("## 1. Configuração"),
    code(SPARK_CFG),
    md("## 2. Por que o código da pergunta não serve como chave\n\n"
       "O exemplo abaixo mostra o problema. O mesmo código `2.q` identifica perguntas diferentes conforme a edição."),
    code('''from schema import ler_cabecalhos

cabecalhos = ler_cabecalhos("../dados/raw")
for edicao, linhas in cabecalhos.items():
    for codigo, descricao, _, _ in linhas:
        if codigo == "2.q":
            print(f"{edicao}  ->  {descricao[:70]}")'''),
    md("**Leitura do resultado.** Em 2023-2024 e 2024-2025 o código `2.q` trata de demissões em massa. "
       "Em 2025-2026 trata do modelo de trabalho. Uma união pelo código colocaria as duas coisas na mesma coluna, "
       "sem gerar nenhum erro visível.\n\n"
       "Por isso o projeto adota **tripla confirmação**: código, texto da pergunta e conjunto de categorias "
       "observado nos dados. Só entra na análise a coluna aprovada nos três critérios."),
    md("## 3. Mapa de conceitos de negócio\n\nCada conceito aponta para a descrição exata da pergunta em cada edição."),
    code('''from conceitos import CONCEITOS

indice = {ed: {dn: h for c, d, dn, h in linhas} for ed, linhas in cabecalhos.items()}
faltas = [(n, ed) for n, cfg in CONCEITOS.items() for ed, alvo in cfg["desc"].items() if alvo not in indice[ed]]
print(f"conceitos mapeados: {len(CONCEITOS)}")
print(f"conceitos sem correspondencia: {len(faltas)}")'''),
    md("## 4. Regras de harmonização\n\nCada regra nasceu de uma divergência observada nos dados, nunca de suposição."),
    code('''import harmonizacao as H

print("booleanos com codificacao divergente:", H.CONCEITOS_BOOLEANOS)
print("correcoes de erro tipografico da pesquisa:")
for conceito, mapa in H.CORRECOES_TIPOGRAFICAS.items():
    for origem, destino in mapa.items():
        print(f"   {conceito}: '{origem}'  ->  '{destino}'")'''),
    md("## 5. Execução do Glue Job 01\n\nO mesmo arquivo roda aqui e no AWS Glue."),
    code('''from job01_bronze_silver import processar

silver, relatorio = processar(spark, "../dados/raw", "../dados/silver")
for r in relatorio:
    print(f"{r['edicao']}: bronze={r['linhas_bronze']}  duplicatas={r['duplicatas_removidas']}  silver={r['linhas_silver']}")
print(f"total: {silver.count()} linhas, {len(silver.columns)} colunas")'''),
    md("## 6. Verificação da camada Silver"),
    code('''from pyspark.sql import functions as F

print("booleanos harmonizados:")
silver.groupBy("atua_como_gestor").count().show()

print("erros tipograficos eliminados:")
for coluna, valor in [("faixa_salarial", "de R$ 101/mês a R$ 2.000/mês"), ("porte_empresa", "de 501 a 100")]:
    n = silver.filter(F.col(coluna) == valor).count()
    print(f"   {coluna} = '{valor[:34]}...': {n} ocorrencia(s)")'''),
    md("**Leitura do resultado.** Os booleanos passaram a usar Sim e Não nas três edições, e as duas categorias "
       "criadas por erro de digitação na pesquisa de origem foram absorvidas pelas faixas corretas. "
       "A camada Silver está pronta para agregação."),
  ]),

"03_silver_para_gold.ipynb": dict(
  titulo="Transformação da camada Silver para a camada Gold",
  etapa="construção das tabelas analíticas",
  intro="A camada Gold é organizada por pergunta de negócio. Cada tabela responde a um conjunto de perguntas "
        "do enunciado e já chega pronta para consulta no Athena e para geração de gráficos.",
  celulas=[
    md("## 1. Configuração"),
    code(SPARK_CFG),
    md("## 2. Execução do Glue Job 02"),
    code('''from job02_silver_gold import tabela_distribuicoes, tabela_cruzamentos, tabela_salario, tabela_mencoes

silver = spark.read.parquet("../dados/silver").cache()
print(f"camada Silver: {silver.count()} linhas")

distribuicoes = tabela_distribuicoes(silver)
cruzamentos = tabela_cruzamentos(silver)
salario = tabela_salario(silver)
mencoes = tabela_mencoes(silver)

for nome, df in [("distribuicoes", distribuicoes), ("cruzamentos", cruzamentos),
                 ("salario", salario), ("mencoes", mencoes)]:
    print(f"gold_{nome}: {df.count()} linhas")'''),
    md("## 3. Estrutura das tabelas\n\nTodas são tabelas longas, formato que facilita tanto a consulta SQL quanto o gráfico."),
    code('''distribuicoes.printSchema()
distribuicoes.filter("dimensao = 'genero'").orderBy("categoria", "edicao").show(12, truncate=False)'''),
    md("**Leitura do resultado.** A participação feminina cai de 24,4% para 22,0% ao longo da série. "
       "A série tem três pontos e, portanto, duas transições, e a queda ocorre nas duas, sempre na mesma direção, "
       "somando 2,5 pontos. É tendência, não oscilação de amostra."),
    md("## 4. Premissa da estatística salarial\n\nA pesquisa coleta faixa de remuneração, não valor. "
       "Toda estatística usa o ponto médio da faixa e é apresentada como faixa mediana, nunca como salário médio. "
       "A faixa aberta do topo usa o próprio limite inferior, o que é conservador."),
    code('''salario.filter("recorte = 'nivel'").orderBy("categoria", "edicao").show(truncate=False)'''),
    md("**Leitura do resultado.** A faixa mediana do nível Sênior subiu de R$ 10.000 para R$ 14.000 entre a primeira "
       "e a segunda edição, alta de 40%, e depois estabilizou. Júnior e Pleno ficaram parados nas três edições. "
       "Para uma empresa que precisa montar time, isso significa que contratar pronto ficou mais caro e formar não."),
    md("## 5. Gravação da camada Gold"),
    code('''for nome, df in [("gold_distribuicoes", distribuicoes), ("gold_cruzamentos", cruzamentos),
                 ("gold_salario", salario), ("gold_mencoes", mencoes)]:
    df.coalesce(1).write.mode("overwrite").parquet(f"../dados/gold/{nome}")
    print(f"gravada: {nome}")'''),
  ]),

"04_consultas_athena.ipynb": dict(
  titulo="Consultas analíticas",
  etapa="consulta SQL sobre a camada Gold",
  intro="As consultas abaixo são as mesmas do arquivo `sql/consultas_athena.sql`, executadas aqui em Spark SQL "
        "para comprovar que funcionam sobre os dados reais. No AWS Academy Lab elas rodam no Amazon Athena, "
        "sobre as tabelas registradas no Glue Data Catalog.",
  celulas=[
    md("## 1. Configuração e registro das tabelas"),
    code(SPARK_CFG),
    code('''for tabela in ["gold_distribuicoes", "gold_cruzamentos", "gold_salario", "gold_mencoes"]:
    spark.read.parquet(f"../dados/gold/{tabela}").createOrReplaceTempView(tabela)
    print(f"registrada: {tabela}")'''),
    md("## 2. R21. Qual é o índice de adoção de inteligência artificial?"),
    code('''spark.sql("""
    SELECT edicao,
           ROUND(SUM(CASE WHEN categoria LIKE 'Sim,%' THEN participacao_pct ELSE 0 END), 2) AS pct_ia_e_prioridade,
           ROUND(SUM(CASE WHEN categoria LIKE 'Não é uma iniciativa%' THEN participacao_pct ELSE 0 END), 2) AS pct_ia_nao_e_prioridade
    FROM gold_distribuicoes
    WHERE dimensao = 'ia_prioridade'
    GROUP BY edicao
    ORDER BY edicao
""").show()'''),
    md("**Leitura do resultado.** A IA generativa passou de prioridade declarada por 36,2% dos respondentes para 60,6% "
       "em duas edições, enquanto a rejeição caiu de 28,8% para 11,4%. É a maior mudança observada em todo o período. "
       "A pergunta é respondida apenas por quem trabalha em empresa, com bases de 896, 1.045 e 652 respostas, "
       "portanto menores que as da edição. O enunciado pede também o impacto, tratado na consulta seguinte."),
    md("### R21, segunda parte. E qual é o impacto declarado?\n\n"
       "Prioridade não é resultado. A edição 2025-2026 pergunta pelo estágio dos projetos de IA generativa, "
       "com 646 respostas válidas."),
    code('''spark.sql("""
    SELECT categoria AS estagio_declarado,
           respondentes,
           participacao_pct
    FROM gold_distribuicoes
    WHERE dimensao = 'ia_resultados' AND edicao = '2025-2026'
    ORDER BY participacao_pct DESC
""").show(truncate=False)'''),
    md("**Leitura do resultado.** Enquanto 60,6% declaram a IA como prioridade, apenas 26,5% dizem ter projetos "
       "em produção gerando resultado no negócio, e 38,4% mantêm pilotos rodando sem impacto declarado. "
       "Somados aos 15,0% ainda em planejamento, mais da metade do mercado não saiu da experimentação. "
       "A vantagem competitiva deixou de estar em adotar IA e passou a estar em operacionalizá-la."),
    md("## 3. R18. Quais perfis são mais valorizados?"),
    code('''spark.sql("""
    SELECT categoria AS nivel,
           MAX(CASE WHEN edicao = '2023-2024' THEN mediana_faixa_reais END) AS mediana_2023_2024,
           MAX(CASE WHEN edicao = '2024-2025' THEN mediana_faixa_reais END) AS mediana_2024_2025,
           MAX(CASE WHEN edicao = '2025-2026' THEN mediana_faixa_reais END) AS mediana_2025_2026
    FROM gold_salario
    WHERE recorte = 'nivel'
    GROUP BY categoria
    ORDER BY mediana_2025_2026
""").show()'''),
    md("**Leitura do resultado.** O nível Especialista/Staff+ aparece apenas em 2025-2026, com faixa mediana de "
       "R$ 18.000. É categoria nova do questionário, não comparável com as edições anteriores, e por isso é sempre "
       "apresentada em separado."),
    md("## 4. R22. Existem diferenças entre modelos de trabalho?"),
    code('''spark.sql("""
    SELECT categoria AS modelo_de_trabalho,
           MAX(CASE WHEN edicao = '2023-2024' THEN participacao_pct END) AS pct_2023_2024,
           MAX(CASE WHEN edicao = '2024-2025' THEN participacao_pct END) AS pct_2024_2025,
           MAX(CASE WHEN edicao = '2025-2026' THEN participacao_pct END) AS pct_2025_2026
    FROM gold_distribuicoes
    WHERE dimensao = 'modelo_trabalho'
    GROUP BY categoria
    ORDER BY pct_2025_2026 DESC
""").show(truncate=False)'''),
    md("**Leitura do resultado.** O trabalho totalmente remoto caiu de 46,3% para 39,7% e o totalmente presencial "
       "subiu de 16,6% para 20,8%. O movimento de retorno ao escritório é real e recente, concentrado na última edição."),
    md("## 5. R23. Satisfação por modelo de trabalho"),
    code('''spark.sql("""
    SELECT categoria_1 AS modelo_de_trabalho,
           ROUND(MAX(CASE WHEN categoria_2 = 'Sim' THEN participacao_pct END), 2) AS pct_satisfeitos,
           MAX(total_no_grupo) AS respondentes_no_modelo
    FROM gold_cruzamentos
    WHERE dimensao_1 = 'modelo_trabalho' AND dimensao_2 = 'satisfacao' AND edicao = '2025-2026'
    GROUP BY categoria_1
    ORDER BY pct_satisfeitos DESC
""").show(truncate=False)'''),
    md("**Leitura do resultado.** Remoto integral e híbrido flexível empatam no topo, com 74,5% e 75,0% de satisfeitos. "
       "A diferença de 0,5 ponto tem z igual a 0,23 e não é significativa a 95% de confiança, portanto afirmar que o remoto "
       "lidera seria ler ruído como resultado. O que separa satisfeitos de insatisfeitos é a presença de flexibilidade: "
       "são 20,9 pontos entre o híbrido flexível e o presencial integral, que fica em 54,0%. "
       "Para uma empresa que precisa reter talento escasso, a política de trabalho deixa de ser assunto "
       "administrativo e passa a ser fator de retenção."),
  ]),
}


def montar():
    import os
    os.makedirs("notebooks", exist_ok=True)
    for arquivo, cfg in NOTEBOOKS.items():
        nb = nbf.v4.new_notebook()
        nb.cells = [md(CABECALHO.format(titulo=cfg["titulo"], etapa=cfg["etapa"], intro=cfg["intro"]))] + cfg["celulas"]
        nb.metadata = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        }
        caminho = f"notebooks/{arquivo}"
        nbf.write(nb, caminho)
        print(f"gerado: {caminho}  ({len(nb.cells)} celulas)")


if __name__ == "__main__":
    montar()
