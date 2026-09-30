"""Confere denominadores e alcance nas células da análise de produção."""

import contextlib
import io
import json
from pathlib import Path
import unittest

import networkx as nx
import numpy as np
import pandas as pd


class ConcentracaoDependencia(unittest.TestCase):
    def executar(self, matriz, ids):
        caminho = Path(__file__).resolve().parents[1] / "analise_concentracao_dependencia.ipynb"
        notebook = json.loads(caminho.read_text(encoding="utf-8"))
        estado = {"P": matriz, "setores": pd.Series(matriz.index, index=matriz.index),
                  "np": np, "pd": pd, "nx": nx, "display": lambda *args: None}
        with contextlib.redirect_stdout(io.StringIO()):
            for celula in notebook["cells"]:
                if celula.get("id") in ids:
                    exec(compile("".join(celula["source"]), celula["id"], "exec"), estado)
        return estado

    def test_denominadores_diagonal_e_destino_sem_emissoes(self):
        matriz = pd.DataFrame([[10., 2., 0.], [0., 8., 0.], [0., 0., 0.]],
                              index=["01", "02", "03"], columns=["01", "02", "03"])
        original = matriz.copy()
        s = self.executar(matriz, ["medidas-rede"])
        np.testing.assert_allclose(s["emissoes"], [12, 8, 0])
        self.assertAlmostEqual(s["R"].loc["01", "02"], .2)
        self.assertAlmostEqual(s["D"].loc["01", "02"], 1.)
        self.assertTrue(s["R"]["03"].isna().all())
        self.assertTrue(s["D"]["01"].isna().all())
        self.assertEqual(list(s["G"].edges()), [("01", "02")])
        self.assertEqual(s["metricas"].loc["01", "alcance_total_5pct"], 1)
        self.assertAlmostEqual(s["metricas"].loc["01", "fracao_outros_destinos"], 2/12)
        self.assertTrue(np.isnan(s["metricas"].loc["03", "fracao_outros_destinos"]))
        pd.testing.assert_frame_equal(matriz, original)

    def test_limiar_inclui_igualdade(self):
        matriz = pd.DataFrame([[1., 1.], [0., 19.]], index=["01", "02"], columns=["01", "02"])
        s = self.executar(matriz, ["medidas-rede"])
        self.assertAlmostEqual(s["R"].loc["01", "02"], .05)
        self.assertEqual(s["G"].out_degree("01"), 1)
        self.assertEqual(s["metricas"].loc["01", "alcance_total_10pct"], 0)

    def test_concentracao_uniforme_e_grupo_exclui_proprios_membros(self):
        codigos = [f"{i:02d}" for i in range(12)]
        valores = np.ones((12, 12))
        np.fill_diagonal(valores, 10)
        matriz = pd.DataFrame(valores, index=codigos, columns=codigos)
        s = self.executar(matriz, ["medidas-rede", "concentracao", "alcance-coletivo"])
        c = s["concentracao"].iloc[0]
        self.assertAlmostEqual(c.top5, 5/12)
        self.assertAlmostEqual(c.hhi, 1/12)
        self.assertAlmostEqual(c.gini, 0)
        self.assertEqual(c.n50, 6)
        self.assertEqual(c.n80, 10)
        grupo = s["dependencias_grupos"].query("top_k == 5")
        self.assertEqual(set(grupo.destino), set(codigos[5:]))
        np.testing.assert_allclose(grupo.participacao_grupo, 5/21)
        alcance = s["alcance_grupos"].query("top_k == 5 and limiar == 0.2").iloc[0]
        self.assertEqual(alcance.destinos_acima_limiar, 7)


if __name__ == "__main__":
    unittest.main()
