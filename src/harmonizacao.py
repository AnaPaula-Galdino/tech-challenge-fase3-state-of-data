"""
Regras de harmonizacao entre as tres edicoes do State of Data Brazil.

Cada regra foi criada a partir de divergencia observada nos dados, nao por suposicao.
A origem de cada uma esta comentada, para auditoria.
"""

# --------------------------------------------------------------------------
# 1. Booleanos com codificacao diferente entre edicoes
#    2023-2024 e 2025-2026 usam "0" e "1"; 2024-2025 usa "FALSE" e "TRUE".
# --------------------------------------------------------------------------
CONCEITOS_BOOLEANOS = ["atua_como_gestor", "satisfacao"]

MAPA_BOOLEANO = {
    "0": "Nao", "1": "Sim",
    "false": "Nao", "true": "Sim",
    "FALSE": "Nao", "TRUE": "Sim",
}

# --------------------------------------------------------------------------
# 2. Erros de digitacao presentes na propria pesquisa de origem.
#    Em todos os casos a categoria correta tambem existe na mesma edicao,
#    portanto a fusao apenas reagrupa respostas da mesma faixa.
# --------------------------------------------------------------------------
CORRECOES_TIPOGRAFICAS = {
    "faixa_salarial": {
        # 2023-2024: faixa duplicada por erro de digitacao do limite inferior
        "de R$ 101/mês a R$ 2.000/mês": "de R$ 1.001/mês a R$ 2.000/mês",
        # 2025-2026: erro de digitacao do limite superior
        "de R$ 25.001/mês a R$ 3000/mês": "de R$ 25.001/mês a R$ 30.000/mês",
    },
    "porte_empresa": {
        # 2023-2024 e 2025-2026: erro de digitacao do limite superior
        "de 501 a 100": "de 501 a 1.000",
    },
}

# --------------------------------------------------------------------------
# 3. Categorias que mudaram de redacao mantendo o mesmo significado.
# --------------------------------------------------------------------------
PADRONIZACAO_CATEGORIAS = {
    "area_formacao": {
        "Outras Engenharias": "Outras Engenharias (não incluir engenharia de software ou TI)",
        # 2023-2024 tinha as duas separadas; as edicoes seguintes as fundiram
        "Marketing / Publicidade / Comunicação / Jornalismo": "Marketing / Publicidade / Comunicação / Jornalismo / Ciências Sociais",
        "Ciências Sociais": "Marketing / Publicidade / Comunicação / Jornalismo / Ciências Sociais",
    },
    "cargo": {
        # 2023-2024 tratava engenharia e arquitetura de dados como um cargo so.
        # As edicoes seguintes separaram. Para a serie historica, o agrupamento
        # volta ao denominador comum das tres edicoes.
        "Engenheiro de Dados/Arquiteto de Dados/Data Engineer/Data Architect": "Engenharia e Arquitetura de Dados",
        "Engenheiro de Dados/Data Engineer/Data Architect": "Engenharia e Arquitetura de Dados",
        "Arquiteto de Dados/Data Architect": "Engenharia e Arquitetura de Dados",
    },
}

# --------------------------------------------------------------------------
# 4. Agrupamentos usados apenas na serie historica, quando uma edicao usou
#    faixas que nao coincidem com as demais.
# --------------------------------------------------------------------------
AGRUPAMENTOS_SERIE = {
    "tempo_exp_dados": {
        # 2023-2024 ofereceu "de 4 a 6 anos", faixa que atravessa duas faixas
        # das outras edicoes. Alocar em uma delas seria arbitrario, entao a
        # serie historica usa faixas mais largas, onde as tres edicoes coincidem.
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

# --------------------------------------------------------------------------
# 5. Categorias que existem em apenas uma edicao. Nao sao erro, sao mudanca
#    real do questionario, e precisam de tratamento explicito no grafico.
# --------------------------------------------------------------------------
CATEGORIAS_NOVAS = {
    "nivel": {"Especialista/Staff+": "2025-2026"},
    "area_formacao": {"Ciência de Dados / Inteligência Artificial": "2025-2026"},
}

# --------------------------------------------------------------------------
# 6. Ordem canonica das categorias ordinais, para eixos e tabelas.
# --------------------------------------------------------------------------
ORDEM = {
    "faixa_salarial": [
        "Menos de R$ 1.000/mês", "de R$ 1.001/mês a R$ 2.000/mês", "de R$ 2.001/mês a R$ 3.000/mês",
        "de R$ 3.001/mês a R$ 4.000/mês", "de R$ 4.001/mês a R$ 6.000/mês", "de R$ 6.001/mês a R$ 8.000/mês",
        "de R$ 8.001/mês a R$ 12.000/mês", "de R$ 12.001/mês a R$ 16.000/mês", "de R$ 16.001/mês a R$ 20.000/mês",
        "de R$ 20.001/mês a R$ 25.000/mês", "de R$ 25.001/mês a R$ 30.000/mês", "de R$ 30.001/mês a R$ 40.000/mês",
        "Acima de R$ 40.001/mês",
    ],
    "nivel": ["Júnior", "Pleno", "Sênior", "Especialista/Staff+"],
    "porte_empresa": ["de 1 a 5", "de 6 a 10", "de 11 a 50", "de 51 a 100", "de 101 a 500",
                      "de 501 a 1.000", "de 1.001 a 3.000", "Acima de 3.000"],
    "tempo_exp_dados_serie": ["Sem experiência", "Até 2 anos", "De 3 a 6 anos", "De 7 a 10 anos", "Mais de 10 anos"],
}

# --------------------------------------------------------------------------
# 7. Ponto medio das faixas salariais, em reais por mes.
#    Usado apenas para calcular mediana de faixa, nunca apresentado como
#    "salario medio". A faixa aberta do topo usa o proprio limite inferior.
# --------------------------------------------------------------------------
PONTO_MEDIO_SALARIO = {
    "Menos de R$ 1.000/mês": 500, "de R$ 1.001/mês a R$ 2.000/mês": 1500,
    "de R$ 2.001/mês a R$ 3.000/mês": 2500, "de R$ 3.001/mês a R$ 4.000/mês": 3500,
    "de R$ 4.001/mês a R$ 6.000/mês": 5000, "de R$ 6.001/mês a R$ 8.000/mês": 7000,
    "de R$ 8.001/mês a R$ 12.000/mês": 10000, "de R$ 12.001/mês a R$ 16.000/mês": 14000,
    "de R$ 16.001/mês a R$ 20.000/mês": 18000, "de R$ 20.001/mês a R$ 25.000/mês": 22500,
    "de R$ 25.001/mês a R$ 30.000/mês": 27500, "de R$ 30.001/mês a R$ 40.000/mês": 35000,
    "Acima de R$ 40.001/mês": 40001,
}


# --------------------------------------------------------------------------
# 8. Conceitos que mudaram de escolha unica para escolha multipla.
#    Em 2023-2024 e 2024-2025 a linguagem preferida admitia uma resposta.
#    Em 2025-2026 passou a admitir varias, separadas por virgula.
#    A metrica comparavel entre as tres edicoes e a mencao: percentual de
#    respondentes que citam a linguagem como preferida. Isso e declarado no grafico.
# --------------------------------------------------------------------------
CONCEITOS_MULTIPLA_ESCOLHA = ["linguagem_preferida"]

# Sinonimos e variacoes de grafia observados no texto livre da pesquisa.
SINONIMOS_LINGUAGEM = {
    "sql": "SQL", "Sql": "SQL", "SQL ": "SQL",
    "python": "Python", "Pyhton": "Python",
    "pyspark": "PySpark", "Pyspark": "PySpark",
    "GO": "Go", "Golang": "Go", "golang": "Go",
    "javascript": "JavaScript", "Javascript": "JavaScript",
    "dax": "DAX/M", "Dax": "DAX/M", "DAX": "DAX/M", "M": "DAX/M",
    "M/DAX": "DAX/M", "M e Dax": "DAX/M", "DAX/M": "DAX/M", "Linguagem M": "DAX/M",
    "sas": "SAS", "kotli": "Kotlin", "Kotli": "Kotlin",
}

# Linguagens com volume suficiente para leitura comparavel entre edicoes.
LINGUAGENS_PRINCIPAIS = ["Python", "SQL", "R", "Scala", "C/C++/C#", "Java", "JavaScript", "Go", "Rust", "DAX/M"]
