"""Visualizações reutilizáveis do projeto."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Rótulos abreviados das 67 atividades da MIP IBGE 2015 (aba 15).
# Usados somente nos gráficos; os códigos e a ordem dos dados são preservados.
ROTULOS_ATIVIDADES_IBGE = {
    "0191": "Agricultura e apoio",
    "0192": "Pecuária e apoio",
    "0280": "Produção florestal, pesca e aquic.",
    "0580": "Extração de carvão e não metálicos",
    "0680": "Extração de petróleo e gás",
    "0791": "Extração de minério de ferro",
    "0792": "Extração de metais não ferrosos",
    "1091": "Carnes, laticínios e pescado",
    "1092": "Açúcar",
    "1093": "Outros alimentos",
    "1100": "Bebidas",
    "1200": "Produtos do fumo",
    "1300": "Têxteis",
    "1400": "Vestuário e acessórios",
    "1500": "Calçados e couro",
    "1600": "Produtos de madeira",
    "1700": "Celulose e papel",
    "1800": "Impressão e reprodução",
    "1991": "Refino de petróleo e coquerias",
    "1992": "Biocombustíveis",
    "2091": "Químicos, resinas e elastômeros",
    "2092": "Defensivos, tintas e outros quím.",
    "2093": "Limpeza, cosméticos e higiene",
    "2100": "Farmoquímicos e farmacêuticos",
    "2200": "Borracha e plástico",
    "2300": "Produtos minerais não metálicos",
    "2491": "Siderurgia e ferro-ligas",
    "2492": "Metais não ferrosos e fundição",
    "2500": "Produtos de metal",
    "2600": "Informática, eletrônicos e ópticos",
    "2700": "Máquinas e equip. elétricos",
    "2800": "Máquinas e equip. mecânicos",
    "2991": "Automóveis, caminhões e ônibus",
    "2992": "Peças e acessórios automotivos",
    "3000": "Outros equip. de transporte",
    "3180": "Móveis e indústrias diversas",
    "3300": "Manutenção e instalação de equip.",
    "3500": "Eletricidade, gás e utilidades",
    "3680": "Água, esgoto e resíduos",
    "4180": "Construção",
    "4580": "Comércio",
    "4900": "Transporte terrestre",
    "5000": "Transporte aquaviário",
    "5100": "Transporte aéreo",
    "5280": "Armazenamento, apoio e correio",
    "5500": "Alojamento",
    "5600": "Alimentação",
    "5800": "Edição e impressão integrada",
    "5980": "TV, rádio, cinema, som e imagem",
    "6100": "Telecomunicações",
    "6280": "Sistemas e serviços de informação",
    "6480": "Finanças, seguros e previdência",
    "6800": "Atividades imobiliárias",
    "6980": "Jurídico, contábil e consultoria",
    "7180": "Arquitetura, engenharia e P&D",
    "7380": "Outros serv. profissionais e técn.",
    "7700": "Aluguéis e ativos intelectuais",
    "7880": "Serv. administrativos e de apoio",
    "8000": "Vigilância e segurança",
    "8400": "Admin. pública, defesa e segurid.",
    "8591": "Educação pública",
    "8592": "Educação privada",
    "8691": "Saúde pública",
    "8692": "Saúde privada",
    "9080": "Artes, cultura e espetáculos",
    "9480": "Associações e serviços pessoais",
    "9700": "Serviços domésticos",
}


SECAO_EMISSOES_VAB = '''<section class="figure" id="emissoes-vab">
<h2>2. Emissões por atividade e participação na economia</h2>
<p class="descricao">O peso de uma atividade nas emissões pode diferir de sua participação na economia. A comparação com o valor adicionado bruto (VAB) permite examinar essa diferença.</p>
<a href="imagens/emissoes_vab.png" target="_blank" rel="noopener" title="Abrir gráfico em tamanho original">
<img src="imagens/emissoes_vab.png" alt="Comparação das 67 atividades: emissões próprias, índice emissões próprias/VAB e participação no valor adicionado bruto" style="display:block;width:100%;height:auto">
</a><p>Selecione a imagem para ampliar.</p>
</section>'''


SECAO_SANKEYS_SETORES = '''<section class="figure" id="sankeys-setores">
<h2>5. Construção e Administração pública: origens e destinos</h2>
<p class="descricao">Construção e Administração pública são exemplos exploratórios selecionados para comparar os dois lados da atribuição. As entradas reúnem emissões de outras atividades associadas à demanda final do setor; as saídas distribuem suas emissões próprias entre outros destinos finais. Essa diferença explica por que os dois lados não precisam ter o mesmo volume.</p><details><summary>Leitura dos diagramas</summary><p>As faixas mostram até dez origens e dez destinos, em Gg de CO₂, com cobertura percentual e diagonal separada.</p></details>
<iframe src="sankeys_setores.html" title="Sankeys da Construção e da Administração pública" style="width:100%;height:1700px;border:0" loading="lazy"></iframe>
<a href="sankeys_setores.html" target="_blank" rel="noopener">Abrir os diagramas em uma página separada</a>
</section>'''


def plotar_emissoes_atividade(contas: pd.DataFrame) -> tuple[plt.Figure, tuple[plt.Axes, plt.Axes, plt.Axes]]:
    """Desenha as contas já calculadas e ordenadas no notebook, em Gg de CO₂.

    Recebe uma atividade por linha, com descrição, emissões próprias,
    participacao_vab e indice_emissoes_vab.
    Preserva a ordem recebida e não calcula indicadores.
    """
    dados = contas.copy()
    dados["atividade"] = (dados.index.astype(str) + " · " + dados["descricao"]).str.rstrip(" ·")
    ordem = dados["atividade"].tolist()

    with sns.axes_style("whitegrid"):
        figura, eixos = plt.subplots(
            1, 3, sharey=True, figsize=(25, max(9, len(dados) * 0.44)),
            gridspec_kw={"width_ratios": [2.3, 1.2, 1.2], "wspace": 0.30},
        )
        eixo, eixo_indice, eixo_vab = eixos
        sns.barplot(
            data=dados, x="emissoes_proprias", y="atividade", order=ordem,
            color="#4C78A8", orient="h", errorbar=None,
            label="Emissões próprias", ax=eixo,
        )

        sns.scatterplot(
            x=dados["indice_emissoes_vab"].to_numpy(), y=list(range(len(dados))),
            color="#5B4B8A", s=30, label="Participação nas emissões / VAB", ax=eixo_indice,
        )
        eixo_indice.axvline(1, color="#666666", linestyle="--", linewidth=1,
                           label="1 = participações iguais")
        sns.barplot(
            data=dados, x="participacao_vab", y="atividade", order=ordem,
            color="#28689B", orient="h", errorbar=None,
            label="VAB = Valor Adicionado Bruto\nParticipação no VAB total", ax=eixo_vab,
        )

    from matplotlib.ticker import PercentFormatter, MaxNLocator
    from matplotlib.lines import Line2D
    from matplotlib.transforms import ScaledTranslation
    eixo_indice.set_title("2. Emissões em relação ao VAB", pad=145, fontweight="bold")
    eixo_indice.set_xlabel("Índice = % emissões próprias / % VAB\n< 1: menor participação | > 1: maior participação", labelpad=12)
    eixo_indice.xaxis.set_major_locator(MaxNLocator(nbins=4))
    eixo_indice.set_xlim(left=0)
    eixo_vab.set_title("3. Relevância econômica", pad=145, fontweight="bold")
    eixo_vab.set_xlabel("Participação no valor adicionado bruto\n(% do VAB total)", labelpad=12)
    eixo_vab.xaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    eixo_vab.xaxis.set_major_locator(MaxNLocator(nbins=4))
    eixo_vab.set_xlim(left=0)
    eixo_vab.margins(x=0.22)
    # Os rótulos expressam as frações já calculadas no notebook em porcentagem.
    for barras_vab in eixo_vab.containers:
        eixo_vab.bar_label(
            barras_vab, labels=[f"{valor:.2%}".replace(".", ",") for valor in dados["participacao_vab"]],
            padding=4, fontsize=9, color="#24445C",
        )
    for painel in [eixo_indice, eixo_vab]:
        painel.set_ylabel("")
        painel.tick_params(axis="y", left=False, labelleft=False)
        painel.yaxis.grid(False)
        sns.despine(ax=painel, left=True)

    eixo.set_title("1. Emissões por atividade", pad=145, fontweight="bold")
    eixo.set_xlabel("Emissões de CO$_2$ (Gg)\nEmissões próprias", labelpad=12)
    eixo.set_ylabel("Atividade")
    eixo.set_xlim(left=0)
    eixo.tick_params(axis="y", labelsize=9)
    eixo.ticklabel_format(axis="x", style="plain")
    eixo.yaxis.grid(False)
    sns.despine(ax=eixo)
    # Escalas superiores repetem as unidades e acompanham os limites inferiores.
    rotulos_superiores = ["Emissões de CO$_2$ (Gg)", "Razão das participações (adimensional)", "% do VAB total"]
    for painel, rotulo in zip(eixos, rotulos_superiores):
        superior = painel.secondary_xaxis("top")
        superior.set_xlabel(rotulo, labelpad=10)
        superior.xaxis.set_major_locator(MaxNLocator(nbins=4))
        if painel is eixo_vab:
            superior.xaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
        painel.xaxis.set_major_locator(MaxNLocator(nbins=4))
        titulo_legenda = None
        if painel is eixo_indice:
            titulo_legenda = "< 1: % emissões menor que % VAB\n> 1: % emissões maior que % VAB"
        painel.legend(
            title=titulo_legenda, loc="lower left", bbox_to_anchor=(0, 1),
            bbox_transform=painel.transAxes + ScaledTranslation(0, 0.8, figura.dpi_scale_trans),
            frameon=False, fontsize=9, title_fontsize=9, borderaxespad=0,
        )
    altura = figura.get_figheight()
    figura.subplots_adjust(left=0.28, right=0.98, bottom=0.9 / altura, top=1 - 2.7 / altura)
    # Separadores no espaço entre painéis mantêm as atividades alinhadas.
    for esquerda, direita in zip(eixos[:-1], eixos[1:]):
        separador = (esquerda.get_position().x1 + direita.get_position().x0) / 2
        figura.add_artist(Line2D(
            [separador, separador], [0.35 / altura, 1 - 0.2 / altura],
            transform=figura.transFigure, color="#657486", linewidth=2,
        ))
    return figura, tuple(eixos)


def mostrar_heatmap_emissoes(C: pd.DataFrame) -> None:
    """Mostra C = ΦL: linhas emissoras e colunas de demanda final unitária.

    Mantém a diagonal e os valores originais; zeros recebem a cor mais clara.
    Códigos IBGE recebem nomes abreviados, sem consultar arquivos externos.
    """
    from matplotlib.colors import LogNorm, Normalize

    if C.empty or not C.index.is_unique or not C.index.equals(C.columns):
        raise ValueError("C deve ter as mesmas atividades únicas nas linhas e colunas.")
    valores = C.to_numpy(dtype=float)
    if not np.isfinite(valores).all() or (valores < 0).any():
        raise ValueError("C deve conter valores finitos e não negativos.")
    positivos = valores[valores > 0]
    cores = plt.get_cmap("viridis_r")
    cores = cores.with_extremes(bad=cores(0.0))
    norma = LogNorm(vmin=positivos.min(), vmax=positivos.max()) if positivos.size else Normalize(0, 1)

    figura, eixo = plt.subplots(figsize=(17, 15), layout="constrained")
    imagem = eixo.imshow(np.ma.masked_equal(valores, 0), cmap=cores,
                         interpolation="nearest", norm=norma)
    rotulos = [ROTULOS_ATIVIDADES_IBGE.get(str(codigo), str(codigo)) for codigo in C.index]
    eixo.set_xticks(range(len(C)), labels=rotulos, rotation=90, fontsize=8)
    eixo.set_yticks(range(len(C)), labels=rotulos, fontsize=8)
    eixo.set_xlabel("Atividade j da demanda final — uma coluna por experimento de R$ 1 milhão")
    eixo.set_ylabel("Atividade emissora i")
    eixo.set_title("C = ΦL: emissões nacionais por demanda final unitária\nClaro = menos emissões · escuro = mais emissões")
    if positivos.size:
        figura.colorbar(imagem, ax=eixo, shrink=0.75,
                        label="Gg de CO₂ / R$ milhão de demanda final (escala logarítmica)")
    plt.show()


def mostrar_emissoes_vab(c: pd.Series, vab: pd.Series) -> None:
    """Compara emissões e VAB em três painéis, ordenados por emissões.

    c em Gg de CO₂ e vab em R$ milhões. O painel central usa
    (c_i / soma(c)) / (vab_i / soma(vab)), não c_i / vab_i.
    Os dois vetores devem cobrir as mesmas atividades; a ordem pode diferir.
    """
    if c.empty or not c.index.is_unique or not vab.index.is_unique:
        raise ValueError("c e vab devem conter atividades únicas e não podem estar vazios.")
    if len(c) != len(vab) or not c.index.isin(vab.index).all():
        raise ValueError("c e vab devem representar as mesmas atividades.")
    vab = vab.reindex(c.index)
    if not np.isfinite(c).all() or (c < 0).any() or not np.isfinite(vab).all() or (vab <= 0).any():
        raise ValueError("Emissões devem ser finitas e não negativas; VAB deve ser finito e positivo.")

    participacao_vab = vab / vab.sum()
    participacao_emissoes = c / c.sum() if c.sum() > 0 else c * np.nan
    contas = pd.DataFrame({
        "descricao": "", "emissoes_proprias": c,
        "participacao_vab": participacao_vab,
        "indice_emissoes_vab": participacao_emissoes / participacao_vab,
    }).sort_values("emissoes_proprias", ascending=False, kind="stable")
    _, eixos = plotar_emissoes_atividade(contas)
    rotulos = [ROTULOS_ATIVIDADES_IBGE.get(str(codigo), str(codigo)) for codigo in contas.index]
    eixos[0].set_yticks(range(len(contas)), labels=rotulos)
    plt.show()


def mostrar_pesos_microrregioes(participacoes: pd.DataFrame) -> None:
    """Heatmap anotado: atividade × microrregião, frações do total setorial em SC."""
    valores = participacoes.to_numpy(dtype=float)
    if not np.isfinite(valores).all() or (valores < 0).any():
        raise ValueError("As participações devem ser finitas e não negativas.")
    np.testing.assert_allclose(valores.sum(axis=1), 1, rtol=0, atol=1e-8)
    rotulos = [ROTULOS_ATIVIDADES_IBGE.get(str(codigo), str(codigo)) for codigo in participacoes.index]
    figura, eixo = plt.subplots(figsize=(18, 23), layout="constrained")
    sns.heatmap(
        participacoes * 100, ax=eixo, cmap="viridis_r", vmin=0,
        annot=True, fmt=".1f", annot_kws={"fontsize": 8},
        yticklabels=rotulos, xticklabels=participacoes.columns,
        linewidths=0.2, linecolor="#dddddd",
        cbar_kws={"label": "% da produção estimada do setor em SC", "shrink": 0.5},
    )
    eixo.set_title("Distribuição estimada de cada setor entre as microrregiões de SC\n"
                   "Cada linha soma 100% antes do arredondamento · pesos de cenário", pad=16)
    eixo.set_xlabel("Microrregião histórica")
    eixo.set_ylabel("Atividade produtiva")
    eixo.tick_params(axis="y", labelsize=9, rotation=0)
    eixo.tick_params(axis="x", labelsize=9, rotation=90)
    plt.show()


def mostrar_mapa_microrregioes(emissoes: pd.Series, regioes: list[dict]) -> None:
    """Exibe o mapa já usado no projeto, recebendo totais por código e GeoJSON."""
    from io import BytesIO
    from IPython.display import SVG, display
    from matplotlib.colors import Normalize
    from microrregioes_sc.mapas import desenhar_mapa, normalizar

    codigos = [r["properties"]["codigo_ibge"] for r in regioes]
    if not emissoes.index.is_unique or set(emissoes.index) != set(codigos):
        raise ValueError("As emissões devem cobrir exatamente as microrregiões da malha.")
    if not np.isfinite(emissoes).all() or (emissoes < 0).any():
        raise ValueError("Emissões regionais devem ser finitas e não negativas.")
    valores = {normalizar(r["properties"]["microrregiao"]): emissoes.loc[r["properties"]["codigo_ibge"]]
               for r in regioes}
    arquivo = BytesIO()
    desenhar_mapa(
        regioes, valores, arquivo, "Emissões da produção regionalizada", "Gg de CO₂",
        "MIP 2015 × pesos setoriais estimados · cenário exploratório\n"
        "Intensidades nacionais comuns às regiões · não é um inventário observado",
        Normalize(vmin=0, vmax=float(emissoes.max()) or 1), paleta="viridis_r",
    )
    display(SVG(data=arquivo.getvalue().decode("utf-8")))


def mostrar_comparacao_satelite(emissoes: pd.Series, regioes: list[dict], grade: dict) -> None:
    """Compara o cenário de CO₂ de 2015 à coluna de NO₂ de 2023, em escalas próprias."""
    from matplotlib.colors import Normalize
    from shapely.geometry import shape, box
    from shapely.ops import unary_union
    from shapely.plotting import patch_from_polygon

    codigos = [r["properties"]["codigo_ibge"] for r in regioes]
    if not emissoes.index.is_unique or set(emissoes.index) != set(codigos):
        raise ValueError("Emissões e limites devem conter as mesmas microrregiões.")
    if not np.isfinite(emissoes).all() or (emissoes < 0).any():
        raise ValueError("As emissões devem ser finitas e não negativas.")
    lat, lon = grade["latitude"], grade["longitude"]
    valores, pesos = grade["no2_pmolec_cm2"], grade["peso_harp"]
    if valores.shape != (len(lat), len(lon)) or pesos.shape != valores.shape:
        raise ValueError("A grade deve ter latitude nas linhas e longitude nas colunas.")
    if not (np.allclose(np.diff(lat), .05) and np.allclose(np.diff(lon), .05)):
        raise ValueError("Este recorte FMI deve ter grade crescente de 0,05 grau.")
    poligonos = [shape(r["geometry"]) for r in regioes]
    terra = unary_union(poligonos)
    # Mesma máscara terrestre do painel original; não modifica os valores L3.
    participa = np.array([
        [terra.intersection(box(x-.025, y-.025, x+.025, y+.025)).area > 0
         for x in lon] for y in lat
    ])
    validos = participa & np.isfinite(valores) & np.isfinite(pesos) & (pesos > 0)
    if not validos.any():
        raise ValueError("Não há observações válidas sobre o recorte terrestre.")
    minimo, maximo = valores[validos].min(), valores[validos].max()
    norma_no2 = Normalize(minimo, maximo if maximo > minimo else minimo + 1e-12)
    norma_co2 = Normalize(0, float(emissoes.max()) or 1)
    paleta = plt.get_cmap("viridis_r").copy()
    paleta.set_bad("#d9d9d9")
    figura, eixos = plt.subplots(1, 2, figsize=(16, 7), layout="constrained")
    imagem = eixos[1].pcolormesh(
        np.r_[lon-.025, lon[-1]+.025], np.r_[lat-.025, lat[-1]+.025],
        np.ma.array(valores, mask=~validos), cmap=paleta, norm=norma_no2,
        shading="flat",
    )
    imagem.set_clip_path(patch_from_polygon(terra, transform=eixos[1].transData))
    for codigo, poligono in zip(codigos, poligonos):
        eixos[0].add_patch(patch_from_polygon(
            poligono, facecolor=paleta(norma_co2(emissoes.loc[codigo])),
            edgecolor="#475569", linewidth=.5,
        ))
        eixos[1].add_patch(patch_from_polygon(
            poligono, facecolor="none", edgecolor="#475569", linewidth=.5,
        ))
    xmin, ymin, xmax, ymax = terra.bounds
    for eixo in eixos:
        eixo.set(xlim=(xmin-.1, xmax+.1), ylim=(ymin-.1, ymax+.1))
        eixo.set_aspect(1 / np.cos(np.deg2rad(27)))
        eixo.set_axis_off()
    eixos[0].set_title("CO₂ estimado · base 2015\nProdução regionalizada por microrregião")
    eixos[1].set_title("NO₂ por satélite · 2023\nComposição anual TROPOMI/FMI · grade de 0,05°")
    figura.colorbar(plt.cm.ScalarMappable(norm=norma_co2, cmap=paleta),
                   ax=eixos[0], orientation="horizontal", shrink=.8, pad=.04,
                   label="Emissões estimadas (Gg de CO₂)")
    figura.colorbar(imagem, ax=eixos[1], orientation="horizontal", shrink=.8, pad=.04,
                   label="Coluna troposférica de NO₂ (10¹⁵ moléculas/cm²)")
    figura.suptitle("Santa Catarina · comparação espacial descritiva", fontsize=16)
    plt.show()


def figura_distribuicao_p(celulas):
    """Mostra todas as células e os positivos em log10, calculado no notebook."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    figura = make_subplots(rows=1, cols=2, subplot_titles=[
        "Todas as células, incluindo zeros e diagonal", "Valores positivos em log₁₀ (Gg)"])
    positivos = celulas.loc[celulas["peso_gg"] > 0]
    for coluna, tabela, variavel, nome in [
        (1, celulas, "peso_gg", "P completa"),
        (2, positivos, "log10_peso", "P positiva"),
    ]:
        figura.add_trace(go.Box(
            y=tabela[variavel], name=nome, quartilemethod="linear",
            boxpoints="all", jitter=.45, pointpos=0,
            marker=dict(size=3, opacity=.4, color="#376E9B"),
            customdata=tabela[["origem", "descricao_origem", "destino", "descricao_destino", "peso_gg", "diagonal"]].to_numpy(),
            hovertemplate=("Origem: %{customdata[0]} · %{customdata[1]}<br>"
                "Destino: %{customdata[2]} · %{customdata[3]}<br>"
                "Peso: %{customdata[4]:.8g} Gg de CO₂<br>Diagonal: %{customdata[5]}<extra></extra>"),
        ), row=1, col=coluna)
    figura.update_yaxes(title_text="Emissões atribuídas (Gg de CO₂)", row=1, col=1)
    figura.update_yaxes(title_text="log₁₀ do peso em Gg (−6 = 0,000001 Gg)", row=1, col=2)
    figura.update_layout(height=620, template="plotly_white", showlegend=False,
                         margin=dict(l=70, r=30, t=75, b=65))
    return figura


def figura_mapa_calor(matriz, setores, titulo, max_peso, dependencia=False, incluir_diagonal=False):
    """Mostra todos os pesos intersetoriais com escala logarítmica comum."""
    import numpy as np
    import plotly.graph_objects as go

    valores = matriz.to_numpy(copy=True)
    if not incluir_diagonal:
        np.fill_diagonal(valores, np.nan)
    # A transformação só afeta a cor; o hover conserva a unidade original.
    cores = 100 * valores if dependencia else np.log10(1 + valores)
    rotulos = [f"{s} · {setores[s]}" for s in matriz.index]
    figura = go.Figure(go.Heatmap(
        z=cores, x=rotulos, y=rotulos, customdata=valores,
        zmin=0, zmax=100 if dependencia else np.log10(1 + max_peso), colorscale="YlGnBu",
        colorbar=dict(title="Participação (%)" if dependencia else "log10(1 + Gg)", thickness=12),
        hovertemplate=("Emissora: %{y}<br>Demanda final: %{x}<br>%{customdata:.2%} das atribuições intersetoriais<extra></extra>" if dependencia else
                       "Emissora: %{y}<br>Demanda final: %{x}<br>%{customdata:,.4f} Gg de CO₂<extra></extra>"),
        hoverongaps=False,
    ))
    figura.update_layout(title=titulo, height=650, template="plotly_white",
                         margin=dict(l=65, r=25, t=65, b=75))
    figura.update_xaxes(title="Destino da atribuição (demanda final)", tickvals=rotulos[::6],
                        ticktext=list(matriz.columns[::6]), tickangle=-45, tickfont=dict(size=9))
    figura.update_yaxes(title="Origem das emissões", tickvals=rotulos[::6],
                        ticktext=list(matriz.index[::6]), tickfont=dict(size=9), autorange="reversed")
    return figura


def figura_setor(estados, titulo):
    """Exploração de entradas e saídas já selecionadas no notebook, sem métricas novas."""
    import plotly.graph_objects as go

    configuracoes = []
    for estado in estados:
        entradas, saidas = estado["entradas"], estado["saidas"]
        pares = entradas + [(estado["setor"], estado["descricao"], 0)] + saidas
        centro = len(entradas)
        rotulos = [f"{codigo} · {descricao}" for codigo, descricao, _ in pares]
        fontes = list(range(centro)) + [centro] * len(saidas)
        destinos = [centro] * len(entradas) + list(range(centro + 1, len(pares)))
        pesos = [v for _, _, v in entradas + saidas]
        node = dict(label=[codigo for codigo, _, _ in pares], customdata=rotulos, pad=16, thickness=16,
                    color=["#4c91a4"] * centro + ["#db8a32"] + ["#4c91a4"] * len(saidas),
                    hovertemplate="%{customdata}<extra></extra>")
        link = dict(source=fontes, target=destinos, value=pesos,
                    hovertemplate="%{source.customdata} → %{target.customdata}<br>%{value:,.3f} Gg de CO₂<extra></extra>")
        from textwrap import fill
        descricao_quebrada = fill(f"{estado['setor']} · {estado['descricao']}", width=45).replace("\n", "<br>")
        subtitulo = (f"{descricao_quebrada}<br>"
                     f"Entradas: {estado['cobertura_entrada']:.1f}% · Saídas: {estado['cobertura_saida']:.1f}% do peso<br>"
                     f"Diagonal separada: {estado['diagonal']:,.2f} Gg")
        if not pesos:
            subtitulo += "<br>Sem conexões intersetoriais; não significa ausência de emissões."
        configuracoes.append((node, link, subtitulo))
    node, link, subtitulo = configuracoes[0]
    figura = go.Figure(go.Sankey(node=node, link=link, arrangement="snap"))
    botoes = [dict(label=f"{e['setor']} · {e['descricao'][:26]}…", method="update",
                  args=[{"node": [n], "link": [l]}, {"annotations[0].text": subt}])
              for e, (n, l, subt) in zip(estados, configuracoes)]
    figura.update_layout(
        title=titulo, height=820, template="plotly_white", font=dict(size=11),
        margin=dict(l=15, r=15, t=220, b=25),
        updatemenus=[dict(buttons=botoes, x=0, y=1.30, xanchor="left", yanchor="top")],
        annotations=[dict(text=subtitulo, x=0, y=1.15, xref="paper", yref="paper",
                          xanchor="left", yanchor="top", showarrow=False, align="left")],
    )
    if len(estados) == 1:
        figura.layout.updatemenus = ()
    return figura


def figura_rede(grafo, metricas, titulo, max_peso, max_emissoes, organizacao="circular"):
    """Desenha o grafo com NetworkX/Matplotlib, sem alterar pesos ou indicadores.

    node_size é área em pontos quadrados, proporcional às emissões próprias.
    NetworkX desenha cada curva e sua ponta como uma única aresta dirigida,
    respeitando o tamanho dos nós. Os dois layouts usam as mesmas escalas.
    """
    import math
    import networkx as nx

    if organizacao not in ["circular", "forcas"]:
        raise ValueError("Organização deve ser 'circular' ou 'forcas'.")
    nos = metricas.index.tolist()
    if set(nos) != set(grafo.nodes):
        raise ValueError("Os nós do grafo e das métricas devem coincidir.")
    if organizacao == "circular":
        posicoes = nx.circular_layout(nos)
    else:
        posicoes = nx.spring_layout(grafo.to_undirected(), seed=42, weight=None, k=.8, iterations=200)

    areas = [2500 * valor / max_emissoes if max_emissoes else 0
             for valor in metricas["emissoes_totais"]]
    larguras = [.5 + 4 * math.sqrt(peso / max_peso) if max_peso else .5
                for _, _, peso in grafo.edges(data="weight")]
    with plt.rc_context({"font.family": "DejaVu Sans"}):
        figura, eixo = plt.subplots(figsize=(13, 11))
        nx.draw_networkx_edges(
            grafo, posicoes, ax=eixo, nodelist=nos, node_size=areas,
            width=larguras, edge_color="#3f6f82", alpha=.35,
            arrows=True, arrowstyle="-|>", arrowsize=13,
            connectionstyle="arc3,rad=0.10", min_source_margin=2, min_target_margin=2,
        )
        pontos = nx.draw_networkx_nodes(
            grafo, posicoes, ax=eixo, nodelist=nos, node_size=areas,
            node_color=metricas["destinos_efetivos"].to_numpy(), cmap="viridis",
            vmin=0, vmax=max(1, metricas["destinos_efetivos"].max()),
            edgecolors="white", linewidths=1.2,
        )
        # Códigos ficam um pouco acima dos nós; nomes completos estão na tabela setorial.
        rotulos = {no: (x, y + .08) for no, (x, y) in posicoes.items()}
        nx.draw_networkx_labels(grafo, rotulos, ax=eixo, font_size=9, font_color="#17374b")
        figura.colorbar(pontos, ax=eixo, shrink=.7, pad=.03, label="Diversidade de destinos")
        eixo.set_title(titulo, pad=20)
        eixo.set_aspect("equal")
        eixo.margins(.18)
        eixo.set_axis_off()
        figura.text(.5, .025,
                    "Área dos nós: emissões próprias · Espessura: peso da relação · Ponta: destino da atribuição",
                    ha="center", fontsize=10)
        figura.tight_layout(rect=(0, .05, 1, 1))
    return figura, eixo


def exportar_pagina_redes(caminho, figuras, tabelas, conclusoes, proveniencia, cobertura, descricoes_figuras, notas_metodologicas):
    """Empacota figuras e resultados já calculados em um único HTML offline."""
    from base64 import b64encode
    from html import escape

    import plotly.io as pio

    blocos = {}
    for i, (titulo, figura) in enumerate(figuras.items()):
        if isinstance(figura, Path):
            endereco = escape(figura.as_posix(), quote=True)
            grafico = (f'<a href="{endereco}" target="_blank" rel="noopener">'
                       f'<img src="{endereco}" alt="{escape(titulo)}" style="width:100%;height:auto"></a>')
        else:
            grafico = pio.to_html(figura, full_html=False, include_plotlyjs=(titulo == "Matriz P completa"),
                                  div_id=f"grafico-{i}", config={"responsive": True, "displaylogo": False})
        bloco = (f'<section class="figure"><h3>{escape("Matriz P: Heatmap" if titulo == "Matriz P completa" else titulo)}</h3>'
                 f'<p class="descricao">{escape(descricoes_figuras[titulo])}</p>{grafico}</section>')
        blocos[titulo] = bloco
    tabelas_html = []
    tabelas_distribuicao = []
    titulos_distribuicao = {
        "distribuicao_celulas_p": "Resumo da distribuição de P (escala original e logaritmo)",
        "metricas_producao": "Indicadores por atividade", "rankings_producao": "Rankings das atividades",
        "concentracao_producao": "Indicadores de concentração", "dependencia_producao": "Participação das origens por destino",
        "resumo_redes": "Resumo da rede", "cobertura_visual": "Cobertura do recorte visual",
        "principais_emissores_por_destino": "Principais emissores por destino",
        "destinos_dependentes_por_emissor": "Destinos com maior participação de cada emissor",
    }
    for nome, tabela in tabelas.items():
        csv = tabela.to_csv(index=True, lineterminator="\n").encode("utf-8")
        download = b64encode(csv).decode("ascii")
        bloco_tabela = (
            f'<details><summary>{escape(titulos_distribuicao.get(nome, nome))}</summary>'
            f'<a download="{escape(nome)}.csv" href="data:text/csv;base64,{download}">Baixar CSV completo</a>'
            f'<div class="scroll">{tabela.to_html(float_format=lambda v: f"{v:.6g}", escape=True)}</div></details>'
        )
        if nome == "distribuicao_celulas_p":
            tabelas_distribuicao.append(bloco_tabela)
        else:
            tabelas_html.append(bloco_tabela)
    pagina = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rede intersetorial de emissões no Brasil</title><style>
:root{color-scheme:light}body{margin:0;background:#f4f6f3;color:#172f3b;font:16px/1.6 system-ui,sans-serif}
main{max-width:1280px;margin:auto;padding:40px 24px}header{max-width:900px;margin-bottom:32px}
h1{font-size:clamp(30px,5vw,52px);line-height:1.1;letter-spacing:-1.5px}h2{font-size:25px}h3{font-size:20px}section[id]{scroll-margin-top:24px}nav{line-height:2.2}img,iframe{max-width:100%}*{box-sizing:border-box}
.eyebrow{color:#087f8c;font-weight:700;letter-spacing:.15em;font-size:12px}
.figure,details,.note{background:white;border:1px solid #dbe3df;border-radius:12px;padding:20px;margin:18px 0}
.descricao{max-width:90ch;margin:0 0 20px;color:#334e5a;line-height:1.65}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.grid .figure{min-width:0}
.scroll{overflow:auto;max-height:520px}.plotly-graph-div{max-width:100%}table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:9px;border-bottom:1px solid #e5ebe8;white-space:nowrap}
thead{position:sticky;top:0;background:#eaf0ed}summary{cursor:pointer;font-weight:650}
a{color:#006b78}code{overflow-wrap:anywhere}
@media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:24px 12px}.figure{padding:8px}}
</style></head><body><main><header><p class="eyebrow">CNM410028 - Desigualdade, Diversidade e Redes</p>
<p>Gabriel Cintra</p>
<h1>Rede intersetorial de emissões no Brasil</h1>
<p>Esta página acompanha a análise exploratória do trabalho apresentado no <a href="https://github.com/G-Cintra/Redes#readme">README</a>. A matriz de emissões construída a partir da MIP brasileira de 2015 é a base da rede examinada aqui.</p>
<p>Nesta etapa, buscamos reconhecer padrões na distribuição das emissões e avaliar quais medidas ajudam a descrevê-los. Os resultados e suas interpretações são preliminares; a <a href="https://github.com/G-Cintra/Redes#nota-metodol%C3%B3gica">nota metodológica</a> e a <a href="https://github.com/G-Cintra/Redes#terminologia">terminologia</a> estão no README.</p>
<nav aria-label="Seções"><a href="#dados">Dados</a> · <a href="#emissoes-vab">Emissões e VAB</a> · <a href="#redes">Redes</a> · <a href="#concentracao">Concentração</a> · <a href="#sankeys-setores">Setores</a> · <a href="#metodo">Método e dados</a> · <a href="index.html">Página principal · Árvores geradoras</a></nav>
</header><section id="dados"><h2>1. Da matriz de emissões à estrutura setorial</h2>

'''
    pagina += blocos["Matriz P completa"] + '</section>' + SECAO_EMISSOES_VAB
    pagina += '<section id="redes"><h2>3. Distribuição das emissões na rede</h2>'
    pagina += f"""<p class="descricao">A rede completa tem {format(tabelas['resumo_redes'].iloc[0]['densidade'], '.1%').replace('.', ',')} das ligações possíveis entre atividades distintas. Essa densidade torna a presença de uma conexão pouco relevante.</p><p class="descricao">Nas visualizações abaixo estão representadas as 20 atividades com maior nível de emissões; as demais estão consolidadas no grupo Outras.</p>"""
    pagina += '<p class="descricao">A área dos nós representa emissões próprias; a espessura das ligações, as emissões daquela relação; e a cor, a diversidade de destinos. Em P<sub>ij</sub>, i é a atividade emissora e j é o destino da demanda final. A área do nó corresponde à soma de sua linha, incluindo a diagonal, e não apenas a P<sub>ii</sub>.</p><details><summary>Leitura dos desenhos</summary><p>As arestas atribuem emissões aos destinos da demanda final. A inversa de Leontief já incorpora requisitos diretos e indiretos; percursos no desenho não representam etapas físicas adicionais da produção.</p><p>As cores vão do roxo ao amarelo conforme aumenta a diversidade entre grupos. Relações internas ficam fora do desenho; as demais análises mantêm as 67 atividades. As duas disposições usam os mesmos dados e suas posições não têm significado econômico.</p></details>'
    pagina += SECAO_REDES_INTERATIVAS
    pagina += '<details><summary>Cobertura das relações exibidas</summary><p class="descricao">Comparação entre a rede agregada e a original, excluindo relações internas a Outras do desenho.</p><div class="scroll">'
    pagina += cobertura.to_html(float_format=lambda v: f"{v:.3f}", escape=True) + '</div></details></section>'
    pagina += '<section id="concentracao"><h2>4. Concentração e diversidade</h2><p>As emissões se concentram em poucos emissores? E cada emissor distribui suas atribuições entre muitos destinos relevantes? As duas figuras examinam essas dimensões separadamente.</p>'
    pagina += blocos["Participação acumulada dos maiores"] + blocos["Volume e diversidade dos destinos"]
    pagina += '<details><summary>Análises complementares</summary>' + blocos["Curva de Lorenz"] + blocos["Distribuição das células de P"] + ''.join(tabelas_distribuicao)
    pagina += blocos["Magnitude intersetorial"] + blocos["Participação dos emissores por destino"] + '</details></section>'
    pagina += SECAO_SANKEYS_SETORES
    pagina += '<details><summary>Explorar outro setor</summary>' + blocos["Explorar um setor"] + '</details>'
    pagina += f"""<section id="metodo"><h2>6. Método, referências e dados</h2><details><summary>Fórmulas, hipóteses e referências</summary>"""
    for titulo, texto in notas_metodologicas.items():
        pagina += f'<h3>{escape(titulo)}</h3><p>{escape(texto)}</p>'
    pagina += '<p>Referências: <a href="https://doi.org/10.2307/1934352">Hill (1973)</a>; <a href="https://doi.org/10.1155/2008/375452">Antoniou e Tsompa (2008)</a>; <a href="https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html">PageRank — NetworkX</a>; <a href="https://doi.org/10.1016/j.rspp.2024.100015">Sanguinet e Azzoni (2024)</a>.</p></details>'
    pagina += '<details><summary>Tabelas e rankings</summary>'
    pagina += ''.join(tabelas_html) + '</details>'
    pagina += '<details><summary>Entradas, código e versões</summary><div class="scroll">'
    pagina += proveniencia.to_html(index=False, escape=True) + '</div></details>'
    pagina += '''</section><script>document.querySelectorAll('details').forEach(el => el.addEventListener('toggle', () => { if(el.open) requestAnimationFrame(() => el.querySelectorAll('.plotly-graph-div').forEach(g => Plotly.Plots.resize(g))); }));</script></main></body></html>'''
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(pagina, encoding="utf-8")


def plotar_contabilidade_co2(
    resultados: pd.DataFrame,
    caminho_saida: Path | str,
    *,
    titulo: str = "Contabilidade setorial de CO2",
    metadados: dict[str, str] | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Gera e salva barras de consumo/renda e linha de producao por atividade.

    ``resultados`` deve ter uma atividade por linha e as colunas ``producao``,
    ``consumo`` e ``renda``. A coluna opcional ``descricao_atividade`` e usada
    nos rotulos do eixo vertical. O PNG e salvo em ``caminho_saida``.
    """
    colunas_necessarias = {"producao", "consumo", "renda"}
    colunas_ausentes = colunas_necessarias - set(resultados.columns)
    if colunas_ausentes:
        raise ValueError(f"Colunas ausentes para o grafico: {sorted(colunas_ausentes)}")
    if resultados.empty:
        raise ValueError("Nao e possivel gerar um grafico sem atividades.")

    dados = resultados.copy()
    dados.index = dados.index.astype(str)
    if "descricao_atividade" in dados:
        dados["atividade"] = dados.index + " - " + dados["descricao_atividade"].astype(str)
    else:
        dados["atividade"] = dados.index
    dados = dados.sort_values("producao", ascending=False)
    ordem = dados["atividade"].tolist()

    dados_barras = dados.melt(
        id_vars="atividade",
        value_vars=["consumo", "renda"],
        var_name="abordagem",
        value_name="emissoes_gg_co2",
    )

    altura = max(12, len(dados) * 0.38)
    figura, eixo = plt.subplots(figsize=(16, altura))
    sns.barplot(
        data=dados_barras,
        y="atividade",
        x="emissoes_gg_co2",
        hue="abordagem",
        hue_order=["consumo", "renda"],
        order=ordem,
        palette={"consumo": "#4C78A8", "renda": "#F58518"},
        errorbar=None,
        orient="h",
        ax=eixo,
    )
    sns.lineplot(
        data=dados,
        y="atividade",
        x="producao",
        sort=False,
        marker="o",
        markersize=4,
        linewidth=1.2,
        color="#202020",
        label="producao",
        estimator=None,
        errorbar=None,
        ax=eixo,
    )

    eixo.set_title(titulo)
    eixo.set_xlabel("Emissoes de CO2 (Gg)")
    eixo.set_ylabel("Atividade")
    eixo.legend(title="Abordagem", loc="lower right")
    figura.tight_layout()

    destino = Path(caminho_saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=300, bbox_inches="tight", metadata=metadados)
    return figura, eixo


def figura_rede_interativa(grafo, metricas, organizacao="circular"):
    """Converte uma cópia do grafo em PyVis; a biblioteca desenha as setas.

    As métricas chegam prontas. A cópia protege os pesos científicos, pois
    from_nx modifica atributos do grafo recebido durante a conversão.
    """
    import math
    import networkx as nx
    from matplotlib.colors import to_hex
    from pyvis.network import Network

    if organizacao not in ("circular", "forcas"):
        raise ValueError("Organização deve ser circular ou forcas.")
    if set(grafo.nodes) != set(metricas.index):
        raise ValueError("Métricas e grafo devem conter os mesmos nós.")
    posicoes = (nx.circular_layout(metricas.index.tolist()) if organizacao == "circular"
                else nx.spring_layout(grafo.to_undirected(), seed=42, weight=None, k=.8, iterations=200))
    rede = Network(height="760px", width="100%", directed=True, cdn_resources="in_line")
    rede.from_nx(grafo.copy())
    max_emissoes = metricas["emissoes_totais"].max()
    max_diversidade = max(1, metricas["destinos_efetivos"].max())
    max_peso = max((d["weight"] for _, _, d in grafo.edges(data=True)), default=0)
    for no in rede.nodes:
        codigo = no["id"]
        m = metricas.loc[codigo]
        no.update(x=float(posicoes[codigo][0] * 500), y=float(-posicoes[codigo][1] * 500),
                  shape="dot", size=35 * math.sqrt(m["emissoes_totais"] / max_emissoes) if max_emissoes else 0,
                  color=to_hex(plt.get_cmap("viridis")(m["destinos_efetivos"] / max_diversidade)),
                  title=(f"{codigo} — {m['descricao']}\n"
                         f"Emissões próprias: {m['emissoes_totais']:,.3f} Gg de CO₂\n"
                         f"Diversidade de destinos: {m['destinos_efetivos']:.2f}"))
    for aresta in rede.edges:
        origem, destino = aresta["from"], aresta["to"]
        peso = grafo[origem][destino]["weight"]
        aresta.pop("value", None)
        aresta.update(weight=peso, width=.5 + 4 * math.sqrt(peso / max_peso) if max_peso else .5,
                      title=f"{origem} → {destino}: {peso:,.3f} Gg de CO₂")
    rede.set_options('''{
      "physics": {"enabled": false},
      "interaction": {"hover": true, "navigationButtons": true, "keyboard": true},
      "nodes": {"borderWidth": 1, "font": {"size": 14}},
      "edges": {"arrows": {"to": {"enabled": true, "scaleFactor": 0.6}},
                "color": {"color": "#3f6f82", "opacity": 0.35},
                "smooth": {"enabled": true, "type": "curvedCW", "roundness": 0.1}}
    }''')
    return rede


SECAO_REDES_INTERATIVAS = '<!-- redes-interativas-inicio -->\n<section class="figure"><h3>Circular interativa · 20 maiores emissores e Outras</h3>\n\n<iframe src="redes_interativas/circular.html" title="Rede circular interativa" loading="lazy" style="width:100%;height:800px;border:0"></iframe></section>\n<section class="figure"><h3>Por forças interativa · 20 maiores emissores e Outras</h3>\n\n<iframe src="redes_interativas/forcas.html" title="Rede por forças interativa" loading="lazy" style="width:100%;height:800px;border:0"></iframe></section>\n<details><summary>Experimento: movimento e sombras (2D)</summary><p>Arraste um nó para mover a rede. physics/enabled pausa a simulação.</p>\n\n<iframe src="redes_interativas/movimento_sombras.html" title="Experimento com movimento e sombras" loading="lazy" style="width:100%;height:1000px;border:0"></iframe></details>\n<!-- redes-interativas-fim -->'
