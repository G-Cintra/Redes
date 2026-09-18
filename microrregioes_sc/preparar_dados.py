"""Baixa a malha oficial e cria apenas o CSV demonstrativo (semente fixa)."""
import csv
import gzip
import hashlib
import json
from pathlib import Path
import random
from datetime import datetime, timezone
from urllib.request import urlopen

PASTA = Path(__file__).resolve().parent
URL = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/42?formato=application/vnd.geo+json&qualidade=intermediaria&intrarregiao=microrregiao"
NOMES = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/microrregioes"


def preparar():
    dados = PASTA / "dados"
    dados.mkdir(exist_ok=True)
    with urlopen(NOMES, timeout=90) as resposta:
        conteudo = resposta.read()
    if conteudo.startswith(b"\x1f\x8b"):
        conteudo = gzip.decompress(conteudo)
    nomes = {str(item["id"]): item["nome"] for item in json.loads(conteudo)}
    with urlopen(URL, timeout=90) as resposta:
        original = resposta.read()
    malha = json.loads(gzip.decompress(original) if original.startswith(b"\x1f\x8b") else original)
    for item in malha["features"]:
        codigo = str(item["properties"]["codarea"])
        item["properties"] = {"codigo_ibge": codigo, "microrregiao": nomes[codigo]}
    assert len(malha["features"]) == len(nomes) == 20
    (dados / "microrregioes_sc.geojson").write_text(json.dumps(malha, ensure_ascii=False), encoding="utf-8")
    metadados = {"malha_url": URL, "nomes_url": NOMES,
                 "acesso_utc": datetime.now(timezone.utc).isoformat(),
                 "sha256_resposta_malha": hashlib.sha256(original).hexdigest(),
                 "sha256_geojson": hashlib.sha256((dados / "microrregioes_sc.geojson").read_bytes()).hexdigest(),
                 "nota": "Recorte histórico de microrregiões; API sem ano fixado. Cópia local é a referência reproduzível.",
                 "semente_exemplo": 42}
    (dados / "fontes.json").write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
    rng = random.Random(42)
    with (dados / "emissoes_exemplo.csv").open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["microrregiao", "emissoes_diretas", "emissoes_encadeadas"])
        for codigo, nome in sorted(nomes.items()):
            writer.writerow([nome, round(rng.uniform(100, 1000), 2), round(rng.uniform(100, 1000), 2)])
    print("Malha e exemplo preparados:", dados)


if __name__ == "__main__":
    preparar()
