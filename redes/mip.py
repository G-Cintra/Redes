"""Extracao das tabelas IBGE e conversao da demanda de produtos para atividades."""

from __future__ import annotations

import pandas as pd


def _extrair_matriz_atividade_67(tabela: pd.DataFrame) -> pd.DataFrame:
    """Extrai o bloco 67 × 67 de uma tabela de atividades da MIP."""
    linhas = slice(5, 72)
    colunas = slice(2, 69)
    codigos_linhas = tabela.iloc[linhas, 0].astype(str).tolist()
    codigos_colunas = [str(valor).split("\n", maxsplit=1)[0] for valor in tabela.iloc[3, colunas]]

    if len(codigos_linhas) != 67 or codigos_linhas != codigos_colunas:
        raise ValueError("A tabela não contém uma matriz de atividades 67 × 67 consistente.")

    valores = tabela.iloc[linhas, colunas].apply(pd.to_numeric, errors="raise")
    matriz = pd.DataFrame(valores.to_numpy(dtype=float), index=codigos_linhas, columns=codigos_colunas)
    matriz.index.name = "atividade_origem"
    matriz.columns.name = "atividade_destino"
    return matriz


def carregar_coeficientes_tecnicos_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai a matriz A de coeficientes técnicos da Tabela 14 da MIP.

    Cada elemento ``a_ij`` expressa o insumo da atividade ``i`` requerido para
    uma unidade de produção da atividade ``j``. A matriz corresponde à D.Bn do
    IBGE, isto é, aos coeficientes técnicos intersetoriais de insumos nacionais.
    """
    try:
        return _extrair_matriz_atividade_67(tabelas["14"])
    except KeyError as erro:
        raise ValueError("A Tabela 14 não foi encontrada no arquivo da MIP.") from erro


def carregar_matriz_bn_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai Bn (produto × atividade) da Tabela 11 da MIP.

    Bn contém os coeficientes técnicos de insumos nacionais: cada coluna é uma
    atividade e cada linha é um produto.
    """
    try:
        tabela = tabelas["11"]
    except KeyError as erro:
        raise ValueError("A Tabela 11 não foi encontrada no arquivo da MIP.") from erro

    linhas = slice(5, 132)
    colunas = slice(2, 69)
    produtos = tabela.iloc[linhas, 0].astype(str).tolist()
    atividades = [str(valor).split("\n", maxsplit=1)[0] for valor in tabela.iloc[3, colunas]]
    valores = tabela.iloc[linhas, colunas].apply(pd.to_numeric, errors="raise")

    if len(produtos) != 127 or len(atividades) != 67:
        raise ValueError("A Tabela 11 não contém a matriz Bn esperada (127 × 67).")

    matriz = pd.DataFrame(valores.to_numpy(dtype=float), index=produtos, columns=atividades)
    matriz.index.name = "produto"
    matriz.columns.name = "atividade_destino"
    return matriz


def carregar_matriz_bm_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai Bm (produto × atividade) da Tabela 12 da MIP.

    Bm contém os coeficientes de insumos importados. Cada coluna indica os
    produtos importados requeridos diretamente por unidade de produção da
    atividade correspondente.
    """
    try:
        tabela = tabelas["12"]
    except KeyError as erro:
        raise ValueError("A Tabela 12 não foi encontrada no arquivo da MIP.") from erro
    return _extrair_produto_atividade_67(tabela, 2, 69)


def carregar_matriz_participacao_tabela_13_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai D (atividade × produto) da Tabela 13 da MIP.

    D é a matriz de participação setorial (*market share*) da produção nacional.
    """
    try:
        tabela = tabelas["13"]
    except KeyError as erro:
        raise ValueError("A Tabela 13 não foi encontrada no arquivo da MIP.") from erro

    linhas = slice(5, 72)
    colunas = slice(2, 129)
    atividades = tabela.iloc[linhas, 0].astype(str).tolist()
    produtos = [str(valor).split("\n", maxsplit=1)[0] for valor in tabela.iloc[3, colunas]]
    valores = tabela.iloc[linhas, colunas].apply(pd.to_numeric, errors="raise")

    if len(atividades) != 67 or len(produtos) != 127:
        raise ValueError("A Tabela 13 não contém a matriz D esperada (67 × 127).")

    matriz = pd.DataFrame(valores.to_numpy(dtype=float), index=atividades, columns=produtos)
    matriz.index.name = "atividade_origem"
    matriz.columns.name = "produto"
    return matriz


def _extrair_produto_atividade_67(
    tabela: pd.DataFrame, inicio_colunas: int, fim_colunas: int
) -> pd.DataFrame:
    """Extrai uma matriz de 127 produtos por 67 atividades."""
    linhas = slice(5, 132)
    colunas = slice(inicio_colunas, fim_colunas)
    produtos = tabela.iloc[linhas, 0].astype(str).tolist()
    atividades = [str(valor).split("\n", maxsplit=1)[0] for valor in tabela.iloc[3, colunas]]
    valores = tabela.iloc[linhas, colunas].apply(pd.to_numeric, errors="raise")

    if len(produtos) != 127 or len(atividades) != 67:
        raise ValueError("A tabela não contém uma matriz produto × atividade (127 × 67).")

    matriz = pd.DataFrame(valores.to_numpy(dtype=float), index=produtos, columns=atividades)
    matriz.index.name = "produto"
    matriz.columns.name = "atividade"
    return matriz


def carregar_matriz_producao_tabela_01_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai V, a produção nacional por produto (linhas) e atividade (colunas)."""
    try:
        return _extrair_produto_atividade_67(tabelas["01"], 7, 74)
    except KeyError as erro:
        raise ValueError("A Tabela 01 não foi encontrada no arquivo da MIP.") from erro


def carregar_matriz_uso_nacional_tabela_03_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai U, os usos intermediários nacionais por produto e atividade."""
    try:
        return _extrair_produto_atividade_67(tabelas["03"], 3, 70)
    except KeyError as erro:
        raise ValueError("A Tabela 03 não foi encontrada no arquivo da MIP.") from erro


def carregar_demanda_final_nacional_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Calcula a demanda final nacional por atividade a partir da Tabela 03.

    A Tabela 03 registra a demanda final por produto. A matriz D da Tabela 13
    converte esse vetor para atividades, mantendo a tecnologia nacional usada
    na matriz A. O resultado ``f`` satisfaz ``x = Z @ 1 + f`` (salvo erro de
    arredondamento) no sistema doméstico da MIP.
    """
    try:
        tabela = tabelas["03"]
    except KeyError as erro:
        raise ValueError("A Tabela 03 não foi encontrada no arquivo da MIP.") from erro

    # Coluna 77: "Demanda final"; linhas 5:132: os 127 produtos.
    demanda_por_produto = pd.to_numeric(tabela.iloc[5:132, 77], errors="raise").to_numpy(dtype=float)
    matriz_d = carregar_matriz_participacao_tabela_13_67(tabelas)
    demanda_final = pd.Series(matriz_d.to_numpy() @ demanda_por_produto, index=matriz_d.index)
    demanda_final.name = "demanda_final_nacional"
    demanda_final.index.name = "atividade"
    return demanda_final


def _carregar_demanda_final_por_produto_67(
    tabelas: dict[str, pd.DataFrame], aba: str, colunas: slice, nome: str
) -> pd.Series:
    """Converte componentes da demanda final por produto em atividade."""
    try:
        tabela = tabelas[aba]
    except KeyError as erro:
        raise ValueError(f"A Tabela {aba} não foi encontrada no arquivo da MIP.") from erro

    demanda_por_produto = tabela.iloc[5:132, colunas].apply(pd.to_numeric, errors="raise").sum(axis=1).to_numpy(dtype=float)
    matriz_d = carregar_matriz_participacao_tabela_13_67(tabelas)
    demanda_final = pd.Series(matriz_d.to_numpy() @ demanda_por_produto, index=matriz_d.index, name=nome)
    demanda_final.index.name = "atividade"
    return demanda_final


def carregar_demanda_final_domestica_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Carrega a demanda final doméstica pela produção nacional da Tabela 03.

    Soma governo, ISFLSF, famílias, FBCF e variação de estoques, excluindo a
    coluna de exportações.
    """
    return _carregar_demanda_final_por_produto_67(
        tabelas, "03", slice(72, 77), "demanda_final_domestica_nacional"
    )


def carregar_demanda_final_exportacoes_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Carrega as exportações da produção nacional da Tabela 03."""
    return _carregar_demanda_final_por_produto_67(tabelas, "03", slice(71, 72), "exportacoes_nacionais")


def carregar_demanda_final_importada_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Carrega a demanda final doméstica atendida por importações da Tabela 04."""
    return _carregar_demanda_final_por_produto_67(
        tabelas, "04", slice(72, 77), "demanda_final_importada"
    )


def carregar_inversa_leontief_ibge_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai a Matriz de Leontief divulgada pelo IBGE na Tabela 15."""
    try:
        return _extrair_matriz_atividade_67(tabelas["15"])
    except KeyError as erro:
        raise ValueError("A Tabela 15 não foi encontrada no arquivo da MIP.") from erro
