"""Verificações acadêmicas com as entradas reais do projeto."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from scr import arquivos, emissoes, modelos
from scr.proveniencia import Execucao


class ConsistenciaAcademica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(
            (arquivos.RAIZ_PROJETO / "analise_matriz_insumo_produto.ipynb")
            .read_text(encoding="utf-8")
        )
        cls.resultados = {"display": lambda *args: None}
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in notebook["cells"]:
                source = "".join(cell["source"])
                # O gráfico é exercitado separadamente em diretório temporário.
                if cell["cell_type"] == "code" and "execucao.exportar(" not in source:
                    exec(compile(source, "<notebook>", "exec"), cls.resultados)

    def test_referencias_ibge_e_inversa_ghosh(self):
        r = self.resultados
        self.assertLess(r["erro_a"], 1e-10)
        self.assertLess(r["erro_l"], 1e-10)
        self.assertLess(r["residuo_ghosh"], 1e-10)

    def test_fechamento_economico(self):
        r = self.resultados
        np.testing.assert_allclose(
            r["producao_bruta"],
            r["matriz_transacoes"].sum(axis=1) + r["demanda_final"],
            rtol=0, atol=1e-6,
        )
        np.testing.assert_allclose(
            r["producao_bruta"],
            r["matriz_transacoes"].sum(axis=0) + r["insumos_primarios"],
            rtol=0, atol=1e-6,
        )

    def test_contabilidade_co2(self):
        r = self.resultados
        totais = r["totais_contabilidade_co2"]
        np.testing.assert_allclose(totais["producao"], totais["renda"], rtol=1e-10)
        componentes = r["componentes_consumo_co2"]
        np.testing.assert_allclose(
            totais["consumo"],
            componentes[["producao_domestica_para_consumo", "importacoes_finais",
                         "importacoes_intermediarias"]].sum(axis=1),
            rtol=1e-10,
        )

    def test_rejeita_setores_desalinhados(self):
        r = self.resultados
        with self.assertRaises(ValueError):
            emissoes.calcular_emissoes_producao(
                r["intensidades_co2"][2018].iloc[::-1], r["producao_bruta"]
            )
        with self.assertRaises(ValueError):
            modelos.calcular_inversa_leontief(r["coeficientes_tecnicos"].iloc[::-1])

    def test_checksum_invalido(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / arquivos.ARQUIVO_MIP_67.name
            arquivo.write_bytes(b"dados alterados")
            with self.assertRaises(arquivos.ChecksumInvalidoError):
                arquivos.verificar_checksum(arquivo)

    def test_grafico(self):
        with tempfile.TemporaryDirectory() as pasta:
            execucao = self.resultados["execucao"]
            tabela = self.resultados["tabela_final_2018"]
            figura, _, manifesto = execucao.exportar(tabela, pasta)
            registro = json.loads(manifesto.read_text(encoding="utf-8"))
            self.assertEqual(len(registro["entradas"]), 4)
            self.assertIn("commit", registro["repositorio"])
            self.assertIn("scr/modelos.py", registro["fontes"])
            for output in registro["outputs"]:
                self.assertEqual(
                    arquivos.calcular_sha256(manifesto.parent / output["arquivo"]),
                    output["sha256"],
                )
            with Image.open(manifesto.with_name("contabilidade_co2_2018.png")) as imagem:
                metadados = json.loads(imagem.info["Proveniencia"])
                self.assertEqual(metadados["entradas"], registro["entradas"])
                self.assertEqual(metadados["execucao_id"], registro["execucao_id"])
            csv = pd.read_csv(manifesto.with_name("contabilidade_co2_2018.csv"), index_col=0)
            np.testing.assert_allclose(csv[["producao", "consumo", "renda"]],
                                       tabela[["producao", "consumo", "renda"]], rtol=1e-14)
            plt.close(figura)

    def test_hash_exterior(self):
        for leitor, original in (
            (arquivos.carregar_intensidades_co2_exterior_representativo,
             arquivos.ARQUIVO_INTENSIDADES_CO2_EXTERIOR),
            (arquivos.carregar_inversa_leontief_exterior_representativo,
             arquivos.ARQUIVO_INVERSA_LEONTIEF_EXTERIOR),
        ):
            with self.subTest(arquivo=original.name), tempfile.TemporaryDirectory() as pasta:
                copia = Path(pasta) / original.name
                copia.write_bytes(original.read_bytes() + b"\n")
                with self.assertRaises(arquivos.ChecksumInvalidoError):
                    leitor(copia)

    def test_entrada_alterada_apos_leitura(self):
        with tempfile.TemporaryDirectory() as pasta:
            copia = Path(pasta) / arquivos.ARQUIVO_COEFICIENTES_CO2.name
            copia.write_bytes(arquivos.ARQUIVO_COEFICIENTES_CO2.read_bytes())
            execucao = Execucao("analise_matriz_insumo_produto.ipynb")
            execucao.carregar(arquivos.carregar_coeficientes_co2, copia, "Cópia para teste")
            copia.write_bytes(copia.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "entrada mudou"):
                execucao.exportar(self.resultados["tabela_final_2018"], Path(pasta) / "outputs")
            self.assertFalse((Path(pasta) / "outputs").exists())

    def test_leitura_rejeitada_nao_registrada(self):
        with tempfile.TemporaryDirectory() as pasta:
            copia = Path(pasta) / arquivos.ARQUIVO_COEFICIENTES_CO2.name
            copia.write_bytes(b"conteudo adulterado")
            execucao = Execucao("analise_matriz_insumo_produto.ipynb")
            with self.assertRaises(arquivos.ChecksumInvalidoError):
                execucao.carregar(arquivos.carregar_coeficientes_co2, copia, "Inválido")
            self.assertEqual(execucao.entradas, [])

    def test_checksum_coeficientes_co2(self):
        with tempfile.TemporaryDirectory() as pasta:
            copia = Path(pasta) / arquivos.ARQUIVO_COEFICIENTES_CO2.name
            conteudo = arquivos.ARQUIVO_COEFICIENTES_CO2.read_bytes()
            copia.write_bytes(conteudo)
            self.assertEqual(arquivos.carregar_coeficientes_co2(copia).shape, (67, 2))
            copia.write_bytes(conteudo + b"\n")
            with self.assertRaises(arquivos.ChecksumInvalidoError):
                arquivos.carregar_coeficientes_co2(copia)
            copia.unlink()
            with self.assertRaises(arquivos.ChecksumInvalidoError):
                arquivos.carregar_coeficientes_co2(copia)


if __name__ == "__main__":
    unittest.main()
