"""Protege a interface CSV e as decisões metodológicas visíveis no notebook."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import networkx as nx
import numpy as np
import pandas as pd

from redes.redes import carregar_matriz_emissoes, matriz_para_grafo


class RedesEmissoes(unittest.TestCase):
    def test_mapa_calor_preserva_pesos_e_mascara_so_diagonal(self):
        from redes.visualizacoes import figura_mapa_calor
        setores = pd.Series(['A', 'B', 'C'], index=self.matriz.index)
        antes = self.matriz.copy()
        figura = figura_mapa_calor(self.matriz, setores, 'Teste', 2.)
        self.assertTrue(np.isnan(np.diag(figura.data[0].customdata)).all())
        self.assertEqual(figura.data[0].customdata[0, 1], 2.)
        self.assertEqual(figura.data[0].customdata[1, 0], 0.)
        self.assertAlmostEqual(figura.data[0].z[0, 1], np.log10(3))
        self.assertEqual(figura.data[0].zmax, np.log10(3))
        pd.testing.assert_frame_equal(self.matriz, antes)

    def test_etapa_independente_e_margens_reais(self):
        from redes import dados
        n = json.loads(Path('analise_redes_emissoes.ipynb').read_text(encoding='utf-8'))
        s = {'display': lambda *a: None}
        with patch.object(dados, 'carregar_matriz_67', side_effect=AssertionError('Não acessar a MIP')), \
             patch.object(dados, 'entrada', wraps=dados.entrada) as entrada, \
             contextlib.redirect_stdout(io.StringIO()):
            for c in n['cells']:
                if c['cell_type'] == 'code' and c.get('id') not in ['figuras', 'interpretacao', 'exportar-redes']:
                    exec(compile(''.join(c['source']), c['id'], 'exec'), s)
        self.assertEqual({c.args[0] for c in entrada.call_args_list}, {'matriz_emissoes_producao_2015', 'setores_mip_2015'})
        self.assertEqual(s['G'].number_of_nodes(), 67)
        np.testing.assert_allclose(s['metricas']['forca_entrada'] + s['diagonal'], s['P'].sum(axis=0))
        np.testing.assert_allclose(s['metricas']['forca_saida'] + s['diagonal'], s['P'].sum(axis=1))

    def setUp(self):
        self.matriz = pd.DataFrame([[5., 2., .5], [0., 6., 2.], [0., 0., 7.]],
                                   index=['01', '02', '03'], columns=['01', '02', '03'])

    def test_matriz_grafo_preserva_rotulos_direcao_peso_e_diagonal(self):
        g = matriz_para_grafo(self.matriz)
        self.assertEqual(list(g), ['01', '02', '03'])
        self.assertEqual(g['01']['02']['weight'], 2)
        self.assertFalse(g.has_edge('02', '01'))
        self.assertEqual(nx.number_of_selfloops(g), 3)
        self.assertEqual(g.size(weight='weight'), self.matriz.to_numpy().sum())

    def test_inconsistencias_interrompem_conversao(self):
        for matriz in [self.matriz.iloc[:, ::-1], self.matriz.rename(index={'02': '01'}),
                       self.matriz.replace(2., -1.), self.matriz.replace(2., np.inf),
                       self.matriz.replace(2., np.nan)]:
            with self.assertRaises(ValueError):
                matriz_para_grafo(matriz)

    def test_csv_verifica_hash_antes_da_leitura(self):
        with patch('redes.redes.dados.entrada', return_value={'arquivo': 'x.csv', 'sha256': 'x'}), \
             patch('redes.redes.dados.check_sha256', side_effect=ValueError('hash')), \
             patch('redes.redes.pd.read_csv') as ler:
            with self.assertRaisesRegex(ValueError, 'hash'):
                carregar_matriz_emissoes('x')
            ler.assert_not_called()

    def test_csv_preserva_zeros_iniciais_e_rejeita_cabecalho_repetido(self):
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as pasta:
            p = Path(pasta) / 'matriz.csv'
            self.matriz.to_csv(p, index_label='atividade_emissora')
            item = {'arquivo': str(p), 'sha256': sha256(p.read_bytes()).hexdigest()}
            with patch('redes.redes.dados.entrada', return_value=item):
                lida = carregar_matriz_emissoes('x')
            self.assertEqual(lida.index.tolist(), ['01', '02', '03'])
            np.testing.assert_array_equal(lida, self.matriz)
            p.write_text('atividade_emissora,01,01\n01,1,2\n02,3,4\n', encoding='utf-8')
            item['sha256'] = sha256(p.read_bytes()).hexdigest()
            with patch('redes.redes.dados.entrada', return_value=item), self.assertRaises(ValueError):
                carregar_matriz_emissoes('x')

    def executar_metodo(self, matriz, ids):
        # Executa as próprias células metodológicas; não duplica sua implementação.
        n = json.loads(Path('analise_redes_emissoes.ipynb').read_text(encoding='utf-8'))
        s = {'np': np, 'pd': pd, 'nx': nx, 'matriz_para_grafo': matriz_para_grafo,
             'P': matriz, 'setores': pd.Series(matriz.index, index=matriz.index), 'display': lambda *a: None}
        with contextlib.redirect_stdout(io.StringIO()):
            for c in n['cells']:
                if c.get('id') in ids:
                    exec(''.join(c['source']), s)
        return s

    def test_diagonal_alcance_e_dependencia(self):
        s = self.executar_metodo(self.matriz, ['construcao', 'volumes', 'pagerank', 'alcance-dependencia'])
        g = s['G']
        self.assertEqual(nx.number_of_selfloops(g), 0)
        self.assertEqual(g.size(weight='weight'), 4.5)
        self.assertEqual(s['diagonal'].sum(), 18.)
        m = s['metricas']
        self.assertEqual(m.loc['02', 'destinos_efetivos'], 1.)
        self.assertEqual(m.loc['03', 'destinos_efetivos'], 0.)
        self.assertAlmostEqual(m.loc['01', 'destinos_efetivos'], 1 / (.8**2 + .2**2))
        self.assertEqual(s['d'].loc['01', '02'], 1.)
        self.assertEqual(s['d'].loc['01', '03'], .2)
        np.testing.assert_allclose(s['d'].sum(), [0, 1, 1])
        self.assertEqual(m.loc['01', 'forca_saida'], 2.5)

    def test_k_destinos_iguais_e_pagerank_invertido(self):
        matriz = self.matriz * 0
        matriz.loc['01', ['02', '03']] = 2
        s = self.executar_metodo(matriz, ['construcao', 'volumes', 'pagerank', 'alcance-dependencia'])
        m = s['metricas']
        self.assertEqual(m.loc['01', 'destinos_efetivos'], 2.)
        # Estrela assimétrica: o centro fornece, as folhas recebem.
        self.assertGreater(m.loc['01', 'pagerank_emissor'], m.loc['02', 'pagerank_emissor'])
        self.assertLess(m.loc['01', 'pagerank_destino'], m.loc['02', 'pagerank_destino'])
        np.testing.assert_allclose(m[['pagerank_emissor', 'pagerank_destino']].sum(), [1, 1])

    def test_concentracao_igual_concentrada_e_nula(self):
        for valores, gini, hhi in [([1, 1, 1], 0, 1/3), ([3, 0, 0], 2/3, 1), ([0, 0, 0], 0, 0)]:
            matriz = pd.DataFrame(np.diag(valores), index=self.matriz.index, columns=self.matriz.index).astype(float)
            s = self.executar_metodo(matriz, ['construcao', 'volumes', 'concentracao'])
            linha = s['concentracao'].loc['total_com_diagonal']
            self.assertAlmostEqual(linha.gini, gini)
            self.assertAlmostEqual(linha.hhi, hhi)
            self.assertEqual(linha.top5, 1 if sum(valores) else 0)
            self.assertEqual(s['concentracao'].loc['intersetorial_sem_diagonal', 'peso_gg'], 0.)

    def test_diversidade_invariante_a_escala_da_linha(self):
        ids = ['construcao', 'volumes', 'pagerank', 'alcance-dependencia']
        original = self.executar_metodo(self.matriz, ids)
        escalada = self.matriz.copy()
        escalada.loc['01'] *= 10
        alterada = self.executar_metodo(escalada, ids)
        # Intensidade do emissor cancela em q, mas afeta a participação na coluna.
        pd.testing.assert_frame_equal(original['q'], alterada['q'])
        pd.testing.assert_series_equal(original['metricas']['destinos_efetivos'],
                                      alterada['metricas']['destinos_efetivos'])
        self.assertGreater(alterada['d'].loc['01', '03'], original['d'].loc['01', '03'])

    def test_isolado_tem_pagerank_sem_distribuicao_de_saidas(self):
        matriz = self.matriz * 0
        matriz.loc['01', '02'] = 1
        s = self.executar_metodo(matriz, ['construcao', 'volumes', 'pagerank', 'alcance-dependencia'])
        self.assertEqual(s['metricas'].loc['03', 'destinos_efetivos'], 0)
        self.assertGreater(s['metricas'].loc['03', 'pagerank_destino'], 0)
        self.assertGreater(s['metricas'].loc['03', 'pagerank_emissor'], 0)

    def test_mapa_dependencia_percentual(self):
        from redes.visualizacoes import figura_mapa_calor
        d = self.matriz * 0
        d.loc['01', '02'] = .25
        figura = figura_mapa_calor(d, pd.Series(d.index, index=d.index), 'Teste', 1, dependencia=True)
        self.assertEqual(figura.data[0].z[0, 1], 25)
        self.assertEqual(figura.data[0].customdata[0, 1], .25)
        self.assertEqual(figura.data[0].zmax, 100)


if __name__ == '__main__':
    unittest.main()
