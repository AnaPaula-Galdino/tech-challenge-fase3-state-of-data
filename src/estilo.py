"""
Sistema visual dos graficos do Tech Challenge Fase 3.

Herda a estrutura do material da Fase 2 e usa rampa monocromatica azul,
escolhida pela Ana. A rampa e sequencial, nao categorica: os tres passos
codificam a edicao da pesquisa, que e uma variavel ordinal.

Validacoes executadas sobre a rampa, com resultado registrado no relatorio:
  luminosidade estritamente decrescente ......... aprovado
  separacao entre passos adjacentes ............. aprovado
  separacao para daltonismo protan e tritan ..... aprovado, delta E 19,5
  separacao em visao normal ..................... aprovado, delta E 19,7
  contraste do tom mais claro sobre o fundo ..... abaixo de 3:1, por isso todo
      grafico traz rotulo de valor visivel, exigencia ja prevista no padrao do projeto.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# rampa por edicao, do mais antigo (claro) ao mais recente (escuro)
AZUL_CLARO = "#8FBCD4"
AZUL_MEDIO = "#4E8098"
AZUL_ESCURO = "#1B3A5C"
CINZA_CONTEXTO = "#C9D3D9"

CORES_EDICAO = {"2023-2024": AZUL_CLARO, "2024-2025": AZUL_MEDIO, "2025-2026": AZUL_ESCURO}
ORDEM_EDICOES = ["2023-2024", "2024-2025", "2025-2026"]

TINTA_TITULO = "#1A1A1A"
TINTA_APOIO = "#6E6E6E"
GRID = "#E4E9EC"

FONTE_DADOS = "Fonte: State of Data Brazil, Data Hackers e Bain, edições 2023-2024, 2024-2025 e 2025-2026."


def aplicar_estilo():
    plt.rcParams.update({
        "figure.dpi": 200,
        "savefig.dpi": 200,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 12,
        "axes.titleweight": "regular",
        "axes.labelsize": 9,
        "axes.labelcolor": TINTA_APOIO,
        "axes.edgecolor": GRID,
        "axes.linewidth": 0.8,
        "xtick.color": TINTA_APOIO,
        "ytick.color": TINTA_APOIO,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.frameon": False,
        "legend.fontsize": 8.5,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
    })


# Quando ligado, os graficos saem sem titulo, subtitulo e fonte, porque esses
# elementos passam a ser responsabilidade do slide. Evita duplicacao no material.
MODO_DECK = False


def moldura(ax, titulo, subtitulo=None, eixo_x=None, eixo_y=None, fonte=FONTE_DADOS):
    """Aplica a anatomia padrao do slide: titulo afirmativo, subtitulo, eixos rotulados e fonte.

    O subtitulo e a fonte sao posicionados na figura, nao no eixo, para nao colidirem
    com a area de plotagem nem com o rotulo do eixo horizontal.
    """
    import textwrap
    fig = ax.figure
    if MODO_DECK:
        if eixo_x:
            ax.set_xlabel(eixo_x, labelpad=6)
        if eixo_y:
            ax.set_ylabel(eixo_y, labelpad=6)
        for lado in ["top", "right"]:
            ax.spines[lado].set_visible(False)
        fig.subplots_adjust(top=0.97)
        return
    sub_linhas = textwrap.wrap(subtitulo, 110) if subtitulo else []
    topo = 0.99
    fig.text(0.0, topo, titulo, fontsize=12.5, color=TINTA_TITULO, ha="left", va="top")
    for i, linha in enumerate(sub_linhas):
        fig.text(0.0, topo - 0.055 - i * 0.042, linha, fontsize=8.5, color=TINTA_APOIO,
                 ha="left", va="top")
    if eixo_x:
        ax.set_xlabel(eixo_x, labelpad=6)
    if eixo_y:
        ax.set_ylabel(eixo_y, labelpad=6)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    fig.text(0.0, -0.055, fonte, fontsize=7, color=TINTA_APOIO, ha="left", va="top")
    # espaco reservado para titulo e subtitulo acima da area de plotagem
    fig.subplots_adjust(top=0.99 - 0.075 - 0.045 * max(len(sub_linhas), 1))


def formatar_percentual(ax, eixo="x"):
    f = FuncFormatter(lambda v, _: f"{v:.0f}%".replace(".", ","))
    (ax.xaxis if eixo == "x" else ax.yaxis).set_major_formatter(f)


def ticks_percentuais(ax, eixo="x", passo=None):
    """Fixa marcas de eixo em intervalos regulares, evitando sequencias irregulares."""
    import numpy as np
    lim = ax.get_xlim()[1] if eixo == "x" else ax.get_ylim()[1]
    if passo is None:
        passo = 5 if lim <= 40 else (10 if lim <= 80 else 20)
    marcas = np.arange(0, lim + passo, passo)
    (ax.set_xticks if eixo == "x" else ax.set_yticks)(marcas)


def formatar_reais(ax, eixo="y"):
    f = FuncFormatter(lambda v, _: f"R$ {v:,.0f}".replace(",", "."))
    (ax.xaxis if eixo == "x" else ax.yaxis).set_major_formatter(f)


def num_br(valor, casas=1):
    """Formata numero no padrao brasileiro, com arredondamento meio para cima.

    A formatacao padrao do Python arredonda 21,95 para 21,9, porque o valor
    binario mais proximo e ligeiramente menor. Isso gerava divergencia entre
    o numero do grafico e o mesmo numero citado no texto.
    """
    from decimal import Decimal, ROUND_HALF_UP
    quantum = Decimal(1).scaleb(-casas)
    arredondado = Decimal(str(valor)).quantize(quantum, rounding=ROUND_HALF_UP)
    return f"{arredondado:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def salvar(fig, caminho):
    fig.savefig(caminho, bbox_inches="tight", facecolor="white")
    plt.close(fig)
