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

    def test_resultado_2018(self):
        totais = self.resultados["totais_contabilidade_co2"].loc[2018]
        np.testing.assert_allclose(
            totais[["producao", "consumo", "renda"]],
            [677191.9300000001, 675133.2396386318, 677191.9300000001],
            rtol=1e-12,
        )

    def test_ids_do_notebook_existem_no_manifesto(self):
        for id_entrada in (
            "mip_ibge_2015_67",
            "sanguinet_azzoni_2011",
            "sanguinet_azzoni_2018",
            "exterior_proxy_brasil",
            "exterior_proxy_brasil_2015",
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
