# Rede intersetorial de emissões no Brasil

## Índice

[Apresentação](#apresentacao) · [Nota metodológica](#nota-metodológica) · [Terminologia](#terminologia) · [Exploração inicial](#exploração-inicial) · [Código fonte](#código-fonte) · [Referências](#referências) · [Reprodução da análise](#reprodução-da-análise)

<a id="apresentacao"></a>

Os processos produtivos geram externalidades ambientais. A percepção geral é de que os níveis atuais de produção são insustentáveis e de que estamos caminhando para mudanças climáticas irreversíveis ([Armstrong McKay et al., 2022](https://doi.org/10.1126/science.abn7950)).

Entre essas externalidades, as emissões de dióxido de carbono (CO₂) ocupam posição central no debate sobre mudanças climáticas e constituem o foco deste ensaio.

Para poder controlar as emissões e mitigar seus efeitos, é essencial que possamos quantificá-las de forma a atribuir responsabilidades aos agentes econômicos envolvidos ([Marques et al., 2012](https://doi.org/10.1016/j.ecolecon.2012.09.010)).

Há ampla discussão sobre os critérios utilizados para mensurar as emissões e atribuir responsabilidade aos agentes econômicos envolvidos. A metologia estabelecida no protocolo de Kyoto ([UNFCCC, 2008](https://unfccc.int/resource/docs/publications/08_unfccc_kp_ref_manual.pdf)) é amplamente utilizada e atribui a responsabilidade ao território onde as emissões foram realizadas.

Diversos estudos foram feitos para contabilizar as emissões brasileiras, incluindo trabalhos recentes de [Sanguinet e Azzoni (2024)](https://doi.org/10.1016/j.rspp.2024.100015) e [Montoya et al. (2026)](https://doi.org/10.1007/s10668-024-05251-8). Esses estudos permitem identificar os setores responsáveis pelos maiores volumes de emissões, mas não evidenciam a estrutura das relações intersetoriais associadas a essas emissões.

O presente ensaio propõe uma análise de redes para explorar a estrutura intersetorial das emissões atribuídas à produção brasileira. A análise busca identificar não apenas quais setores concentram os maiores volumes de emissões, mas também como essas emissões se distribuem ao longo da cadeia produtiva.

A primeira hipótese é de que os setores com maiores níveis de emissões estejam amplamente conectados à estrutura produtiva.

A segunda hipótese é de que existam setores com baixos níveis de emissões diretas, mas cuja produção dependa de insumos provenientes de múltiplos setores intensivos em emissões.

A rede será construída a partir da MIP 2015, nível 67 ([IBGE](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9085-matriz-de-insumo-produto.html)), utilizando coeficientes de emissão propostos por [Sanguinet e Azzoni (2024)](https://doi.org/10.1016/j.rspp.2024.100015) e adotando a abordagem de responsabilidade baseada na produção discutida por [Marques et al. (2012)](https://doi.org/10.1016/j.ecolecon.2012.09.010) e adotada no protocolo de Kyoto ([UNFCCC, 2008](https://unfccc.int/resource/docs/publications/08_unfccc_kp_ref_manual.pdf)). As relações entre os setores serão representadas por uma rede ponderada pelos volumes de emissões atribuídos às relações intersetoriais. A análise será feita em Python, utilizando a biblioteca NetworkX. O código-fonte e os resultados serão disponibilizados no [repositório do projeto](https://github.com/G-Cintra/Redes).

A partir dos resultados, serão discutidas possíveis implicações para políticas públicas e tecnologias de mitigação, considerando as propostas apresentadas por [Rissman et al. (2020)](https://doi.org/10.1016/j.apenergy.2020.114848).

## Nota metodológica

O [notebook da MIP](analise_matriz_insumo_produto.ipynb) constrói a matriz de emissões $P$ a partir da matriz insumo-produto brasileira de 2015. Essa matriz é a entrada da análise de redes.

A sequência abaixo resume as operações implementadas. Os símbolos e suas unidades estão reunidos na seção [Terminologia](#terminologia).

### Derivação da matriz P

**1. Dados de produção e uso.** Carregam-se $V$ da Tabela 01, $U$ da Tabela 03 e $D$ da Tabela 13 do IBGE. Calculam-se $x$ e $q$ a partir de $V$; a expressão de $D$ abaixo explicita o cálculo das participações publicadas.

$$
x=V^\top\mathbf{1},\qquad q=V\mathbf{1},\qquad D=V^\top\operatorname{diag}(q)^{-1}.
$$

**2. Transações e demanda final por atividade.** Aplicam-se as participações de $D$ aos usos intermediários e à demanda final por produto:

$$
Z=DU,\qquad y=Dy^{\mathrm{prod}},\qquad x=Z\mathbf{1}+y.
$$

As compras registradas por produto são atribuídas às atividades fornecedoras conforme as participações de $D$. O notebook verifica o fechamento entre produção bruta, vendas intermediárias e demanda final.

**3. Coeficientes técnicos e encadeamentos.** Cada coluna de $Z$ é dividida pela produção bruta da compradora:

$$
A=Z\operatorname{diag}(x)^{-1},\qquad L=(I-A)^{-1},\qquad x=Ly.
$$

O notebook confere $A$ e $L$ com as Tabelas 14 e 15 do IBGE e verifica a identidade $x=Ly$.

**4. Intensidades de emissão.** Estimam-se os coeficientes de 2015 por interpolação linear dos valores de 2011 e 2018 de Sanguinet e Azzoni (2024):

$$
\gamma^{2015}=\gamma^{2011}+\frac{4}{7}\left(\gamma^{2018}-\gamma^{2011}\right).
$$

Os coeficientes publicados são arredondados. Além disso, o notebook adota fator monetário 1 entre a base de preços dos coeficientes e os valores de 2015, sem deflação efetiva; os níveis de emissão são, portanto, aproximações.

**5. Emissões por origem e destino da demanda final.** Primeiro, $L\operatorname{diag}(y)$ distribui a produção requerida entre os destinos finais. Depois, cada linha é multiplicada pela intensidade da atividade emissora:

$$
\boxed{P=\operatorname{diag}(\gamma)\,L\,\operatorname{diag}(y).}
$$

O cálculo atribui as emissões geradas no Brasil aos destinos da demanda final por produtos nacionais, incluindo exportações.

### Como interpretar a matriz P

Em $P_{ij}$, **$i$ identifica quem emite e $j$, a atividade cujo produto atende à demanda final**. O destino não é necessariamente o comprador direto do insumo.

| Expressão | Significado |
| --- | --- |
| $P_{ij}=\gamma_iL_{ij}y_j$ | Emissões geradas em $i$ e atribuídas à demanda final pelos produtos de $j$, pelos encadeamentos diretos e indiretos. |
| $P_{ii}$ | Emissões geradas em $i$ e atribuídas à demanda final pelos produtos da própria atividade. Não é simplesmente o insumo comprado pela atividade de si mesma. |
| $\sum_j P_{ij}=\gamma_i x_i$ | Soma da linha: todas as emissões próprias da atividade $i$, qualquer que seja o destino final. Inclui a diagonal. |
| $\sum_i P_{ij}$ | Soma da coluna: emissões de todas as atividades brasileiras atribuídas à demanda final pelos produtos de $j$. Inclui a diagonal. |
| $\sum_{i\ne j}P_{ij}$ | Soma da coluna sem diagonal: a parcela anterior gerada nas outras atividades. Não cobre os insumos necessários para toda a produção de $j$. |

Por exemplo, $P_{\text{cimento, construção}}$ reúne emissões **geradas na fabricação de cimento** para atender à demanda final por construção, tanto pelo fornecimento direto quanto por caminhos indiretos existentes na estrutura produtiva. As emissões geradas em outras atividades desses caminhos aparecem em suas respectivas linhas. Já a coluna cimento considera somente a demanda final por cimento, não o cimento utilizado como insumo pela construção ou por outras atividades.

A soma da linha e a soma da coluna de uma mesma atividade geralmente diferem; apenas o total de todas as linhas coincide necessariamente com o total de todas as colunas. No gráfico setorial atual, a barra azul usa a linha completa e a laranja, a coluna sem diagonal. Elas representam perspectivas distintas: sua soma não deve ser interpretada como emissões próprias mais emissões dos insumos de toda a produção da atividade, nem agregada entre setores como um total físico sem sobreposição.

## Terminologia

Os valores monetários estão em R$ milhões e as emissões, em Gg de CO₂ (mil toneladas). Os índices $p$, $i$ e $j$ identificam produtos e atividades, conforme os eixos de cada matriz.

**Notação matricial:** $\operatorname{diag}(v)$ é a matriz diagonal formada pelo vetor $v$; $\mathbf{1}$ é um vetor de uns com dimensão compatível; $I$ é a matriz identidade; $V^\top$ é a transposta de $V$. Multiplicar uma matriz por $\mathbf{1}$ à direita soma suas linhas.

**Matriz de produção ($V$):** registra o valor produzido de cada produto por cada atividade. As linhas representam os 127 produtos e as colunas, as 67 atividades; $V_{pi}$ é a produção do produto $p$ pela atividade $i$.

**Matriz de uso intermediário nacional ($U$):** registra os produtos nacionais utilizados como insumos por cada atividade compradora (Tabela 03). Tem 127 produtos nas linhas e 67 atividades nas colunas.

**Produção por produto ($q$):** valor total produzido de cada produto, obtido pela soma de sua linha em $V$: $q_p=\sum_i V_{pi}$.

**Matriz de participação na produção ($D$):** participação de cada atividade na produção nacional de cada produto (Tabela 13). Tem 67 atividades nas linhas e 127 produtos nas colunas; $D_{ip}=V_{pi}/q_p$.

**Matriz de transações intermediárias ($Z$):** registra o valor dos insumos nacionais fornecidos entre as 67 atividades. As linhas representam as fornecedoras e as colunas, as compradoras; $Z_{ij}$ é o fornecimento da atividade $i$ à atividade $j$.

**Demanda intermediária ($d^{\mathrm{int}}$):** bens e serviços fornecidos como insumos às atividades produtivas. Para a atividade fornecedora $i$, corresponde à soma de sua linha em $Z$:

$$
d_i^{\mathrm{int}} = \sum_{j=1}^{67} Z_{ij}.
$$

**Demanda final doméstica ($y_{\mathrm{dom}}$):** consumo das famílias, governo e instituições sem fins lucrativos a serviço das famílias, formação bruta de capital fixo e variação de estoques, no Brasil.

**Exportações ($y_{\mathrm{exp}}$):** produtos nacionais destinados ao exterior.

**Demanda final total ($y$):** soma da demanda final doméstica e das exportações de produtos nacionais, por atividade: $y = y_{\mathrm{dom}} + y_{\mathrm{exp}}$. Neste texto, “demanda final” refere-se a esse total.

**Demanda final por produto ($y^{\mathrm{prod}}$):** o mesmo conjunto de usos finais, registrado por produto na Tabela 03. A matriz $D$ converte esse vetor de 127 produtos em $y$, com 67 atividades.

**Produção bruta ($x$):** valor total produzido pela atividade, destinado aos usos intermediários e finais. É a soma da coluna da atividade em $V$ e corresponde à soma de suas vendas intermediárias com sua demanda final:

$$
x_i = \sum_{p=1}^{127} V_{pi} = d_i^{\mathrm{int}} + y_i = \sum_{j=1}^{67} Z_{ij} + y_i.
$$

**Matriz de coeficientes técnicos ($A$):** insumos nacionais necessários por unidade de produção de cada atividade compradora. Cada elemento é $A_{ij}=Z_{ij}/x_j$; a matriz tem dimensão $67\times67$ e coeficientes adimensionais.

**Inversa de Leontief ($L$):** requisitos diretos e indiretos de produção, calculados por $L=(I-A)^{-1}$. O elemento $L_{ij}$ mede a produção de $i$ necessária por unidade de demanda final de $j$; a matriz tem dimensão $67\times67$ e coeficientes adimensionais.

**Intensidade de emissão ($\gamma$):** emissões diretas por unidade de produção bruta de cada atividade, em Gg de CO₂ por R$ milhão.

**Matriz de emissões ($P$):** emissões brasileiras modeladas por atividade emissora (linhas) e atividade da demanda final (colunas). Tem dimensão $67\times67$, em Gg de CO₂, e cobre a produção nacional destinada à demanda final doméstica e às exportações.

## Exploração inicial

[Resultados preliminares e exploratórios.](https://g-cintra.github.io/Redes/)

## Código Fonte

O código fonte foi estruturado a partir dos notebooks abaixo:

- [**Matriz insumo-produto**](analise_matriz_insumo_produto.ipynb): carrega a MIP e calcula a matriz de emissões. *[Versão revisada e validada.]*
- [**Análise de redes**](analise_redes_emissoes.ipynb) e [**análise de interativa**](analise_redes_interativas.ipynb): realizam a análise de redes e as visualizações gráficas. *[Versão prelimnar, pendente revisão e validação.]*

## Referências

1. **Armstrong McKay, D. I. et al. (2022).** [*Exceeding 1.5°C global warming could trigger multiple climate tipping points*](https://doi.org/10.1126/science.abn7950). *Science*, 377, eabn7950.
2. **IBGE.** [*Matriz de Insumo-Produto: Brasil, 2015*](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9085-matriz-de-insumo-produto.html).
3. **Marques, A.; Rodrigues, J.; Lenzen, M.; Domingos, T. (2012).** [*Income-based environmental responsibility*](https://doi.org/10.1016/j.ecolecon.2012.09.010). *Ecological Economics*, 84, 57–65.
4. **Miller, R. E.; Blair, P. D. (2009).** [*Input–Output Analysis: Foundations and Extensions*](https://doi.org/10.1017/CBO9780511626982). 2ª ed. Cambridge University Press.
5. **Montoya, M. A.; Bertussi, L. A. S.; Allegretti, G.; Talamini, E. (2026).** [*Brazilian energy and carbon footprints: structural changes and sectoral contributions to climate change*](https://doi.org/10.1007/s10668-024-05251-8). *Environment, Development and Sustainability*, 28, 6725–6755.
6. **Rissman, J. et al. (2020).** [*Technologies and policies to decarbonize global industry: Review and assessment of mitigation drivers through 2070*](https://doi.org/10.1016/j.apenergy.2020.114848). *Applied Energy*, 266, 114848.
7. **Sanguinet, E. R.; Azzoni, C. R. (2024).** [*Carbon emissions drivers in Brazilian regional production chains: Value-added and consumption-based approaches*](https://doi.org/10.1016/j.rspp.2024.100015). *Regional Science Policy & Practice*, 16, 100015.
8. **UNFCCC (2008).** [*Kyoto Protocol reference manual on accounting of emissions and assigned amount*](https://unfccc.int/resource/docs/publications/08_unfccc_kp_ref_manual.pdf). United Nations Framework Convention on Climate Change.

## Reprodução da análise

Os notebooks podem ser executados em qualquer ambiente com suporte a Python e Jupyter. Clone esse repositório, prepare o ambiente com as dependências e versões especificadas em [requirements.txt](requirements.txt).

Execute integralmente as células de cada notebook, na ordem em que aparecem, seguindo esta sequência:

1. [**Matriz insumo-produto**](analise_matriz_insumo_produto.ipynb): prepara os dados e exporta a matriz de emissões atribuídas à produção brasileira e o catálogo de setores.
2. [**Análise de redes**](analise_redes_emissoes.ipynb): utiliza esses arquivos para construir a rede, calcular os indicadores e gerar as visualizações.

Os arquivos de entrada são verificados por SHA-256 conforme o [manifesto](raw/manifesto.csv), portanto mantenha os arquivos com permissões apenas para leitura. As hipóteses e decisões metodológicas estão documentadas nos notebooks. A execução da análise de redes gera as tabelas em `outputs/redes/` e a página interativa em `docs/index.html`.


### Redes interativas

Execute `analise_redes_interativas.ipynb` após exportar os dados da MIP. O notebook verifica as entradas pelo manifesto, agrega P em 20 atividades e Outras e cria o grafo NetworkX antes de renderizar com PyVis. Os arquivos `docs/redes_interativas/circular.html` e `forcas.html` alimentam os dois cards interativos em `docs/index.html`; reexecutar o notebook atualiza esses cards. Instale as dependências de `requirements.txt` no mesmo ambiente do notebook.
