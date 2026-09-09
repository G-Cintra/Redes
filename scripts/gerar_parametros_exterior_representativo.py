"""Gera os CSVs iniciais do cenário de exterior representativo.

O cenário inicial replica a hipótese didática: exterior e Brasil têm as mesmas
intensidades de CO2 e a mesma inversa de Leontief. Os CSVs resultantes são os
arquivos lidos pelo notebook e podem ser substituídos por um cenário empírico.
"""

from scr.dados import (
    ARQUIVO_INTENSIDADES_CO2_EXTERIOR,
    ARQUIVO_INVERSA_LEONTIEF_EXTERIOR,
    calcular_coeficientes_tecnicos_67,
    calcular_inversa_leontief,
    carregar_coeficientes_co2,
    carregar_matriz_67,
)


def main() -> None:
    tabelas = carregar_matriz_67()
    inversa_brasil = calcular_inversa_leontief(calcular_coeficientes_tecnicos_67(tabelas))
    intensidades = carregar_coeficientes_co2()

    intensidades.index = inversa_brasil.index
    intensidades.index.name = "atividade"
    intensidades.columns = intensidades.columns.astype(str)

    ARQUIVO_INTENSIDADES_CO2_EXTERIOR.parent.mkdir(parents=True, exist_ok=True)
    intensidades.to_csv(ARQUIVO_INTENSIDADES_CO2_EXTERIOR)
    inversa_brasil.rename_axis("atividade").to_csv(ARQUIVO_INVERSA_LEONTIEF_EXTERIOR)


if __name__ == "__main__":
    main()
