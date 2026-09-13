"""Construcao dos sistemas domesticos de Leontief e Ghosh."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .mip import (
    carregar_matriz_bm_67,
    carregar_matriz_bn_67,
    carregar_matriz_participacao_tabela_13_67,
    carregar_matriz_producao_tabela_01_67,
    carregar_matriz_uso_nacional_tabela_03_67,
)


def calcular_coeficientes_tecnicos_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calcula A = D @ Bn a partir das Tabelas 13 e 11 da MIP.

    A conversão produto × atividade para atividade × atividade segue a
    composição publicada pelo IBGE na Tabela 14 (D.Bn).
    """
    matriz_bn = carregar_matriz_bn_67(tabelas)
    matriz_d = carregar_matriz_participacao_tabela_13_67(tabelas)
    if not matriz_d.columns.equals(matriz_bn.index):
        raise ValueError("Os produtos das matrizes D e Bn não estão alinhados.")

    matriz_a = matriz_d @ matriz_bn
    matriz_a.index.name = "atividade_origem"
    matriz_a.columns.name = "atividade_destino"
    return matriz_a


def calcular_matriz_transacoes_intersetoriais_67(
    tabelas: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Calcula Z = D @ U, a matriz de fluxos intersetoriais nacionais."""
    matriz_d = carregar_matriz_participacao_tabela_13_67(tabelas)
    matriz_u = carregar_matriz_uso_nacional_tabela_03_67(tabelas)
    if not matriz_d.columns.equals(matriz_u.index):
        raise ValueError("Os produtos das matrizes D e U não estão alinhados.")

    matriz_z = matriz_d @ matriz_u
    matriz_z.index.name = "atividade_origem"
    matriz_z.columns.name = "atividade_destino"
    return matriz_z


def calcular_producao_bruta_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Calcula x, o vetor de produção bruta das 67 atividades."""
    matriz_v = carregar_matriz_producao_tabela_01_67(tabelas)
    producao_bruta = matriz_v.sum(axis=0)
    producao_bruta.name = "producao_bruta"
    producao_bruta.index.name = "atividade"
    if (producao_bruta <= 0).any():
        raise ValueError("A produção bruta deve ser positiva para todas as atividades.")
    return producao_bruta


def calcular_coeficientes_importados_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calcula Am = D @ Bm, os insumos importados por atividade.

    Am é expresso na classificação atividade × atividade e permite calcular os
    insumos importados induzidos pela produção nacional.
    """
    matriz_d = carregar_matriz_participacao_tabela_13_67(tabelas)
    matriz_bm = carregar_matriz_bm_67(tabelas)
    if not matriz_d.columns.equals(matriz_bm.index):
        raise ValueError("Os produtos das matrizes D e Bm não estão alinhados.")
    matriz_am = matriz_d @ matriz_bm
    matriz_am.index.name = "atividade_origem"
    matriz_am.columns.name = "atividade_destino"
    return matriz_am


def calcular_insumos_primarios_ghosh_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Calcula o vetor de entradas primárias compatível com o sistema de Ghosh.

    No sistema doméstico publicado pelo IBGE, ``r = x - 1'Z`` fecha as contas
    por coluna e inclui valor adicionado e os demais itens exógenos ao bloco
    de fluxos nacionais (por exemplo, conteúdo importado). Não deve ser lido
    como o VAB oficial isoladamente.
    """
    matriz_z = calcular_matriz_transacoes_intersetoriais_67(tabelas)
    producao_bruta = calcular_producao_bruta_67(tabelas)
    insumos_primarios = producao_bruta - matriz_z.sum(axis=0)
    insumos_primarios.name = "insumos_primarios_ghosh"
    insumos_primarios.index.name = "atividade"
    if (insumos_primarios < -1e-8).any():
        raise ValueError("Há entradas primárias negativas no sistema de Ghosh.")
    return insumos_primarios


def calcular_coeficientes_alocacao_ghosh_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calcula B = diag(x)⁻¹ @ Z, os coeficientes de alocação de Ghosh.

    As linhas de B são atividades fornecedoras; cada elemento mostra a fração
    da produção bruta da atividade de origem destinada à atividade de coluna.
    """
    matriz_z = calcular_matriz_transacoes_intersetoriais_67(tabelas)
    producao_bruta = calcular_producao_bruta_67(tabelas)
    if not matriz_z.index.equals(producao_bruta.index):
        raise ValueError("A matriz Z e o vetor de produção bruta não estão alinhados.")

    matriz_b = matriz_z.div(producao_bruta, axis=0)
    matriz_b.index.name = "atividade_origem"
    matriz_b.columns.name = "atividade_destino"
    return matriz_b


def calcular_inversa_ghosh(coeficientes_alocacao: pd.DataFrame) -> pd.DataFrame:
    """Calcula G = (I - B)⁻¹ para a matriz de coeficientes de Ghosh."""
    if coeficientes_alocacao.shape[0] != coeficientes_alocacao.shape[1]:
        raise ValueError("A matriz de coeficientes de alocação deve ser quadrada.")
    if not coeficientes_alocacao.index.equals(coeficientes_alocacao.columns):
        raise ValueError("Índices e colunas devem representar os mesmos setores, na mesma ordem.")

    identidade = np.eye(coeficientes_alocacao.shape[0])
    inversa = np.linalg.inv(identidade - coeficientes_alocacao.to_numpy(dtype=float))
    resultado = pd.DataFrame(inversa, index=coeficientes_alocacao.index, columns=coeficientes_alocacao.columns)
    resultado.index.name = coeficientes_alocacao.index.name
    resultado.columns.name = coeficientes_alocacao.columns.name
    return resultado


def calcular_inversa_leontief(coeficientes_tecnicos: pd.DataFrame) -> pd.DataFrame:
    """Calcula L = (I - A)⁻¹ para uma matriz quadrada de coeficientes técnicos."""
    if coeficientes_tecnicos.shape[0] != coeficientes_tecnicos.shape[1]:
        raise ValueError("A matriz de coeficientes técnicos deve ser quadrada.")
    if not coeficientes_tecnicos.index.equals(coeficientes_tecnicos.columns):
        raise ValueError("Índices e colunas devem representar os mesmos setores, na mesma ordem.")

    identidade = np.eye(coeficientes_tecnicos.shape[0])
    inversa = np.linalg.inv(identidade - coeficientes_tecnicos.to_numpy(dtype=float))
    resultado = pd.DataFrame(
        inversa,
        index=coeficientes_tecnicos.index,
        columns=coeficientes_tecnicos.columns,
    )
    resultado.index.name = coeficientes_tecnicos.index.name
    resultado.columns.name = coeficientes_tecnicos.columns.name
    return resultado
