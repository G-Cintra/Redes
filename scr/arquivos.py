"""Leitura e integridade dos arquivos de entrada e parametros de cenario."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pandas as pd


RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_RAW = RAIZ_PROJETO / "raw"
MANIFESTO_CHECKSUMS = PASTA_RAW / "SHA256SUMS"
ARQUIVO_MIP_67 = PASTA_RAW / "Matriz_de_Insumo_Produto_2015_Nivel_67.xls"
ARQUIVO_COEFICIENTES_CO2 = (
    RAIZ_PROJETO
    / "references"
    / "sanguinet_azzoni_2024"
    / "coeficientes_co2_2011_2018.csv"
)
PASTA_PARAMETROS_EXTERIOR = RAIZ_PROJETO / "parameters" / "exterior_representativo"
MANIFESTO_EXTERIOR = PASTA_PARAMETROS_EXTERIOR / "SHA256SUMS"
MANIFESTO_COEFICIENTES_CO2 = ARQUIVO_COEFICIENTES_CO2.parent / "SHA256SUMS"
ARQUIVO_INTENSIDADES_CO2_EXTERIOR = (
    PASTA_PARAMETROS_EXTERIOR / "intensidades_co2_exterior_representativo.csv"
)
ARQUIVO_INVERSA_LEONTIEF_EXTERIOR = (
    PASTA_PARAMETROS_EXTERIOR / "inversa_leontief_exterior_representativo.csv"
)


class ChecksumInvalidoError(ValueError):
    """Indica que um arquivo bruto não corresponde ao manifesto SHA-256."""


def ler_manifesto_checksums(caminho_manifesto: Path = MANIFESTO_CHECKSUMS) -> dict[str, str]:
    """Retorna os hashes SHA-256 esperados, indexados pelo nome do arquivo."""
    hashes: dict[str, str] = {}
    for numero_linha, linha in enumerate(caminho_manifesto.read_text(encoding="utf-8").splitlines(), start=1):
        if not linha.strip():
            continue
        try:
            hash_esperado, nome_arquivo = linha.split(" *", maxsplit=1)
        except ValueError as erro:
            raise ValueError(f"Manifesto inválido na linha {numero_linha}: {linha!r}") from erro
        if len(hash_esperado) != 64 or any(caractere not in "0123456789abcdefABCDEF" for caractere in hash_esperado):
            raise ValueError(f"SHA-256 inválido na linha {numero_linha}.")
        hashes[nome_arquivo] = hash_esperado.upper()
    return hashes


def calcular_sha256(caminho: Path, tamanho_bloco: int = 1024 * 1024) -> str:
    """Calcula o SHA-256 de um arquivo sem carregá-lo inteiro na memória."""
    digest = sha256()
    with caminho.open("rb") as arquivo:
        while bloco := arquivo.read(tamanho_bloco):
            digest.update(bloco)
    return digest.hexdigest().upper()


def verificar_checksum(caminho: Path, caminho_manifesto: Path = MANIFESTO_CHECKSUMS) -> None:
    """Confirma que o arquivo existe e tem o SHA-256 registrado no manifesto."""
    caminho = Path(caminho)
    if not caminho.is_file():
        raise ChecksumInvalidoError(f"Arquivo não encontrado: {caminho}")
    hash_esperado = ler_manifesto_checksums(caminho_manifesto).get(caminho.name)
    if hash_esperado is None:
        raise ChecksumInvalidoError(f"Arquivo não registrado no manifesto: {caminho.name}")
    hash_atual = calcular_sha256(caminho)
    if hash_atual != hash_esperado:
        raise ChecksumInvalidoError(
            f"Checksum divergente para {caminho.name}. Esperado: {hash_esperado}; atual: {hash_atual}."
        )
    print(f"Checksum validado: {caminho.name}")


def carregar_matriz_67(caminho: Path = ARQUIVO_MIP_67) -> dict[str, pd.DataFrame]:
    """Valida e carrega as 15 abas da MIP 2015 de nível 67."""
    verificar_checksum(caminho)
    tabelas = pd.read_excel(caminho, sheet_name=None, header=None, engine="xlrd")
    return tabelas


def carregar_coeficientes_co2(
    caminho: Path = ARQUIVO_COEFICIENTES_CO2,
) -> pd.DataFrame:
    """Valida o SHA-256 e carrega as intensidades de CO₂ de Sanguinet e Azzoni.

    Retorna uma matriz de dimensão 67 × 2, com setores ``S1`` a ``S67`` no
    índice e anos 2011 e 2018 nas colunas. A unidade é Gg de CO₂ por R$ milhão
    de produção bruta, conforme a Tabela 2 do artigo.
    """
    verificar_checksum(caminho, MANIFESTO_COEFICIENTES_CO2)
    colunas_origem = [
        "coeficiente_2011_gg_co2_por_r_milhao",
        "coeficiente_2018_gg_co2_por_r_milhao",
    ]
    dados = pd.read_csv(caminho)

    colunas_ausentes = {"setor_id", *colunas_origem} - set(dados.columns)
    if colunas_ausentes:
        raise ValueError(f"Colunas ausentes no CSV de coeficientes: {colunas_ausentes}")

    setores_esperados = [f"S{i}" for i in range(1, 68)]
    matriz = dados.set_index("setor_id")[colunas_origem].copy()
    matriz.columns = pd.Index([2011, 2018], name="ano")

    if matriz.index.tolist() != setores_esperados:
        raise ValueError("O CSV deve conter exatamente os setores S1 a S67, nessa ordem.")
    if matriz.isna().any().any():
        raise ValueError("Há coeficientes de CO₂ ausentes no CSV.")

    return matriz


def carregar_intensidades_co2_exterior_representativo(
    caminho: Path = ARQUIVO_INTENSIDADES_CO2_EXTERIOR,
) -> pd.DataFrame:
    """Carrega intensidades de CO2 do exterior representativo (67 × anos).

    Os valores são parâmetros de cenário, documentados junto ao CSV; não são
    observações empíricas de uma MRIO mundial. O índice usa os códigos das 67
    atividades da MIP brasileira e as colunas são os anos das intensidades.
    """
    verificar_checksum(caminho, MANIFESTO_EXTERIOR)
    dados = pd.read_csv(caminho, dtype={"atividade": str})
    if "atividade" not in dados.columns:
        raise ValueError("O CSV do exterior deve conter a coluna 'atividade'.")
    matriz = dados.set_index("atividade").copy()
    try:
        matriz.columns = pd.Index([int(coluna) for coluna in matriz.columns], name="ano")
    except ValueError as erro:
        raise ValueError("As colunas de intensidade do exterior devem ser anos numéricos.") from erro
    matriz = matriz.apply(pd.to_numeric, errors="raise")
    if matriz.shape[0] != 67 or matriz.isna().any().any():
        raise ValueError("O CSV de intensidades do exterior deve conter 67 atividades sem valores ausentes.")
    return matriz


def carregar_inversa_leontief_exterior_representativo(
    caminho: Path = ARQUIVO_INVERSA_LEONTIEF_EXTERIOR,
) -> pd.DataFrame:
    """Carrega a inversa de Leontief (67 × 67) do exterior representativo."""
    verificar_checksum(caminho, MANIFESTO_EXTERIOR)
    dados = pd.read_csv(caminho, dtype={"atividade": str})
    if "atividade" not in dados.columns:
        raise ValueError("O CSV da inversa exterior deve conter a coluna 'atividade'.")
    matriz = dados.set_index("atividade")
    matriz.columns = matriz.columns.astype(str)
    matriz = matriz.apply(pd.to_numeric, errors="raise")
    if matriz.shape != (67, 67):
        raise ValueError("A inversa de Leontief exterior deve ter dimensão 67 × 67.")
    if not matriz.index.equals(matriz.columns):
        raise ValueError("Índice e colunas da inversa exterior devem ter as mesmas atividades na mesma ordem.")
    matriz.index.name = "atividade_origem"
    matriz.columns.name = "atividade_destino"
    return matriz
