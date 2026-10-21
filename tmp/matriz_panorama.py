import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator

# Ordem canônica: não ordenar por resultado nem agregar setores.
F_panorama = F.copy(deep=True)
c_panorama = F_panorama.sum(axis=1)
u_panorama = F_panorama.sum(axis=0)
np.testing.assert_allclose(c_panorama,c,rtol=0,atol=1e-6)
np.testing.assert_allclose(u_panorama,u,rtol=0,atol=1e-8)
np.testing.assert_allclose(c_panorama.sum(),u_panorama.sum(),rtol=0,atol=1e-6)
assert F_panorama.shape == (67,67)
assert F_panorama.index.equals(atividades) and F_panorama.columns.equals(atividades)
valores_panorama = F_panorama.to_numpy(copy=True)
mascara_panorama = valores_panorama == 0
positivos_panorama = valores_panorama[valores_panorama>0]
norma_panorama = LogNorm(vmin=positivos_panorama.min(),vmax=positivos_panorama.max())
cores_panorama = plt.get_cmap('viridis').copy()
cores_panorama.set_bad('#E1E5E8')
fig_panorama = plt.figure(figsize=(11.7,7.5))
grade_panorama = fig_panorama.add_gridspec(2,3,width_ratios=[5.7,1.35,.18],height_ratios=[1.05,5.7],
    left=.12,right=.97,bottom=.13,top=.95,wspace=.08,hspace=.04)
ax_demanda=fig_panorama.add_subplot(grade_panorama[0,0])
ax_matriz=fig_panorama.add_subplot(grade_panorama[1,0],sharex=ax_demanda)
ax_producao=fig_panorama.add_subplot(grade_panorama[1,1],sharey=ax_matriz)
ax_cor=fig_panorama.add_subplot(grade_panorama[1,2])
imagem_panorama=ax_matriz.imshow(np.ma.array(valores_panorama,mask=mascara_panorama),
    cmap=cores_panorama,norm=norma_panorama,aspect='auto',origin='upper',interpolation='none')
np.testing.assert_array_equal(imagem_panorama.get_array().data,valores_panorama)
np.testing.assert_array_equal(np.ma.getmaskarray(imagem_panorama.get_array()),mascara_panorama)
ticks_panorama=np.arange(67)
ax_matriz.set_xticks(ticks_panorama,atividades,rotation=90,fontsize=6.5)
ax_matriz.set_yticks(ticks_panorama,atividades,fontsize=6.5)
ax_matriz.tick_params(length=0,pad=2)
ax_matriz.set_xlabel('Produto final: destino da atribuição (código IBGE)',fontsize=9,labelpad=7)
ax_matriz.set_ylabel('Origem emissora (código IBGE)',fontsize=9,labelpad=8)
ax_demanda.bar(ticks_panorama,u_panorama/1000,color='#C46527',width=.85)
ax_producao.barh(ticks_panorama,c_panorama/1000,color='#2672A3',height=.85)
# Mesma escala linear dos totais nas duas orientações.
max_margem=1.08*max(c_panorama.max(),u_panorama.max())/1000
ax_demanda.set_ylim(0,max_margem);ax_producao.set_xlim(0,max_margem)
ax_matriz.set_xlim(-.5,66.5);ax_matriz.set_ylim(66.5,-.5)
ax_demanda.tick_params(axis='x',labelbottom=False,bottom=False)
ax_producao.tick_params(axis='y',labelleft=False,left=False)
ax_demanda.set_title('Demanda: total por produto final (u)',fontsize=10,loc='left',pad=5)
ax_demanda.set_ylabel('mil Gg CO₂',fontsize=8)
ax_producao.set_xlabel('mil Gg CO₂',fontsize=8)
ax_producao.set_title('Produção (c)',fontsize=10,loc='left',pad=7)
ax_demanda.yaxis.set_major_locator(MaxNLocator(3))
ax_producao.xaxis.set_major_locator(MaxNLocator(3))
for ax in (ax_demanda,ax_producao):
    ax.spines[['top','right']].set_visible(False);ax.tick_params(labelsize=7)
barra_panorama=fig_panorama.colorbar(imagem_panorama,cax=ax_cor)
barra_panorama.set_label('Atribuição Fᵢⱼ · Gg CO₂ · escala logarítmica',fontsize=8)
barra_panorama.ax.tick_params(labelsize=7)
ax_info=fig_panorama.add_subplot(grade_panorama[0,1:]);ax_info.axis('off')
fracao_diagonal=np.trace(valores_panorama)/valores_panorama.sum()
ax_info.text(0,.85,f'67 × 67 atividades\nSem filtro; diagonal preservada\nTotal: {c_panorama.sum()/1000:.2f} mil Gg\nDiagonal: {100*fracao_diagonal:.2f}% do total',
    va='top',fontsize=8,linespacing=1.5)
pasta_panorama=raiz/'entrega_final/entrega/figuras'
for extensao in ('pdf','png','svg'):
    fig_panorama.savefig(pasta_panorama/f'artigo_matriz_F.{extensao}',dpi=190,bbox_inches='tight',facecolor='white')
F_panorama.to_csv(raiz/'entrega_final/matriz_F_artigo.csv')
pd.concat([nomes,c_panorama.rename('producao_Gg'),u_panorama.rename('demanda_Gg')],axis=1).to_csv(
    raiz/'entrega_final/margens_F_artigo.csv')
pd.testing.assert_frame_equal(F,F_panorama,check_exact=True)
print(f'4.489 células preservadas, {mascara_panorama.sum()} zeros; margens e conservação verificadas. Diagonal: {100*fracao_diagonal:.2f}%.')
display(fig_panorama)
plt.close(fig_panorama)
