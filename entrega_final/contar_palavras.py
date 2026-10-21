"""Conta a prosa do artigo com TeXcount, excluindo títulos e blocos gráficos.

Execute: python entrega_final/contar_palavras.py
Requer TeXcount (TeX Live). O relatório JSON inclui hashes dos fontes contados.
"""

from pathlib import Path
import hashlib
import json
import re
import subprocess


def main():
    pasta = Path(__file__).resolve().parent
    secoes = {
        "Resumo": ["resumo.tex"],
        "Introdução": ["introducao.tex"],
        "Dados e método": ["dados.tex", "modelo_atribuicao.tex"],
        "Resultados": ["resultados.tex"],
        "Discussão": ["discussao.tex"],
        "Conclusão": ["conclusoes.tex"],
    }
    linhas = []
    for secao, arquivos in secoes.items():
        for nome in arquivos:
            arquivo = pasta / "entrega" / nome
            fonte = arquivo.read_text(encoding="utf-8")
            assert fonte.count("%TC:ignore") == fonte.count("%TC:endignore")
            # Fontes completos são fornecidos ao TeXcount; só o contador de prosa é somado.
            resultado = subprocess.run(
                ["texcount", "-utf8", "-sum", str(arquivo)],
                capture_output=True, text=True, encoding="utf-8", errors="replace", check=True,
            )
            contador = re.search(r"Words in text:\s*(\d+)", resultado.stdout)
            if not contador:
                raise RuntimeError(f"TeXcount não retornou contagem para {nome}")
            linhas.append({"secao": secao, "arquivo": nome,
                           "palavras": int(contador.group(1)),
                           "sha256": hashlib.sha256(arquivo.read_bytes()).hexdigest()})
    totais = {secao: sum(x["palavras"] for x in linhas if x["secao"] == secao)
              for secao in secoes}
    relatorio = {
        "metodo": "TeXcount: Words in text; soma dos sete fontes ativos",
        "inclusoes": "Resumo e prosa de introdução, dados/método, resultados, discussão e conclusão",
        "exclusoes": "Títulos, legendas/notas de figuras (%TC:ignore), fórmulas, comandos de citação, referências e apêndices",
        "observacao": "Contagem editorial de prosa; fórmulas inline não são palavras. O resumo é incluído por precaução.",
        "por_secao": totais, "total": sum(totais.values()), "limite": 2500, "fontes": linhas,
    }
    (pasta / "contagem_palavras.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for secao, valor in totais.items():
        print(f"{secao}: {valor}")
    print(f"TOTAL: {relatorio['total']} / {relatorio['limite']}")
    if relatorio["total"] > relatorio["limite"]:
        raise SystemExit("O artigo excede o limite de palavras.")


if __name__ == "__main__":
    main()
