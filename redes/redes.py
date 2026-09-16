"""Leitura das matrizes exportadas e conversão operacional para grafos."""

import csv

import networkx as nx
import numpy as np
import pandas as pd

from redes import dados


def validar_matriz(matriz):
    """Exige os mesmos setores nos dois eixos e pesos finitos não negativos."""
    if matriz.empty or not matriz.index.is_unique or not matriz.columns.is_unique:
        raise ValueError("A matriz deve ter setores únicos e não pode estar vazia.")
    if not matriz.index.equals(matriz.columns):
        raise ValueError("Linhas e colunas devem ter os mesmos setores, na mesma ordem.")
    if any(not isinstance(c, str) or not c.strip() for c in matriz.index):
        raise ValueError("Os códigos dos setores devem ser textos não vazios.")
    valores = matriz.to_numpy(dtype=float)
    if not np.isfinite(valores).all() or (valores < 0).any():
        raise ValueError("Os pesos devem ser finitos e não negativos.")


def carregar_matriz_emissoes(id_entrada):
    """Verifica o hash antes de abrir o CSV; preserva códigos com zeros iniciais."""
    item = dados.entrada(id_entrada)
    caminho = dados.RAIZ_PROJETO / item["arquivo"]
    dados.check_sha256(caminho, item["sha256"])
    # pandas renomeia cabeçalhos repetidos; verifica o original antes da leitura.
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        cabecalho = next(csv.reader(arquivo))
    if cabecalho[0] != "atividade_emissora" or len(set(cabecalho[1:])) != len(cabecalho[1:]):
        raise ValueError("Cabeçalho ausente ou setores repetidos no CSV.")
    matriz = pd.read_csv(caminho, dtype={"atividade_emissora": str},
                         index_col="atividade_emissora", float_precision="round_trip")
    matriz = matriz.apply(pd.to_numeric, errors="raise")
    validar_matriz(matriz)
    return matriz


def carregar_setores(id_entrada):
    """Lê apenas o catálogo exportado, sem acessar a MIP."""
    item = dados.entrada(id_entrada)
    caminho = dados.RAIZ_PROJETO / item["arquivo"]
    dados.check_sha256(caminho, item["sha256"])
    setores = pd.read_csv(caminho, dtype=str).set_index("atividade")
    if not setores.index.is_unique or setores["descricao"].isna().any():
        raise ValueError("Catálogo com códigos repetidos ou descrições ausentes.")
    return setores["descricao"]


def carregar_valor_adicionado(id_entrada):
    """Lê o VAB exportado pela MIP, com hash e códigos setoriais preservados."""
    item = dados.entrada(id_entrada)
    caminho = dados.RAIZ_PROJETO / item["arquivo"]
    dados.check_sha256(caminho, item["sha256"])
    tabela = pd.read_csv(caminho, dtype={"atividade": str})
    if tabela["atividade"].isna().any() or not tabela["atividade"].is_unique:
        raise ValueError("VAB com códigos ausentes ou repetidos.")
    vab = tabela.set_index("atividade")["vab_r_milhao"].apply(pd.to_numeric, errors="raise")
    if vab.empty or not np.isfinite(vab).all() or (vab <= 0).any():
        raise ValueError("O VAB deve ser finito e positivo em todas as atividades.")
    return vab


def matriz_para_grafo(matriz):
    """Linha i → coluna j, peso original; zeros ausentes e diagonal preservada."""
    validar_matriz(matriz)
    grafo = nx.DiGraph()
    grafo.add_nodes_from(matriz.index)
    for i, origem in enumerate(matriz.index):
        for j, destino in enumerate(matriz.columns):
            peso = float(matriz.iloc[i, j])
            if peso > 0:
                grafo.add_edge(origem, destino, weight=peso)
    return grafo
