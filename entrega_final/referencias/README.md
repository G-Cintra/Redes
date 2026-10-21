# Referências de Huang et al. pertinentes ao trabalho

Seleção realizada em 18/10/2026 a partir da bibliografia de [Huang et al. (2019)](../../references/huang_et_al_2019/carbon_communities_hotspots_china.pdf), pp. 28–29. Os números abaixo são os da lista de referências desse artigo. Esta pasta reúne cinco textos integrais obtidos de repositórios acadêmicos ou páginas institucionais de autores.

**Finalidade:** fundamentar as ferramentas discutidas no [planejamento](../02_planejamento_academico.md), não ampliar automaticamente o escopo do trabalho. Após a triagem inicial, foram elaboradas as cinco leituras críticas abaixo, com consulta aos textos principais e conferência visual de equações críticas. O suplemento de Serrano integra o PDF e foi consultado; suplementos separados de Liang e del Río-Chanona não foram obtidos. Não houve reprodução empírica ou implementação dos métodos.

## Leituras críticas por artigo

- [Serrano et al. (2009)](leitura_critica_serrano_2009.md): filtro dirigido, modelo nulo e exceções de grau um.
- [Blondel et al. (2008)](leitura_critica_blondel_2008.md): modularidade, hierarquia, limite de resolução e adaptação dirigida.
- [Liang et al. (2016)](leitura_critica_liang_2016.md): definição correta de Jᵢ, passagem intermediária e contagem não conservativa.
- [Li et al. (2017)](leitura_critica_li_2017.md): rede produtiva versus conta ambiental, pequeno mundo e denominador de intensidade.
- [del Río-Chanona et al. (2017)](leitura_critica_del_rio_chanona_2017.md): rede primária versus derivada, PageRank e limites de correlação temporal.

As recomendações são adaptações propostas para nosso contexto, não novos métodos já aprovados. O planejamento e os notebooks não foram alterados nesta rodada.

## 1. Ordem de leitura recomendada

| Prioridade | Referência em Huang | Texto local | O que precisamos conferir |
| --- | --- | --- | --- |
| 1 — método central candidato | 19 | [Serrano, Boguñá e Vespignani (2009)](serrano_2009_backbone_arxiv.pdf) | Modelo nulo, fórmula do filtro, direção e casos especiais de grau |
| 2 — esclarecer uma inconsistência | 17 | [Liang, Qu e Xu (2016)](liang_2016_betweenness.pdf) | Definição original de intermediação produtiva, distinta de caminhos mínimos em F |
| 3 — extensão possível | 20 | [Blondel et al. (2008)](blondel_2008_louvain_arxiv.pdf) | Otimização de modularidade e pressupostos de comunidades |
| 4 — comparação de desenhos | 16 | [Li et al. (2017)](li_2017_sna_io_china_japan_manuscrito.pdf) | Diferença entre rede de transações e conta ambiental; métricas e seleção |
| 5 — contexto de redes de MIP | 21 | [del Río-Chanona, Grujić e Jensen (2017)](del_rio_chanona_2017_input_output_network.pdf) | Forças, PageRank e separação entre rede primária e rede derivada |

## 2. Pertinência e limites por referência

### Serrano, Boguñá e Vespignani (2009) — referência 19

**Título:** *Extracting the multiscale backbone of complex weighted networks*. PNAS, 106, 6483–6488. [DOI publicado](https://doi.org/10.1073/pnas.0808904106).

**Pertinência alta:** é a fonte original do disparity filter utilizado por Huang e candidato ao nosso backbone. Permite substituir uma justificativa apenas visual por um critério local formal. O texto trata da normalização dos pesos e da comparação com um modelo nulo; sua extensão dirigida aparece no material de apoio incluído na versão obtida.

**Limite:** foi baixada a versão de autor do arXiv, não a diagramação editorial da PNAS. Antes do código, conferir integralmente a extensão dirigida, a regra de retenção e os nós de grau zero/um. O modelo nulo de pesos não é um modelo de erro dos coeficientes ambientais. O método não garante preservar todos os nós ou uma proporção predeterminada de emissões.

- Fonte e versão: [arXiv:0904.2389v1](https://arxiv.org/abs/0904.2389v1).
- Download: [PDF do arXiv](https://arxiv.org/pdf/0904.2389).

### Liang, Qu e Xu (2016) — referência 17

**Título:** *Betweenness-Based Method to Identify Critical Transmission Sectors for Supply Chain Environmental Pressure Mitigation*. Environmental Science & Technology, 50, 1330–1337. [DOI](https://doi.org/10.1021/acs.est.5b04855).

**Pertinência alta para esclarecer o método:** Huang remete a este estudo para sua intermediação. A definição original usa caminhos da análise estrutural de caminhos (SPA), com direção, pesos, retornos e posição intermediária. A seção metodológica permite investigar a inconsistência de Jᵢ registrada na nossa leitura crítica de Huang.

**Limite:** não corresponde a aplicar `nx.betweenness_centrality` sobre F. O download não altera a decisão atual de manter intermediação fora do núcleo; sua inclusão exigiria leitura e validação próprias. O arquivo principal menciona Supporting Information, que não foi baixado nesta coleta.

- Fonte: página acadêmica de Ming Xu, University of Michigan.
- Download: [PDF disponibilizado pelo autor](https://public.websites.umich.edu/~mingxu/file/J46.pdf).
- Versão conferida: artigo com paginação e DOI da publicação.

### Blondel et al. (2008) — referência 20

**Título:** *Fast unfolding of communities in large networks*. Journal of Statistical Mechanics: Theory and Experiment, P10008. [DOI publicado](https://doi.org/10.1088/1742-5468/2008/10/P10008).

**Pertinência condicional:** fundamenta o método multinível de comunidades citado por Huang, conhecido como Louvain. É útil se uma partição e uma rede agregada por comunidades acrescentarem informação à comparação entre origens e destinos.

**Limite:** é uma referência de otimização de modularidade, não prova de que nossa rede tenha comunidades estáveis. Conferir a função objetivo e a adaptação à direção; não presumir que qualquer implementação chamada Louvain mantenha automaticamente a informação dirigida. No nosso desenho, pesos, laços, resolução e sementes precisam ser explícitos.

- Fonte e versão: [arXiv:0803.0476v2](https://arxiv.org/abs/0803.0476v2), versão de autor.
- Download: [PDF v2](https://arxiv.org/pdf/0803.0476v2).

### Li et al. (2017) — referência 16

**Título:** *Examining industrial structure changes and corresponding carbon emission reduction effect by combining input-output analysis and social network analysis: A comparison study of China and Japan*. Journal of Cleaner Production, 162, 61–70. [DOI](https://doi.org/10.1016/j.jclepro.2017.05.200).

**Pertinência como comparação:** combina análise de redes da estrutura produtiva com avaliação ambiental. Ajuda a distinguir indicadores de uma rede de transações econômicas de indicadores de uma matriz de atribuição final como F. É uma alternativa de desenho se precisarmos estudar relações produtivas diretas, mas não uma aplicação equivalente à nossa matriz.

**Ressalva já identificada na triagem:** a seção 2.1.1 apresenta características de pequeno mundo como requisito para aplicar SNA. Isso não é uma condição geral para análise de redes e não deve ser adotado como teste de validade do nosso projeto. A comparação temporal e entre países também não é transferível a uma única MIP nacional de 2015.

- Fonte: [PolyU Institutional Research Archive](https://ira.lib.polyu.edu.hk/handle/10397/104303).
- Download: [manuscrito aceito](https://ira.lib.polyu.edu.hk/bitstream/10397/104303/1/Ren_Examining_Industrial_Structure.pdf).
- Versão: Final Accepted Manuscript / Pre-Published Version, disponibilizada sob CC BY-NC-ND 4.0 segundo o repositório; arquivo preservado sem alterações.

### del Río-Chanona, Grujić e Jensen (2017) — referência 21

**Título:** *Trends of the World Input and Output Network of Global Trade*. PLOS ONE, 12(1), e0170817. [DOI](https://doi.org/10.1371/journal.pone.0170817).

**Pertinência de apoio:** aplicação de forças, PageRank e comunidades a redes derivadas da WIOD. Ajuda a reconhecer que uma rede de fluxos econômicos e uma rede secundária de correlações são objetos distintos, com interpretações diferentes.

**Limite:** não é uma rede ambiental equivalente a F. Parte importante da análise usa séries temporais, ausentes no nosso recorte; PageRank e redes de correlação não passam a integrar o trabalho apenas porque aparecem nesta referência.

- Fonte: [INET Oxford](https://www.inet.ox.ac.uk/publications/trends-of-the-world-input-and-output-network-of-global-trade).
- Download: [PDF institucional](https://oms-inet.files.svdcdn.com/production/files/Trends_of_the_World_Input_and_Output_Network_of_Global_Trade.pdf).
- Versão: artigo publicado, com DOI e paginação editorial; licença CC BY indicada no texto.

## 3. Pertinente, mas não obtida integralmente

**Referência 15 — Hanaka et al. (2017).** *Finding environmentally critical transmission sectors, transactions, and paths in global supply chain networks*. Energy Economics, 68, 44–52. [DOI](https://doi.org/10.1016/j.eneco.2017.09.012).

É pertinente para aprofundar a intermediação de setores e transações na MIP ambiental. Na busca desta etapa foram conferidos registros bibliográficos e a página acadêmica de um autor, mas não foi localizada uma cópia integral aberta verificável para download. Não foi salvo um resumo, relatório de projeto ou documento de título diferente como se fosse o artigo. A obtenção do texto pode ser retomada por acesso institucional; não é necessária para iniciar a leitura do filtro.

## 4. Referências não priorizadas nesta coleta

- **Martin et al. (2011), referência 25, OpenOrd:** pertinente ao layout usado por Huang, mas é uma ferramenta de posicionamento para grafos grandes; não resolve por si a escolha da rede ou do filtro. Mantida para a etapa de visualização, sem download de slides como substituto do artigo.
- **Newman (2010), referência 31:** livro geral de redes, útil como fundamento, mas não foi buscada uma cópia informal do livro integral.
- **Inventários e aplicações regionais chinesas:** importantes para a reprodução empírica de Huang, mas não substituem nossa base brasileira e não são prioridades para escolher os métodos agora.
- **Exemplos de modularidade em domínios distantes:** não são necessários para fundamentar nossa implementação enquanto as referências originais já atendem à questão.

## 5. Uso no fluxo de trabalho

Começar por Serrano para conferir a regra dirigida do filtro. Consultar Liang para esclarecer a intermediação antes de considerar qualquer ampliação do escopo. Ler Blondel se decidirmos avançar para comunidades. Os demais textos servem para comparar construções e evitar misturar objetos de rede.

Nesta etapa não foram alterados pergunta, hipóteses, notebooks ou resultados. Download e triagem de pertinência não equivalem a aprovação de implementação. O artigo de Huang permanece no acervo principal, ligado no início deste índice, sem duplicação do PDF nesta pasta.

## 6. Integridade dos arquivos

As assinaturas PDF, a identificação por título/autoria e a leitura de todas as páginas pelo Poppler foram verificadas; contagens e SHA-256 estão na tabela abaixo. Hash identifica os bytes obtidos, não certifica a validade metodológica de cada estudo.

<!-- INTEGRIDADE -->

| Arquivo | Páginas | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| [serrano_2009_backbone_arxiv.pdf](serrano_2009_backbone_arxiv.pdf) | 9 | 942303 | `eeeeae1103002e7e656fe6852f55cfd551c186c0e95e7199fec5834c48f70c06` |
| [blondel_2008_louvain_arxiv.pdf](blondel_2008_louvain_arxiv.pdf) | 12 | 1594808 | `7765151a1c6556a6e24623bcced75f2c6ac04093b8e27ba8df50bc8f2ecb5577` |
| [liang_2016_betweenness.pdf](liang_2016_betweenness.pdf) | 8 | 1159979 | `229c16c87471430419cc81bd899cf1c440d880f3f966907a8da2a09c008949e0` |
| [li_2017_sna_io_china_japan_manuscrito.pdf](li_2017_sna_io_china_japan_manuscrito.pdf) | 35 | 1570514 | `8e978b7487cd18bbd986c656658ae8945ce5c79be3686a00a8ccb5931b9689a2` |
| [del_rio_chanona_2017_input_output_network.pdf](del_rio_chanona_2017_input_output_network.pdf) | 14 | 2696312 | `d217c7298f3e1f7364485903ff937ee8f16e01322891b5d051a2a4140b79c2e1` |
