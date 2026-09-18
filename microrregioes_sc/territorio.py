"""Recorta os limites administrativos pela terra emersa GSHHG 2.3.7."""
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import shutil
from urllib.request import urlopen
import zipfile

import shapefile
from shapely.geometry import shape, mapping, box
from shapely.ops import unary_union

PASTA = Path(__file__).resolve().parent
URL = "https://www.soest.hawaii.edu/pwessel/gshhg/gshhg-shp-2.3.7.zip"


def carregar_terra():
    arquivo = PASTA / "dados/microrregioes_sc_terra.geojson"
    if not arquivo.exists():
        preparar_terra()
    fontes = json.loads((PASTA / "dados/terra_fontes.json").read_text(encoding="utf-8"))
    if hashlib.sha256(arquivo.read_bytes()).hexdigest() != fontes["sha256_recorte"]:
        raise ValueError("Hash do recorte terrestre divergente.")
    if hashlib.sha256((PASTA / "dados/microrregioes_sc.geojson").read_bytes()).hexdigest() != fontes["sha256_malha_ibge"]:
        raise ValueError("A malha IBGE mudou. Refaça territorio.py e a agregação antes de usar o recorte.")
    return json.loads(arquivo.read_text(encoding="utf-8"))["features"]


def preparar_terra():
    cache = PASTA / "dados/cache_satelite"
    cache.mkdir(exist_ok=True)
    arquivo = cache / "gshhg-shp-2.3.7.zip"
    if not arquivo.exists():
        temporario = arquivo.with_suffix(".part")
        with urlopen(URL, timeout=120) as entrada, temporario.open("wb") as saida:
            shutil.copyfileobj(entrada, saida)
        temporario.replace(arquivo)
    recorte = box(-54, -30, -48, -25)
    camadas = []
    with zipfile.ZipFile(arquivo) as zipado:
        for nivel in range(1, 5):
            base = f"GSHHS_shp/f/GSHHS_f_L{nivel}"
            leitor = shapefile.Reader(**{ext: io.BytesIO(zipado.read(base + "." + ext))
                                       for ext in ("shp", "shx", "dbf")})
            partes = []
            for geometria in leitor.iterShapes(bbox=recorte.bounds):
                poligono = shape(geometria.__geo_interface__)
                if not poligono.is_valid:
                    raise ValueError("Polígono GSHHG inválido; não aplicar reparo silencioso.")
                intersecao = poligono.intersection(recorte)
                if not intersecao.is_empty:
                    partes.append(intersecao)
            camadas.append(unary_union(partes))
        # Alternância da hierarquia: terra, lagos, ilhas em lagos, lagoas em ilhas.
        terra = camadas[0].difference(camadas[1]).union(camadas[2]).difference(camadas[3])
        licencas = {n: zipado.read(n).decode("utf-8", errors="replace") for n in zipado.namelist()
                    if Path(n).name.lower() in ("copying", "copying.lesser", "copyingv3", "copying.lesserv3", "license", "license.txt")}
    original = PASTA / "dados/microrregioes_sc.geojson"
    regioes = json.loads(original.read_text(encoding="utf-8"))
    for item in regioes["features"]:
        poligono = shape(item["geometry"]).intersection(terra)
        if poligono.is_empty or not poligono.is_valid or poligono.geom_type not in ("Polygon", "MultiPolygon"):
            raise ValueError("Recorte terrestre inválido: " + item["properties"]["microrregiao"])
        item["geometry"] = mapping(poligono)
    destino = PASTA / "dados/microrregioes_sc_terra.geojson"
    destino.write_text(json.dumps(regioes, ensure_ascii=False), encoding="utf-8")
    with arquivo.open("rb") as entrada:
        digest = hashlib.file_digest(entrada, "sha256").hexdigest()
    manifesto = {"url": URL, "versao": "2.3.7", "resolucao": "full (f)",
                 "niveis": [1, 2, 3, 4], "acesso_utc": datetime.now(timezone.utc).isoformat(),
                 "sha256_zip": digest, "sha256_malha_ibge": hashlib.sha256(original.read_bytes()).hexdigest(),
                 "sha256_recorte": hashlib.sha256(destino.read_bytes()).hexdigest(),
                 "metodo": "IBGE intersecao ((L1 - L2) uniao L3 - L4), sem simplificacao adicional",
                 "licencas_distribuidas": licencas,
                 "limite": "Exclui agua mapeada no GSHHG; rios estreitos e agua nao cartografada podem permanecer."}
    (PASTA / "dados/terra_fontes.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Recorte terrestre:", destino)


if __name__ == "__main__":
    preparar_terra()
