r"""Exporta as figuras completas do notebook em SVG e PDF vetoriais.

Execute da raiz: .venv\Scripts\python apresentacao_exploratoria/gerar_material.py
As contas e o notebook são preservados; o LaTeX incorpora os PDFs vetoriais.
"""
from pathlib import Path
import contextlib
import hashlib
import io
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import QuadMesh
import nbformat
import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
PASTA = Path(__file__).resolve().parent
FIGURAS = PASTA / 'figuras'
FIGURAS.mkdir(exist_ok=True)
plt.rcParams.update({'svg.fonttype': 'none', 'pdf.fonttype': 42})
notebook = RAIZ / 'analise_exploratoria.ipynb'
hash_antes = hashlib.sha256(notebook.read_bytes()).hexdigest()
ambiente = {'__name__': '__main__'}

# Reproduz todas as contas sem modificar as células ou seus resultados salvos.
plt.show = lambda: plt.close('all')
with contextlib.redirect_stdout(io.StringIO()):
    for celula in nbformat.read(notebook, 4).cells:
        if celula.cell_type == 'code':
            ambiente['display'] = lambda *args, **kwargs: None
            exec(compile(celula.source, str(notebook), 'exec'), ambiente)

from redes.visualizacoes import (
    ROTULOS_ATIVIDADES_IBGE, mostrar_heatmap_emissoes, mostrar_emissoes_vab,
    mostrar_pesos_microrregioes, mostrar_comparacao_satelite,
)
C, x, y, c, vab, q, S, e_sc = (ambiente[k] for k in ('C', 'x', 'y', 'c', 'vab', 'q', 'S', 'e_sc'))
np.testing.assert_allclose(c, C @ y)
np.testing.assert_allclose(e_sc.sum(), q @ c)
np.testing.assert_allclose(S.sum(axis=1), 1)

def numero(valor, casas=2):
    return f'{valor:,.{casas}f}'.replace(',', '@').replace('.', '{,}').replace('@', r'\,')

def macro(nome, conteudo):
    return '\\newcommand{\\' + nome + '}{' + conteudo + '}\n'

dados = '% Valores calculados pelo notebook; gerado por gerar_material.py.\n'
for nome, valor in [('TotalBrasil',c.sum()),('TotalSC',e_sc.sum()),('ParcelaSC',100*e_sc.sum()/c.sum()),('MaiorEmissao',c.max())]:
    dados += macro(nome,numero(valor))
dados += macro('MaiorAtividade',ROTULOS_ATIVIDADES_IBGE[c.idxmax()])
linhas = []
for codigo in x.index[:4]:
    valores = [x.loc[codigo],ambiente['ci'].loc[codigo],vab.loc[codigo]]
    linhas.append(codigo + ' & ' + ' & '.join('$'+numero(v)+'$' for v in valores) + r' \\')
dados += macro('LinhasVAB','\n'.join(linhas))
(PASTA/'dados_notebook.tex').write_text(dados,encoding='utf-8')

def salvar_vetorial(nome):
    figura = plt.gcf()
    # imshow é raster mesmo em SVG. Substitui cada célula por um quadrilátero
    # com os mesmos valores, cores, normalização e limites do gráfico original.
    for eixo in figura.axes:
        for imagem in list(eixo.images):
            valores = imagem.get_array()
            xmin, xmax = eixo.get_xlim()
            ymin, ymax = eixo.get_ylim()
            eixo.pcolormesh(np.arange(valores.shape[1]+1)-.5,
                           np.arange(valores.shape[0]+1)-.5, valores,
                           norm=imagem.norm, cmap=imagem.cmap, shading='flat',
                           edgecolors='face', linewidth=.05, antialiased=False)
            imagem.remove()
            eixo.set_xlim(xmin,xmax)
            eixo.set_ylim(ymin,ymax)
        if nome == 'heatmap_c':
            eixo.tick_params(axis='both',labelsize=11)
        elif nome == 'pesos_sc':
            eixo.tick_params(axis='both',labelsize=12)
            for anotacao in eixo.texts:
                anotacao.set_fontsize(11)
        elif nome == 'emissoes_vab':
            eixo.tick_params(axis='y',labelsize=13)
        # Contornos da mesma cor eliminam frestas de antialiasing entre células
        # em leitores de PDF. O heatmap de S mantém sua grade explícita original.
        for colecao in eixo.collections:
            if isinstance(colecao, QuadMesh) and (nome != 'pesos_sc' or eixo is not figura.axes[0]):
                colecao.set_edgecolor('face')
                colecao.set_linewidth(.05)
                colecao.set_antialiased(False)
    # Colorbars podem ser rasterizadas automaticamente pelo Matplotlib.
    for artista in figura.findobj():
        if hasattr(artista,'set_rasterized'):
            artista.set_rasterized(False)
    for extensao in ('svg','pdf'):
        figura.savefig(FIGURAS/f'{nome}.{extensao}',bbox_inches='tight')
    plt.close(figura)

for nome, funcao, argumentos in [
    ('heatmap_c',mostrar_heatmap_emissoes,(C,)),
    ('emissoes_vab',mostrar_emissoes_vab,(c,vab)),
    ('pesos_sc',mostrar_pesos_microrregioes,(S.rename(columns=ambiente['nomes_micro']),)),
    ('comparacao_satelite',mostrar_comparacao_satelite,(e_sc,ambiente['regioes_sc'],ambiente['grade_no2'])),
]:
    plt.show = lambda nome=nome: salvar_vetorial(nome)
    funcao(*argumentos)
    svg = (FIGURAS/f'{nome}.svg').read_text(encoding='utf-8')
    assert '<image' not in svg, f'Imagem raster inesperada: {nome}'
assert hashlib.sha256(notebook.read_bytes()).hexdigest() == hash_antes
print('Quatro figuras completas exportadas em SVG e PDF, sem imagens raster embutidas.')
