"""Regionalização exploratória: VAB observado e perfis setoriais estimados."""
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
from urllib.request import urlopen

import numpy as np
from mip import PASTA, ler_p, ler_tecnologia, calcular_contas

GRUPOS = {"agropecuaria": "513", "industria": "517", "servicos": "6575", "administracao_publica": "525"}
IDS = [str(i) for i in range(42001, 42021)]
URL = ("https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2015/variaveis/513|517|6575|525"
       + "?localidades=N9[" + ",".join(IDS) + "]|N1[1]|N3[42]")


def grupo_atividade(atividade):
    """Correspondência agregada SCN → quatro grupos do PIB municipal, não CNAE detalhada."""
    if atividade in {"8400", "8591", "8691"}:
        return "administracao_publica"
    divisao = int(atividade[:2])
    if divisao <= 3:
        return "agropecuaria"
    if divisao <= 43:
        return "industria"
    return "servicos"


def carregar_vab():
    """Soma quatro componentes disjuntos do VAB publicado; mil reais → bilhões.

    Serviços (6575) excluem administração pública (525). VAB não inclui
    impostos líquidos sobre produtos, portanto não é o PIB.
    """
    arquivo = PASTA / "dados/sidra_vab_2015.json"
    fonte = json.loads((PASTA / "dados/regionalizacao_fontes.json").read_text(encoding="utf-8"))
    if hashlib.sha256(arquivo.read_bytes()).hexdigest() != fonte["sha256_resposta"]:
        raise ValueError("Dados de VAB divergem do manifesto.")
    componentes, nomes = {}, {}
    for variavel in json.loads(arquivo.read_text(encoding="utf-8")):
        if variavel["id"] in componentes or variavel["unidade"] != "Mil Reais":
            raise ValueError("Componente de VAB repetido ou unidade inesperada.")
        valores = {}
        for item in variavel["resultados"][0]["series"]:
            codigo = item["localidade"]["id"]
            if codigo in valores:
                raise ValueError("Localidade repetida no VAB.")
            valores[codigo] = float(item["serie"]["2015"])
            nomes[codigo] = item["localidade"]["nome"]
        if set(valores) != set(IDS + ["1", "42"]) or any(not np.isfinite(v) or v < 0 for v in valores.values()):
            raise ValueError("Localidades ou valores inválidos no VAB.")
        componentes[variavel["id"]] = valores
    if set(componentes) != set(GRUPOS.values()):
        raise ValueError("O VAB requer os quatro componentes esperados.")
    totais = {c: sum(v[c] for v in componentes.values()) for c in IDS + ["42"]}
    if not np.isclose(sum(totais[c] for c in IDS), totais["42"], rtol=1e-6, atol=80):
        raise ValueError("VAB das microrregiões não fecha com o total estadual.")
    nomes_malha = {r["properties"]["codigo_ibge"]: r["properties"]["microrregiao"] for r in
                   json.loads((PASTA / "dados/microrregioes_sc.geojson").read_text(encoding="utf-8"))["features"]}
    linhas = [{"codigo_ibge": c, "microrregiao": nomes_malha[c], "nome_sidra": nomes[c], "ano": 2015,
               **{f"vab_{g}_mil_reais": componentes[v][c] for g, v in GRUPOS.items()},
               "vab_total_mil_reais": totais[c], "vab_total_bilhoes_reais": totais[c]/1e6}
              for c in IDS]
    destino = PASTA / "dados/vab_microrregioes_2015.csv"
    with destino.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    return linhas


def produzir_pesos():
    dados = PASTA / "dados"
    fonte = dados / "sidra_vab_2015.json"
    manifesto_path = dados / "regionalizacao_fontes.json"
    # Downloads ficam congelados localmente, com hash; não atualizar séries silenciosamente.
    if not fonte.exists() or not manifesto_path.exists():
        with urlopen(URL, timeout=90) as resposta:
            conteudo = resposta.read()
        if conteudo.startswith(b"\x1f\x8b"):
            conteudo = gzip.decompress(conteudo)
        json.loads(conteudo)
        fonte.write_bytes(conteudo)
        manifesto = {"url": URL, "tabela": "IBGE SIDRA 5938", "ano": 2015,
                     "acesso_utc": datetime.now(timezone.utc).isoformat(),
                     "sha256_resposta": hashlib.sha256(conteudo).hexdigest(),
                     "metadados_url": "https://servicodados.ibge.gov.br/api/v3/agregados/5938/metadados",
                     "metodo": "peso r,i = VAB r,grupo(i) / VAB Brasil,grupo(i)",
                     "limite": "67 atividades recebem apenas quatro perfis espaciais; VAB nao e emissao nem demanda final."}
        manifesto_path.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    manifesto = json.loads(manifesto_path.read_text(encoding="utf-8"))
    if hashlib.sha256(fonte.read_bytes()).hexdigest() != manifesto["sha256_resposta"]:
        raise ValueError("Hash dos dados SIDRA divergente.")
    vab = {}
    for variavel in json.loads(fonte.read_text(encoding="utf-8")):
        if variavel["unidade"] != "Mil Reais":
            raise ValueError("Unidade de VAB inesperada.")
        serie = variavel["resultados"][0]["series"]
        valores = {}
        for item in serie:
            codigo = item["localidade"]["id"]
            if codigo in valores:
                raise ValueError("Localidade repetida na série SIDRA.")
            valor = float(item["serie"]["2015"])
            if not np.isfinite(valor) or valor < 0:
                raise ValueError("VAB ausente, suprimido ou inválido; não imputar zero.")
            valores[codigo] = valor
        if set(valores) != set(IDS + ["1", "42"]):
            raise ValueError("SIDRA precisa conter 20 microrregiões, SC e Brasil.")
        if not np.isclose(sum(valores[c] for c in IDS), valores["42"], rtol=1e-6, atol=20):
            raise ValueError("VAB das microrregiões não fecha com SC, além do arredondamento publicado.")
        if not 0 < valores["42"] <= valores["1"]:
            raise ValueError("Totais SC/Brasil inválidos.")
        vab[variavel["id"]] = valores
    if set(vab) != set(GRUPOS.values()):
        raise ValueError("Esperadas as quatro variáveis de VAB.")
    atividades, _ = ler_p()
    nomes = {f["properties"]["codigo_ibge"]: f["properties"]["microrregiao"] for f in
             json.loads((dados / "microrregioes_sc.geojson").read_text(encoding="utf-8"))["features"]}
    # O catálogo existente identifica precisamente cada código SCN usado em P.
    catalogo = dados / "setores_mip_2015.csv"
    if not catalogo.exists():
        with (PASTA.parent / "raw/manifesto.csv").open(encoding="utf-8") as arquivo:
            item = next(r for r in csv.DictReader(arquivo) if r["id"] == "setores_mip_2015")
        conteudo = (PASTA.parent / item["arquivo"]).read_bytes()
        if hashlib.sha256(conteudo).hexdigest().lower() != item["sha256"].lower():
            raise ValueError("Catálogo MIP diverge do manifesto original.")
        catalogo.write_bytes(conteudo)
    with catalogo.open(encoding="utf-8") as arquivo:
        descricoes = {r["atividade"]: r["descricao"] for r in csv.DictReader(arquivo)}
    if set(descricoes) != set(atividades):
        raise ValueError("Catálogo e matriz P não correspondem.")
    destino_base = dados / "pesos_vab_quatro_grupos_2015.csv"
    linhas = []
    for codigo in IDS:
        for atividade in atividades:
            grupo = grupo_atividade(atividade)
            v = vab[GRUPOS[grupo]]
            linhas.append({"codigo_ibge": codigo, "microrregiao": nomes[codigo], "atividade": atividade,
                           "descricao": descricoes[atividade], "grupo_vab": grupo, "variavel_sidra": GRUPOS[grupo],
                           "ano": 2015, "vab_micro_mil_reais": v[codigo], "vab_sc_mil_reais": v["42"],
                           "vab_brasil_mil_reais": v["1"], "peso_micro_brasil": v[codigo]/v["1"],
                           "peso_micro_sc": v[codigo]/v["42"], "peso_sc_brasil": v["42"]/v["1"]})
    with destino_base.open("w", encoding="utf-8", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)
    fatores, anotacoes = ler_fatores(atividades)
    base = np.array([[float(linhas[r*len(atividades)+i]["peso_micro_brasil"])
                      for i in range(len(atividades))] for r in range(20)])
    pesos = ajustar_distribuicao(base, fatores)
    participacao_sc = base.sum(axis=0)
    for r in range(20):
        for i, atividade in enumerate(atividades):
            linha = linhas[r*len(atividades)+i]
            linha["peso_micro_brasil_vab"] = linha["peso_micro_brasil"]
            linha["peso_micro_sc_vab"] = linha["peso_micro_sc"]
            linha["fator_setorial_estimado"] = fatores[r, i]
            linha["peso_micro_brasil"] = pesos[r, i]
            linha["peso_micro_sc"] = pesos[r, i] / participacao_sc[i]
            # Preserva exatamente a soma do cenário anterior (arredondamento SIDRA incluído).
            linha["peso_sc_brasil"] = participacao_sc[i]
            linha.update(anotacoes[atividade])
    destino = dados / "pesos_setores_microrregioes_2015.csv"
    with destino.open("w", encoding="utf-8", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)
    manifesto["sha256_pesos"] = hashlib.sha256(destino.read_bytes()).hexdigest()
    manifesto["sha256_catalogo"] = hashlib.sha256(catalogo.read_bytes()).hexdigest()
    manifesto["sha256_base_vab"] = hashlib.sha256(destino_base.read_bytes()).hexdigest()
    manifesto["sha256_fatores"] = hashlib.sha256((dados / "fatores_setoriais_estimados.csv").read_bytes()).hexdigest()
    manifesto["sha256_fontes_perfis"] = hashlib.sha256((dados / "fontes_perfis_setoriais.json").read_bytes()).hexdigest()
    manifesto["metodo"] = "w[r,i] = soma_r(b[r,i]) * b[r,i]*f[r,i] / soma_r(b[r,i]*f[r,i]); b=VAB micro/grupo Brasil; f=hipotese setorial"
    manifesto["limite"] = "67 perfis julgamentais, nao observados; escala SC/Brasil ainda por quatro grupos; fontes multitemporais; nao e estimativa estatistica de 2015"
    manifesto_path.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    return destino


def ler_fatores(atividades):
    """Lê todas as 1.340 hipóteses explicitamente; falta não significa fator neutro."""
    fonte = json.loads((PASTA / "dados/fontes_perfis_setoriais.json").read_text(encoding="utf-8"))["fontes"]
    with (PASTA / "dados/fatores_setoriais_estimados.csv").open(encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    if len(linhas) != len(atividades) or {r["atividade"] for r in linhas} != set(atividades):
        raise ValueError("Fatores devem conter cada atividade uma única vez.")
    por_atividade = {r["atividade"]: r for r in linhas}
    fatores = np.array([[float(por_atividade[a][c]) for a in atividades] for c in IDS])
    if not np.isfinite(fatores).all() or (fatores < 0).any() or (fatores.sum(axis=0) <= 0).any():
        raise ValueError("Fatores inválidos ou setor sem região elegível.")
    anotacoes = {}
    for a, r in por_atividade.items():
        ids = r["fontes_contexto"].split(";")
        if not all(i in fonte for i in ids) or not r["justificativa"]:
            raise ValueError("Hipótese sem justificativa ou com fonte desconhecida.")
        anotacoes[a] = {k: r[k] for k in ("natureza", "confianca_quantitativa", "fontes_contexto", "justificativa")}
        anotacoes[a]["urls_contexto"] = " ; ".join(fonte[i]["url"] for i in ids if fonte[i]["url"])
        anotacoes[a]["data_cenario"] = "2026-09-18"
    return fatores, anotacoes


def ajustar_distribuicao(base, fatores):
    """Muda a distribuição intraestadual, preservando o subtotal de cada atividade em SC."""
    if base.ndim != 2 or base.shape != fatores.shape:
        raise ValueError("Base e fatores precisam da mesma forma região × atividade.")
    if any(not np.isfinite(a).all() or (a < 0).any() for a in (base, fatores)):
        raise ValueError("Base e fatores precisam ser finitos e não negativos.")
    ajustada = base * fatores
    denominador = ajustada.sum(axis=0)
    if (denominador <= 0).any():
        raise ValueError("Setor sem massa para normalização.")
    return ajustada / denominador[None, :] * base.sum(axis=0)[None, :]


def ler_pesos(arquivo, atividades):
    """Lê o arquivo de pesos como entrada efetiva; não depende da ordem das linhas."""
    indice = {a: i for i, a in enumerate(atividades)}
    pesos = np.full((20, len(atividades)), np.nan)
    with arquivo.open(encoding="utf-8", newline="") as entrada:
        for linha in csv.DictReader(entrada):
            if linha["codigo_ibge"] not in IDS or linha["atividade"] not in indice:
                raise ValueError("Código territorial ou setorial desconhecido nos pesos.")
            r, i = IDS.index(linha["codigo_ibge"]), indice[linha["atividade"]]
            if np.isfinite(pesos[r, i]):
                raise ValueError("Par setor/microrregião duplicado.")
            pesos[r, i] = float(linha["peso_micro_brasil"])
    if not np.isfinite(pesos).all() or (pesos < 0).any() or (pesos > 1).any() or (pesos.sum(axis=0) > 1).any():
        raise ValueError("Pesos incompletos ou participações inválidas.")
    return pesos


def aplicar_pesos(diretas, totais, pesos):
    """Localiza a produção compradora; a cadeia fornecedora pode estar fora da região."""
    if diretas.ndim != 1 or totais.shape != diretas.shape or pesos.ndim != 2 or pesos.shape[1] != len(diretas):
        raise ValueError("Dimensões das contas e dos pesos incompatíveis.")
    if any(not np.isfinite(a).all() or (a < 0).any() for a in (diretas, totais, pesos)):
        raise ValueError("Contas e pesos devem ser finitos e não negativos.")
    if (totais < diretas - 1e-8).any():
        raise ValueError("Totais não podem ser menores que diretas.")
    return pesos * diretas[None, :], pesos * totais[None, :]


def regionalizar():
    atividades, gamma, x, l = ler_tecnologia()
    arquivo = PASTA / "dados/pesos_setores_microrregioes_2015.csv"
    if not arquivo.exists():
        produzir_pesos()
    manifesto = json.loads((PASTA / "dados/regionalizacao_fontes.json").read_text(encoding="utf-8"))
    if hashlib.sha256(arquivo.read_bytes()).hexdigest() != manifesto["sha256_pesos"]:
        raise ValueError("Pesos diferem do manifesto; revise sua proveniência.")
    for nome, chave in [("fatores_setoriais_estimados.csv", "sha256_fatores"),
                        ("fontes_perfis_setoriais.json", "sha256_fontes_perfis")]:
        if hashlib.sha256((PASTA / "dados" / nome).read_bytes()).hexdigest() != manifesto[chave]:
            raise ValueError("Hipóteses alteradas: execute regionalizacao.py para atualizar os pesos.")
    pesos = ler_pesos(arquivo, atividades)
    diretas, totais = aplicar_pesos(*calcular_contas(gamma, x, l), pesos)
    with arquivo.open(encoding="utf-8") as f:
        nomes = {r["codigo_ibge"]: r["microrregiao"] for r in csv.DictReader(f)}
    resultados = [{"codigo_ibge": c, "microrregiao": nomes[c], "emissoes_diretas": float(diretas[r].sum()),
                   "emissoes_insumos": float((totais[r]-diretas[r]).sum()),
                   "emissoes_totais": float(totais[r].sum())} for r, c in enumerate(IDS)]
    destino = PASTA / "dados/emissoes_mip_microrregioes_2015.csv"
    with destino.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(resultados[0]))
        w.writeheader()
        w.writerows(resultados)
    with (PASTA / "dados/mip_setores_microrregioes_2015.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["codigo_ibge", "microrregiao", "atividade", "producao_estimada_r_milhao", "diretas_gg_co2", "insumos_gg_co2", "totais_gg_co2"])
        w.writerows((c, nomes[c], a, pesos[r, i]*x[i], diretas[r, i], totais[r, i]-diretas[r, i], totais[r, i])
                    for r, c in enumerate(IDS) for i, a in enumerate(atividades))
    print(f"Regionalização: {len(resultados)} regiões × {len(atividades)} atividades; perfis setoriais estimados.")
    print(f"Totais SC aproximados: diretas {diretas.sum():.2f}; totais da cadeia nacional {totais.sum():.2f} Gg CO2.")
    return resultados


def comparar_sensibilidade():
    """Varia a força dos fatores, mantendo a escala estadual; não estima incerteza estatística."""
    atividades, gamma, x, l = ler_tecnologia()
    fatores, _ = ler_fatores(atividades)
    base = ler_pesos(PASTA / "dados/pesos_vab_quatro_grupos_2015.csv", atividades)
    d, t = calcular_contas(gamma, x, l)
    d0, t0 = base @ d, base @ t
    with (PASTA / "dados/pesos_setores_microrregioes_2015.csv").open(encoding="utf-8") as f:
        nomes = {r["codigo_ibge"]: r["microrregiao"] for r in csv.DictReader(f)}
    linhas = []
    for expoente in (0., .5, 1., 1.5):
        pesos = ajustar_distribuicao(base, fatores ** expoente)
        diretas, totais = pesos @ d, pesos @ t
        for r, codigo in enumerate(IDS):
            linhas.append({"expoente_fator": expoente, "codigo_ibge": codigo, "microrregiao": nomes[codigo],
                           "diretas_gg_co2": diretas[r], "totais_gg_co2": totais[r],
                           "variacao_diretas_vs_vab_pct": 100*(diretas[r]/d0[r]-1),
                           "variacao_totais_vs_vab_pct": 100*(totais[r]/t0[r]-1)})
    with (PASTA / "dados/sensibilidade_perfis_setoriais.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)


if __name__ == "__main__":
    produzir_pesos()
    regionalizar()
    comparar_sensibilidade()
