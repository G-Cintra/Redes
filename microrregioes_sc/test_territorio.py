import unittest
from shapely.geometry import shape, Point, mapping, box
from territorio import carregar_terra
from satelite import agregar_regioes


class TestTerra(unittest.TestCase):
    def test_ilha_e_baia(self):
        regioes = carregar_terra()
        self.assertEqual(len(regioes), 20)
        florianopolis = shape(next(r["geometry"] for r in regioes if r["properties"]["codigo_ibge"] == "42016"))
        self.assertTrue(florianopolis.contains(Point(-48.48, -27.6)))
        self.assertFalse(florianopolis.contains(Point(-48.57, -27.5)))
        self.assertFalse(florianopolis.contains(Point(-48.56, -27.7)))
        self.assertTrue(all(shape(r["geometry"]).is_valid for r in regioes))

    def test_agua_nao_entra_na_media(self):
        # A segunda célula é água: mesmo um valor extremo não contribui.
        terra = box(-51.025, -27.025, -50.975, -26.975)
        regiao = {"properties": {"microrregiao": "Teste"}, "geometry": mapping(terra)}
        r = agregar_regioes([regiao], [-27], [-51, -50.95], [[2, 1000]], [[1, 1]])[0]
        self.assertEqual(r["no2_pmolec_cm2"], 2)
        self.assertEqual(r["celulas_validas"], 1)


if __name__ == "__main__":
    unittest.main()
