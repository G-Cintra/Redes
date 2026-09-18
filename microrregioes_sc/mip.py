"""Importa P da análise existente e explicita seus totais setoriais nacionais."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

PASTA = Path(__file__).resolve().parent


def importar_p():
    raiz = PASTA.parent
    with (raiz / "raw/manifesto.csv").open(encoding="utf-8", newline="") as arquivo:
        entradas = list(csv.DictReader(arquivo))
    fonte = next(r for r in entradas if r["id"] == "matriz_emissoes_producao_2015")
    origens = [r for r in entradas if r["id"] in {"mip_ibge_2015_67", "sanguinet_azzoni_2011", "sanguinet_azzoni_2018"}]
    for origem in origens:
        if hashlib.sha256((raiz / origem["arquivo"]).read_bytes()).hexdigest().lower() != origem["sha256"].lower():
            raise ValueError("Entrada original da MIP diverge do manifesto: " + origem["arquivo"])
    conteudo = (raiz / fonte["arquivo"]).read_bytes()
    digest = hashlib.sha256(conteudo).hexdigest()
    if digest.lower() != fonte["sha256"].lower():
        raise ValueError("P não corresponde ao hash declarado no manifesto da análise MIP.")
    (PASTA / "dados/matriz_p_nacional_2015.csv").write_bytes(conteudo)
    manifesto = PASTA / "dados/mip_fontes.json"
    anterior = json.loads(manifesto.read_text(encoding="utf-8")) if manifesto.exists() else {}
    tecnologia = {k: anterior[k] for k in ("sha256_tecnologia", "tecnologia", "contas_mapas") if k in anterior}
    manifesto.write_text(json.dumps({
        **tecnologia,
        "origem": fonte, "sha256": digest, "escopo": "Brasil, 67 atividades, 2015",
        "entradas_da_analise_original": origens,
        "coeficientes_2015": "interpolacao linear gamma_2011 + (4/7)*(gamma_2018-gamma_2011), conforme notebook MIP",
        "diretas": "soma das linhas de P, incluindo diagonal",
        "demanda_final": "soma das colunas de P, incluindo emissões diretas e indiretas",
        "regionalizacao": "P nacional; pesos externos de VAB são aplicados em regionalizacao.py"
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def ler_p():
    arquivo = PASTA / "dados/matriz_p_nacional_2015.csv"
    if not arquivo.exists():
        importar_p()
    manifesto = json.loads((PASTA / "dados/mip_fontes.json").read_text(encoding="utf-8"))
    if hashlib.sha256(arquivo.read_bytes()).hexdigest() != manifesto["sha256"]:
        raise ValueError("Hash da cópia de P divergente.")
    with arquivo.open(encoding="utf-8", newline="") as entrada:
        linhas = list(csv.reader(entrada))
    atividades = linhas[0][1:]
    if [r[0] for r in linhas[1:]] != atividades or len(set(atividades)) != 67:
        raise ValueError("P deve conter as mesmas 67 atividades únicas nos dois eixos.")
    matriz = np.array([r[1:] for r in linhas[1:]], dtype=float)
    if matriz.shape != (67, 67) or not np.isfinite(matriz).all() or (matriz < 0).any():
        raise ValueError("Valores inválidos na matriz P.")
    return atividades, matriz


def exportar_totais():
    atividades, matriz = ler_p()
    _, gamma, x, l = ler_tecnologia()
    diretas, totais = calcular_contas(gamma, x, l)
    destino = PASTA / "dados/mip_totais_setoriais_2015.csv"
    with destino.open("w", encoding="utf-8", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["atividade", "emissoes_diretas_gg_co2", "emissoes_insumos_gg_co2", "emissoes_totais_gg_co2"])
        writer.writerows(zip(atividades, diretas, totais-diretas, totais))
    print("P importada: 67 atividades nacionais; pesos regionais tratados separadamente.")
    return matriz


def importar_tecnologia():
    """Congela x, gamma e L das mesmas fontes da análise original, sem executar notebook."""
    import sys
    sys.path.insert(0, str(PASTA.parent))
    from redes import dados, modelo
    tabelas = dados.carregar_matriz_67("mip_ibge_2015_67")
    x = modelo.calcular_producao_bruta_67(tabelas)
    l = modelo.calcular_inversa_leontief(modelo.calcular_coeficientes_tecnicos_67(tabelas))
    g11 = dados.carregar_coeficientes_co2("sanguinet_azzoni_2011")[2011].to_numpy()
    g18 = dados.carregar_coeficientes_co2("sanguinet_azzoni_2018")[2018].to_numpy()
    gamma = g11 + (4/7)*(g18-g11)
    atividades, p = ler_p()
    if x.index.tolist() != atividades or l.index.tolist() != atividades:
        raise ValueError("Tecnologia e P têm atividades desalinhadas.")
    np.testing.assert_allclose(gamma*x.to_numpy(), p.sum(axis=1), rtol=1e-10, atol=1e-8)
    arquivo = PASTA / "dados/tecnologia_nacional_2015.npz"
    np.savez_compressed(arquivo, atividades=np.array(atividades), gamma=gamma, x=x.to_numpy(), l=l.to_numpy())
    manifesto = PASTA / "dados/mip_fontes.json"
    fonte = json.loads(manifesto.read_text(encoding="utf-8"))
    fonte["sha256_tecnologia"] = hashlib.sha256(arquivo.read_bytes()).hexdigest()
    fonte["tecnologia"] = "x: tabela 01; A=D@Bn: tabelas 13 e 11; L=inv(I-A); gamma interpolado 2011/2018"
    fonte["contas_mapas"] = "diretas=gamma*x; totais=(gamma@L)*x; insumos=totais-diretas; cadeia nacional, sem emissoes externas"
    manifesto.write_text(json.dumps(fonte, ensure_ascii=False, indent=2), encoding="utf-8")


def ler_tecnologia():
    arquivo = PASTA / "dados/tecnologia_nacional_2015.npz"
    if not arquivo.exists():
        importar_tecnologia()
    fonte = json.loads((PASTA / "dados/mip_fontes.json").read_text(encoding="utf-8"))
    if hashlib.sha256(arquivo.read_bytes()).hexdigest() != fonte["sha256_tecnologia"]:
        raise ValueError("Tecnologia difere do manifesto.")
    atividades, p = ler_p()
    with np.load(arquivo, allow_pickle=False) as dados:
        if dados["atividades"].tolist() != atividades:
            raise ValueError("Tecnologia desalinhada com P.")
        gamma, x, l = dados["gamma"], dados["x"], dados["l"]
    diretas, _ = calcular_contas(gamma, x, l)
    np.testing.assert_allclose(diretas, p.sum(axis=1), rtol=1e-10, atol=1e-8)
    return atividades, gamma, x, l


def calcular_contas(gamma, x, l):
    """Pegadas da produção bruta de cada atividade; totais não são inventário territorial.

    D_j=gamma_j*x_j; T_j=(gamma@L)_j*x_j;
    I_j=(gamma@(L-I))_j*x_j. As pegadas se sobrepõem entre atividades.
    L contém apenas os encadeamentos nacionais da MIP.
    """
    n = len(gamma)
    if gamma.shape != (n,) or x.shape != (n,) or l.shape != (n, n):
        raise ValueError("Dimensões de gamma, x e L incompatíveis.")
    if any(not np.isfinite(a).all() or (a < 0).any() for a in (gamma, x, l)):
        raise ValueError("Gamma, x e L devem ser finitos e não negativos.")
    if (l - np.eye(n) < -1e-10).any():
        raise ValueError("L deve incluir a produção própria e requisitos não negativos.")
    return gamma*x, (gamma@l)*x


if __name__ == "__main__":
    importar_p()
    exportar_totais()
