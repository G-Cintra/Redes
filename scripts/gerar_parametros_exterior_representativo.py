"""Gera os CSVs iniciais do cenário de exterior representativo.

O cenário inicial replica a hipótese didática: exterior e Brasil têm as mesmas
intensidades de CO2 e a mesma inversa de Leontief. Os CSVs resultantes são os
arquivos lidos pelo notebook e podem ser substituídos por um cenário empírico.
"""

from scr import arquivos, modelos


def main() -> None:
    tabelas = arquivos.carregar_matriz_67()
    inversa_brasil = modelos.calcular_inversa_leontief(modelos.calcular_coeficientes_tecnicos_67(tabelas))
    intensidades = arquivos.carregar_coeficientes_co2()

    intensidades.index = inversa_brasil.index
    intensidades.index.name = "atividade"
    intensidades.columns = intensidades.columns.astype(str)

    arquivos.ARQUIVO_INTENSIDADES_CO2_EXTERIOR.parent.mkdir(parents=True, exist_ok=True)
    intensidades.to_csv(arquivos.ARQUIVO_INTENSIDADES_CO2_EXTERIOR)
    inversa_brasil.rename_axis("atividade").to_csv(arquivos.ARQUIVO_INVERSA_LEONTIEF_EXTERIOR)
    arquivos.MANIFESTO_EXTERIOR.write_text(
        "".join(
            f"{arquivos.calcular_sha256(caminho)} *{caminho.name}\n"
            for caminho in (arquivos.ARQUIVO_INTENSIDADES_CO2_EXTERIOR,
                            arquivos.ARQUIVO_INVERSA_LEONTIEF_EXTERIOR)
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
