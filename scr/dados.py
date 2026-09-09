"""Leitura e verificação dos dados brutos da MIP."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import numpy as np
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


def carregar_matriz_67(caminho: Path = ARQUIVO_MIP_67) -> dict[str, pd.DataFrame]:
    """Valida e carrega as 15 abas da MIP 2015 de nível 67."""
    verificar_checksum(caminho)
    return pd.read_excel(caminho, sheet_name=None, header=None, engine="xlrd")


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


def carregar_matriz_participacao_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
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


def calcular_coeficientes_tecnicos_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calcula A = D @ Bn a partir das Tabelas 13 e 11 da MIP.

    A conversão produto × atividade para atividade × atividade segue a
    composição publicada pelo IBGE na Tabela 14 (D.Bn).
    """
    matriz_bn = carregar_matriz_bn_67(tabelas)
    matriz_d = carregar_matriz_participacao_67(tabelas)
    if not matriz_d.columns.equals(matriz_bn.index):
        raise ValueError("Os produtos das matrizes D e Bn não estão alinhados.")

    matriz_a = matriz_d @ matriz_bn
    matriz_a.index.name = "atividade_origem"
    matriz_a.columns.name = "atividade_destino"
    return matriz_a


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


def carregar_matriz_producao_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai V, a produção nacional por produto (linhas) e atividade (colunas)."""
    try:
        return _extrair_produto_atividade_67(tabelas["01"], 7, 74)
    except KeyError as erro:
        raise ValueError("A Tabela 01 não foi encontrada no arquivo da MIP.") from erro


def carregar_matriz_uso_nacional_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai U, os usos intermediários nacionais por produto e atividade."""
    try:
        return _extrair_produto_atividade_67(tabelas["03"], 3, 70)
    except KeyError as erro:
        raise ValueError("A Tabela 03 não foi encontrada no arquivo da MIP.") from erro


def calcular_matriz_transacoes_intersetoriais_67(
    tabelas: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Calcula Z = D @ U, a matriz de fluxos intersetoriais nacionais."""
    matriz_d = carregar_matriz_participacao_67(tabelas)
    matriz_u = carregar_matriz_uso_nacional_67(tabelas)
    if not matriz_d.columns.equals(matriz_u.index):
        raise ValueError("Os produtos das matrizes D e U não estão alinhados.")

    matriz_z = matriz_d @ matriz_u
    matriz_z.index.name = "atividade_origem"
    matriz_z.columns.name = "atividade_destino"
    return matriz_z


def calcular_producao_bruta_67(tabelas: dict[str, pd.DataFrame]) -> pd.Series:
    """Calcula x, o vetor de produção bruta das 67 atividades."""
    matriz_v = carregar_matriz_producao_67(tabelas)
    producao_bruta = matriz_v.sum(axis=0)
    producao_bruta.name = "producao_bruta"
    producao_bruta.index.name = "atividade"
    if (producao_bruta <= 0).any():
        raise ValueError("A produção bruta deve ser positiva para todas as atividades.")
    return producao_bruta


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
    matriz_d = carregar_matriz_participacao_67(tabelas)
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
    matriz_d = carregar_matriz_participacao_67(tabelas)
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


def calcular_coeficientes_importados_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calcula Am = D @ Bm, os insumos importados por atividade.

    Am é expresso na classificação atividade × atividade e permite calcular os
    insumos importados induzidos pela produção nacional.
    """
    matriz_d = carregar_matriz_participacao_67(tabelas)
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


def carregar_inversa_leontief_ibge_67(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Extrai a Matriz de Leontief divulgada pelo IBGE na Tabela 15."""
    try:
        return _extrair_matriz_atividade_67(tabelas["15"])
    except KeyError as erro:
        raise ValueError("A Tabela 15 não foi encontrada no arquivo da MIP.") from erro


def carregar_coeficientes_co2(
    caminho: Path = ARQUIVO_COEFICIENTES_CO2,
) -> pd.DataFrame:
    """Carrega a matriz de intensidades diretas de CO₂ do Sanguinet e Azzoni.

    Retorna uma matriz de dimensão 67 × 2, com setores ``S1`` a ``S67`` no
    índice e anos 2011 e 2018 nas colunas. A unidade é Gg de CO₂ por R$ milhão
    de produção bruta, conforme a Tabela 2 do artigo.
    """
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
