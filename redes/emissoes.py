"""Contabilidade de CO2 por producao, consumo e renda."""

from __future__ import annotations

import numpy as np
import pandas as pd


def calcular_emissoes_producao(
    intensidade_co2: pd.Series, producao_bruta: pd.Series
) -> pd.Series:
    """Calcula emissões diretas: ``e = γ ⊙ x``."""
    if not intensidade_co2.index.equals(producao_bruta.index):
        raise ValueError("Intensidade e produção bruta devem ter os mesmos setores, na mesma ordem.")
    resultado = intensidade_co2 * producao_bruta
    resultado.name = "emissoes_producao_gg_co2"
    return resultado


def calcular_matriz_emissoes_consumo(
    intensidade_co2: pd.Series,
    inversa_leontief: pd.DataFrame,
    demanda_final: pd.Series,
) -> pd.DataFrame:
    """Atribui emissões à demanda final: ``diag(γ) @ L @ diag(f)``.

    Linhas são os setores emissores e colunas os setores dos bens demandados
    na demanda final. A soma das colunas é a responsabilidade pelo consumo.
    """
    indice = inversa_leontief.index
    if not (indice.equals(inversa_leontief.columns) and indice.equals(intensidade_co2.index) and indice.equals(demanda_final.index)):
        raise ValueError("Intensidade, demanda final e inversa de Leontief devem estar alinhadas.")
    valores = np.diag(intensidade_co2.to_numpy()) @ inversa_leontief.to_numpy() @ np.diag(demanda_final.to_numpy())
    resultado = pd.DataFrame(valores, index=indice, columns=indice)
    resultado.index.name = "atividade_emissora"
    resultado.columns.name = "atividade_da_demanda_final"
    return resultado


def calcular_matrizes_emissoes_consumo_com_importacoes(
    intensidade_domestica: pd.Series,
    intensidade_externa: pd.Series,
    inversa_leontief_domestica: pd.DataFrame,
    inversa_leontief_externa: pd.DataFrame,
    demanda_final_domestica: pd.Series,
    demanda_final_importada: pd.Series,
    coeficientes_importados: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Calcula emissões do consumo brasileiro com importações explícitas.

    A conta tem três componentes: produção doméstica para demanda doméstica,
    importações finais e importações intermediárias requeridas pela produção
    doméstica. A tecnologia e as intensidades do exterior são parâmetros
    independentes recebidos do cenário; esta função não presume que sejam
    iguais aos brasileiros.
    """
    indice = inversa_leontief_domestica.index
    objetos = [
        inversa_leontief_domestica.columns,
        inversa_leontief_externa.index,
        inversa_leontief_externa.columns,
        intensidade_domestica.index,
        intensidade_externa.index,
        demanda_final_domestica.index,
        demanda_final_importada.index,
        coeficientes_importados.index,
        coeficientes_importados.columns,
    ]
    if not all(indice.equals(objeto) for objeto in objetos):
        raise ValueError("Todas as matrizes e vetores da conta de consumo devem estar alinhados.")

    l = inversa_leontief_domestica.to_numpy(dtype=float)
    l_ext = inversa_leontief_externa.to_numpy(dtype=float)
    am = coeficientes_importados.to_numpy(dtype=float)
    gamma_dom = intensidade_domestica.to_numpy(dtype=float)
    gamma_ext = intensidade_externa.to_numpy(dtype=float)
    f_dom = demanda_final_domestica.to_numpy(dtype=float)
    f_imp = demanda_final_importada.to_numpy(dtype=float)

    componentes = {
        "domestica": np.diag(gamma_dom) @ l @ np.diag(f_dom),
        "importacoes_finais": np.diag(gamma_ext) @ l_ext @ np.diag(f_imp),
        "importacoes_intermediarias": np.diag(gamma_ext) @ l_ext @ am @ l @ np.diag(f_dom),
    }
    resultado: dict[str, pd.DataFrame] = {}
    for nome, valores in componentes.items():
        matriz = pd.DataFrame(valores, index=indice, columns=indice)
        matriz.index.name = "atividade_emissora"
        matriz.columns.name = "atividade_da_demanda_final"
        resultado[nome] = matriz
    resultado["total"] = resultado["domestica"] + resultado["importacoes_finais"] + resultado["importacoes_intermediarias"]
    return resultado


def calcular_matriz_emissoes_renda(
    insumos_primarios: pd.Series,
    inversa_ghosh: pd.DataFrame,
    intensidade_co2: pd.Series,
) -> pd.DataFrame:
    """Atribui emissões às entradas primárias: ``diag(r) @ G @ diag(γ)``.

    Linhas são os setores que recebem a renda/entrada primária e colunas os
    setores emissores. A soma das linhas é a responsabilidade baseada em renda.
    """
    indice = inversa_ghosh.index
    if not (indice.equals(inversa_ghosh.columns) and indice.equals(insumos_primarios.index) and indice.equals(intensidade_co2.index)):
        raise ValueError("Entradas primárias, intensidade e inversa de Ghosh devem estar alinhadas.")
    valores = np.diag(insumos_primarios.to_numpy()) @ inversa_ghosh.to_numpy() @ np.diag(intensidade_co2.to_numpy())
    resultado = pd.DataFrame(valores, index=indice, columns=indice)
    resultado.index.name = "atividade_da_renda"
    resultado.columns.name = "atividade_emissora"
    return resultado
