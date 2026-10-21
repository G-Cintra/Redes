# Huang et al. (2019): leitura crítica e adaptação ao trabalho de redes

18/10/2026. Leitura do texto principal, metodologia, resultados e apêndices do [PDF local](../references/huang_et_al_2019/carbon_communities_hotspots_china.pdf), com conferência visual das equações e figuras metodologicamente críticas. A paginação citada é a impressa no artigo, de 1 a 29. Não foram reproduzidos os resultados nem auditados os dados originais dos autores.

**Referência:** Huang, L.; Kelly, S.; Lu, X.; Lv, K.; Shi, X.; Giurco, D. *Carbon Communities and Hotspots for Carbon Emissions Reduction in China*. Sustainability, 11(19), 5508, 2019. [DOI](https://doi.org/10.3390/su11195508). Proveniência do download no [README da referência](../references/huang_et_al_2019/README.md).

## 1. Parecer para o nosso projeto

O artigo é um precedente pertinente para construir uma rede dirigida a partir de F e extrair um backbone antes de estudar conectividade e comunidades. Não é uma receita integralmente reproduzível. Há ambiguidades operacionais e uma tensão entre a matriz de atribuição final definida na equação (4) e a interpretação de transmissão por etapas usada em exemplos e na discussão.

**Recomendação desta leitura:** manter o foco em origem emissora e produto final; recomendar uma rede dirigida de 67 atividades; avaliar o filtro de disparidade; distinguir volume de conectividade; deixar comunidades como extensão condicionada à robustez. Não incluir intermediação produtiva no núcleo sem consultar e validar sua referência original. O planejamento foi ajustado nesse sentido, como proposta para discussão, sem executar os métodos.

## 2. Resumo do estudo e mapa de leitura

| Elemento | O que o artigo faz | Onde conferir |
| --- | --- | --- |
| Motivação | Acrescentar uma perspectiva de transmissão às contas por produção e consumo | Introdução, pp. 1–2 |
| Dados | China, 2012; 30 atividades em 30 províncias; inventário originalmente com 45 atividades compatibilizado com a MRIO | Seção 2, pp. 2–3; Tabela A1, pp. 20–21 |
| Matriz | G = diag(k) L diag(f), com L = (I − A)⁻¹ | Seção 3.1, equação (4), p. 3 |
| Rede | Nós setor-província, arestas dirigidas com pesos positivos | Seção 3.1, pp. 3–4 |
| Redução | Disparity filter de Serrano et al., α = 0,05, regra de relevância em pelo menos uma extremidade; depois piso de uma tonelada | Seção 3.2, p. 4 |
| Comunidades | Otimização multinível de modularidade, citando Blondel et al. e R/igraph | Seção 3.3, pp. 4–5 |
| Posições | Grau e força de entrada/saída; intermediação adaptada por Liang et al. (2016) | Tabela 1, p. 5; Apêndice A.2, pp. 21–22 |
| Desenho | Gephi/OpenOrd; seleção adicional de arestas na Figura 1; agregação por comunidades na Figura 5 | Pp. 6, 11 e 15 |

Os autores reportam uma rede inicial de 900 nós e 774.391 arestas, redução para 886 nós, retenção aproximada de 7% das arestas e 93% do peso. Reportam 19 comunidades e modularidade 0,688. Eletricidade/calor, construção e metalurgia se destacam, respectivamente, nas perspectivas de saída, entrada e intermediação (seções 4 e 5).

Esses são resultados reportados, não metas para o Brasil. Os grupos do artigo têm forte componente provincial; sem dimensão regional, nossa aplicação não pode reproduzir sua interpretação territorial.

## 3. Correspondência exata com a nossa matriz

Na nossa notação:

$$F=\Phi L\widehat y,\qquad F_{ij}=\varphi_iL_{ij}y_j.$$

O G da equação (4) corresponde a F, k corresponde a φ e f à nossa demanda final y. A região associada à coluna identifica a atividade produtora do produto final, não necessariamente o território de residência do consumidor; o vetor f já soma destinos de demanda final na definição do artigo.

**Interpretação que adotamos:** emissão ocorrida em i e atribuída à demanda final pelos produtos de j, incluindo todas as rodadas de produção. Não é emissão de todos os fornecedores entregue diretamente ao comprador j, nem uma transação observada de CO₂.

Consequências derivadas para nosso projeto:

$$s_i^{out}(F)=\sum_jF_{ij}=c_i,\qquad s_i^{in}(F)=\sum_jF_{ji}=u_i.$$

As forças completas são as duas contas ambientais. Não são uma confirmação independente delas. A diferença entre atribuições é exatamente:

$$u_i-c_i=\sum_{j\ne i}F_{ji}-\sum_{j\ne i}F_{ij}.$$

Para estudar relações entre atividades distintas, propomos W com Wᵢⱼ = Fᵢⱼ para i ≠ j e diagonal zero. Então as forças são cᵢ − Fᵢᵢ e uᵢ − Fᵢᵢ, não os totais completos. O saldo permanece igual. Manter F integral nas contas e declarar a retirada da diagonal em W evita confundir essas medidas.

## 4. Leitura crítica: o que não devemos transportar automaticamente

### 4.1. Os exemplos de transmissão não são a rede da equação (4)

Na Figura 2 (p. 8), só A emite; B tem emissão própria zero, mas aparece com força de saída positiva e ligações para D, E e F. Sob a equação (4), φ_B = 0 implica F_Bj = 0 para todo j. Portanto, a figura pode ilustrar uma cadeia de transações com emissões incorporadas, mas não demonstra o grau de saída da matriz de atribuição definida pelo artigo.

Na Figura 3 (p. 9), D não atende à demanda final e aparece recebendo emissões. Sob a equação (4), y_D = 0 implica F_iD = 0. Novamente, o desenho de uma cadeia intermediária não é equivalente à rede de atribuição final.

Essas incompatibilidades são deduções a partir da equação e das hipóteses dos próprios exemplos, não uma reestimação dos dados chineses. Não demonstram que todo resultado numérico do artigo esteja errado. Exigem, porém, abandonar a identificação automática entre grau em F e capacidade de transmitir emissões ao longo de etapas produtivas.

### 4.2. A intermediação não é a função usual do NetworkX

O Apêndice A.2.3 (p. 22) reconhece que o indicador clássico de caminhos mínimos não tem a interpretação pretendida e remete a Liang, Qu e Xu (2016). Mas escreve bᵢ = f T Jᵢ T y e descreve Jᵢ como diagonal com todos os elementos diagonais iguais a um. Tomada literalmente, Jᵢ = I para qualquer i, e o resultado não varia por setor. Isso é uma inconsistência de especificação, possivelmente editorial, que impede implementar a fórmula impressa como está.

Não corrigir silenciosamente Jᵢ, não inferir o algoritmo dos rankings e não substituir por `nx.betweenness_centrality(F)`. Uma eventual análise de transmissão exige leitura da referência original, derivação própria e outro estimando claramente identificado. Também é incorreto generalizar que betweenness só exista para redes não dirigidas e não ponderadas: a questão relevante é a interpretação dos caminhos e pesos.

**Atualização após consulta à fonte original:** a [leitura de Liang et al. (2016)](referencias/leitura_critica_liang_2016.md), p. 1332, confirma que Jᵢ tem somente (i,i) igual a um e todos os demais elementos zero. A definição esclarece a inconsistência da descrição de Huang; não transforma b em betweenness de caminhos mínimos sobre F. Sua inclusão no trabalho continua sendo uma decisão separada.

### 4.3. A filtragem define outro objeto analítico

O filtro seleciona saliência frente a um modelo nulo local; não estima erro de medição, não identifica causalidade e não certifica emissões. Chamar toda ligação retirada de ruído é mais forte do que o método permite. Pesos pequenos podem representar relações contábeis legítimas.

Após a filtragem, grau significa número de relações selecionadas. Força significa peso retido. As correlações de 0,94/0,96 entre forças e contas ambientais reportadas nas pp. 7–8 não são evidência de novas contas: a filtragem e o tratamento dos laços alteram somas que, em F completa, correspondem às identidades acima.

### 4.4. Comunidades não estão inteiramente especificadas

A referência a Blondel e ao algoritmo multinível sugere a família Louvain, mas não basta para reproduzir exatamente a aplicação: faltam detalhes suficientes sobre função/versão, tratamento da direção, pesos, laços, semente e estabilidade. Não se deve presumir que uma função multinível citada operou como modularidade dirigida sem conferir a implementação usada.

O artigo caracteriza Q como variando de zero a um (p. 11); essa não é uma propriedade geral da modularidade, que pode ser negativa. Um Q alto em uma partição otimizada não demonstra por si só comunidades naturais, significância ou estabilidade. Devemos explicitar modelo nulo, resolução e sensibilidade; não buscar 19 comunidades nem Q = 0,688.

### 4.5. A figura tem um corte além do backbone

A p. 6 descreve uma exclusão adicional na Figura 1, expressa como “100,000 thousand tons”. A leitura literal é 100 milhões de toneladas, acima do máximo de 82,95 milhões informado na p. 5. Há uma inconsistência aparente de unidade/limiar que não foi resolvida nesta leitura. A ilustração não é uma especificação segura de corte para copiar.

O PDF também contém duplicações de camadas de texto em algumas páginas; conferimos visualmente as passagens críticas. No nosso trabalho, publicar a lista das arestas desenhadas e sua cobertura evita depender de uma legenda ambígua. Proximidade no layout não é distância econômica.

### 4.6. Limites empíricos e normativos

Os totais de produção e consumo reportados nas Tabelas A4/A8 usam denominadores que não coincidem, enquanto uma única matriz fechada tem somas de linhas e colunas iguais. A relação exata dessas colunas com a matriz analisada exige esclarecimento; não assumir que todas as tabelas usem a mesma conta e fronteira.

As propostas de mitigação do artigo são interpretações dos autores. Grau, força ou comunidade não estimam custo de abatimento, substituição, bem-estar ou efeito causal de intervenção. Nosso resultado pode indicar relações a investigar para coordenação, não definir política ótima.

## 5. Ferramentas a trazer para nosso contexto

| Ferramenta | Uso recomendado | Adaptação ou limite |
| --- | --- | --- |
| Rede dirigida ponderada | Um nó por atividade, peso de origem emissora para produto final | 67 nós; papéis distintos na interpretação, sem exigir duplicação bipartida |
| Disparity filter | Selecionar relações localmente desproporcionais, preservando diferentes escalas | Avaliar em W sem laços; comparar perspectivas de saída e entrada |
| Grau de saída/entrada | Número de destinos/origens no backbone | Conectividade selecionada, não clientes/fornecedores diretos nem transmissão |
| Força de saída/entrada | Volume completo, externo e retido | Informar qual matriz; não chamar identidades de descoberta |
| Comparação de postos | Contrastar volume e conectividade | Descritiva, com empates e sensibilidade ao filtro |
| Comunidades e rede agregada | Possível estrutura mesoscópica e desenho mais legível | Etapa complementar, dependente de especificação e robustez |
| Intermediação adaptada | Não integra o núcleo proposto | Referência original e validação adicionais necessárias |
| Corte de uma tonelada e OpenOrd | Não importar automaticamente | Outro tamanho, unidade e objetivo; layout não é método de inferência |

### 5.1. Proposta operacional de filtro, ainda a validar

Se sᵢᵒᵘᵗ > 0 e sⱼⁱⁿ > 0 em W, definir pᵢⱼᵒᵘᵗ = Wᵢⱼ/sᵢᵒᵘᵗ e pᵢⱼⁱⁿ = Wᵢⱼ/sⱼⁱⁿ. Na formulação usual do filtro para grau k > 1, a probabilidade de cauda é (1 − p)^(k − 1). Esse desenvolvimento remete a Serrano et al. (2009), não está detalhado por Huang. Sua derivação e os casos k = 0/1 precisam ser conferidos antes do código.

Como referência inicial, avaliar α = 0,05 e regra OU: reter se a ligação se destaca na saída da origem **ou** na entrada do destino. Comparar α = 0,01 e 0,10; a regra E pode ser diagnóstico complementar se houver justificativa. Não selecionar α pela quantidade visualmente conveniente de arestas. Não aplicar piso absoluto sem fundamento material, precisão da base e unidade explícitos. Isolados continuam identificados.

Não há garantia de conectividade, de cobertura de peso ou de preservação de cada setor. Reportar essas perdas globalmente e por nó. O filtro não é um ajuste de múltiplos testes nem gera confiança de 95% sobre a verdade de uma ligação ambiental.

### 5.2. Consequência algébrica importante para interpretar o filtro

Esta é uma dedução para a nossa aplicação, não um resultado reportado por Huang. Para intensidades positivas e perfis definidos, na normalização de saída de W:

$$\frac{W_{ij}}{\sum_{h\ne i}W_{ih}}=\frac{L_{ij}y_j}{\sum_{h\ne i}L_{ih}y_h}.$$

A intensidade φᵢ cancela. O filtro apenas de saída descreve a composição dos destinos do emissor, não seu nível absoluto de intensidade ambiental. Na normalização de entrada, yⱼ cancela:

$$\frac{W_{ij}}{\sum_{h\ne j}W_{hj}}=\frac{\varphi_iL_{ij}}{\sum_{h\ne j}\varphi_hL_{hj}}.$$

A seleção de entrada descreve a composição emissora da pegada por unidade de demanda do destino. A regra OU combina esses dois critérios, não remove toda influência ambiental ou de escala. Zeros e mudanças no suporte precisam ser tratados separadamente. Esse fato deve orientar a interpretação das associações entre volume e grau.

### 5.3. Como avaliar sem confundir as redes

1. **F integral:** contas c, u, diagonal e diferenças de participação, preservando o total.
2. **W sem diagonal:** relações entre atividades, forças externas e diagnóstico de pesos.
3. **Bα:** backbone ponderado, graus, forças retidas e cobertura de cada perfil.
4. **Objeto gráfico:** igual a Bα, salvo seleção adicional explicitada e exportada.

Comparar fração de arestas e peso retidos, isolados, componentes, cobertura por origem/destino e estabilidade das ligações/postos. Uma comparação de conjuntos por Jaccard é possível, mas estabilidade de graus sob limiares aninhados não prova adequação do modelo nulo. Não adotar uma meta de 93% de peso porque o artigo a atingiu.

Se comunidades forem úteis, recomendar modularidade dirigida ponderada explicitada, com parâmetro de resolução e sementes registrados. Avaliar mais de uma semente/resolução e comparar rede completa externa e backbone. Usar a partição para agregar **W completa**, além de informar o resultado filtrado, permite medir quanto a estrutura também explica fora da seleção. Não afirmar significância estatística sem definir e avaliar uma comparação nula apropriada.

## 6. Reformulação acadêmica recomendada

**Tema:** volume e conectividade nas relações intersetoriais de atribuição de CO₂.

**Pergunta principal:** em que medida os setores com maiores volumes de emissões próprias e de emissões atribuídas à demanda final também concentram maior número de relações localmente relevantes, como origens e destinos, na rede brasileira de 2015?

**Objetivo geral:** comparar volume e conectividade de origens emissoras e destinos finais, utilizando um backbone fundamentado de rede dirigida ponderada, e interpretar suas diferenças à luz das duas atribuições ambientais.

**Hipótese de trabalho H1:** a ordenação dos setores pelo volume de emissões próprias não reproduz integralmente sua ordenação pelo número de destinos relevantes no backbone.

**Hipótese de trabalho H2:** a ordenação dos produtos finais pela pegada não reproduz integralmente sua ordenação pelo número de origens relevantes no backbone.

São expectativas descritivas formuladas após exploração, não hipóteses confirmatórias pré-registradas. Avaliar concordância global, magnitude das diferenças e estabilidade; poucas inversões não bastam como apoio substantivo. Não há corte arbitrário de correlação que “prove” as hipóteses. Coincidência elevada e diferenças pequenas enfraquecem a expectativa, e isso é um resultado aceitável. Se o filtro tornar a comparação pouco informativa, registrar o diagnóstico e reconsiderar o desenho antes de acrescentar métricas.

**Questão complementar:** há agrupamentos estáveis de atividades nas relações de atribuição e que leitura adicional oferecem? Não tornar comunidades obrigatórias antes de demonstrar sua utilidade.

**Ligação com a dissertação:** a comparação c versus u muda o critério de atribuição; graus de saída/entrada acrescentam o alcance relacional selecionado de cada papel. A decomposição dos saldos explica a mudança das participações; não é teste de H1/H2. O método pode ser aplicado a SC/2018 com dados harmonizados, sem transportar resultados nacionais nem prometer cooperação territorial a partir de uma rede sem regiões.

## 7. Encaminhamento desta etapa

O artigo sustenta uma adaptação de conceitos de redes ao nosso tema, mas a contribuição central recomendada é **volume versus conectividade de atribuições**, e não transmissão intermediária ou identificação de políticas ótimas. A [versão revisada do planejamento](02_planejamento_academico.md) incorpora esse recorte.

**Próxima etapa a discutir:** validar pergunta, nós e significado de aresta, juntamente com o tratamento da diagonal. Depois, conferir a formulação original do disparity filter e avaliar sua implementação em um caso pequeno verificável. Não foram alterados notebooks ou resultados nesta leitura.

## Referências metodológicas adicionais

- Serrano, M. Á.; Boguñá, M.; Vespignani, A. (2009). *Extracting the multiscale backbone of complex weighted networks*. PNAS, 106, 6483–6488. [DOI](https://doi.org/10.1073/pnas.0808904106).
- Blondel, V. D. et al. (2008). *Fast unfolding of communities in large networks*. [DOI](https://doi.org/10.1088/1742-5468/2008/10/P10008).
- Liang, S.; Qu, S.; Xu, M. (2016). *Betweenness-Based Method to Identify Critical Transmission Sectors for Supply Chain Environmental Pressure Mitigation*. Environmental Science & Technology, 50, 1330–1337. Referência 17 de Huang; derivação ainda não validada neste projeto.
