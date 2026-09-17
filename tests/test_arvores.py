"""Exercita as células metodológicas do experimento em casos verificáveis."""

import contextlib
import io
import hashlib
import json
from pathlib import Path
import unittest

import networkx as nx
import numpy as np
import pandas as pd

from redes.redes import matriz_para_grafo
from redes.visualizacoes_arvores import figura_arvore


class ArvoresEmissoes(unittest.TestCase):
    def test_copia_experimental_e_resultados_completos(self):
        origem = json.loads(Path("raw/experimento_arvores/proveniencia.json").read_text(encoding="utf-8"))
        caminho = Path(origem["copia"])
        self.assertEqual(hashlib.sha256(caminho.read_bytes()).hexdigest(), origem["sha256_copia"])
        p = pd.read_csv(caminho, dtype={"atividade_emissora": str},
                        index_col="atividade_emissora", float_precision="round_trip")
        self.assertEqual(p.shape, (67, 67))
        a = self.executar(p, ["grafos", "selecao", "comparacao", "validacao"])
        self.assertEqual(sorted(map(len, a["componentes"])), [1, 66])
        self.assertEqual(a["resumo"].ligacoes.tolist(), [65, 65, 65])
        self.assertTrue(all(len(codigo) == 4 for codigo in p.index))

    def executar(self, matriz, etapas):
        notebook = json.loads(Path("analise_arvores_emissoes.ipynb").read_text(encoding="utf-8"))
        ambiente = dict(P=matriz.copy(), P_original=matriz.copy(), nx=nx, np=np, pd=pd,
                        setores=pd.Series(matriz.index, index=matriz.index),
                        matriz_para_grafo=matriz_para_grafo, display=lambda *a: None)
        with contextlib.redirect_stdout(io.StringIO()):
            for celula in notebook["cells"]:
                if set(celula.get("metadata", {}).get("tags", [])) & set(etapas):
                    exec("".join(celula["source"]), ambiente)
        return ambiente

    def test_selecao_pesos_direcao_e_isolado(self):
        # Bilaterais AB=7, AC=3, BC=11: mínima=10, máxima=18.
        p = pd.DataFrame([[100, 5, 1, 0], [2, 200, 7, 0], [2, 4, 300, 0], [0, 0, 0, 0]],
                         index=["01", "02", "03", "04"], columns=["01", "02", "03", "04"], dtype=float)
        a = self.executar(p, ["grafos", "selecao", "comparacao", "validacao"])
        self.assertEqual(a["arvore_minima"].size(weight="weight"), 10)
        self.assertEqual(a["arvore_maxima"].size(weight="weight"), 18)
        self.assertEqual(a["arvore_dirigida"].size(weight="weight"), 12)
        self.assertEqual(a["raizes"], ["01"])
        self.assertEqual(a["isolados"], ["04"])
        np.testing.assert_allclose(a["resumo"].participacao_pct, np.array([10, 18, 12]) / 21 * 100)
        pd.testing.assert_frame_equal(a["P"], p)

    def test_sem_arborescencia_nao_substitui_metodo(self):
        p = pd.DataFrame([[0, 1, 0], [0, 0, 0], [0, 1, 0]],
                         index=["A", "B", "C"], columns=["A", "B", "C"], dtype=float)
        with self.assertRaisesRegex(ValueError, "não admite arborescência"):
            self.executar(p, ["grafos", "selecao"])

    def test_visualizacao_preserva_grafo_e_escalas(self):
        p = pd.DataFrame([[1, 2, 0], [3, 4, 0], [0, 0, 0]],
                         index=["01", "02", "03"], columns=["01", "02", "03"], dtype=float)
        a = self.executar(p, ["grafos", "selecao", "comparacao"])
        pos = nx.circular_layout(a["B"])
        for g in a["resultados"].values():
            antes = g.copy()
            figura = figura_arvore(g, a["metricas"], pos, 5)
            self.assertTrue(nx.utils.graphs_equal(g, antes))
            self.assertEqual(figura.directed, g.is_directed())
            nos = {n["id"]: n for n in figura.nodes}
            self.assertEqual(nos["03"]["shape"], "diamond")
            self.assertAlmostEqual((nos["01"]["size"] / nos["02"]["size"]) ** 2, 3 / 7)


if __name__ == "__main__":
    unittest.main()
