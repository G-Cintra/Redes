"""Desenho e publicação do experimento de árvores; cálculos ficam no notebook."""

from html import escape
import json
import math
from pathlib import Path

from matplotlib import colormaps
from matplotlib.colors import to_hex
from pyvis.network import Network


def figura_arvore(grafo, metricas, posicoes, max_peso):
    """Usa as posições recebidas e escalas comuns, sem recalcular indicadores."""
    rede = Network(height="780px", width="100%", directed=grafo.is_directed(),
                   cdn_resources="in_line")
    rede.from_nx(grafo.copy())
    max_emissoes = metricas.emissoes_proprias.max()
    max_diversidade = max(1, metricas.destinos_efetivos.max())
    for no in rede.nodes:
        codigo = no["id"]
        m = metricas.loc[codigo]
        raio = 36 * math.sqrt(m.emissoes_proprias / max_emissoes) if max_emissoes else 0
        isolado = grafo.degree(codigo) == 0
        no.update(
            label=codigo + (" · isolada" if isolado else ""),
            x=float(posicoes[codigo][0] * 850), y=float(-posicoes[codigo][1] * 850),
            shape="diamond" if raio == 0 else "dot", size=6 if raio == 0 else raio,
            color=to_hex(colormaps["viridis"](m.destinos_efetivos / max_diversidade)),
            title=(f"{codigo} — {escape(str(m.descricao))}\n"
                   f"Emissões próprias: {m.emissoes_proprias:,.6g} Gg de CO₂\n"
                   f"Destinos efetivos na rede completa: {m.destinos_efetivos:.2f}"))
    for aresta in rede.edges:
        i, j = aresta["from"], aresta["to"]
        peso = grafo[i][j]["weight"]
        aresta.pop("value", None)
        relacao = "→" if grafo.is_directed() else "↔"
        aresta.update(weight=peso, width=.5 + 5 * math.sqrt(peso / max_peso) if max_peso else .5,
                      title=f"{i} {relacao} {j}: {peso:,.6g} Gg de CO₂")
    rede.set_options(json.dumps({
        "physics": {"enabled": False},
        "interaction": {"hover": True, "navigationButtons": True, "keyboard": True},
        "nodes": {"borderWidth": 1, "font": {"size": 14}},
        "edges": {"arrows": {"to": {"enabled": grafo.is_directed(), "scaleFactor": .6}},
                  "color": {"color": "#3f6f82", "opacity": .65}, "smooth": False}}))
    return rede


def exportar_pagina_arvores(caminho, resultados, resumo, proveniencia, raizes, isolados,
                           max_diversidade):
    """Publica somente esta exploração; não reexecuta a página principal."""
    repo = "https://github.com/G-Cintra/Redes/blob/main/"
    titulos = {"minima": "Árvore mínima bilateral", "maxima": "Árvore máxima bilateral",
               "dirigida": "Arborescência máxima dirigida"}
    descricoes = {
        "minima": "Minimiza a soma dos pesos, conectando as atividades por relações de menor volume. Serve de contraste às seleções de maior peso.",
        "maxima": "Maximiza a soma dos pesos mantendo a conexão entre atividades, sem ciclos. Cada ligação soma os dois sentidos: Pᵢⱼ + Pⱼᵢ.",
        "dirigida": "Maximiza a soma das emissões nas setas selecionadas. Cada atividade conectada recebe uma única seta, exceto a raiz. A raiz resulta da otimização e não indica origem causal da economia."}
    tabela = resumo.rename(columns={"abordagem": "Abordagem", "nos": "Nós", "ligacoes": "Ligações",
        "componentes": "Componentes", "peso_gg": "Peso selecionado (Gg)",
        "participacao_pct": "Peso intersetorial preservado (%)"}).to_html(index=False, border=0,
            float_format=lambda x: f"{x:,.6g}")
    cards = []
    for chave in resultados:
        extra = f" Raiz: {escape(', '.join(raizes))}." if chave == "dirigida" else ""
        cards.append(f'<section id="{chave}"><h2>{titulos[chave]}</h2><p>{descricoes[chave]}{extra}</p>'
                     f'<iframe src="arvores/{chave}.html" title="{titulos[chave]}" loading="lazy"></iframe>'
                     f'<p><a href="arvores/{chave}.csv" download>Baixar ligações (CSV)</a></p></section>')
    html = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Árvores geradoras · Emissões brasileiras</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f5f1;color:#17374b;font:16px/1.6 system-ui,sans-serif}}
main{{max-width:1250px;margin:auto;padding:28px}}h1{{font-size:clamp(28px,4vw,42px);line-height:1.2}}
h2{{font-size:24px}}a{{color:#087f8c}}section,details{{background:white;border:1px solid #d4deda;border-radius:12px;padding:24px;margin:24px 0}}
iframe{{width:100%;height:800px;border:0}}.tabela{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}
th,td{{padding:10px;text-align:left;border-bottom:1px solid #d4deda}}summary{{cursor:pointer}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
.escala{{display:inline-block;width:130px;height:12px;background:linear-gradient(to right,#440154,#31688e,#35b779,#fde725)}}
@media(max-width:600px){{main{{padding:12px}}section,details{{padding:14px}}iframe{{height:680px}}}}
</style></head><body><main>
<h1>Árvores geradoras na matriz P</h1>
<p>Três seleções de ligações entre as 67 atividades brasileiras, sem agregação. A diagonal é omitida da seleção; as relações incluem efeitos diretos e indiretos atribuídos à demanda final.</p>
<p><a href="{repo}README.md#nota-metodológica">Notas metodológicas</a> · <a href="{repo}README.md#terminologia">Terminologia</a> · <a href="{repo}analise_arvores_emissoes.ipynb">Notebook</a></p>
<nav><a href="#minima">Mínima</a> · <a href="#maxima">Máxima</a> · <a href="#dirigida">Dirigida</a> · <a href="#comparacao">Comparação</a></nav>
<p>Área: emissões próprias na P completa. Espessura: peso da ligação em Gg de CO₂, em escala comum. Cor: diversidade de destinos na rede original, do roxo ao amarelo <span class="escala"></span> (0 a {max_diversidade:.2f}). Nas árvores bilaterais, o peso soma os dois sentidos; na dirigida, a seta aponta da emissora i ao destino j.</p>
<p>Cada desenho usa Kamada–Kawai sobre sua própria árvore, com distâncias medidas pelo número de ligações. As posições não representam distâncias econômicas. Arraste os nós e use zoom; passe o mouse para consultar valores. O losango marca emissão zero, sem área proporcional. Atividade isolada: {escape(', '.join(isolados))}.</p>
{''.join(cards)}
<section id="comparacao"><h2>Comparação das seleções</h2><div class="tabela">{tabela}</div>
<p>O denominador é a soma de P sem diagonal. Nas árvores bilaterais, cada par é contado uma vez com o peso dos dois sentidos; na dirigida, contam-se apenas as setas selecionadas. As porcentagens medem cobertura do peso, não equivalência das estruturas.</p>
<p>O componente de 66 atividades gera 65 ligações; a atividade isolada permanece no desenho. As ligações omitidas continuam relevantes. Caminhos nas árvores não representam etapas produtivas, e os indicadores dos nós descrevem a rede completa.</p>
<a href="arvores/comparacao.csv" download>Baixar comparação (CSV)</a></section>
<details><summary>Entrada experimental e reprodução</summary><p>Foi usada uma cópia exata do CSV local de P. Seu hash diverge do manifesto canônico; esta exploração não resolve essa divergência nem substitui a entrada canônica. O notebook verifica o hash próprio da cópia antes de calcular.</p>
<pre>{escape(json.dumps(proveniencia, ensure_ascii=False, indent=2))}</pre>
<p>Execute o notebook a partir da raiz do repositório, com as dependências já declaradas. Ele gera esta página, os três desenhos e os CSVs.</p>
<p><a href="{repo}raw/experimento_arvores/P.csv">Cópia de P</a> · <a href="https://networkx.org/documentation/stable/reference/algorithms/tree.html">Algoritmos do NetworkX</a> · <a href="https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html">Layout Kamada–Kawai</a></p></details>
<footer><p><a href="exploracao_inicial.html">Exploração inicial →</a></p></footer>
</main></body></html>'''
    Path(caminho).write_text(html, encoding="utf-8")
