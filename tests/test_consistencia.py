"""Verificações das entradas e dos resultados da análise."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from redes import dados


class ConsistenciaAcademica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(Path("analise_matriz_insumo_produto.ipynb").read_text(encoding="utf-8"))
        cls.resultados = {"display": lambda *args: None}
        with contextlib.redirect_stdout(io.StringIO()):
            for celula in notebook["cells"]:
                fonte = "".join(celula.get("source", []))
                if celula["cell_type"] == "code" and "pasta_outputs =" not in fonte:
                    exec(compile(fonte, "<notebook>", "exec"), cls.resultados)

    def test_interpolacao_2015(self):
        estimados = self.resultados["matriz_coeficientes_co2"]
        self.assertEqual(estimados.columns.tolist(), [2015])
        inicio = self.resultados["coeficientes_2011"][2011]
        fim = self.resultados["coeficientes_2018"][2018]
        self.assertTrue(estimados.index.equals(inicio.index))
        np.testing.assert_allclose(estimados[2015], (3 * inicio + 4 * fim) / 7, rtol=1e-14)
        exterior = self.resultados["intensidades_co2_exterior"]
        self.assertEqual(exterior.columns.tolist(), [2015])
        # O cenário externo de referência usa as mesmas intensidades brasileiras.
        np.testing.assert_allclose(exterior[2015], estimados[2015], rtol=1e-14)

    def test_resultado_2015(self):
        self.assertEqual(self.resultados["totais_contabilidade_co2"].index.tolist(), [2015])
        totais = self.resultados["totais_contabilidade_co2"].loc[2015]
        # Referência obtida ponderando os resultados anteriores de 2011 e 2018.
        np.testing.assert_allclose(
            totais[["producao", "consumo", "renda"]],
            [683696.0414285715, 683890.2443365547, 683696.0414285713],
            rtol=1e-12,
        )

    def test_ids_do_notebook_existem_no_manifesto(self):
        for id_entrada in (
            "mip_ibge_2015_67",
            "sanguinet_azzoni_2011",
            "sanguinet_azzoni_2018",
            "coeficientes_co2_exterior_proxy_brasil",
            "inversa_leontief_exterior_proxy_brasil_2015",
        ):
            item = dados.entrada(id_entrada)
            self.assertTrue((dados.RAIZ_PROJETO / item["arquivo"]).is_file())

    def test_hash_incorreto_interrompe_leitura(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "entrada.csv"
            caminho.write_text("conteudo alterado", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA-256 divergente"):
                dados.check_sha256(caminho, "0" * 64)

    def test_leitor_verifica_antes_do_pandas(self):
        with (
            patch.object(dados, "check_sha256", side_effect=ValueError("hash inválido")),
            patch.object(dados.pd, "read_csv") as ler_csv,
        ):
            with self.assertRaisesRegex(ValueError, "hash inválido"):
                dados.carregar_coeficientes_co2("sanguinet_azzoni_2018")
            ler_csv.assert_not_called()


if __name__ == "__main__":
    unittest.main()
