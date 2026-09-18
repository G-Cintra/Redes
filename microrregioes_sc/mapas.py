"""Mapas coropléticos de duas medidas já calculadas pela análise da MIP."""
import argparse
import csv
import json
import math
from pathlib import Path
import unicodedata

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.path import Path as Caminho
from matplotlib.patches import PathPatch
from matplotlib.patches import Patch

PASTA = Path(__file__).resolve().parent
COLUNAS = ("emissoes_diretas", "emissoes_encadeadas")


def normalizar(nome):
    return " ".join("".join(c for c in unicodedata.normalize("NFKD", nome)
                            if not unicodedata.combining(c)).casefold().split())


def ler_emissoes(arquivo, regioes):
    """Exige correspondência um a um; nunca transforma ausência em zero."""
    esperados = {normalizar(f["properties"]["microrregiao"]) for f in regioes}
    valores = {}
    with Path(arquivo).open(encoding="utf-8-sig", newline="") as entrada:
        leitor = csv.DictReader(entrada)
        if not {"microrregiao", *COLUNAS}.issubset(leitor.fieldnames or []):
            raise ValueError("CSV precisa de microrregiao, emissoes_diretas, emissoes_encadeadas.")
        for linha in leitor:
            nome = normalizar(linha["microrregiao"])
            if nome in valores:
                raise ValueError(f"Microrregião duplicada: {linha['microrregiao']}")
            numeros = tuple(float(linha[c]) for c in COLUNAS)
            if any(not math.isfinite(v) or v < 0 for v in numeros):
                raise ValueError(f"Emissões devem ser finitas e não negativas: {nome}")
            valores[nome] = numeros
    if set(valores) != esperados:
        raise ValueError(f"Ausentes: {sorted(esperados - valores.keys())}; desconhecidas: {sorted(valores.keys() - esperados)}")
    return valores


def desenhar_mapa(regioes, valores, destino, titulo, unidade, nota, norma, paleta="YlOrRd"):
    """Longitudes/latitudes com aspecto corrigido em 27° S; sem cálculo de áreas."""
    fig, ax = plt.subplots(figsize=(11, 7))
    cmap = plt.get_cmap(paleta)
    tem_ausentes = any(not math.isfinite(v) for v in valores.values())
    for item in regioes:
        nome = item["properties"]["microrregiao"]
        geometria = item["geometry"]
        if geometria["type"] not in ("Polygon", "MultiPolygon"):
            raise ValueError(f"Geometria inesperada: {geometria['type']}")
        poligonos = [geometria["coordinates"]] if geometria["type"] == "Polygon" else geometria["coordinates"]
        for poligono in poligonos:
            vertices, codigos = [], []
            for i, anel in enumerate(poligono):
                # Exterior anti-horário e furos horários para preservar ilhas e vazios.
                area = sum(a[0]*b[1] - b[0]*a[1] for a, b in zip(anel, anel[1:]))
                if (area > 0) != (i == 0):
                    anel = list(reversed(anel))
                vertices.extend(anel)
                codigos.extend([Caminho.MOVETO] + [Caminho.LINETO]*(len(anel)-2) + [Caminho.CLOSEPOLY])
            valor = valores[normalizar(nome)]
            cor = cmap(norma(valor)) if math.isfinite(valor) else "#d9d9d9"
            ax.add_patch(PathPatch(Caminho(vertices, codigos), facecolor=cor,
                                   edgecolor="#444444", linewidth=0.55))
    ax.autoscale_view()
    ax.set_aspect(1 / math.cos(math.radians(27)))
    ax.set_axis_off()
    if tem_ausentes:
        ax.legend(handles=[Patch(facecolor="#d9d9d9", label="Sem observações válidas")], loc="lower left")
    ax.set_title("Santa Catarina • " + titulo, fontsize=17, loc="left", pad=20)
    fig.colorbar(plt.cm.ScalarMappable(norm=norma, cmap=cmap), ax=ax, shrink=0.7, label=unidade)
    fig.text(0.08, 0.035, nota + "\nMalha: IBGE • 20 microrregiões históricas • escala linear", fontsize=9)
    fig.savefig(destino, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def gerar_mapas(arquivo, saida, unidade, nota):
    from territorio import carregar_terra
    regioes = carregar_terra()
    valores = ler_emissoes(arquivo, regioes)
    # Mesma escala nos dois mapas permite comparar magnitudes, inclusive zeros.
    norma = Normalize(vmin=0, vmax=max(v for par in valores.values() for v in par) or 1)
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    for i, titulo in enumerate(("Emissões diretas", "Emissões encadeadas")):
        desenhar_mapa(regioes, {n: v[i] for n, v in valores.items()}, saida / f"{COLUNAS[i]}.svg",
                      titulo, unidade, nota, norma)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path)
    parser.add_argument("--saida", type=Path, default=PASTA / "figuras")
    parser.add_argument("--unidade")
    parser.add_argument("--nota")
    args = parser.parse_args()
    if args.entrada and (not args.unidade or not args.nota):
        parser.error("Para dados próprios, informe --unidade e --nota (poluente, ano e definição de encadeadas).")
    gerar_mapas(args.entrada or PASTA / "dados/emissoes_exemplo.csv", args.saida,
                args.unidade or "Unidades arbitrárias", args.nota or "DADOS SINTÉTICOS • semente 42 • sem interpretação empírica")
