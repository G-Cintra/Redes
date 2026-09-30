"""Valida cálculos identificáveis do notebook exploratório, com sistemas pequenos."""

import ast
import contextlib
import io
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd


NOTEBOOK = Path(__file__).resolve().parents[1] / "investigacao_redes_emissoes_2015.ipynb"


class Investigacao2015(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        cls.cells = {c["id"]: "".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"}

    def ambiente(self):
        ns = {"np": np, "pd": pd, "display": lambda *args: None}
        # Executa as funções reais, sem repetir sua implementação nos testes.
        for cell_id in ["funcoes-concentracao", "extracao"]:
            tree = ast.parse(self.cells[cell_id])
            tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
            exec(compile(tree, cell_id, "exec"), ns)
        return ns

    def test_concentracao_uniforme_e_um_emissor(self):
        fn = self.ambiente()["concentracao"]
        uniforme = fn(np.ones(20))
        self.assertAlmostEqual(uniforme["gini"], 0)
        self.assertAlmostEqual(uniforme["hhi"], 1 / 20)
        self.assertAlmostEqual(uniforme["efetivos_q1"], 20)
        self.assertAlmostEqual(uniforme["efetivos_q2"], 20)
        self.assertAlmostEqual(uniforme["top5"], .25)
        self.assertEqual(uniforme["n50"], 10)
        self.assertEqual(uniforme["n75"], 15)
        self.assertEqual(uniforme["n90"], 18)
        unico = fn([100, 0, 0, 0])
        self.assertAlmostEqual(unico["gini"], .75)
        self.assertEqual(unico["n90"], 1)
        self.assertEqual(unico["efetivos_q2"], 1)
        with self.assertRaises(ValueError):
            fn([1, -1])

    def test_diversidade_nao_inventa_destino_em_linha_vazia(self):
        ns = self.ambiente()
        ns["ids"] = pd.Index(["a", "b", "c"])
        div = ns["diversidade_destinos"](np.array([[0., 2, 2], [0, 0, 0], [1, 0, 0]]))
        self.assertAlmostEqual(div.loc["a", "q2"], 2)
        self.assertTrue(np.isnan(div.loc["b", "q2"]))
        self.assertEqual(div.loc["c", "q2"], 1)

    def test_extracao_preserva_direcao_e_exclui_perda_propria(self):
        ns = self.ambiente()
        A = np.array([[0., .25, 0], [0, 0, 0], [0, 0, 0]])
        L = np.linalg.inv(np.eye(3) - A)
        y = np.array([10., 20, 30])
        x = L @ y
        perdas = ns["perdas_extracao"](A, L, x, y)
        # Retirar o comprador 1 elimina cinco unidades do fornecedor 0.
        # Retirar 0 no fechamento de demanda não simula escassez do insumo de 1.
        esperado = np.zeros((3, 3))
        esperado[0, 1] = 5
        np.testing.assert_allclose(perdas, esperado)

    def test_normalizacoes_no_codigo_do_notebook(self):
        ns = self.ambiente()
        ids = pd.Index(["a", "b", "c"])
        A = np.array([[0., .25, 0], [0, 0, 0], [0, 0, 0]])
        L = np.array([[1., .25, 0], [0, 1, 0], [0, 0, 1]])
        x, y, gamma = np.array([15., 20, 30]), np.array([10., 20, 30]), np.array([2., 1, 3])
        Z, H = A * x, gamma[:, None] * L
        P = H * y
        B = Z / x[:, None]
        ns.update(ids=ids, n=3, I=np.eye(3), A=A, L=L, x=x, y=y, gamma=gamma, Z=Z, H=H, P=P,
                  B=B, G=np.linalg.inv(np.eye(3)-B), e=gamma*x, f=P.sum(axis=0), vab=x,
                  nomes=pd.Series(["A", "B", "C"], index=ids))
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(self.cells["metricas-rede"], "metricas-rede", "exec"), ns)
        self.assertAlmostEqual(ns["R"][0, 1], 1/3)
        self.assertAlmostEqual(ns["S"][0, 1], .2)
        self.assertAlmostEqual(ns["Do"][0, 1], 1.)
        self.assertAlmostEqual(ns["M"].loc["a", "R_media"], 1/6)
        self.assertAlmostEqual(ns["M"].loc["a", "fracao_outros"], 1/3)
        self.assertTrue(np.isnan(ns["M"].loc["c", "destinos_q2"]))
        np.testing.assert_allclose(ns["q"].sum(axis=1), 1)


if __name__ == "__main__":
    unittest.main()
