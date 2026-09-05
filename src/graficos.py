"""
Geracao dos graficos do material executivo, a partir da camada Gold.

Cada grafico responde a uma pergunta do enunciado, traz titulo afirmativo,
rotulos de eixo com unidade, rotulo de valor visivel e fonte dos dados.
"""
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estilo as E
from harmonizacao import ORDEM

E.aplicar_estilo()
G = "dados/gold_csv"
# keep_default_na=False porque existem categorias cujo texto literal e "NA" e "N/A",
# digitadas por respondentes no campo livre de ferramenta preferida. Sem esse ajuste
# o leitor as converteria em valor ausente e a categoria sumiria da contagem.
_ler = lambda arq: pd.read_csv(f"{G}/{arq}", keep_default_na=False)
DIST = _ler("gold_distribuicoes.csv")
CRUZ = _ler("gold_cruzamentos.csv")
SAL = _ler("gold_salario.csv")
MEN = _ler("gold_mencoes.csv")

# diretorio de saida: "figuras" para a versao completa, com titulo, subtitulo e fonte,
# e "figuras/deck" para a versao usada nos slides, em que esses elementos sao do slide
FIG = "figuras"

# proporcao unica para todos os graficos do material, o que mantem
# o alinhamento horizontal entre os slides
LARGURA = 9.0
ALTURA = 5.0


def barras_por_edicao(df, categorias, titulo, subtitulo, arquivo, eixo_x="Participação (%)", largura=0.26):
    """Barras horizontais agrupadas, uma barra por edicao, rampa do claro ao escuro."""
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    y = np.arange(len(categorias))
    for i, ed in enumerate(E.ORDEM_EDICOES):
        sub = df[df.edicao == ed].set_index("categoria").reindex(categorias)
        vals = sub["participacao_pct"].fillna(0).values
        pos = y + (i - 1) * largura
        ax.barh(pos, vals, height=largura * 0.92, color=E.CORES_EDICAO[ed], label=ed, zorder=3)
        for p, v in zip(pos, vals):
            if v > 0:
                ax.text(v + 0.4, p, f"{E.num_br(v)}%", va="center", fontsize=7.4, color=E.TINTA_APOIO)
    ax.set_yticks(y)
    import textwrap as _tw
    ax.set_yticklabels(["\n".join(_tw.wrap(c, 34)) for c in categorias])
    ax.invert_yaxis()
    ax.xaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, ax.get_xlim()[1] * 1.12)  # folga para o rotulo de valor
    E.ticks_percentuais(ax, "x")
    E.formatar_percentual(ax, "x")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3)
    E.moldura(ax, titulo, subtitulo, eixo_x=eixo_x)
    E.salvar(fig, f"{FIG}/{arquivo}")
    return f"{FIG}/{arquivo}"


def linha_por_edicao(series, titulo, subtitulo, arquivo, eixo_y, formato="pct"):
    """Serie historica de uma ou mais linhas ao longo das tres edicoes."""
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    # rampa ordinal: a primeira serie e a mais clara, a ultima a mais escura,
    # para que a ordem visual acompanhe a ordem da variavel
    cores = [E.AZUL_CLARO, E.AZUL_MEDIO, E.AZUL_ESCURO, E.CINZA_CONTEXTO]
    for i, (nome, vals) in enumerate(series.items()):
        ax.plot(E.ORDEM_EDICOES, vals, marker="o", markersize=7, linewidth=2.4,
                color=cores[i % len(cores)], label=nome, zorder=3)
        for x, v in zip(E.ORDEM_EDICOES, vals):
            rot = f"{E.num_br(v)}%" if formato == "pct" else f"R$ {E.num_br(v,0)}"
            ax.annotate(rot, (x, v), textcoords="offset points", xytext=(0, 9),
                        ha="center", fontsize=8, color=E.TINTA_TITULO)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(max(v) for v in series.values()) * 1.22)
    if formato == "pct":
        E.formatar_percentual(ax, "y")
    else:
        E.formatar_reais(ax, "y")
    if len(series) > 1:
        # a legenda fica fora da area de plotagem para nunca cruzar linha de grade
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=min(len(series), 3))
    E.moldura(ax, titulo, subtitulo, eixo_x="Edição da pesquisa", eixo_y=eixo_y)
    E.salvar(fig, f"{FIG}/{arquivo}")
    return f"{FIG}/{arquivo}"


def foco_contexto(df_ed, titulo, subtitulo, arquivo, destaque=None, top=10, eixo_x="Participação (%)",
                  fonte=None):
    """Ranking de uma unica edicao: barra em foco no azul escuro, demais no azul claro."""
    d = df_ed.nlargest(top, "participacao_pct").sort_values("participacao_pct")
    cores = [E.AZUL_ESCURO if (destaque and c == destaque) else E.AZUL_CLARO for c in d["categoria"]]
    if destaque is None:
        cores = [E.AZUL_ESCURO] + [E.AZUL_CLARO] * (len(d) - 1)
        cores = cores[::-1]
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    import textwrap as _tw
    rotulos = ["\n".join(_tw.wrap(c, 34)) for c in d["categoria"]]
    ax.barh(rotulos, d["participacao_pct"], color=cores, height=0.66, zorder=3)
    for i, (c, v) in enumerate(zip(d["categoria"], d["participacao_pct"])):
        ax.text(v + 0.4, i, f"{E.num_br(v)}%", va="center", fontsize=8, color=E.TINTA_APOIO)
    ax.xaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, ax.get_xlim()[1] * 1.12)
    E.ticks_percentuais(ax, "x")
    E.formatar_percentual(ax, "x")
    E.moldura(ax, titulo, subtitulo, eixo_x=eixo_x, fonte=fonte or E.FONTE_DADOS)
    E.salvar(fig, f"{FIG}/{arquivo}")
    return f"{FIG}/{arquivo}"


# graficos de uma unica edicao nao podem citar as tres como fonte
FONTE_2025 = "Fonte: State of Data Brazil, Data Hackers e Bain, edição 2025-2026."


def d(dim):
    return DIST[DIST.dimensao == dim]


if __name__ == "__main__":
    # a versao de deck sai sem titulo, subtitulo e fonte dentro da imagem,
    # porque esses elementos pertencem ao slide e duplica-los polui a leitura
    if "--deck" in sys.argv:
        E.MODO_DECK = True
        FIG = "figuras/deck"
        Path(FIG).mkdir(parents=True, exist_ok=True)

    gerados = []

    # ---------- R19: diversidade de genero ----------
    g = d("genero")
    fem = [float(g[(g.edicao == e) & (g.categoria == "Feminino")]["participacao_pct"].iloc[0]) for e in E.ORDEM_EDICOES]
    gerados.append(linha_por_edicao(
        {"Mulheres": fem},
        "A participação feminina cai edição após edição, de 24,4% para 22,0%",
        "Percentual de mulheres entre os respondentes, por edição da pesquisa. A queda ocorre nas duas transições da série, sempre na mesma direção",
        "fig01_genero_serie.png", "Participação entre respondentes (%)"))

    # genero por senioridade, edicao mais recente
    c = CRUZ[(CRUZ.dimensao_1 == "genero") & (CRUZ.dimensao_2 == "nivel") & (CRUZ.edicao == "2025-2026")]
    niveis = [n for n in ORDEM["nivel"] if n in set(c.categoria_2)]
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    x = np.arange(len(niveis))
    for i, gen in enumerate(["Masculino", "Feminino"]):
        sub = c[c.categoria_1 == gen].set_index("categoria_2").reindex(niveis)
        cor = E.AZUL_CLARO if gen == "Masculino" else E.AZUL_ESCURO
        ax.bar(x + (i - 0.5) * 0.34, sub["participacao_pct"].fillna(0), width=0.32, color=cor, label=gen, zorder=3)
        for xi, v in zip(x + (i - 0.5) * 0.34, sub["participacao_pct"].fillna(0)):
            ax.text(xi, v + 0.7, f"{E.num_br(v)}%", ha="center", fontsize=7.8, color=E.TINTA_APOIO)
    ax.set_xticks(x); ax.set_xticklabels(niveis)
    ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
    E.formatar_percentual(ax, "y"); ax.legend(loc="upper center", bbox_to_anchor=(0.5,-0.16), ncol=2)
    ax.set_ylim(0, ax.get_ylim()[1]*1.1)
    E.moldura(ax, "Mulheres se concentram nos níveis de entrada da carreira",
              "Distribuição por nível dentro de cada gênero, edição 2025-2026",
              eixo_x="Nível declarado", eixo_y="Participação dentro do gênero (%)", fonte=FONTE_2025)
    E.salvar(fig, f"{FIG}/fig02_genero_nivel.png"); gerados.append(f"{FIG}/fig02_genero_nivel.png")

    # ---------- R18: remuneracao por nivel ----------
    s = SAL[SAL.recorte == "nivel"]
    series = {}
    for nivel in ["Júnior", "Pleno", "Sênior"]:
        series[nivel] = [float(s[(s.edicao == e) & (s.categoria == nivel)]["mediana_faixa_reais"].iloc[0]) for e in E.ORDEM_EDICOES]
    gerados.append(linha_por_edicao(
        series, "A faixa mediana do Sênior subiu 40% e as de entrada não se moveram",
        "Mediana do ponto médio da faixa salarial declarada, por nível e edição. Valores nominais, sem correção pela inflação do período",
        "fig03_salario_nivel.png", "Mediana da faixa salarial (R$/mês)", formato="reais"))

    # ---------- R22: modelo de trabalho ----------
    mt = d("modelo_trabalho").copy()
    mt["categoria"] = mt["categoria"].str.replace(r" \(.*\)", "", regex=True)
    cats = ["Modelo 100% remoto", "Modelo híbrido flexível", "Modelo híbrido com dias fixos de trabalho presencial", "Modelo 100% presencial"]
    cats = [c for c in cats if c in set(mt.categoria)]
    gerados.append(barras_por_edicao(
        mt, cats, "O trabalho remoto recua e o presencial avança",
        "Distribuição do modelo de trabalho declarado, por edição",
        "fig04_modelo_trabalho.png"))

    # ---------- R21: adocao de IA ----------
    ia = d("ia_prioridade").copy()
    def rotulo_ia(t):
        if t.startswith("Sim, é nossa principal"): return "Principal prioridade da empresa"
        if t.startswith("Sim, está entre"): return "Entre as principais prioridades"
        if t.startswith("Mais ou menos"): return "Iniciativa isolada, sem foco"
        if t.startswith("Não é uma iniciativa"): return "Não é prioridade"
        return "Não sabe opinar"
    ia["categoria"] = ia["categoria"].map(rotulo_ia)
    ia = ia.groupby(["edicao", "categoria"], as_index=False)["participacao_pct"].sum()
    ordem_ia = ["Principal prioridade da empresa", "Entre as principais prioridades", "Iniciativa isolada, sem foco", "Não é prioridade", "Não sabe opinar"]
    gerados.append(barras_por_edicao(
        ia, ordem_ia, "Em duas edições, a IA generativa saiu da margem e virou prioridade",
        "Posição declarada da IA generativa na agenda da empresa do respondente, por edição. Bases: 896, 1.045 e 652 respostas válidas",
        "fig05_ia_prioridade.png"))

    # linha consolidada de prioridade
    prio = []
    for e in E.ORDEM_EDICOES:
        sub = ia[(ia.edicao == e) & (ia.categoria.isin(ordem_ia[:2]))]
        prio.append(round(float(sub["participacao_pct"].sum()), 2))
    nao = [round(float(ia[(ia.edicao == e) & (ia.categoria == "Não é prioridade")]["participacao_pct"].iloc[0]), 2) for e in E.ORDEM_EDICOES]
    gerados.append(linha_por_edicao(
        {"IA é prioridade na empresa": prio, "IA não é prioridade": nao},
        "A adoção de IA quase dobrou enquanto a rejeição caiu pela metade",
        "Percentual de respondentes por posição declarada da empresa sobre IA generativa. Bases: 896, 1.045 e 652 respostas válidas",
        "fig06_ia_serie.png", "Participação entre respondentes (%)"))

    # ---------- R20: tecnologias ----------
    men = MEN.copy()
    top_ling = ["Python", "SQL", "R", "Scala", "C/C++/C#"]
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    x = np.arange(len(top_ling))
    for i, ed in enumerate(E.ORDEM_EDICOES):
        sub = men[men.edicao == ed].set_index("categoria").reindex(top_ling)
        v = sub["mencoes_pct"].fillna(0).values
        ax.bar(x + (i - 1) * 0.27, v, width=0.25, color=E.CORES_EDICAO[ed], label=ed, zorder=3)
        for xi, vi in zip(x + (i - 1) * 0.27, v):
            if vi >= 1.0:  # abaixo de 1% o rotulo colide com o vizinho e nao informa
                ax.text(xi, vi + 1.6, f"{E.num_br(vi)}%", ha="center", fontsize=7.0, color=E.TINTA_APOIO)
    ax.set_xticks(x); ax.set_xticklabels(top_ling)
    ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
    E.formatar_percentual(ax, "y"); ax.legend(loc="upper center", bbox_to_anchor=(0.5,-0.16), ncol=3)
    ax.set_ylim(0, ax.get_ylim()[1]*1.12)
    E.moldura(ax, "Python domina e o SQL aparece ao lado dele, não no lugar",
              "Percentual de respondentes que citam a linguagem como preferida. Em 2025-2026 a pergunta passou a aceitar mais de uma resposta, por isso a soma supera 100%",
              eixo_x="Linguagem", eixo_y="Menções entre respondentes (%)")
    E.salvar(fig, f"{FIG}/fig07_linguagens.png"); gerados.append(f"{FIG}/fig07_linguagens.png")

    # ---------- R17: setor ----------
    setor = d("setor")
    setor_25 = setor[setor.edicao == "2025-2026"]
    gerados.append(foco_contexto(
        setor_25, "Finanças e tecnologia concentram mais de um terço do mercado",
        "Dez setores com maior participação entre os respondentes, edição 2025-2026. Finanças e tecnologia somam 36,0%, e a diferença entre os dois primeiros, de 1,1 ponto, não é estatisticamente significativa a 95% de confiança",
        "fig08_setor.png", destaque="Finanças ou Bancos", top=10, fonte=FONTE_2025))

    # ---------- R22: regiao ----------
    reg = d("regiao_onde_mora")
    gerados.append(barras_por_edicao(
        reg, ["Sudeste", "Sul", "Nordeste", "Centro-oeste", "Norte"],
        "A concentração no Sudeste aumentou em vez de ceder ao trabalho remoto",
        "Distribuição dos respondentes por região de moradia, por edição. O Sudeste sai de 61,4% para 64,4% entre a primeira e a última edição",
        "fig09_regiao.png"))

    # ---------- R23: satisfacao por modelo de trabalho ----------
    cs = CRUZ[(CRUZ.dimensao_1 == "modelo_trabalho") & (CRUZ.dimensao_2 == "satisfacao") & (CRUZ.edicao == "2025-2026") & (CRUZ.categoria_2 == "Sim")].copy()
    cs["categoria_1"] = cs["categoria_1"].str.replace(r" \(.*\)", "", regex=True)
    cs = cs.sort_values("participacao_pct")
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    # os dois modelos flexiveis empatam no topo, por isso ambos recebem o tom de destaque
    _flex = {"Modelo 100% remoto", "Modelo híbrido flexível"}
    cores = [E.AZUL_ESCURO if c in _flex else E.AZUL_CLARO for c in cs["categoria_1"]]
    ax.barh(cs["categoria_1"], cs["participacao_pct"], color=cores, height=0.6, zorder=3)
    for i, v in enumerate(cs["participacao_pct"]):
        ax.text(v + 0.6, i, f"{E.num_br(v)}%", va="center", fontsize=8, color=E.TINTA_APOIO)
    ax.xaxis.grid(True, zorder=0); ax.set_axisbelow(True)
    E.formatar_percentual(ax, "x")
    E.moldura(ax, "Flexibilidade, e não o remoto puro, é o que separa satisfeitos de insatisfeitos",
              "Percentual de satisfeitos dentro de cada modelo de trabalho, edição 2025-2026. Remoto integral e híbrido flexível empatam no topo, diferença de 0,5 ponto, z igual a 0,23, sem significância a 95%. Bases: 1.281, 631, 645 e 670 respostas",
              eixo_x="Satisfeitos no modelo (%)", fonte=FONTE_2025)
    E.salvar(fig, f"{FIG}/fig10_satisfacao_modelo.png"); gerados.append(f"{FIG}/fig10_satisfacao_modelo.png")

    # ---------- R21: impacto declarado da IA generativa ----------
    # o enunciado pergunta pelo indice de adocao "e seu impacto": a adocao esta em
    # fig05 e fig06, e o impacto e esta pergunta, existente apenas na ultima edicao
    ir = d("ia_resultados")
    ir = ir[ir.edicao == "2025-2026"].copy()

    def rotulo_impacto(t):
        if t.startswith("Sim."): return "Projetos em produção, gerando resultado"
        if t.startswith("Em partes"): return "Pilotos rodando, sem impacto no negócio"
        if t.startswith("Não. Os projetos"): return "Ainda em investigação e planejamento"
        if t.startswith("Não, ainda não"): return "Nenhum projeto iniciado"
        return "Não sabe opinar"

    ir["categoria"] = ir["categoria"].map(rotulo_impacto)
    gerados.append(foco_contexto(
        ir, "A IA já é prioridade, mas só um quarto declara resultado em produção",
        "Estágio declarado dos projetos de IA generativa e modelos LLM na empresa do respondente, edição 2025-2026, 646 respostas válidas",
        "fig11_ia_impacto.png", destaque="Projetos em produção, gerando resultado", top=5,
        fonte=FONTE_2025))

    # ---------- R18: remuneracao por cargo ----------
    # responde a pergunta "quais perfis profissionais sao mais valorizados" no
    # nivel do cargo, e nao apenas no nivel de senioridade
    sc = SAL[(SAL.recorte == "cargo") & (SAL.edicao == "2025-2026")].copy()
    sc = sc[sc.categoria != "Outra Opção"]
    sc = sc[sc.respondentes >= 30].sort_values("mediana_faixa_reais")
    import textwrap as _tw2
    fig, ax = plt.subplots(figsize=(LARGURA, ALTURA))
    cores = [E.AZUL_ESCURO if v >= 14000 else E.AZUL_CLARO for v in sc["mediana_faixa_reais"]]
    rot = ["\n".join(_tw2.wrap(c, 38)) for c in sc["categoria"]]
    ax.barh(rot, sc["mediana_faixa_reais"], color=cores, height=0.66, zorder=3)
    for i, (v, n) in enumerate(zip(sc["mediana_faixa_reais"], sc["respondentes"])):
        ax.text(v * 1.02, i, f"R$ {E.num_br(v, 0)}  (n={E.num_br(n, 0)})", va="center",
                fontsize=7.6, color=E.TINTA_APOIO)
    ax.xaxis.grid(True, zorder=0); ax.set_axisbelow(True)
    ax.set_xlim(0, float(sc["mediana_faixa_reais"].max()) * 1.32)
    E.formatar_reais(ax, "x")
    E.moldura(ax, "Engenharia de dados e machine learning lideram a mediana salarial",
              "Mediana do ponto médio da faixa salarial declarada, por cargo, edição 2025-2026. Cargos com menos de 30 respostas foram omitidos. Valores nominais",
              eixo_x="Mediana da faixa salarial (R$/mês)", fonte=FONTE_2025)
    E.salvar(fig, f"{FIG}/fig12_salario_cargo.png"); gerados.append(f"{FIG}/fig12_salario_cargo.png")

    # ---------- R20: ferramentas de nuvem e de BI ----------
    # completa a pergunta de tecnologias, que ate aqui cobria apenas linguagem
    nuv = d("cloud_preferida"); nuv = nuv[nuv.edicao == "2025-2026"]
    bi = d("bi_preferida"); bi = bi[bi.edicao == "2025-2026"]
    top_nuv = ["Amazon Web Services (AWS)", "Google Cloud (GCP)", "Azure (Microsoft)"]
    top_bi = ["Microsoft PowerBI", "Tableau", "Looker"]
    v_nuv = [float(nuv[nuv.categoria == c]["participacao_pct"].iloc[0]) for c in top_nuv]
    v_bi = [float(bi[bi.categoria == c]["participacao_pct"].iloc[0]) for c in top_bi]
    rot_nuv = ["AWS", "Google Cloud", "Azure"]
    rot_bi = ["Power BI", "Tableau", "Looker"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(LARGURA, ALTURA))
    for eixo, rotulos, valores, tit in [(a1, rot_nuv, v_nuv, "Nuvem preferida"),
                                        (a2, rot_bi, v_bi, "Ferramenta de BI preferida")]:
        cores = [E.AZUL_ESCURO] + [E.AZUL_CLARO] * (len(valores) - 1)
        eixo.bar(rotulos, valores, color=cores, width=0.58, zorder=3)
        for i, v in enumerate(valores):
            eixo.text(i, v + 1.2, f"{E.num_br(v)}%", ha="center", fontsize=8.4, color=E.TINTA_APOIO)
        eixo.yaxis.grid(True, zorder=0); eixo.set_axisbelow(True)
        eixo.set_ylim(0, 62)
        E.formatar_percentual(eixo, "y")
        # o nome do painel vai no rotulo do eixo, e nao em um titulo de subplot,
        # que colidiria com o subtitulo da figura
        eixo.set_xlabel(tit, labelpad=8)
        for lado in ["top", "right"]:
            eixo.spines[lado].set_visible(False)
    a1.set_ylabel("Participação entre respondentes (%)", labelpad=6)
    a2.set_ylabel("")
    fig.subplots_adjust(wspace=0.28)
    E.moldura(a2, "AWS lidera na nuvem e o Power BI não tem concorrente em BI",
              "Preferência declarada de nuvem e de ferramenta de BI, edição 2025-2026. Bases: 2.095 e 1.866 respostas válidas. Excluídas as respostas sem preferência, 32,5% em nuvem e 23,0% em BI",
              fonte=FONTE_2025)
    E.salvar(fig, f"{FIG}/fig13_ferramentas.png"); gerados.append(f"{FIG}/fig13_ferramentas.png")

    print(f"\n{len(gerados)} graficos gerados:")
    for g_ in gerados:
        print("  ", g_)
