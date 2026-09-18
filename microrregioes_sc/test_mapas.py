"""Testes de alinhamento territorial e integridade dos valores."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from mapas import PASTA, ler_emissoes


class TestEmissoes(unittest.TestCase):
    def setUp(self):
        self.regioes = json.loads((PASTA / "dados/microrregioes_sc.geojson").read_text(encoding="utf-8"))["features"]
        with (PASTA / "dados/emissoes_exemplo.csv").open(encoding="utf-8") as arquivo:
            self.linhas = list(csv.reader(arquivo))

    def ler(self, linhas):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "teste.csv"
            with arquivo.open("w", encoding="utf-8", newline="") as saida:
                csv.writer(saida).writerows(linhas)
            return ler_emissoes(arquivo, self.regioes)

    def test_ordem_independente(self):
        self.assertEqual(self.ler(self.linhas), self.ler([self.linhas[0]] + self.linhas[:0:-1]))
        self.assertEqual(len(self.ler(self.linhas)), 20)

    def test_regioes_invalidas(self):
        for linhas in (self.linhas[:-1], self.linhas + [self.linhas[1]],
                       self.linhas + [["Inexistente", "1", "2"]]):
            with self.subTest(linhas=len(linhas)), self.assertRaises(ValueError):
                self.ler(linhas)

    def test_valores_invalidos(self):
        for valor in ("nan", "inf", "-1", "", "texto"):
            linhas = [linha.copy() for linha in self.linhas]
            linhas[1][1] = valor
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                self.ler(linhas)

    def test_zero_e_acentos(self):
        linhas = [linha.copy() for linha in self.linhas]
        linhas[1] = ["  sao miguel do oeste  ", "0", "0"]
        self.assertEqual(self.ler(linhas)["sao miguel do oeste"], (0, 0))


if __name__ == "__main__":
    unittest.main()
