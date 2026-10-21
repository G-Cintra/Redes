# Contexto, requisitos e histórico do trabalho

Registro de trabalho em 18/10/2026. Esta pasta organiza a preparação da entrega final; seus documentos ainda não constituem um projeto metodológico aprovado ou um relatório de resultados finais.

## 1. Finalidade e contexto da disciplina

O trabalho integra a disciplina **Desigualdade, Diversidade e Redes**, do mestrado em Economia da UFSC, conforme o cabeçalho do resumo entregue ao professor. O tema é a estrutura intersetorial das emissões de CO₂ associadas à produção brasileira.

O requisito central estabelecido na discussão é produzir uma **análise de redes substantiva**, com conceitos, indicadores e técnicas reconhecidos na área. A rede deve contribuir para responder à pergunta; não basta apresentar contas ambientais e acrescentar um grafo ilustrativo.

A ementa, a rubrica de avaliação, os métodos obrigatórios, o formato, a extensão e o prazo da entrega ainda não foram conferidos. A adequação formal à disciplina permanece pendente dessa informação. Não se pressupõe que uma técnica específica seja exigida pelo professor.

## 2. Relação pretendida com a dissertação

O projeto de dissertação está em `C:/GitHub/Mestrado/0-Projeto de Dissertação`. Na versão consultada de `secoes/01_introdução.tex`, sua pergunta é:

> Como as emissões de CO₂ geradas em Santa Catarina em 2018 se distribuem entre os setores produtivos quando são atribuídas pelo lado da produção e pelo lado da demanda?

A dissertação prevê a MIP estadual de 2018, cujo relatório distingue 74 atividades. O acesso aos arquivos numéricos e o detalhamento ambiental efetivamente viável ainda precisam ser confirmados, conforme a metodologia consultada.

A fronteira proposta considera emissões na produção localizada em SC e encadeamentos de insumos produzidos no estado. Inclui vendas a outros estados e países como saídas na fronteira do modelo, sem acompanhar o processamento posterior fora de SC. Não equivale à pegada completa do consumo catarinense nem a um inventário territorial completo de GEE.

O trabalho da disciplina deve fornecer um procedimento e uma interpretação aproveitáveis nessa comparação. A aplicação nacional de 2015 pode ser um estudo próprio e uma preparação metodológica; seus resultados numéricos não podem ser transferidos para SC/2018. Não foi decidido ampliar ou reescrever os objetivos da dissertação.

## 3. Base e notação de referência nesta etapa

Preservar a notação de `analise_exploratoria_v3.ipynb` e `analise_exploratoria_v4.ipynb`:

| Objeto | Definição | Significado |
| --- | --- | --- |
| Z | Transações intermediárias nacionais | Fornecedora na linha, compradora na coluna |
| x | Produção bruta por atividade | R$ milhões |
| y | Demanda final por atividade | Produtos nacionais, incluindo exportações |
| A | Z diag(x)⁻¹ | Requisitos diretos de insumos nacionais |
| L | (I − A)⁻¹ | Requisitos diretos e indiretos de produção |
| φ; Φ | Intensidades diretas; diag(φ) | Gg CO₂/R$ milhão de produção |
| C | ΦL | Emissões por origem e unidade monetária de demanda final |
| c | Φx = Cy | Emissões próprias de cada atividade |
| F | C diag(y) | Emissões por origem emissora e destino final, em Gg CO₂ |
| u | Fᵀ1 | Emissões atribuídas à demanda final de cada atividade |

Em Fᵢⱼ, i identifica onde a emissão ocorre; j identifica o produto setorial destinado à demanda final. O destino não é necessariamente o comprador direto. F já incorpora encadeamentos indiretos: não substituir A por F em uma inversa de Leontief nem interpretar automaticamente caminhos concatenados em F como etapas produtivas.

Há outros usos de C, P, γ e F em arquivos históricos do repositório, inclusive F para uma medida de extração. Identificar a definição local antes de reutilizar qualquer símbolo ou saída. A matriz C desta tabela não é a classificação de qualidade ambiental “categoria C” usada na auditoria.

## 4. O que já foi feito

### 4.1. Resumo entregue ao professor

Fonte: [Gabriel_Cintra_-_Resumo_v2.pdf](../relatorio/Gabriel_Cintra_-_Resumo_v2.pdf).

O resumo propunha investigar se grandes emissores estão amplamente conectados à estrutura produtiva e se atividades com baixas emissões diretas dependem de insumos de atividades intensivas em emissões. Utilizava a MIP brasileira de 2015, com 67 atividades, e coeficientes de Sanguinet e Azzoni.

As figuras incluíam matriz ambiental, comparação com VAB, árvore geradora máxima bilateral e arborescência máxima dirigida. Naquele resultado, as árvores mantinham 65 ligações entre 66 atividades e uma atividade isolada. Preservavam, respectivamente, 30,58% e 19,96% do peso entre atividades distintas. Esses percentuais são históricos e devem ser recalculados se mudar a entrada ou a regra.

### 4.2. Evolução dos notebooks

- [v2](../analise_exploratoria_v2.ipynb): reúne contas ambientais e explorações mais amplas, incluindo similaridade e componentes territoriais. Essas extensões não são requisitos da entrega atual.
- [v3](../analise_exploratoria_v3.ipynb): organiza a distinção entre local de emissão e demanda final que mobiliza a produção, com C, c e F explícitas.
- [v4](../analise_exploratoria_v4.ipynb): acrescenta uma economia ilustrativa de quatro setores, calibrada, e um Sankey. O exemplo não é uma submatriz observada da economia brasileira.
- [Sankeys de 20 e 67 atividades](../sankeys_mip20_67.ipynb): representam a atribuição entre origens e destinos. São apoio visual, não uma análise independente da mesma matriz.

### 4.3. Notebook criado antes da validação por etapas

Foi criado [rede_bipartida_atribuicao_2015.ipynb](../rede_bipartida_atribuicao_2015.ipynb), com reconstrução econômica, extensão ambiental, rede NetworkX, saldos, diversidade e figuras. Suas 14 células de código foram executadas e passaram pelas verificações locais de alinhamento e conservação.

O usuário esclareceu que pretendia avançar **passo a passo, validando cada etapa**, e avaliou a visualização como inadequada. Portanto, esse notebook é um protótipo exploratório, não a implementação metodológica aprovada para a entrega.

Na execução registrada, a representação bipartida teve 134 nós e 4.357 ligações positivas entre 4.489 pares possíveis, aproximadamente 97%. Essa densidade decorre também dos encadeamentos indiretos contidos em F. A duplicação dos setores em dois papéis não está decidida como representação final.

### 4.4. Outras investigações existentes

O repositório também contém investigação de emissão própria versus centralidade de fornecedor, validações e uma especificação acadêmica dessa investigação. Esses documentos registram uma linha anterior de trabalho. Suas escolhas não são automaticamente as decisões deste novo planejamento; os históricos devem ser preservados e as diferenças explicitadas.

## 5. Requisitos estabelecidos na conversa

1. Trabalhar por etapas conceituais e metodológicas, discutindo cada decisão antes de implementar a etapa seguinte.
2. Usar análise de redes reconhecida e pertinente à pergunta, sem inserir métricas apenas para cumprir uma aparência de trabalho de redes.
3. Manter uma relação clara e útil com a dissertação.
4. Preferir preservar o núcleo da pergunta; reformulá-lo se necessário para uma contribuição de redes defensável.
5. Justificar qualquer redução de conexões pelo objetivo analítico e pelos pressupostos da técnica, não somente pela estética.
6. Distinguir seleção para desenho de filtragem que define a rede analisada; informar em qual objeto cada indicador foi calculado.
7. Não tomar a árvore máxima, a representação bipartida ou o filtro de disparidade como escolhas já aprovadas.
8. Avaliar se a figura permite ler relações e sustentar uma interpretação. Uma figura de rede não precisa carregar todas as conclusões do trabalho.
9. Manter as decisões metodológicas e contas principais visíveis no notebook, conforme o AGENTS.md.
10. Preservar arquivos históricos e restringir mudanças ao escopo acordado, sem arquitetura ou dependências desnecessárias.

## 6. Validade ambiental e limites

A [auditoria dos coeficientes](../docs/auditoria_coeficientes_emissoes_2015.md) registra transcrição correta dos valores publicados, mas limitações relevantes de preços, cobertura e alocação setorial. A interpolação 2011–2018 aplicada à estrutura de 2015 permanece um cenário exploratório; fechamento contábil e execução sem erros não validam as emissões físicas.

Antes de resultados ambientais finais, validar, reconstruir ou substituir a base e documentar a fronteira. Filtragem de rede, normalização, estabilidade dos rankings e bom desenho não resolvem esse problema. Caso a entrega use o cenário atual, delimitar explicitamente suas conclusões e verificar se esse escopo é aceitável para a disciplina.

## 7. Literatura localizada e status de leitura

| Referência | Utilidade | Verificação realizada |
| --- | --- | --- |
| Huang et al. (2019), *Carbon Communities and Hotspots for Carbon Emissions Reduction in China* | Matriz equivalente a ΦL diag(y), filtro de disparidade, forças, graus e comunidades | PDF baixado; leitura crítica e adaptação concluídas documentalmente em 18/10/2026; ver documento 03 |
| Liang, Feng e Xu (2015), *Structure of the Global Virtual Carbon Network* | Setores intermediários, caminhos e comunidades | Resumo e descrição de suplementos; derivação ainda não revisada integralmente |
| Hanaka et al. (2017), *Finding environmentally critical transmission sectors, transactions, and paths in global supply chain networks* | Intermediação adaptada à MIP ambiental | Resumo e trechos metodológicos públicos |
| Du et al. (2018), *A network analysis of indirect carbon emission flows among different industries in China* | Rede setorial e indicadores clássicos | Resumo e prévia; definição operacional das arestas ainda a conferir |
| Pereira, Diele-Viegas e Ribeiro (2024), *GHG emissions in Brazilian Agriculture and livestock sectors and the risk to Amazonia conservation* | Aplicação brasileira; fronteira de GEE diferente de CO₂ | Resumo, dados e referências; equações ainda a conferir |
| Rifki, Ono e Kagawa (2017), *The robustest clusters in the input–output networks: global CO₂ emission clusters* | Sensibilidade e robustez dos agrupamentos | Texto aberto consultado na pesquisa inicial; procedimento ainda não reproduzido |

Links bibliográficos e uso proposto estão no [planejamento](02_planejamento_academico.md). Localizar um artigo não significa aprovar ou reproduzir seu método. Este documento e o planejamento constituem a referência para retomar a discussão sem transformar propostas em decisões consolidadas.

## 8. Atualização após a leitura de Huang et al.

O [PDF foi incorporado ao acervo](../references/huang_et_al_2019/carbon_communities_hotspots_china.pdf), com origem e SHA-256 registrados. A [leitura crítica](03_leitura_critica_huang_2019.md) distingue a matriz de atribuição final das ilustrações de transmissão intermediária, aponta uma inconsistência na especificação da intermediação e registra ambiguidades de comunidades e corte gráfico.

O planejamento passou a recomendar, para discussão, **volume versus conectividade de origens e destinos**, rede dirigida de 67 atividades e avaliação do disparity filter. Comunidades são complementares; intermediação produtiva não integra o núcleo. Essa atualização é documental e responde ao pedido de adaptar pergunta, objetivos e hipóteses a partir do artigo. Não representa aprovação antecipada da implementação nem alteração dos notebooks ou resultados.
