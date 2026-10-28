# Rede intersetorial de emissões no Brasil

**Trabalho atual da disciplina:** [planejamento acadêmico](entrega_final/02_planejamento_academico.md) e [texto da entrega](entrega_final/entrega/main.tex). A entrega está em elaboração: a seção de resultados e os painéis do anexo estão redigidos; resumo, discussão e conclusões permanecem pendentes.

**Notebook da implementação em etapas:** [analise_redes_2015.ipynb](entrega_final/analise_redes_2015.ipynb). As etapas implementadas leem as entradas canônicas, constroem e validam F com a diagonal preservada e representam suas relações intersetoriais em W e em um grafo dirigido ponderado. Os 67 nós, as arestas positivas, os pesos e a ausência de laços são conferidos, inclusive pela reconstrução exata de W a partir do grafo. Abra com o kernel Python do ambiente do projeto (`.venv`) e execute as células em ordem, a partir da raiz ou de `entrega_final/`. As verificações e seus resíduos ficam visíveis no notebook; a execução inclui forças, graus, densidade, disparidade e número efetivo da rede completa, com validações e leitura dos resultados, e aplica o filtro de disparidade para alfa 0,01, 0,05 e 0,10, com validação, cobertura por atividade e sensibilidade. O notebook inclui o desenho completo do backbone de alfa 0,05 e um quadro comparativo de volume, concentração, graus com sensibilidade e cobertura; as figuras PNG/SVG ficam em `entrega_final/figuras/`. Não há exportação sobre resultados históricos. É uma versão de trabalho, e a base ambiental permanece um cenário exploratório.

**Reprodução do relatório:** execute o notebook acima até a seção 24 para exportar as oito figuras vetoriais usadas no texto, preservando as mesmas arestas e pesos. Em `entrega_final/entrega/`, compile `main.tex` com `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` (LaTeX e Biber). O texto dos resultados está em `resultados.tex`, e os painéis completos, em `anexos.tex`. As figuras globais de matriz e rede são repartidas em painéis para leitura em A4; as 62 saídas de energia continuam em duas páginas, sem outro filtro.

**Status dos notebooks:** os notebooks deste repositório são exploratórios e versões de trabalho. Registram etapas, exemplos didáticos, alternativas metodológicas e resultados preliminares; podem usar notações e escolhas diferentes entre versões. Sua existência ou execução não significa que seus métodos, figuras e conclusões tenham sido incorporados à entrega. Para o escopo atual, consultar o planejamento acima e as definições do texto da entrega. Os coeficientes ambientais atuais permanecem sujeitos às limitações da [auditoria](docs/auditoria_coeficientes_emissoes_2015.md).

A [especificação da investigação anterior de 2015](docs/especificacao_final_pesquisa_2015.md) e as seções abaixo são preservadas como histórico de trabalho e não substituem o planejamento atual.

## Índice

- [Resumo](#resumo)
- [Exploração inicial](#exploração-inicial)
- [Nota metodológica](#nota-metodológica)
- [Terminologia](#terminologia)
- [Código fonte](#código-fonte)
- [Referências](#referências)
- [Reprodução da análise](#reprodução-da-análise)

## Resumo

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

## Exploração inicial

[Notebook exploratório v4 — matriz F](analise_exploratoria_v4.ipynb): cópia inicial da v3 para continuarmos a exploração da matriz F. Execute as células em ordem, na raiz do repositório.

[Diagrama da MIP brasileira de 12 setores](diagrama_mip12.ipynb): análise independente com os fluxos oficiais de 2015, sem calibração, incluindo todas as conexões e a diagonal. Execute da raiz; as duas redes, o Sankey, as matrizes e a proveniência são exportados para `outputs/mip12_real/`. As emissões são estimadas com os coeficientes do projeto, agregados de 67 para 12 atividades; o notebook explicita o mapeamento e valida os balanços.

[Sankeys completos das MIPs de 20 e 67 atividades](sankeys_mip20_67.ipynb): execute da raiz para gerar os dois diagramas e as matrizes em `outputs/sankeys_mip20_67/`. Todas as parcelas positivas de F são preservadas, inclusive a diagonal, com escala de cores comum e nomes completos. A agregação dos coeficientes para 20 atividades e as limitações das estimativas são documentadas no notebook.

[Rede circular de atribuição da MIP de 67 setores](rede_circular_atribuicao_mip67.ipynb): execute da raiz para gerar PNG, SVG, PDF, matriz F, tabela setorial e auditoria em `outputs/rede_circular_atribuicao_mip67/`. A área representa emissões pela produção; a cor, atribuição ao consumo; os círculos seguem ordem decrescente de área no sentido horário, começando no topo. Todas as 4.357 parcelas positivas de F, incluindo a diagonal, são preservadas. Um nó terminal reúne as contas da demanda final sem somá-las novamente a F; as conexões representam atribuições contábeis, não transações monetárias diretas.

[Resultados preliminares e exploratórios.](https://g-cintra.github.io/Redes/)

O [notebook de concentração e dependência](analise_concentracao_dependencia.ipynb) responde se os maiores emissores brasileiros também têm amplo alcance nas cadeias das demais atividades. Execute-o da raiz após exportar P pelo notebook da MIP. Ele compara concentração das emissões próprias, participações por destino e compras diretas nacionais, com sensibilidade aos limiares, e gera `outputs/concentracao_dependencia/concentracao_dependencia.html`.

A [análise de similaridade do consumo](similaridade_consumo/similaridade_consumo.ipynb) carrega a matriz C exportada pelo notebook da MIP e calcula a similaridade de cosseno entre linhas e entre colunas. Execute suas células na ordem após gerar `outputs/matriz_emissoes_consumo_2015.csv`; as duas matrizes de similaridade são salvas na pasta do notebook. As seções finais geram um Sankey de C sem diagonal, mapas de similaridade dos perfis completos e rankings de pares, reunidos em `similaridade_consumo/sankey_similaridade_C.html`. A seção 9 gera `similaridade_consumo/similaridade_3d_C.html`, com projeções 3D dos perfis normalizados e diagnósticos da perda de informação. O [notebook de clusters](similaridade_consumo/analise_clusters_C.ipynb) avalia partições globais, pequenos grupos de alta similaridade e sensibilidade à diagonal e à ponderação, gerando `similaridade_consumo/clusters_C.html`.

## Nota metodológica

O [notebook da MIP](analise_matriz_insumo_produto.ipynb) constrói a matriz de emissões $P$ a partir da matriz insumo-produto brasileira de 2015. Essa matriz é a entrada da análise de redes.

A sequência abaixo resume as operações implementadas. Os símbolos e suas unidades estão reunidos na seção [Terminologia](#terminologia).

### Derivação da matriz P

**1. Dados de produção e uso.** Carregam-se $V$ da Tabela 01, $U$ da Tabela 03 e $D$ da Tabela 13 do IBGE. Calculam-se $x$ e $q$ a partir de $V$; a expressão de $D$ abaixo explicita o cálculo das participações publicadas.

$$
x=V^\top\mathbf{1},\qquad q=V\mathbf{1},\qquad D=V^\top\mathrm{diag}(q)^{-1}.
$$

**2. Transações e demanda final por atividade.** Aplicam-se as participações de $D$ aos usos intermediários e à demanda final por produto:

$$
Z=DU,\qquad y=Dy^{\mathrm{prod}},\qquad x=Z\mathbf{1}+y.
$$

As compras registradas por produto são atribuídas às atividades fornecedoras conforme as participações de $D$. O notebook verifica o fechamento entre produção bruta, vendas intermediárias e demanda final.

**3. Coeficientes técnicos e encadeamentos.** Cada coluna de $Z$ é dividida pela produção bruta da compradora:

$$
A=Z\mathrm{diag}(x)^{-1},\qquad L=(I-A)^{-1},\qquad x=Ly.
$$

O notebook confere $A$ e $L$ com as Tabelas 14 e 15 do IBGE e verifica a identidade $x=Ly$.

**4. Intensidades de emissão.** Estimam-se os coeficientes de 2015 por interpolação linear dos valores de 2011 e 2018 de Sanguinet e Azzoni (2024):

$$
\gamma^{2015}=\gamma^{2011}+\frac{4}{7}\left(\gamma^{2018}-\gamma^{2011}\right).
$$

Os coeficientes publicados são arredondados. Além disso, o notebook adota fator monetário 1 entre a base de preços dos coeficientes e os valores de 2015, sem deflação efetiva; os níveis de emissão são, portanto, aproximações.

**5. Emissões por origem e destino da demanda final.** Primeiro, $L\mathrm{diag}(y)$ distribui a produção requerida entre os destinos finais. Depois, cada linha é multiplicada pela intensidade da atividade emissora:

$$
\boxed{P=\mathrm{diag}(\gamma)\,L\,\mathrm{diag}(y).}
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

**Notação matricial:** $\mathrm{diag}(v)$ é a matriz diagonal formada pelo vetor $v$; $\mathbf{1}$ é um vetor de uns com dimensão compatível; $I$ é a matriz identidade; $V^\top$ é a transposta de $V$. Multiplicar uma matriz por $\mathbf{1}$ à direita soma suas linhas.

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

## Investigação acadêmica: emissões e posição produtiva (2015)

O novo [notebook exploratório](investigacao_redes_emissoes_2015.ipynb) compara concentração das emissões próprias, centralidade de fornecedor, participação ambiental, diversidade de destinos e alternativas de extração e caminhos. Ele preserva as análises anteriores e documenta também os métodos descartados.

Execute suas células em ordem, a partir da raiz, após preparar as entradas canônicas conforme o manifesto. A execução reconstrói a MIP e gera o [relatório HTML autocontido](outputs/investigacao_redes_2015/relatorio.html), tabelas CSV e figuras PNG/SVG em `outputs/investigacao_redes_2015/`. O relatório gerado não precisa de conexão à internet para exibir figuras ou tabelas.

A conclusão exploratória distingue proeminência emissora de importância como fornecedor. As emissões são estimadas com intensidades interpoladas de 2011/2018; a compatibilidade de preços e a validação ambiental da fonte permanecem limitações para publicação. No novo notebook, `e = gamma * x` é a emissão própria, `H = diag(gamma) @ L` é intensidade e `P = H @ diag(y)` é atribuição por demanda final, evitando a ambiguidade de `C/c` nos notebooks anteriores.

Verificações específicas: `python -m unittest discover -s tests -p test_investigacao_2015.py -v`. A execução do notebook também confere balanços, conservação, as duas versões de extração e derivadas ambientais.

Para avaliação pelo repositório público, consulte o [roteiro de revisão independente](docs/revisao_investigacao_2015.md). O relatório, as tabelas e as figuras da investigação de 2015 estão versionados em `outputs/investigacao_redes_2015/`; as demais saídas continuam ignoradas pelo Git.

### Validação focal da interpretação

A etapa posterior está no [notebook de validação adversarial](validacao_emissao_centralidade_2015.ipynb) e no [relatório de validação](outputs/validacao_emissao_centralidade_2015/relatorio.html). Ela testa somente emissão própria × presença de fornecedor, com S como principal, A e HEM como robustezes finais, e L no suplemento. Execute o notebook da raiz; as matrizes e intensidades são conferidas contra a exploração anterior. A conclusão mantém a divergência dos rankings e a atenuação por tamanho, mas rejeita a universalidade do destaque de Energia sob HEM normalizada. Comércio também é uma exceção importante.

Testes específicos: `python -m unittest discover -s tests -p test_validacao_centralidade.py -v`. Todas as saídas desta etapa estão em `outputs/validacao_emissao_centralidade_2015/`, sem modificar as análises anteriores.
