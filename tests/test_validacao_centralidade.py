"""Verifica direção da HEM, normalização, Pareto e controle de tamanho."""

import ast
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


class ValidacaoCentralidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "validacao_emissao_centralidade_2015.ipynb"
        notebook = json.loads(path.read_text(encoding="utf8"))
        cls.ns = {"np": np, "pd": pd, "spearmanr": spearmanr}
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            tree = ast.parse("".join(cell["source"]))
            tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
            exec(compile(tree, cell["id"], "exec"), cls.ns)

    def test_hem_fornecedor_atinge_comprador_e_exclui_proprio(self):
        Z = np.array([[0., 5, 0], [0, 0, 0], [0, 0, 0]])
        x = np.array([15., 20, 30])
        perdas, _, _ = self.ns["hem_alocacao"](Z, x)
        esperado = np.zeros((3, 3))
        esperado[0, 1] = 5
        np.testing.assert_allclose(perdas, esperado)
        self.assertAlmostEqual(perdas[0].sum() / x[0], 1 / 3)
        # O nó isolado tem perda própria 30, mas efeito externo zero.
        self.assertEqual(perdas[2].sum(), 0)

    def test_hem_circuitos_e_unidade_monetaria(self):
        Z = np.array([[4., 3], [2, 5]])
        x = np.array([10., 20])
        perdas, G, _ = self.ns["hem_alocacao"](Z, x)
        # r=(4,12); extrair 0 deixa output de 1 igual a 12/(1−5/20)=16.
        self.assertAlmostEqual(perdas[0, 1], 4)
        # Extrair 1 deixa output de 0 igual a 4/(1−4/10).
        self.assertAlmostEqual(perdas[1, 0], 10 - 4/.6)
        esc, Ges, _ = self.ns["hem_alocacao"](Z*100, x*100)
        np.testing.assert_allclose(esc, perdas*100)
        np.testing.assert_allclose(Ges, G)
        np.testing.assert_allclose(esc.sum(axis=1)/(x*100), perdas.sum(axis=1)/x)

    def test_s_preserva_denominador_e_exclui_destino_proprio(self):
        # Sistema triangular: fornecedor 0 atende diretamente 1 com coeficiente 0,25.
        L = np.array([[1., .25, 0], [0, 1, 0], [0, 0, 1]])
        S = L/L.sum(axis=0)
        central = self.ns["sem_diagonal"](S).sum(axis=1)/2
        np.testing.assert_allclose(central, [.1, 0, 0])
        # Renormalizar após tirar a diagonal daria .5: outra pergunta.
        self.assertAlmostEqual(S[0, 1], .2)
        np.testing.assert_allclose(S.sum(axis=0), 1)

    def test_pareto_maximo_emissor_nao_implica_centralidade_alta(self):
        a = [10, 5, 5, 1]
        b = [0, 5, 5, 2]
        mask = self.ns["pareto_max"](a, b)
        np.testing.assert_array_equal(mask, [True, True, True, False])
        np.testing.assert_array_equal(self.ns["pareto_max"](np.log(a), np.array(b)*100), mask)
        with self.assertRaises(ValueError):
            self.ns["pareto_max"]([1, np.nan], [1, 2])

    def test_parcial_rank_equivale_formula_e_nao_confunde_escala(self):
        a = np.array([3, 1, 8, 4, 7, 5, 9, 2.])
        b = np.array([5, 3, 9, 2, 6, 8, 1, 4.])
        x = np.array([1, 4, 2, 6, 7, 3, 8, 5.])
        ab, ax, bx = [spearmanr(u, v).statistic for u, v in [(a, b), (a, x), (b, x)]]
        esperado = (ab-ax*bx)/np.sqrt((1-ax**2)*(1-bx**2))
        self.assertAlmostEqual(self.ns["parcial"](a, b, x), esperado)
        self.assertAlmostEqual(self.ns["parcial"](a*100, b, x*1000), esperado)
        self.assertTrue(np.isnan(self.ns["parcial"](x, b, x)))


if __name__ == "__main__":
    unittest.main()
