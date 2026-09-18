"""Cinco mapas: NO₂, emissões diretas e dos insumos e VAB microrregional."""
import argparse
import csv
import json
import hashlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from shapely.geometry import shape, box
from shapely.ops import unary_union
from shapely.plotting import patch_from_polygon

from satelite import PASTA, adquirir_recorte, agregar_regioes
from territorio import carregar_terra
from mip import exportar_totais
from regionalizacao import regionalizar, carregar_vab
from mapas import desenhar_mapa, normalizar


def registrar_entradas(ano):
    """Inventário distingue fontes da P e entradas diretamente lidas pelo painel."""
    dados = PASTA / "dados"
    mip = json.loads((dados / "mip_fontes.json").read_text(encoding="utf-8"))
    registros = []
    for r in mip["entradas_da_analise_original"]:
        registros.append({"categoria": "MIP" if r["id"].startswith("mip_") else "coeficientes_CO2",
                          "arquivo": "../" + r["arquivo"], "ano": r["ano"], "fonte": r["fonte"],
                          "sha256": r["sha256"].lower(), "papel": "entrada da analise original que gerou P"})
    for categoria, nome, periodo, fonte, papel in [
        ("P", "matriz_p_nacional_2015.csv", 2015, "analise_matriz_insumo_produto.ipynb", "emissoes nacionais 67 x 67"),
        ("tecnologia", "tecnologia_nacional_2015.npz", 2015, "MIP IBGE / coeficientes Sanguinet e Azzoni", "gamma, producao bruta x e L nacional; diretas=gamma*x; totais=(gamma@L)*x"),
        ("catalogo", "setores_mip_2015.csv", 2015, "analise MIP / IBGE", "identifica codigos das 67 atividades"),
        ("satelite", f"no2_fmi_{ano}_sc.npz", ano, "TROPOMI/Copernicus - FMI/SAMPO", "coluna NO2 anual; grade 0.05 grau"),
        ("base_pesos", "sidra_vab_2015.json", 2015, "IBGE SIDRA 5938", "VAB observado; ancora da escala e base dos pesos"),
        ("vab_microrregional", "vab_microrregioes_2015.csv", 2015, "IBGE SIDRA 5938", "soma dos quatro componentes do VAB; painel E; bilhoes de reais correntes"),
        ("pesos_microregioes", "pesos_setores_microrregioes_2015.csv", 2015, "regionalizacao.py / SIDRA 5938", "VAB ajustado por hipotese setorial; 1340 pares"),
        ("hipoteses_setoriais", "fatores_setoriais_estimados.csv", "cenario 2026; base 2015", "julgamento informado por pesquisa online", "67 atividades x 20 fatores; numeros estimados"),
        ("fontes_hipoteses", "fontes_perfis_setoriais.json", "multitemporal", "FIESC; ACATE; BMW; fontes locais; Wikipedia", "URLs e evidencias qualitativas, nao fatores medidos"),
        ("base_comparacao", "pesos_vab_quatro_grupos_2015.csv", 2015, "SIDRA 5938", "cenario anterior sem ajuste setorial"),
        ("limites", "microrregioes_sc.geojson", "recorte historico", "IBGE API malhas", "limites administrativos originais"),
        ("terra", "microrregioes_sc_terra.geojson", "GSHHG 2.3.7", "IBGE intersecao GSHHG", "exclusao de agua cartografada"),
    ]:
        registros.append({"categoria": categoria, "arquivo": "dados/"+nome, "ano": periodo, "fonte": fonte,
                          "sha256": hashlib.sha256((dados/nome).read_bytes()).hexdigest(), "papel": papel})
    with (dados / "entradas.csv").open("w", encoding="utf-8", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(registros[0]))
        writer.writeheader()
        writer.writerows(registros)


def gerar_painel(ano=2023, paleta_co2="viridis"):
    if paleta_co2 not in {"verde", "viridis", "cividis", "inferno", "magma", "plasma"}:
        raise ValueError("Paleta de CO₂ desconhecida.")
    sufixo = "" if paleta_co2 == "verde" else f"_{paleta_co2}"
    regioes = carregar_terra()
    poligonos = [shape(r["geometry"]) for r in regioes]
    terra = unary_union(poligonos)
    recorte = adquirir_recorte(ano)
    with np.load(recorte) as grade:
        lat, lon = grade["latitude"], grade["longitude"]
        valores, pesos = grade["no2_pmolec_cm2"], grade["peso_harp"]
        resultados = agregar_regioes(regioes, lat, lon, valores, pesos)
    matriz = exportar_totais()
    mip = regionalizar()
    vab = carregar_vab()
    vab_por_codigo = {r["codigo_ibge"]: r["vab_total_bilhoes_reais"] for r in vab}
    norma_vab = Normalize(0, max(vab_por_codigo.values()) or 1)
    contas = ["emissoes_diretas", "emissoes_insumos"]
    # Uma mesma emissão deve receber exatamente a mesma cor em C e D.
    paleta_mip = LinearSegmentedColormap.from_list("co2", ["#f3f4ef", "#a4c5c0", "#518d89", "#205451"])
    if paleta_co2 != "verde":
        paleta_mip = plt.get_cmap(f"{paleta_co2}_r")
    norma_mip = Normalize(0, max(r[c] for r in mip for c in contas) or 1)
    mip_por_codigo = {r["codigo_ibge"]: r for r in mip}
    participa = np.array([[terra.intersection(box(x-.025, y-.025, x+.025, y+.025)).area > 0
                           for x in lon] for y in lat])
    validos = participa & np.isfinite(valores) & np.isfinite(pesos) & (pesos > 0)
    # Contraste relativo ao recorte observado, sem inferir um fundo natural ou limite sanitário.
    minimo_no2 = float(valores[validos].min())
    maximo_no2 = float(valores[validos].max())
    norma = Normalize(minimo_no2, maximo_no2 if maximo_no2 > minimo_no2 else minimo_no2 + 1e-12)
    cmap = paleta_mip.copy()
    cmap.set_bad("#d9d9d9")
    fig, eixos = plt.subplots(3, 2, figsize=(15, 20))
    fig.subplots_adjust(left=.04, right=.96, top=.88, bottom=.12, hspace=.40, wspace=.10)
    imagem = eixos[0, 0].pcolormesh(np.r_[lon-.025, lon[-1]+.025], np.r_[lat-.025, lat[-1]+.025],
                                   np.ma.array(valores, mask=~validos), cmap=cmap, norm=norma,
                                   shading="flat", edgecolors=(0, 0, 0, .1), linewidth=.1)
    imagem.set_clip_path(patch_from_polygon(terra, transform=eixos[0, 0].transData))
    medias = {r["codigo_ibge"]: r["no2_pmolec_cm2"] for r in resultados}
    for r, poligono in zip(regioes, poligonos):
        valor_vab = vab_por_codigo[r["properties"]["codigo_ibge"]]
        eixos[2, 0].add_patch(patch_from_polygon(poligono, facecolor=paleta_mip(norma_vab(valor_vab)),
                                                edgecolor="#697586", linewidth=.4))
        valor = medias[r["properties"]["codigo_ibge"]]
        eixos[0, 0].add_patch(patch_from_polygon(poligono, facecolor="none", edgecolor="#334155", linewidth=.4))
        eixos[0, 1].add_patch(patch_from_polygon(poligono, facecolor=cmap(norma(valor)) if np.isfinite(valor) else "#d9d9d9",
                                              edgecolor="#334155", linewidth=.4))
        for i, ax in enumerate(eixos[1]):
            valor_mip = mip_por_codigo[r["properties"]["codigo_ibge"]][contas[i]]
            ax.add_patch(patch_from_polygon(poligono, facecolor=paleta_mip(norma_mip(valor_mip)),
                                           edgecolor="#697586", linewidth=.4))
    titulos = ["A  NO₂ troposférico observado por satélite", "B  NO₂ troposférico por microrregião",
               "C  Emissões diretas de CO₂", "D  Emissões de CO₂ dos insumos encadeados",
               "E  Valor adicionado bruto por microrregião"]
    subtitulos = [f"Composição anual de {ano} · células de 0,05° × 0,05°",
                  f"Média ponderada pela área terrestre · {ano}",
                  "Produção das atividades da microrregião · base 2015",
                  "Cadeia nacional fornecedora · sem emissões próprias · base 2015",
                  "VAB total · valores correntes de 2015 · IBGE"]
    xmin, ymin, xmax, ymax = terra.bounds
    for ax, titulo, subtitulo in zip(eixos.flat, titulos, subtitulos):
        ax.set(xlim=(xmin-.10, xmax+.10), ylim=(ymin-.1, ymax+.1))
        ax.set_aspect(1 / np.cos(np.deg2rad(27)))
        ax.set_axis_off()
        ax.set_title(titulo, loc="left", fontsize=13, fontweight="normal", pad=30)
        ax.text(0, 1.015, subtitulo, transform=ax.transAxes, fontsize=10, color="#475569", va="bottom")
    fig.suptitle("Santa Catarina: NO₂, emissões de CO₂ e atividade econômica", fontsize=20, y=.975)
    fig.text(.5, .950, f"NO₂ observado por satélite ({ano}) · emissões estimadas e VAB regional (base 2015)",
             ha="center", fontsize=12, color="#475569")
    barra = fig.add_axes([.34, .655, .32, .008])
    fig.colorbar(plt.cm.ScalarMappable(norm=norma, cmap=cmap), cax=barra, orientation="horizontal",
                 label="Coluna de NO₂ (10¹⁵ moléculas/cm²) · intervalo observado, comum a A e B")
    fig.text(.5, .670, f"Mínimo: {minimo_no2:.3f} · máximo: {maximo_no2:.3f} · cores não indicam limites de qualidade do ar",
             ha="center", fontsize=8, color="#64748b")
    barra_mip = fig.add_axes([.34, .375, .32, .008])
    fig.colorbar(plt.cm.ScalarMappable(norm=norma_mip, cmap=paleta_mip), cax=barra_mip,
                 orientation="horizontal", label="Emissões estimadas (Gg de CO₂) · escala comum a C e D")
    barra_vab = fig.add_axes([.11, .095, .29, .008])
    fig.colorbar(plt.cm.ScalarMappable(norm=norma_vab, cmap=paleta_mip), cax=barra_vab,
                 orientation="horizontal", label="VAB (R$ bilhões, a preços correntes de 2015)")
    notas = eixos[2, 1]
    notas.set_axis_off()
    notas.text(0, 1.06, "INTERPRETAÇÃO E ALCANCE", transform=notas.transAxes,
               fontsize=11, fontweight="bold", color="#334155")
    notas.text(0, .98,
               "A–B  Coluna troposférica de NO₂; médias regionais ponderadas\n"
               "pela área terrestre. Não é concentração ao nível do solo.\n\n"
               "C–D  Emissões próprias e dos insumos, respectivamente.\n"
               "A cadeia fornecedora nacional é atribuída à região compradora.\n"
               "São estimativas para 67 atividades, com pesos regionais\n"
               "exploratórios. Emissões ocorridas no exterior são excluídas.\n"
               "A soma das pegadas não é um inventário territorial, pois\n"
               "há sobreposições entre atividades (1 Gg = 1.000 t).\n\n"
               "E  VAB publicado pelo IBGE, somado em quatro componentes,\n"
               "sem os impostos líquidos sobre produtos que integram o PIB.\n"
               "É a base econômica dos pesos; não é validação independente.\n\n"
               "Leitura  Tons escuros indicam valores maiores. A–B e C–D\n"
               "compartilham suas respectivas escalas; E tem escala própria.\n"
               "As grandezas e os períodos diferem: a comparação é descritiva.\n"
               "Recorte: 20 microrregiões históricas de Santa Catarina.",
               transform=notas.transAxes, va="top", fontsize=10, linespacing=1.45, color="#334155")
    fig.text(.04, .028,
             "Fontes: TROPOMI/FMI; IBGE (MIP, VAB e limites); Sanguinet e Azzoni (coeficientes de CO₂); GSHHG (terra emersa).\n"
             "Elaboração própria. Pesos setoriais estimados em 2026 com fontes de diferentes anos; não representam observações setoriais de 2015.",
             fontsize=9, linespacing=1.5, color="#64748b")
    pasta = PASTA / "figuras"
    pasta.mkdir(exist_ok=True)
    for extensao in ("svg", "png"):
        fig.savefig(pasta / f"painel_cinco_mapas_{ano}{sufixo}.{extensao}", dpi=160, facecolor="white",
                    metadata={"Date": None} if extensao == "svg" else None)
    plt.close(fig)
    desenhar_mapa(regioes, {normalizar(r["microrregiao"]): r["vab_total_bilhoes_reais"] for r in vab},
                  pasta / f"vab_microrregioes_2015{sufixo}.svg", "Valor adicionado bruto por microrregião · 2015",
                  "R$ bilhões", "IBGE/SIDRA 5938 · quatro componentes do VAB · valores correntes de 2015",
                  norma_vab, paleta=paleta_mip)
    for i, titulo in enumerate(("CO₂ direto • aproximação regional • 2015", "CO₂ dos insumos encadeados • cadeia nacional • 2015")):
        desenhar_mapa(regioes, {normalizar(r["microrregiao"]): r[contas[i]] for r in mip},
                      pasta / f"{contas[i]}_mip_2015{sufixo}.svg", titulo, "Gg de CO₂",
                      "MIP Brasil 2015 × pesos setoriais estimados • cenário exploratório\n"
                      + ("Emissões do setor emissor; soma das linhas de P." if i == 0 else
                         "Somente insumos nacionais: (gamma @ (L − I)) × x; exclui emissões próprias."),
                      norma_mip, paleta=paleta_mip)
    fontes = {"ano_no2": ano, "ano_mip": 2015, "status_mip_regional": "cenario_julgamental_67_atividades_ancorado_vab",
              "contas": "C: diretas=gamma*x; D: insumos=(gamma@(L-I))*x; cadeia nacional; pegadas sobrepostas",
              "colunas_mapas": contas,
              "escala_no2": {"comum_a": ["A", "B"], "minimo": norma.vmin, "maximo": norma.vmax, "paleta": cmap.name,
                             "normalizacao": "linear entre minimo e maximo das celulas validas com intersecao terrestre em SC",
                             "interpretacao": "contraste espacial relativo; nao representa fundo natural nem limite sanitario; dados originais preservados"},
              "escala_vab": {"painel": "E", "minimo": norma_vab.vmin, "maximo": norma_vab.vmax,
                             "unidade": "bilhoes de reais correntes de 2015", "paleta": paleta_mip.name},
              "sha256_vab": hashlib.sha256((PASTA / "dados/vab_microrregioes_2015.csv").read_bytes()).hexdigest(),
              "sha256_fonte_vab": hashlib.sha256((PASTA / "dados/sidra_vab_2015.json").read_bytes()).hexdigest(),
              "escala_co2": {"comum_a": ["C", "D"], "minimo": norma_mip.vmin, "maximo": norma_mip.vmax,
                             "paleta": paleta_co2 if paleta_co2 == "verde" else f"{paleta_co2}_r",
                             "rgba_amostras": paleta_mip(np.linspace(0, 1, 5)).tolist()},
              "sha256_tecnologia": hashlib.sha256((PASTA / "dados/tecnologia_nacional_2015.npz").read_bytes()).hexdigest(),
              "sha256_fatores": hashlib.sha256((PASTA / "dados/fatores_setoriais_estimados.csv").read_bytes()).hexdigest(),
              "sha256_fontes_perfis": hashlib.sha256((PASTA / "dados/fontes_perfis_setoriais.json").read_bytes()).hexdigest(),
              "sha256_pesos": hashlib.sha256((PASTA / "dados/pesos_setores_microrregioes_2015.csv").read_bytes()).hexdigest(),
              "sha256_mip_regional": hashlib.sha256((PASTA / "dados/emissoes_mip_microrregioes_2015.csv").read_bytes()).hexdigest(),
              "total_p_gg_co2": float(matriz.sum()),
              "sha256_terra": hashlib.sha256((PASTA / "dados/microrregioes_sc_terra.geojson").read_bytes()).hexdigest(),
              "sha256_recorte_no2": hashlib.sha256(recorte.read_bytes()).hexdigest(),
              "sha256_p": hashlib.sha256((PASTA / "dados/matriz_p_nacional_2015.csv").read_bytes()).hexdigest()}
    (PASTA / f"dados/painel_cinco_mapas_fontes{sufixo}.json").write_text(json.dumps(fontes, indent=2), encoding="utf-8")
    registrar_entradas(ano)
    print("Painel gerado: NO2, CO2 com perfis setoriais estimados e VAB do IBGE.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ano", type=int, default=2023)
    parser.add_argument("--paleta", "--paleta-co2", dest="paleta_co2", choices=("verde", "viridis", "cividis", "inferno", "magma", "plasma"), default="viridis")
    args = parser.parse_args()
    gerar_painel(args.ano, args.paleta_co2)
