r"""Reproduz os dados do notebook e exporta exemplos e figuras para a entrega LaTeX.

Execute da raiz do repositório: .venv\Scripts\python apresentacao_exploratoria/gerar_material.py
Não modifica o notebook. Os recortes gráficos são identificados na entrega.
"""
from pathlib import Path
import contextlib
import hashlib
import io
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import nbformat
import numpy as np
import pandas as pd
import seaborn as sns

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
PASTA = Path(__file__).resolve().parent
FIGURAS = PASTA / 'figuras'
FIGURAS.mkdir(exist_ok=True)
notebook = RAIZ / 'analise_exploratoria.ipynb'
hash_antes = hashlib.sha256(notebook.read_bytes()).hexdigest()
nb = nbformat.read(notebook, 4)
ambiente = {'__name__': '__main__'}

# Executa as mesmas contas; somente a exibição é suprimida.
plt.show = lambda: plt.close('all')
with contextlib.redirect_stdout(io.StringIO()):
    for celula in nb.cells:
        if celula.cell_type == 'code':
            ambiente['display'] = lambda *args, **kwargs: None
            exec(compile(celula.source, str(notebook), 'exec'), ambiente)

from redes.visualizacoes import ROTULOS_ATIVIDADES_IBGE, mostrar_comparacao_satelite
L, C, Phi = (ambiente[k] for k in ('L', 'C', 'Phi'))
x, y, c, phi, vab = (ambiente[k] for k in ('x', 'y', 'c', 'phi', 'vab'))
W, q, S, e_sc = (ambiente[k] for k in ('W', 'q', 'S', 'e_sc'))
nomes_micro = ambiente['nomes_micro']
assert np.allclose(c, C @ y)
np.testing.assert_allclose(e_sc.sum(), q @ c)
np.testing.assert_allclose(S.sum(axis=1), 1)

def numero(valor, casas=4):
    return f'{valor:,.{casas}f}'.replace(',', '@').replace('.', '{,}').replace('@', r'\,')

def matriz(valores, casas=4):
    a = np.asarray(valores)
    if a.ndim == 1:
        a = a[:, None]
    linhas = [' & '.join(numero(v, casas) for v in linha) for linha in a]
    return r'\begin{bmatrix}' + r' \\ '.join(linhas) + r'\end{bmatrix}'

def macro(nome, conteudo):
    return '\\newcommand{\\' + nome + '}{' + conteudo + '}\n'

dados = '% Gerado a partir de analise_exploratoria.ipynb; valores completos nas contas.\n'
for nome, valor in [('TotalBrasil', c.sum()), ('TotalSC', e_sc.sum()), ('ParcelaSC', 100*e_sc.sum()/c.sum())]:
    dados += macro(nome, numero(valor, 2))
ids = x.index[:4]
phi_didatica = np.array([.04, .05, .19, .07])
l_didatica = L.loc[ids, ids].to_numpy()
c_didatica = phi_didatica[:, None] * l_didatica
for nome, valor, casas in [
    ('PhiExemplo', np.diag(phi_didatica), 4), ('LExemplo', l_didatica, 4),
    ('CExemplo', c_didatica, 4), ('YExemplo', y.loc[ids], 4),
    ('XExemplo', x.loc[ids], 0), ('DemandaExemplo', c_didatica @ y.loc[ids], 4),
    ('OfertaExemplo', phi_didatica * x.loc[ids], 4),
    ('PhiInterpolada', Phi.loc[ids, ids], 6), ('CInterpolada', C.loc[ids, ids], 6),
]:
    dados += macro(nome, matriz(valor, casas))

coef11, coef18 = ambiente['coef_2011'], ambiente['coef_2018']
linhas_coef, linhas_contas, linhas_vab, linhas_pesos = [], [], [], []
for posicao, codigo in enumerate(ids):
    linhas_coef.append(codigo + ' & ' + ' & '.join('$'+numero(v, 6)+'$' for v in [coef11.iloc[posicao], coef18.iloc[posicao], phi.loc[codigo]]) + r' \\')
    linhas_contas.append(codigo + ' & ' + ' & '.join('$'+numero(v, 4)+'$' for v in [x.loc[codigo],y.loc[codigo],c.loc[codigo],(C@y).loc[codigo]]) + r' \\')
    linhas_vab.append(codigo + ' & ' + ' & '.join('$'+numero(v, 2)+'$' for v in [x.loc[codigo],ambiente['ci'].loc[codigo],vab.loc[codigo]]) + r' \\')
    linhas_pesos.append(codigo + ' & ' + ' & '.join('$'+numero(v, 4)+'$' for v in [100*q.loc[codigo],100*W.loc[codigo,'42008'],100*S.loc[codigo,'42008'],100*W.loc[codigo,'42018'],100*S.loc[codigo,'42018']]) + r' \\')
for nome, linhas in [('LinhasCoeficientes',linhas_coef),('LinhasContas',linhas_contas),('LinhasVAB',linhas_vab),('LinhasPesos',linhas_pesos)]:
    dados += macro(nome,'\n'.join(linhas))
top_regioes = e_sc.sort_values(ascending=False).head(5)
dados += macro('LinhasRegioes', '\n'.join(nomes_micro.loc[k]+' & $'+numero(v,2)+r'$ \\' for k,v in top_regioes.items()))
dados += macro('EmissaoAgricultura',numero(c.iloc[0],4))
dados += macro('MaiorAtividade',ROTULOS_ATIVIDADES_IBGE[c.idxmax()])
dados += macro('MaiorEmissao',numero(c.max(),2))
(PASTA / 'dados_notebook.tex').write_text(dados,encoding='utf-8')

# Recorte de C: as mesmas oito atividades de maior emissão nas linhas e colunas.
selecionados = c.nlargest(8).index
recorte = C.loc[selecionados, selecionados]
rotulos = [ROTULOS_ATIVIDADES_IBGE[k] for k in selecionados]
fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
positivos = C.to_numpy()[C.to_numpy() > 0]
sns.heatmap(recorte, ax=ax, cmap='viridis_r', norm=LogNorm(positivos.min(), positivos.max()),
            annot=True, fmt='.3f', annot_kws={'size':8}, xticklabels=rotulos, yticklabels=rotulos,
            cbar_kws={'label':'Gg CO₂ / R$ milhão de demanda final'})
ax.tick_params(axis='both',labelsize=9)
plt.setp(ax.get_xticklabels(),rotation=35,ha='right')
ax.set_xlabel('Atividade que recebe demanda final')
ax.set_ylabel('Atividade emissora')
fig.savefig(FIGURAS/'heatmap_c.pdf',bbox_inches='tight')
plt.close(fig)

# Participações calculadas sobre as 67 atividades, antes da seleção gráfica.
indice = (c/c.sum()) / (vab/vab.sum())
fig, axes = plt.subplots(1,3,figsize=(12,4),sharey=True,layout='constrained',gridspec_kw={'width_ratios':[1.7,1,1]})
pos = np.arange(len(selecionados))
axes[0].barh(pos,c.loc[selecionados]/1000,color='#4C78A8')
axes[1].scatter(indice.loc[selecionados],pos,color='#5B4B8A',s=20)
axes[1].axvline(1,color='gray',ls='--',lw=.8)
axes[2].barh(pos,100*vab.loc[selecionados]/vab.sum(),color='#28689B')
axes[0].set_yticks(pos,rotulos,fontsize=9)
axes[0].invert_yaxis()
for ax,titulo,unidade in zip(axes,['Emissões','Emissões / VAB','Participação no VAB'],['Mil Gg de CO₂','Razão das participações','% do VAB nacional']):
    ax.set_title(titulo,fontsize=11)
    ax.set_xlabel(unidade,fontsize=9)
    ax.set_xlim(left=0)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='x',alpha=.2)
fig.savefig(FIGURAS/'emissoes_vab.pdf',bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots(figsize=(12,3.3),layout='constrained')
sns.heatmap(100*S.loc[ids].rename(columns=nomes_micro),ax=ax,cmap='viridis_r',vmin=0,
            annot=True,fmt='.1f',annot_kws={'size':8},cbar_kws={'label':'% da produção do setor em SC'})
ax.set_yticklabels([ROTULOS_ATIVIDADES_IBGE[k] for k in ids],rotation=0,fontsize=9)
ax.set_xticklabels(ax.get_xticklabels(),rotation=55,ha='right',fontsize=8)
ax.set_xlabel('Microrregião'); ax.set_ylabel('Atividade')
fig.savefig(FIGURAS/'pesos_sc.pdf',bbox_inches='tight')
plt.close(fig)

def salvar_mapa():
    figura = plt.gcf()
    figura.set_size_inches(12, 5.6)
    figura.suptitle('')
    for eixo, titulo in zip(figura.axes[:2], ['CO₂ estimado · base 2015', 'NO₂ por satélite · 2023']):
        eixo.set_title(titulo, fontsize=17)
        for colecao in eixo.collections:
            colecao.set_rasterized(True)  # Evita linhas brancas entre pixels no PDF.
    for eixo, rotulo in zip(figura.axes[2:], ['CO₂ (Gg)', 'NO₂ (10¹⁵ moléculas/cm²)']):
        eixo.set_xlabel(rotulo, fontsize=15)
        eixo.tick_params(labelsize=13)
    figura.savefig(FIGURAS/'comparacao_satelite.pdf',bbox_inches='tight',dpi=300)
    plt.close('all')
plt.show = salvar_mapa
mostrar_comparacao_satelite(e_sc,ambiente['regioes_sc'],ambiente['grade_no2'])
assert hashlib.sha256(notebook.read_bytes()).hexdigest() == hash_antes
print('Material gerado sem modificar o notebook.')
print('Brasil:',c.sum(),'SC:',e_sc.sum(),'Maior atividade:',c.idxmax())
