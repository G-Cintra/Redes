"""Verifica as células de indicadores da entrega com casos de solução conhecida."""

from pathlib import Path
import json
import unittest

import networkx as nx
import numpy as np
import pandas as pd


class IndicadoresEntrega(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        caminho = Path(__file__).resolve().parents[1] / "entrega_final/analise_redes_2015.ipynb"
        notebook = json.loads(caminho.read_text(encoding="utf-8"))
        cls.fontes = {
            c["id"]: "".join(c["source"])
            for c in notebook["cells"]
            if c.get("id") in ("indicadores-volume", "indicadores-concentracao",
                               "backbone-caudas", "backbone-selecao")
        }

    def calcular(self, W):
        estado = {"W": W, "G": nx.from_pandas_adjacency(W, create_using=nx.DiGraph),
                  "np": np, "pd": pd, "nx": nx}
        for identificador in ("indicadores-volume", "indicadores-concentracao"):
            exec(compile(self.fontes[identificador], identificador, "exec"), estado)
        return estado

    def matriz(self):
        return pd.DataFrame([[0., 2., 2., 0.], [3., 0., 0., 0.],
                             [1., 0., 0., 0.], [0., 0., 0., 0.]],
                            index=list("abcd"), columns=list("abcd"))

    def test_direcao_e_perfis_com_valores_conhecidos(self):
        s = self.calcular(self.matriz())
        np.testing.assert_array_equal(s["s_out"], [4, 3, 1, 0])
        np.testing.assert_array_equal(s["s_in"], [4, 2, 2, 0])
        self.assertAlmostEqual(s["Y_out"]["a"], .5)
        self.assertAlmostEqual(s["D2_out"]["a"], 2.)
        self.assertAlmostEqual(s["Y_in"]["a"], .625)
        self.assertAlmostEqual(s["D2_in"]["a"], 1.6)
        self.assertAlmostEqual(s["D2_out"]["b"], 1.)
        np.testing.assert_array_equal(s["k_out"], [2, 1, 1, 0])
        self.assertAlmostEqual(s["densidade"], 4/12)

    def test_perfil_nulo_permanece_indefinido(self):
        s = self.calcular(self.matriz())
        self.assertTrue(s["p_out"].loc["d"].isna().all())
        self.assertTrue(s["p_in"]["d"].isna().all())
        for nome in ("Y_out", "Y_in", "D2_out", "D2_in"):
            self.assertTrue(np.isnan(s[nome]["d"]))

    def test_mudanca_de_unidade_preserva_concentracao(self):
        a = self.calcular(self.matriz())
        b = self.calcular(self.matriz() * 1000)
        for nome in ("Y_out", "Y_in", "D2_out", "D2_in"):
            np.testing.assert_allclose(a[nome], b[nome], equal_nan=True)
        np.testing.assert_allclose(b["s_out"], 1000 * a["s_out"])

    def test_permutacao_preserva_rotulos_e_valores(self):
        W = self.matriz()
        a = self.calcular(W)
        b = self.calcular(W.loc[list("dcab"), list("dcab")])
        for nome in ("s_out", "s_in", "Y_out", "Y_in", "D2_out", "D2_in"):
            pd.testing.assert_series_equal(a[nome], b[nome].reindex(W.index))

    def test_uma_direcao_pode_ser_nula_sem_afetar_a_outra(self):
        W = pd.DataFrame([[0., 5., 0.], [0., 0., 0.], [0., 0., 0.]],
                         index=list("abc"), columns=list("abc"))
        s = self.calcular(W)
        self.assertEqual(s["D2_out"]["a"], 1.)
        self.assertTrue(np.isnan(s["D2_in"]["a"]))
        self.assertEqual(s["D2_in"]["b"], 1.)
        self.assertTrue(np.isnan(s["D2_out"]["b"]))

    def test_rede_sem_arestas_nao_produz_infinito(self):
        W = pd.DataFrame(0., index=list("abc"), columns=list("abc"))
        s = self.calcular(W)
        self.assertEqual(s["densidade"], 0.)
        for nome in ("Y_out", "Y_in", "D2_out", "D2_in"):
            self.assertTrue(s[nome].isna().all())

    def filtrar(self, W):
        s = self.calcular(W)
        for identificador in ("backbone-caudas", "backbone-selecao"):
            exec(compile(self.fontes[identificador], identificador, "exec"), s)
        return s

    def test_uniforme_nao_e_selecionado_e_preserva_nos(self):
        W = pd.DataFrame(np.ones((5, 5)) - np.eye(5), index=list("abcde"), columns=list("abcde"))
        s = self.filtrar(W)
        np.testing.assert_allclose(s["arestas_filtro"].cauda_saida, .75**3)
        for alfa in s["alfas"]:
            self.assertEqual(s["backbones"][alfa].number_of_edges(), 0)
            self.assertEqual(s["backbones"][alfa].number_of_nodes(), 5)

    def test_uma_extremidade_decide_sem_aprovar_grau_um(self):
        W = pd.DataFrame([[0., 1., 1.], [1., 0., 0.], [0., 99., 0.]],
                         index=list("abc"), columns=list("abc"))
        s = self.filtrar(W)
        H = s["backbones"][.05]
        self.assertTrue(H.has_edge("c", "b"))
        self.assertEqual(H["c"]["b"]["motivo"], "entrada")
        self.assertFalse(H.has_edge("a", "c"))
        self.assertEqual(H["b"]["a"]["motivo"], "convencao_grau_um")
        transposta = self.filtrar(W.T)["backbones"][.05]
        self.assertEqual(transposta["b"]["c"]["motivo"], "saida")

    def test_diade_exclusiva_e_isolado(self):
        W = pd.DataFrame([[0., 5., 0.], [0., 0., 0.], [0., 0., 0.]],
                         index=list("abc"), columns=list("abc"))
        s = self.filtrar(W)
        for alfa in s["alfas"]:
            H = s["backbones"][alfa]
            self.assertEqual(set(H.edges), {("a", "b")})
            self.assertEqual(H["a"]["b"]["motivo"], "convencao_grau_um")
            self.assertEqual(H["a"]["b"]["weight"], 5.)
            self.assertIn("c", H)

    def test_limite_de_alfa_e_estrito(self):
        s = self.filtrar(self.matriz())
        s["arestas_filtro"]["cauda_saida"] = .05
        s["arestas_filtro"]["cauda_entrada"] = np.nan
        s["arestas_filtro"]["convencao_grau_um"] = False
        exec(self.fontes["backbone-selecao"], s)
        self.assertEqual(s["backbones"][.05].number_of_edges(), 0)
        self.assertEqual(s["backbones"][.10].number_of_edges(), 4)

    def test_filtro_invariante_a_unidade_e_ordem(self):
        W = pd.DataFrame([[0., 1., 1.], [1., 0., 0.], [0., 99., 0.]],
                         index=list("abc"), columns=list("abc"))
        a = self.filtrar(W)
        b = self.filtrar((1000 * W).loc[list("cab"), list("cab")])
        for alfa in a["alfas"]:
            self.assertEqual(set(a["backbones"][alfa].edges), set(b["backbones"][alfa].edges))
            np.testing.assert_allclose(1000 * a["matrizes_backbone"][alfa],
                                       b["matrizes_backbone"][alfa].loc[W.index, W.columns])

    def test_filtro_rede_vazia(self):
        s = self.filtrar(pd.DataFrame(0., index=list("abc"), columns=list("abc")))
        for alfa in s["alfas"]:
            self.assertEqual(s["backbones"][alfa].number_of_edges(), 0)
            self.assertEqual(s["backbones"][alfa].number_of_nodes(), 3)


if __name__ == "__main__":
    unittest.main()
