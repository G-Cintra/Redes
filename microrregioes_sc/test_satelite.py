import unittest
import numpy as np
from shapely.geometry import box, mapping
from satelite import agregar_regioes, AVOGADRO


class TestMediaRegional(unittest.TestCase):
    def calcular(self, valores, pesos=None, xmax=-50.975):
        regiao = {"properties": {"codigo_ibge": "teste", "microrregiao": "Teste"},
                  "geometry": mapping(box(-51.025, -27.025, xmax, -26.975))}
        pesos = [[1, 1]] if pesos is None else pesos
        return agregar_regioes([regiao], [-27], [-51, -50.95], [valores], pesos)[0]

    def test_celula_inteira_e_conversao(self):
        r = self.calcular([2, 100])
        self.assertAlmostEqual(r['no2_pmolec_cm2'], 2)
        self.assertAlmostEqual(r['no2_mol_m2'], 2e19 / AVOGADRO)
        self.assertAlmostEqual(r['fracao_area_observada'], 1)

    def test_intersecao_parcial(self):
        # Primeira célula inteira + metade da segunda: pesos de área 2:1.
        r = self.calcular([2, 8], xmax=-50.95)
        self.assertAlmostEqual(r['no2_pmolec_cm2'], 4, places=5)

    def test_peso_harp_nao_repondera_area(self):
        r = self.calcular([2, 8], pesos=[[100, 1]], xmax=-50.925)
        self.assertAlmostEqual(r['no2_pmolec_cm2'], 5, places=5)

    def test_ausentes_e_negativos(self):
        r = self.calcular([-1, np.nan], xmax=-50.925)
        self.assertEqual(r['no2_pmolec_cm2'], -1)
        self.assertAlmostEqual(r['fracao_area_observada'], 0.5, places=5)
        r = self.calcular([2, 8], pesos=[[0, 0]])
        self.assertTrue(np.isnan(r['no2_pmolec_cm2']))
        self.assertEqual(r['fracao_area_observada'], 0)

    def test_recorte_incompleto(self):
        with self.assertRaisesRegex(ValueError, 'integralmente'):
            self.calcular([2, 8], xmax=-50.8)


if __name__ == '__main__':
    unittest.main()
