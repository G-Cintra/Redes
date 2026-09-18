"""TROPOMI/FMI: download anual, recorte de SC e média por microrregião."""
import argparse
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import shutil
from urllib.request import urlopen

import numpy as np
from netCDF4 import Dataset, num2date
from pyproj import Transformer
from shapely.geometry import box, shape
from shapely.ops import transform
from shapely.ops import unary_union
from shapely.plotting import patch_from_polygon
from matplotlib.colors import Normalize

from mapas import PASTA, desenhar_mapa, normalizar
import matplotlib.pyplot as plt
from territorio import carregar_terra

BANDA = "tropospheric_NO2_column_number_density"
AVOGADRO = 6.02214076e23
# Projeção equivalente local: as interseções são ponderadas em m², não graus².
PROJECAO = "+proj=laea +lat_0=-27 +lon_0=-51 +datum=WGS84 +units=m +no_defs"


def adquirir_recorte(ano):
    """Mantém um recorte pequeno e metadados; o produto global fica só no cache."""
    if not 2019 <= ano < datetime.now(timezone.utc).year:
        raise ValueError("Escolha um ano completo desde 2019, anterior ao ano corrente.")
    dados = PASTA / "dados"
    recorte = dados / f"no2_fmi_{ano}_sc.npz"
    manifesto = dados / f"no2_fmi_{ano}_fontes.json"
    if recorte.exists() and manifesto.exists():
        esperado = json.loads(manifesto.read_text(encoding="utf-8"))["sha256_recorte"]
        if hashlib.sha256(recorte.read_bytes()).hexdigest() != esperado:
            raise ValueError("Hash do recorte difere do manifesto; verifique os arquivos.")
        return recorte
    cache = dados / "cache_satelite"
    cache.mkdir(exist_ok=True)
    nome = f"S5P_OFFL_L3_NO2_yearlycomposite_{ano}.nc.gz"
    url = "https://tropomi-no2-l3.data.lit.fmi.fi/" + nome
    compactado = cache / nome
    if not compactado.exists():
        print("Baixando produto global FMI (~475 MB):", url, flush=True)
        temporario = compactado.with_suffix(".part")
        with urlopen(url, timeout=120) as origem, temporario.open("wb") as saida:
            shutil.copyfileobj(origem, saida)
        temporario.replace(compactado)
    with compactado.open("rb") as arquivo:
        hash_fonte = hashlib.file_digest(arquivo, "sha256").hexdigest()
    nc_path = compactado.with_suffix("")
    if not nc_path.exists():
        temporario = nc_path.with_suffix(".part")
        with gzip.open(compactado, "rb") as origem, temporario.open("wb") as saida:
            shutil.copyfileobj(origem, saida)
        temporario.replace(nc_path)
    with Dataset(nc_path) as nc:
        if nc[BANDA].units != "Pmolec/cm2":
            raise ValueError(f"Unidade inesperada: {nc[BANDA].units}")
        lat, lon = np.asarray(nc["latitude"][:]), np.asarray(nc["longitude"][:])
        # Uma margem além dos limites de SC garante células de borda completas.
        iy = np.flatnonzero((lat >= -30) & (lat <= -25))
        ix = np.flatnonzero((lon >= -54) & (lon <= -48))
        if not len(ix) or not len(iy):
            raise ValueError("Grade não cobre o recorte esperado em longitude/latitude.")
        if not (np.allclose(np.diff(lat), 0.05, atol=1e-5) and np.allclose(np.diff(lon), 0.05, atol=2e-5)):
            raise ValueError("Resolução ou orientação diferente de 0,05 grau; revise o recorte.")
        # Centros float32 têm arredondamento; reconstruímos as bordas na grade nominal.
        lat = np.round(lat[iy].astype(float), 3)
        lon = np.round(lon[ix].astype(float), 3)
        media = np.ma.filled(nc[BANDA][0, iy, ix], np.nan)
        peso = np.ma.filled(nc["weight"][0, iy, ix], np.nan)
        inicio = num2date(float(nc["datetime_start"][0]), nc["datetime_start"].units)
        fim = num2date(float(nc["datetime_stop"][0]), nc["datetime_stop"].units)
        if inicio.year != ano or fim.year != ano or inicio.month != 1 or fim.month != 12:
            raise ValueError("O produto não cobre janeiro a dezembro do ano solicitado.")
        atributos = {nome: str(nc.getncattr(nome)) for nome in nc.ncattrs()}
        np.savez_compressed(recorte, latitude=lat, longitude=lon, no2_pmolec_cm2=media, peso_harp=peso)
        metadados = {
            "url": url, "acesso_utc": datetime.now(timezone.utc).isoformat(),
            "sha256_gzip": hash_fonte, "sha256_recorte": hashlib.sha256(recorte.read_bytes()).hexdigest(),
            "ano": ano, "inicio_observacoes": str(inicio), "fim_observacoes": str(fim),
            "unidade_origem": "10^15 moleculas/cm2", "resolucao_graus": 0.05,
            "conversao_mol_m2": 1e19 / AVOGADRO, "atributos_netcdf": atributos,
            "count_global_harp": int(nc["count"][0]),
            "nota_peso": "Peso acumulado HARP; nao e numero de dias validos.",
            "metodo_regional": "Media espacial da composicao anual FMI ponderada pela area de intersecao em LAEA local.",
            "projecao_area": PROJECAO,
            "sha256_malha": hashlib.sha256((dados / "microrregioes_sc.geojson").read_bytes()).hexdigest(),
            "documentacao": "https://sampo.fmi.fi/tropomi_l3/info_dev.php",
        }
    manifesto.write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
    return recorte


def agregar_regioes(regioes, latitudes, longitudes, concentracoes, pesos, passo=0.05):
    """Interseções fracionárias; preserva negativos válidos e ausência como NaN."""
    latitudes, longitudes = np.asarray(latitudes), np.asarray(longitudes)
    concentracoes, pesos = np.asarray(concentracoes), np.asarray(pesos)
    if concentracoes.shape != (len(latitudes), len(longitudes)) or pesos.shape != concentracoes.shape:
        raise ValueError("Dimensões das coordenadas, concentração e pesos não correspondem.")
    projetar = Transformer.from_crs("EPSG:4326", PROJECAO, always_xy=True).transform
    resultados = []
    for item in regioes:
        poligono = shape(item["geometry"])
        if not poligono.is_valid:
            raise ValueError(f"Geometria inválida: {item['properties']['microrregiao']}")
        regional = transform(projetar, poligono)
        xmin, ymin, xmax, ymax = poligono.bounds
        ix = np.flatnonzero((longitudes + passo/2 > xmin) & (longitudes - passo/2 < xmax))
        iy = np.flatnonzero((latitudes + passo/2 > ymin) & (latitudes - passo/2 < ymax))
        numerador = area_valida = peso_area = area_grade = 0.0
        celulas = 0
        for i in iy:
            for j in ix:
                celula = box(longitudes[j]-passo/2, latitudes[i]-passo/2,
                             longitudes[j]+passo/2, latitudes[i]+passo/2)
                # Intersectar no plano lon/lat mantém as bordas compartilhadas.
                intersecao = poligono.intersection(celula)
                if intersecao.is_empty or intersecao.area == 0:
                    continue
                area = transform(projetar, intersecao).area
                area_grade += area
                valor, peso = concentracoes[i, j], pesos[i, j]
                if not np.isfinite(valor) or not np.isfinite(peso) or peso <= 0:
                    continue
                numerador += valor * area
                area_valida += area
                peso_area += peso * area
                celulas += 1
        # Tolerância para projeção de segmentos retos subdivididos nas bordas.
        if not np.isclose(area_grade, regional.area, rtol=1e-4):
            raise ValueError("Recorte não cobre integralmente a região: " + item["properties"]["microrregiao"])
        media = numerador / area_valida if area_valida else float("nan")
        resultados.append({**item["properties"], "no2_pmolec_cm2": media,
                           "no2_mol_m2": media * 1e19 / AVOGADRO,
                           "fracao_area_observada": area_valida / area_grade,
                           "celulas_validas": celulas,
                           "peso_harp_medio_area": peso_area / area_valida if area_valida else float("nan")})
    return resultados


def comparar_granularidade(regioes, grade, resultados, ano):
    """Mesmos valores e extensão: células L3 sem interpolação versus médias regionais."""
    lat, lon = grade["latitude"], grade["longitude"]
    valores, pesos = grade["no2_pmolec_cm2"], grade["peso_harp"]
    poligonos = [shape(r["geometry"]) for r in regioes]
    estado = unary_union(poligonos)
    # Escala considera todas as células que contribuem, inclusive bordas parciais.
    participa = np.array([[estado.intersection(box(x-.025, y-.025, x+.025, y+.025)).area > 0
                           for x in lon] for y in lat])
    validos = participa & np.isfinite(valores) & np.isfinite(pesos) & (pesos > 0)
    if not validos.any():
        raise ValueError("Nenhuma célula válida para a comparação.")
    minimo, maximo = float(valores[validos].min()), float(valores[validos].max())
    norma = Normalize(vmin=min(0, minimo), vmax=maximo if maximo > 0 else 1)
    cmap = plt.get_cmap("YlOrRd").copy()
    cmap.set_bad("#d9d9d9")
    fig, eixos = plt.subplots(1, 2, figsize=(16, 8))
    fig.subplots_adjust(left=.035, right=.965, bottom=.23, top=.81, wspace=.08)
    bordas_lon = np.r_[lon - .025, lon[-1] + .025]
    bordas_lat = np.r_[lat - .025, lat[-1] + .025]
    imagem = eixos[0].pcolormesh(bordas_lon, bordas_lat, np.ma.array(valores, mask=~validos),
                                cmap=cmap, norm=norma, shading="flat",
                                edgecolors=(0, 0, 0, .12), linewidth=.12, antialiased=False)
    imagem.set_clip_path(patch_from_polygon(estado, transform=eixos[0].transData))
    medias = {r["codigo_ibge"]: r["no2_pmolec_cm2"] for r in resultados}
    for item, poligono in zip(regioes, poligonos):
        eixos[0].add_patch(patch_from_polygon(poligono, facecolor="none", edgecolor="#333333", linewidth=.55))
        valor = medias[item["properties"]["codigo_ibge"]]
        cor = cmap(norma(valor)) if np.isfinite(valor) else "#d9d9d9"
        eixos[1].add_patch(patch_from_polygon(poligono, facecolor=cor, edgecolor="#333333", linewidth=.55))
    xmin, ymin, xmax, ymax = estado.bounds
    for ax in eixos:
        ax.set_xlim(xmin-.12, xmax+.12)
        ax.set_ylim(ymin-.12, ymax+.12)
        ax.set_aspect(1 / np.cos(np.deg2rad(27)))
        ax.set_axis_off()
    # O nome refere-se à microrregião histórica, que inclui ilha e continente.
    florianopolis = next(shape(r["geometry"]) for r in regioes
                         if normalizar(r["properties"]["microrregiao"]) == "florianopolis")
    ponto = florianopolis.representative_point()
    for ax in eixos:
        ax.add_patch(patch_from_polygon(florianopolis, facecolor="none", edgecolor="#125a9c",
                                       linewidth=1.8, zorder=5))
        ax.annotate("Florianópolis\n(microrregião)", xy=(ponto.x, ponto.y),
                    xytext=(xmax+.03, -28.35), ha="right", va="center", fontsize=10,
                    color="#125a9c", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#125a9c", alpha=.95),
                    arrowprops=dict(arrowstyle="->", color="#125a9c", linewidth=1.4,
                                    connectionstyle="arc3,rad=-0.2"))
    eixos[0].set_title("1  |  Grade de NO₂: células de 0,05° × 0,05°", loc="left", fontsize=14, pad=16)
    eixos[1].set_title("2  |  NO₂ agregado: 20 microrregiões", loc="left", fontsize=14, pad=16)
    fig.suptitle(f"Santa Catarina • da grade do satélite às microrregiões • {ano}", fontsize=21, y=.955)
    fig.text(.5, .88, "Mesma composição anual TROPOMI/FMI, mesma extensão e mesma escala de cores",
             ha="center", fontsize=12, color="#555555")
    barra = fig.add_axes([.32, .16, .36, .025])
    fig.colorbar(plt.cm.ScalarMappable(norm=norma, cmap=cmap), cax=barra, orientation="horizontal",
                 label="Coluna troposférica de NO₂ (10¹⁵ moléculas/cm²)")
    fig.text(.04, .065, "Como a agregação funciona: cada célula contribui pela área que ocupa dentro da microrregião.\n"
             "Média regional = Σ(valor da célula × área de interseção) / Σ(área válida de interseção).", fontsize=11)
    fig.text(.04, .018, "Fonte: Copernicus/ESA • TROPOMI • FMI/SAMPO | Limites: IBGE | "
             "Grade L3 recortada em SC; não são as faixas orbitais L2. Cinza = sem dados válidos.", fontsize=9, color="#555555")
    for extensao in ("svg", "png"):
        destino = PASTA / "figuras" / f"no2_granularidade_{ano}.{extensao}"
        fig.savefig(destino, dpi=180, facecolor="white", metadata={"Date": None} if extensao == "svg" else None)
    plt.close(fig)


def gerar_mapa_satelite(ano=2023):
    recorte = adquirir_recorte(ano)
    regioes = carregar_terra()
    with np.load(recorte) as grade:
        resultados = agregar_regioes(regioes, grade["latitude"], grade["longitude"],
                                    grade["no2_pmolec_cm2"], grade["peso_harp"])
    for linha in resultados:
        linha["ano"] = ano
    csv_path = PASTA / "dados" / f"no2_microrregioes_{ano}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(resultados[0]))
        writer.writeheader()
        writer.writerows(resultados)
    (PASTA / "dados" / f"no2_agregacao_{ano}_fontes.json").write_text(json.dumps({
        "ano": ano, "metodo": "media ponderada pela area terrestre valida de intersecao",
        "mascara": "IBGE intersecao GSHHG 2.3.7 full, niveis 1 a 4",
        "sha256_terra": hashlib.sha256((PASTA / "dados/microrregioes_sc_terra.geojson").read_bytes()).hexdigest(),
        "sha256_recorte_no2": hashlib.sha256(recorte.read_bytes()).hexdigest(),
        "sha256_resultados": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "limite": "celulas costeiras conservam o valor L3; apenas seus pesos espaciais excluem agua"
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    valores = {normalizar(r["microrregiao"]): r["no2_pmolec_cm2"] for r in resultados}
    validos = [v for v in valores.values() if np.isfinite(v)]
    if not validos:
        raise ValueError("Nenhuma região com dados válidos; mapa não gerado.")
    destino = PASTA / "figuras" / f"no2_satelite_{ano}.svg"
    destino.parent.mkdir(exist_ok=True)
    cobertura = min(r["fracao_area_observada"] for r in resultados)
    desenhar_mapa(regioes, valores, destino, f"NO₂ troposférico • {ano}",
                  "Coluna de NO₂ (10¹⁵ moléculas/cm²)",
                  f"TROPOMI / Copernicus • composição anual FMI • média apenas sobre terra (GSHHG)\n"
                  f"Cobertura espacial mínima: {cobertura:.1%} • coluna atmosférica, não fluxo de emissões",
                  Normalize(vmin=min(0, min(validos)), vmax=max(validos) if max(validos) > 0 else 1))
    with np.load(recorte) as grade:
        comparar_granularidade(regioes, grade, resultados, ano)
    print("Tabela:", csv_path)
    print("Mapa:", destino)
    print(f"NO2 regional: {min(validos):.4f} a {max(validos):.4f} Pmolec/cm2; cobertura mínima {cobertura:.4%}")
    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ano", type=int, default=2023)
    gerar_mapa_satelite(parser.parse_args().ano)
