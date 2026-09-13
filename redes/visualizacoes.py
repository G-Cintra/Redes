"""Visualizações reutilizáveis do projeto."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def figura_mapa_calor(matriz, setores, titulo, max_peso, dependencia=False):
    """Mostra todos os pesos intersetoriais com escala logarítmica comum."""
    import numpy as np
    import plotly.graph_objects as go

    valores = matriz.to_numpy(copy=True)
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
    return figura


def figura_rede(arestas, metricas, posicoes, titulo, max_peso, max_forca):
    """Desenha arestas já selecionadas; não calcula indicadores nem aplica filtros."""
    import math
    from html import escape

    import plotly.graph_objects as go

    figura = go.Figure()
    meios = []
    for origem, destino, atributos in arestas:
        x0, y0 = posicoes[origem]
        x1, y1 = posicoes[destino]
        # Curva leve separa sentidos opostos; a ponta indica o destino.
        dx, dy = x1 - x0, y1 - y0
        mx, my = (x0 + x1) / 2 - .08 * dy, (y0 + y1) / 2 + .08 * dx
        peso = atributos["weight"]
        largura = .5 + 4 * math.sqrt(peso / max_peso)
        rotulo = f"{escape(origem)} → {escape(destino)}<br>{peso:,.3f} Gg de CO₂"
        meios.append((mx, my, rotulo))
        figura.add_trace(go.Scatter(
            x=[x0, mx, x1], y=[y0, my, y1], mode="lines",
            line=dict(width=largura, color="rgba(63,111,130,0.35)", shape="spline"),
            hoverinfo="skip", showlegend=False,
        ))
        figura.add_annotation(x=x1, y=y1, ax=mx, ay=my, xref="x", yref="y",
                              axref="x", ayref="y", text="", showarrow=True,
                              arrowhead=2, arrowsize=1, arrowwidth=largura,
                              arrowcolor="rgba(63,111,130,0.5)", standoff=10)
    # Hover de arestas no meio da curva evita competir com o hover dos nós.
    figura.add_trace(go.Scatter(x=[m[0] for m in meios], y=[m[1] for m in meios],
                                text=[m[2] for m in meios], mode="markers", hoverinfo="text",
                                marker=dict(size=8, color="rgba(0,0,0,0)"), showlegend=False))
    nos = list(metricas.index)
    hover = []
    for no, linha in metricas.iterrows():
        hover.append(
            f"<b>{escape(no)} · {escape(linha['descricao'])}</b><br>"
            f"Força de entrada: {linha['forca_entrada']:,.2f} Gg<br>"
            f"Força de saída: {linha['forca_saida']:,.2f} Gg<br>"
            f"Emissões totais: {linha['emissoes_totais']:,.2f} Gg<br>"
            f"PageRank emissor: {linha['pagerank_emissor']:.5f}<br>"
            f"Destinos efetivos: {linha['destinos_efetivos']:.2f}<br>"
            f"Diagonal separada: {linha['diagonal']:,.2f} Gg"
        )
    figura.add_trace(go.Scatter(
        x=[posicoes[n][0] for n in nos], y=[posicoes[n][1] for n in nos],
        mode="markers", text=hover, hoverinfo="text", showlegend=False,
        marker=dict(size=[8 + 27 * math.sqrt(v / max_forca) if max_forca else 8 for v in metricas['emissoes_totais']],
                    color=metricas['destinos_efetivos'], colorscale="Viridis", cmin=0,
                    cmax=max(1, metricas['destinos_efetivos'].max()), colorbar=dict(title="Destinos<br>efetivos"),
                    line=dict(width=1.5, color="white")),
    ))
    figura.update_layout(title=titulo, height=590, template="plotly_white",
                         margin=dict(l=10, r=10, t=65, b=10), hovermode="closest",
                         xaxis=dict(visible=False, range=[-1.25, 1.25]),
                         yaxis=dict(visible=False, range=[-1.25, 1.25], scaleanchor="x"))
    return figura


def exportar_pagina_redes(caminho, figuras, tabelas, conclusoes, proveniencia, cobertura):
    """Empacota figuras e resultados já calculados em um único HTML offline."""
    from base64 import b64encode
    from html import escape

    import plotly.io as pio

    blocos = []
    for i, (titulo, figura) in enumerate(figuras.items()):
        grafico = pio.to_html(figura, full_html=False, include_plotlyjs=(i == 0),
                              div_id=f"grafico-{i}", config={"responsive": True, "displaylogo": False})
        bloco = f'<section class="figure"><h2>{escape(titulo)}</h2>{grafico}</section>'
        blocos.append(bloco)
    tabelas_html = []
    for nome, tabela in tabelas.items():
        csv = tabela.to_csv(index=True, lineterminator="\n").encode("utf-8")
        download = b64encode(csv).decode("ascii")
        tabelas_html.append(
            f'<details><summary>{escape(nome)}</summary>'
            f'<a download="{escape(nome)}.csv" href="data:text/csv;base64,{download}">Baixar CSV completo</a>'
            f'<div class="scroll">{tabela.to_html(float_format=lambda v: f"{v:.6g}", escape=True)}</div></details>'
        )
    pagina = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Redes de emissões · Brasil 2015</title><style>
:root{color-scheme:light}body{margin:0;background:#f4f6f3;color:#172f3b;font:16px/1.6 system-ui,sans-serif}
main{max-width:1280px;margin:auto;padding:40px 24px}header{max-width:900px;margin-bottom:32px}
h1{font-size:clamp(30px,5vw,52px);line-height:1.1;letter-spacing:-1.5px}h2{font-size:21px}
.eyebrow{color:#087f8c;font-weight:700;letter-spacing:.15em;font-size:12px}.lead{font-size:19px}
.figure,details,.note{background:white;border:1px solid #dbe3df;border-radius:12px;padding:20px;margin:18px 0}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.grid .figure{min-width:0}
.scroll{overflow:auto;max-height:520px}.plotly-graph-div{max-width:100%}table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:9px;border-bottom:1px solid #e5ebe8;white-space:nowrap}
thead{position:sticky;top:0;background:#eaf0ed}summary{cursor:pointer;font-weight:650}
a{color:#006b78}code{overflow-wrap:anywhere}footer{font-size:13px;color:#49626c}
@media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:24px 12px}.figure{padding:8px}}
</style></head><body><main><header><p class="eyebrow">BRASIL · 2015 · ANÁLISE DE REDES</p>
<h1>Emissões, atividades<br>e demanda final</h1>
<p class="lead">Quem emite mais, quem alcança mais destinos relevantes e onde se concentram as atribuições de emissões da produção brasileira.</p>
</header>''' + ''.join(blocos[:2]) + '''<div class="note"><b>Como ler as redes</b><p>A seta i → j associa emissões da atividade i
à demanda final pelo bem da atividade j. O peso é medido em Gg de CO₂. São relações acumuladas diretas e indiretas,
não vendas diretas nem trajetórias físicas de carbono. A fonte é P, incluindo a produção brasileira para exportações.</p>
<p>Os indicadores usam todas as arestas positivas entre setores, sem threshold. A diagonal é contabilizada à parte.
Os mapas mostram magnitudes em log10(1 + Gg) e dependência de 0 a 100%, na mesma ordem de setores.
Dependência é a participação de um emissor nas atribuições intersetoriais de cada destino.
A diagonal é mascarada; as lacunas não são zeros. O hover mostra os valores originais.</p>
<p>Na exploração por setor, escolha uma atividade para ver até dez origens à esquerda e dez destinos à direita.
As larguras representam pesos; entrada e saída são atribuições diferentes e não precisam se equilibrar.
Um mesmo setor pode aparecer nos dois lados. A cobertura e a diagonal são informadas para cada seleção.
Essa figura não supõe conservação de fluxo através do setor central.</p>
<p>Os painéis circular e por forças mostram a mesma rede,
mostrando as 75 maiores arestas e todos os nós.
Tamanhos indicam emissões totais, incluindo diagonal; cores indicam número efetivo de destinos.
Espessuras indicam pesos. Tamanhos e espessuras usam raiz quadrada.
Posições não têm significado econômico.</p>'''
    pagina += '<div class="scroll">' + cobertura.to_html(float_format=lambda v: f"{v:.3f}", escape=True) + '</div></div>'
    pagina += '<div class="grid">' + ''.join(blocos[2:4]) + '</div>' + ''.join(blocos[4:])
    pagina += '''<script>document.querySelectorAll('details').forEach(el => el.addEventListener('toggle', () => {
if(el.open) el.querySelectorAll('.plotly-graph-div').forEach(g => Plotly.Plots.resize(g));
}));</script>'''
    pagina += '<section class="note"><h2>Leitura dos resultados</h2><ul>'
    pagina += ''.join(f'<li>{escape(t)}</li>' for t in conclusoes) + '</ul></section>'
    pagina += '<h2>Tabelas e rankings</h2><p>Abra uma tabela para consultar os 67 setores e baixar os dados.</p>'
    pagina += ''.join(tabelas_html)
    pagina += '''<details><summary>Método e limites</summary><p>Graus contam conexões. Forças somam pesos,
em Gg e excluem a diagonal. PageRank usa amortecimento 0,85 e distribuição uniforme para teletransporte
e nós sem saída: no grafo original destaca destinos; no invertido destaca emissores.
O número efetivo de destinos é o inverso da soma dos quadrados das participações de saída; sem saídas vale zero.
Gini, HHI e participações dos maiores distinguem concentração das emissões totais e intersetoriais.
Essas dimensões são apresentadas separadamente, sem índice único de criticidade ou previsão causal de intervenção.</p>
<p>Os resultados herdam as hipóteses da etapa MIP: intensidades interpoladas de valores arredondados,
fator monetário 1 entre as bases de 2018 e 2015. Não equivalem a um inventário territorial completo.
Alcance significa distribuição ponderada por destinos, não alcançabilidade por caminhos nem número de empresas.</p></details>'''
    pagina += '<details><summary>Inputs, código e versões</summary><div class="scroll">'
    pagina += proveniencia.to_html(index=False, escape=True) + '</div></details>'
    pagina += '<footer><p>Gerado por analise_redes_emissoes.ipynb. Os cálculos são feitos em Python; esta página apenas apresenta os resultados.</p></footer></main></body></html>'
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
