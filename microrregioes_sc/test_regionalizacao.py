import csv
import tempfile
from pathlib import Path
import unittest
import numpy as np
from mip import ler_p, PASTA, ler_tecnologia, calcular_contas
from regionalizacao import aplicar_pesos, grupo_atividade, ler_pesos, IDS, ler_fatores, ajustar_distribuicao, carregar_vab


class TestRegionalizacao(unittest.TestCase):
    def test_vab_componentes_unidade_e_alinhamento(self):
        linhas = carregar_vab()
        self.assertEqual([r['codigo_ibge'] for r in linhas], IDS)
        self.assertEqual(len({r['microrregiao'] for r in linhas}), 20)
        for r in linhas:
            componentes = sum(r[f'vab_{g}_mil_reais'] for g in
                              ('agropecuaria', 'industria', 'servicos', 'administracao_publica'))
            self.assertAlmostEqual(componentes, r['vab_total_mil_reais'])
            self.assertAlmostEqual(componentes/1e6, r['vab_total_bilhoes_reais'])
        joinville = next(r for r in linhas if r['codigo_ibge']=='42008')
        self.assertEqual(joinville['microrregiao'], 'Joinville')
        self.assertAlmostEqual(joinville['vab_total_bilhoes_reais'], 36.349092)

    def test_normalizacao_setorial(self):
        base = np.array([[.01, .03], [.03, .02]])
        fatores = np.array([[3., 0.], [1., 2.]])
        resultado = ajustar_distribuicao(base, fatores)
        np.testing.assert_allclose(resultado, [[.02, 0], [.02, .05]])
        np.testing.assert_allclose(ajustar_distribuicao(base, np.ones_like(base)), base)
        # A escala absoluta de um fator não altera a distribuição; só as proporções.
        np.testing.assert_allclose(ajustar_distribuicao(base, fatores*7), resultado)
        for invalido in [np.zeros_like(base), np.full_like(base, np.nan), -fatores]:
            with self.assertRaises(ValueError):
                ajustar_distribuicao(base, invalido)

    def test_perfis_estimados_completos_e_preservacao(self):
        atividades, _ = ler_p()
        fatores, notas = ler_fatores(atividades)
        self.assertEqual(fatores.shape, (20, 67))
        self.assertEqual(len(notas), 67)
        self.assertTrue(all(r['natureza']=='estimativa_julgamental' for r in notas.values()))
        base = ler_pesos(PASTA/'dados/pesos_vab_quatro_grupos_2015.csv', atividades)
        pesos = ler_pesos(PASTA/'dados/pesos_setores_microrregioes_2015.csv', atividades)
        np.testing.assert_allclose(pesos, ajustar_distribuicao(base, fatores))
        np.testing.assert_allclose(pesos.sum(axis=0), base.sum(axis=0), rtol=1e-12)
        self.assertGreater(np.unique(np.round(pesos.T, 12), axis=0).shape[0], 4)
        # Testa âncoras geográficas em atividades com evidência de localização.
        for a, codigo in [('1300','42012'), ('1500','42015'), ('2991','42008'), ('6280','42016')]:
            self.assertEqual(IDS[np.argmax(pesos[:,atividades.index(a)])], codigo)

    def test_orientacao_das_contas(self):
        # Setor 2 compra 0.5 unidade do setor 1 por unidade produzida.
        gamma = np.array([2., 3.])
        x = np.array([10., 20.])
        l = np.array([[1., .5], [0., 1.]])
        d, t = calcular_contas(gamma, x, l)
        np.testing.assert_allclose(d, [20, 60])
        np.testing.assert_allclose(t, [20, 80])
        w = np.array([[.1, .2], [.3, .1]])
        diretas, totais = aplicar_pesos(d, t, w)
        np.testing.assert_allclose(diretas.sum(axis=1), [14, 12])
        np.testing.assert_allclose(totais.sum(axis=1), [18, 14])
        np.testing.assert_allclose(totais.sum(axis=0), w.sum(axis=0)*t)

    def test_cadeia_multiplas_etapas_e_sem_insumos(self):
        gamma, x = np.array([2., 3., 4.]), np.array([10., 20., 30.])
        a = np.array([[0., .5, 0.], [0., 0., .2], [0., 0., 0.]])
        d, t = calcular_contas(gamma, x, np.linalg.inv(np.eye(3)-a))
        # Terceiro setor: 4 próprios + .2*3 fornecedor + .2*.5*2 segundo nível.
        np.testing.assert_allclose(t, [20., 80., 144.])
        np.testing.assert_allclose(t-d, [0., 20., 24.])
        d, t = calcular_contas(gamma, x, np.eye(3))
        np.testing.assert_allclose(d, t)

    def test_grupos_scn(self):
        for a, grupo in [('0191','agropecuaria'), ('0280','agropecuaria'), ('0580','industria'),
                         ('4180','industria'), ('4580','servicos'), ('8591','administracao_publica'),
                         ('8592','servicos'), ('8691','administracao_publica'), ('8692','servicos'), ('9700','servicos')]:
            with self.subTest(atividade=a):
                self.assertEqual(grupo_atividade(a), grupo)

    def test_pesos_reais_e_fechamento_sc(self):
        atividades, p = ler_p()
        arquivo = PASTA / 'dados/pesos_setores_microrregioes_2015.csv'
        w = ler_pesos(arquivo, atividades)
        self.assertEqual(w.shape, (20, 67))
        with arquivo.open(encoding='utf-8') as f:
            linhas = list(csv.DictReader(f))
        self.assertEqual(len(linhas), 1340)
        for i, a in enumerate(atividades):
            subtotal = [r for r in linhas if r['atividade'] == a]
            self.assertAlmostEqual(w[:,i].sum(), float(subtotal[0]['peso_sc_brasil']), places=7)
            self.assertAlmostEqual(sum(float(r['peso_micro_sc']) for r in subtotal), 1, places=6)
        _, gamma, x, l = ler_tecnologia()
        d, t = calcular_contas(gamma, x, l)
        np.testing.assert_allclose(d, p.sum(axis=1), atol=1e-8)
        diretas, totais = aplicar_pesos(d, t, w)
        self.assertLess(diretas.sum(), p.sum())
        self.assertTrue((totais >= diretas - 1e-8).all())
        np.testing.assert_allclose(totais.sum(axis=0), w.sum(axis=0)*t)

    def test_ordem_duplicacao_e_ausencia(self):
        atividades, _ = ler_p()
        arquivo = PASTA / 'dados/pesos_setores_microrregioes_2015.csv'
        with arquivo.open(encoding='utf-8') as f:
            linhas = list(csv.reader(f))
        with tempfile.TemporaryDirectory() as d:
            teste = Path(d) / 'pesos.csv'
            for tipo, corpo in [('invertido', linhas[:0:-1]), ('duplicado', linhas[1:]+[linhas[1]]), ('ausente', linhas[2:])]:
                with teste.open('w', encoding='utf-8', newline='') as f:
                    csv.writer(f).writerows([linhas[0]] + corpo)
                if tipo == 'invertido':
                    np.testing.assert_array_equal(ler_pesos(teste, atividades), ler_pesos(arquivo, atividades))
                else:
                    with self.assertRaises(ValueError):
                        ler_pesos(teste, atividades)


if __name__ == '__main__':
    unittest.main()
