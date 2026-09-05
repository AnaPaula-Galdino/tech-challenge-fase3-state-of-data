"""
Diagrama da arquitetura da solucao na AWS.

Gera o PNG em alta resolucao usado no material executivo. O arquivo editavel
equivalente, em formato Draw.io, esta em entregaveis/arquitetura_aws.drawio.

Layout em tres faixas: ingestao e processamento em camadas na faixa superior,
catalogo da camada Gold na faixa do meio e consumo analitico na faixa inferior. O fluxo corre
da esquerda para a direita, sem cruzamento de setas.
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estilo as E

E.aplicar_estilo()


def caixa(ax, x, y, larg, alt, titulo, sub, fundo, tinta="white", tam_titulo=9.0):
    ax.add_patch(FancyBboxPatch((x, y), larg, alt, boxstyle="round,pad=0.015,rounding_size=0.05",
                                facecolor=fundo, edgecolor="none", zorder=3))
    ax.text(x + larg / 2, y + alt * 0.64, titulo, ha="center", va="center",
            fontsize=tam_titulo, color=tinta, zorder=4)
    ax.text(x + larg / 2, y + alt * 0.27, sub, ha="center", va="center",
            fontsize=7.0, color=tinta, alpha=0.9, zorder=4, linespacing=1.35)


def seta(ax, p1, p2, rotulo=None, desloc=(0, 0.16)):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=12,
                                 linewidth=1.4, color=E.AZUL_MEDIO, zorder=2,
                                 shrinkA=1, shrinkB=1))
    if rotulo:
        ax.text((p1[0] + p2[0]) / 2 + desloc[0], (p1[1] + p2[1]) / 2 + desloc[1], rotulo,
                ha="center", fontsize=6.9, color=E.TINTA_APOIO, zorder=4)


def gerar(caminho="figuras/arquitetura_aws.png", com_titulo=True):
    fig, ax = plt.subplots(figsize=(13.6, 4.9))
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 5.55)
    ax.axis("off")

    A = 0.82   # altura padrao das caixas
    L = 2.15   # largura padrao

    # moldura da regiao AWS
    # a moldura cobre apenas o que roda dentro do laboratorio da AWS
    ax.add_patch(FancyBboxPatch((3.0, 0.35), 8.75, 5.05, boxstyle="round,pad=0.03,rounding_size=0.06",
                                facecolor="#F5F8FA", edgecolor=E.CINZA_CONTEXTO, linewidth=1, zorder=0))
    ax.text(3.2, 5.12, "AWS Academy Lab   ·   região us-east-1, Norte da Virgínia",
            fontsize=8.2, color=E.TINTA_APOIO, zorder=1)
    ax.add_patch(FancyBboxPatch((11.95, 0.35), 4.0, 5.05, boxstyle="round,pad=0.03,rounding_size=0.06",
                                facecolor="#FAFAFA", edgecolor=E.CINZA_CONTEXTO, linewidth=1,
                                linestyle=(0, (4, 3)), zorder=0))
    ax.text(12.15, 5.12, "Fora do laboratório", fontsize=8.2, color=E.TINTA_APOIO, zorder=1)

    y1, y2, y3 = 3.95, 2.42, 0.9

    # ---- faixa 1: ingestao e camadas ----
    caixa(ax, 0.15, y1, 2.4, A, "Kaggle", "3 edições do State of\nData Brazil, em CSV",
          E.CINZA_CONTEXTO, E.TINTA_TITULO)
    caixa(ax, 3.25, y1, L, A, "S3 · Bronze", "dados crus, fiéis à\norigem, por edição", E.AZUL_CLARO, E.TINTA_TITULO)
    caixa(ax, 6.25, y1, L, A, "Glue Job 01", "PySpark: encoding,\ntipos, de/para, dedupe", E.AZUL_MEDIO)
    caixa(ax, 9.25, y1, L, A, "S3 · Silver", "harmonizada, uma\nlinha por respondente", E.AZUL_MEDIO)
    caixa(ax, 9.35, y2, L, A, "Glue Job 02", "PySpark: agregações\npor pergunta", E.AZUL_MEDIO)

    seta(ax, (2.6, y1 + A / 2), (3.2, y1 + A / 2), "ingestão", desloc=(0, 0.3))
    seta(ax, (5.45, y1 + A / 2), (6.2, y1 + A / 2), "leitura")
    seta(ax, (8.45, y1 + A / 2), (9.2, y1 + A / 2), "escrita")
    seta(ax, (10.42, y1 - 0.02), (10.42, y2 + A + 0.02), "leitura", desloc=(0.6, -0.05))

    # ---- faixa 2: gold e catalogo ----
    caixa(ax, 6.35, y2, L, A, "S3 · Gold", "tabelas analíticas\nem Parquet", E.AZUL_ESCURO)
    seta(ax, (9.3, y2 + A / 2), (8.55, y2 + A / 2), "escrita")

    caixa(ax, 3.25, y2, L, A, "Glue Data Catalog", "camada Gold catalogada\npelo crawler", E.AZUL_ESCURO)
    seta(ax, (6.3, y2 + A / 2), (5.45, y2 + A / 2), "registro")

    # ---- faixa 3: consumo ----
    caixa(ax, 3.25, y3, L, A, "Amazon Athena", "consultas SQL sobre\na camada Gold", E.AZUL_ESCURO)
    caixa(ax, 6.35, y3, L, A, "S3 · Resultados", "saídas das consultas\nem athena-results/", E.AZUL_MEDIO)
    caixa(ax, 9.35, y3, L, A, "Exportação", "tabelas analíticas\nprontas para o gráfico", E.AZUL_MEDIO)
    caixa(ax, 12.15, y3, L, A, "Gráficos em Python", "alta resolução, paleta\núnica do trabalho", E.CINZA_CONTEXTO, E.TINTA_TITULO)
    caixa(ax, 12.15, y2, L, A, "Material executivo", "insights, recomendações\ne storytelling", E.CINZA_CONTEXTO, E.TINTA_TITULO)

    seta(ax, (4.32, y2 - 0.02), (4.32, y3 + A + 0.02))
    seta(ax, (5.45, y3 + A / 2), (6.3, y3 + A / 2))
    seta(ax, (8.55, y3 + A / 2), (9.3, y3 + A / 2))
    seta(ax, (11.55, y3 + A / 2), (12.1, y3 + A / 2))
    seta(ax, (13.22, y3 + A + 0.02), (13.22, y2 - 0.02))

    if com_titulo:
        fig.suptitle("Arquitetura da solução, do arquivo de origem ao material executivo",
                     x=0.011, y=0.995, ha="left", fontsize=12.8, color=E.TINTA_TITULO)
        fig.text(0.011, 0.912,
                 "Todo o processamento distribuído usa Spark, executado pelo AWS Glue. As camadas tratadas são gravadas em Parquet. O enunciado admite Glue Notebook ou Athena para a consulta analítica, e a solução usa o Athena.",
                 fontsize=8.2, color=E.TINTA_APOIO)
    E.salvar(fig, caminho)
    return caminho


if __name__ == "__main__":
    import os
    print("gerado:", gerar())
    os.makedirs("figuras/deck", exist_ok=True)
    # versao para o material executivo, sem titulo, porque o slide ja o traz
    print("gerado:", gerar("figuras/deck/arquitetura_aws.png", com_titulo=False))
