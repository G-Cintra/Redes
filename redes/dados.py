"""Leitura das entradas canônicas da análise."""

import csv
from hashlib import sha256
from pathlib import Path
import re

import pandas as pd


RAIZ_PROJETO = Path(__file__).resolve().parent.parent
MANIFESTO = RAIZ_PROJETO / "raw" / "manifesto.csv"


def check_sha256(caminho, sha256_esperado):
    """Interrompe a leitura se os bytes não forem os declarados no manifesto."""
    caminho = Path(caminho)
    if not caminho.is_file():
        raise ValueError(f"Arquivo de entrada não encontrado: {caminho}")

    digest = sha256()
    with caminho.open("rb") as arquivo:
        while bloco := arquivo.read(1024 * 1024):
            digest.update(bloco)
    if digest.hexdigest().upper() != sha256_esperado.upper():
        raise ValueError(f"SHA-256 divergente para {caminho.name}.")
    print(f"SHA-256 verificado: {caminho.name}")


def entrada(id_entrada):
    """Retorna a linha do manifesto correspondente a uma entrada canônica."""
    encontrada = None
    with MANIFESTO.open(encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            if linha["id"] == id_entrada:
                if encontrada is not None:
                    raise ValueError(f"O manifesto repete o id: {id_entrada}")
                encontrada = linha
    if encontrada is None:
        raise ValueError(f"Entrada não encontrada no manifesto: {id_entrada}")
    return encontrada


def carregar_matriz_67(id_entrada):
    """Verifica e abre a MIP brasileira de nível 67."""
    item = entrada(id_entrada)
    caminho = RAIZ_PROJETO / item["arquivo"]
    check_sha256(caminho, item["sha256"])
    return pd.read_excel(caminho, sheet_name=None, header=None, engine="xlrd")


def carregar_coeficientes_co2(id_entrada):
    """Verifica e abre coeficientes de CO₂ por setor e ano."""
    item = entrada(id_entrada)
    caminho = RAIZ_PROJETO / item["arquivo"]
    check_sha256(caminho, item["sha256"])
    dados = pd.read_csv(caminho)
    if "setor_id" not in dados:
        raise ValueError("O CSV de coeficientes deve conter a coluna 'setor_id'.")

    padrao = re.compile(r"^coeficiente_(\d{4})_gg_co2_por_r_milhao$")
    colunas = [
        (coluna, int(correspondencia.group(1)))
        for coluna in dados.columns
        if (correspondencia := padrao.fullmatch(coluna))
    ]
    if not colunas:
        raise ValueError("O CSV deve conter ao menos uma coluna de coeficiente com ano no nome.")

    nomes, anos = zip(*colunas)
    matriz = dados.set_index("setor_id")[list(nomes)].apply(pd.to_numeric, errors="raise")
    matriz.columns = pd.Index(anos, name="ano")
    if matriz.index.tolist() != [f"S{i}" for i in range(1, 68)] or matriz.isna().any().any():
        raise ValueError("O CSV deve conter S1 a S67, na ordem correta e sem valores ausentes.")
    return matriz


def carregar_intensidades_co2_exterior(id_entrada):
    """Verifica e abre as intensidades do cenário exterior."""
    item = entrada(id_entrada)
    caminho = RAIZ_PROJETO / item["arquivo"]
    check_sha256(caminho, item["sha256"])
    dados = pd.read_csv(caminho, dtype={"atividade": str})
    if "atividade" not in dados:
        raise ValueError("O CSV do exterior deve conter a coluna 'atividade'.")
    matriz = dados.set_index("atividade").apply(pd.to_numeric, errors="raise")
    matriz.columns = pd.Index([int(coluna) for coluna in matriz.columns], name="ano")
    if matriz.shape[0] != 67 or matriz.isna().any().any():
        raise ValueError("O CSV de intensidades deve conter 67 atividades sem valores ausentes.")
    return matriz


def carregar_inversa_leontief_exterior(id_entrada):
    """Verifica e abre a inversa de Leontief do cenário exterior."""
    item = entrada(id_entrada)
    caminho = RAIZ_PROJETO / item["arquivo"]
    check_sha256(caminho, item["sha256"])
    dados = pd.read_csv(caminho, dtype={"atividade": str})
    if "atividade" not in dados:
        raise ValueError("O CSV da inversa exterior deve conter a coluna 'atividade'.")
    matriz = dados.set_index("atividade").apply(pd.to_numeric, errors="raise")
    matriz.columns = matriz.columns.astype(str)
    if matriz.shape != (67, 67) or not matriz.index.equals(matriz.columns):
        raise ValueError("A inversa exterior deve ser 67 × 67, com índice e colunas alinhados.")
    matriz.index.name = "atividade_origem"
    matriz.columns.name = "atividade_destino"
    return matriz
