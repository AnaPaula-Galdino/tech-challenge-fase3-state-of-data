"""
Leitor de cabecalhos e resolvedor de colunas das tres edicoes do State of Data Brazil.

Cobre os tres padroes de nomenclatura observados nos arquivos originais:
  1. tupla            -> ('P1_a ', 'Idade')                     (edicao 2023-2024)
  2. numerico com _   -> 1.a.1_faixa_idade                      (edicoes 2024-2025 e 2025-2026)
  3. numerico com ' ' -> 3.f.1 Colaboradores usando AI generativa
Trata tambem o cabecalho malformado de 2023-2024 sem aspa de fechamento.
"""
import csv, re, sys, unicodedata

csv.field_size_limit(10**9)

EDICOES = {
    "2023-2024": "74cb52c2-archive/State_of_data_BR_2023_Kaggle - df_survey_2023.csv",
    "2024-2025": "51bb6bd7-archive_1/Final Dataset - State of Data 2024 - Kaggle - df_survey_2024.csv",
    "2025-2026": "f136db87-archive_2/Final Dataset - State of Data 2025-2026 - Kaggle.csv",
}

_RE_TUPLA = re.compile(r"^\('\s*([^']+?)\s*'\s*,\s*'?(.*?)'?\)?$")
_RE_NUM = re.compile(r"^(\d+(?:\.[A-Za-z0-9]+)*)[_ ](.*)$")


def parse_header(h):
    """Devolve (codigo_normalizado, descricao, padrao_detectado)."""
    if h.startswith("('"):
        m = _RE_TUPLA.match(h)
        if not m:
            return None, h, "nao_reconhecido"
        cod = re.sub(r"^P", "", m.group(1).strip()).replace("_", ".").lower()
        return cod, m.group(2).strip(), "tupla"
    m = _RE_NUM.match(h)
    if m:
        return m.group(1).lower(), m.group(2).strip(), "numerico"
    return None, h, "nao_reconhecido"


def normalizar(texto):
    """Minusculas, sem acento e sem pontuacao, para comparar descricoes."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def ler_cabecalhos(base_dir="."):
    """Devolve {edicao: [(codigo, descricao, descricao_normalizada, header_original)]}."""
    out = {}
    for ed, arq in EDICOES.items():
        with open(f"{base_dir}/{arq}", encoding="utf-8") as fh:
            headers = next(csv.reader(fh))
        linhas = []
        for h in headers:
            cod, des, padrao = parse_header(h)
            if padrao == "nao_reconhecido":
                raise ValueError(f"cabecalho nao reconhecido em {ed}: {h!r}")
            linhas.append((cod, des, normalizar(des), h))
        out[ed] = linhas
    return out


def buscar(cabecalhos, termos, edicao=None):
    """Busca colunas cuja descricao normalizada contenha todos os termos informados."""
    termos = [normalizar(t) for t in termos]
    res = {}
    for ed, linhas in cabecalhos.items():
        if edicao and ed != edicao:
            continue
        res[ed] = [(c, d, h) for c, d, dn, h in linhas if all(t in dn for t in termos)]
    return res
