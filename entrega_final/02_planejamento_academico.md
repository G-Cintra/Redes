# Planejamento acadêmico do trabalho de redes

Versão revisada após Huang, as cinco fontes complementares e a discussão das implicações de política — 18/10/2026. **Este é o desenho recomendado para discussão antes da implementação.** O [documento de contexto](01_contexto_requisitos_historico.md) registra os requisitos. As [leituras críticas](referencias/README.md) fundamentam a revisão. A pergunta passa a partir explicitamente das diferenças entre produção e demanda; volume, concentração e backbone ajudam a interpretar as relações que compõem essas diferenças. A contribuição de política é um diagnóstico de oportunidades de coordenação, condicionado à validação ambiental. Comunidades continuam complementares; intermediação produtiva não integra o núcleo.

## Síntese da decisão metodológica

**Núcleo recomendado:** rede dirigida ponderada de 67 atividades; F integral nas contas; W sem diagonal nas relações entre atividades; forças para volume; disparidade para concentração; filtro de disparidade para selecionar ligações; graus e cobertura do backbone para interpretar a seleção. É um desenho de análise de redes ponderadas, não uma coleção de centralidades.

**Por que rever a versão anterior:** grau do backbone não é diversidade da rede original. Um perfil uniforme pode perder todas as suas ligações no filtro, apesar de ter alcance amplo. A análise não deve confundir ausência de saliência local com ausência de relação. Comparar apenas volume e grau filtrado tornaria a pergunta excessivamente dependente de α.

**O que permanece aberto:** convenções de grau um, adequação empírica do modelo nulo, eventual sensibilidade à diagonal e utilidade de comunidades. Não haverá mudança de parâmetro para obter uma narrativa ou figura desejada. Não foram executados novos cálculos nesta revisão.

## 1. Tema e recorte

**Tema:** relações intersetoriais que conectam a atribuição de emissões de CO₂ pela produção e pela demanda, sua organização em rede e suas implicações para a coordenação da mitigação.

**Recorte empírico de partida:** MIP nacional de 2015, 67 atividades, produção nacional para demanda final doméstica e exportações, excluindo emissões ocorridas no exterior. A base ambiental atual é exploratória e requer validação ou substituição.

**Título provisório:** *Da produção à demanda: estrutura da rede intersetorial de atribuição de CO₂ no Brasil e implicações para a coordenação da mitigação*.

O trabalho deve distinguir volume emitido, posição na rede e forma de atribuição. Não se propõe medir transporte atmosférico, essencialidade de insumos ou efeitos causais de políticas.

## 2. Problema e contribuição pretendida

A atribuição pela produção identifica os setores onde as emissões ocorrem. A atribuição pela demanda identifica os produtos finais associados a essas emissões. As duas distribuições não mostram, isoladamente, como se organizam as relações que as conectam.

A contribuição pretendida é distinguir volume, concentração dos perfis e alcance das relações selecionadas, usando conceitos de redes ponderadas. Dois setores de volume semelhante podem distribuir suas relações de forma diferente; isso precisa ser examinado, não presumido. A seleção por backbone revela ligações desproporcionais sob um modelo nulo e não mede, sozinha, diversidade. Filtrar uma matriz ou produzir um desenho não responde por si só ao problema.

**Contribuição de política pretendida:** mostrar como a estrutura das relações entre setores emissores e demandas finais ajuda a identificar oportunidades de coordenação para a mitigação, complementando os rankings de emissões pela produção e pela demanda. O diagnóstico deve indicar conjuntos de setores e relações a investigar conjuntamente, sem pretender escolher uma política ótima.

### Como as duas contas se conectam pela rede

Adotar a notação dos notebooks: Φ é a matriz diagonal de intensidades diretas, L é a inversa de Leontief, C = ΦL e F = C diag(y). Cada Fᵢⱼ representa emissões ocorridas na atividade i e atribuídas à demanda final de produtos da atividade j, incorporando os requisitos diretos e indiretos de produção nacional. O destino j identifica o produto final, não necessariamente seu comprador imediato ou uma categoria institucional de consumidor.

As somas das linhas e colunas são as duas perspectivas sobre o mesmo total de emissões dentro da fronteira adotada:

- **Produção:** cᵢ = Σⱼ Fᵢⱼ, emissões próprias da atividade i.
- **Demanda:** uᵢ = Σⱼ Fⱼᵢ, emissões atribuídas à demanda final dos produtos da atividade i.
- **Diferença:** uᵢ − cᵢ = Σⱼ≠ᵢ Fⱼᵢ − Σⱼ≠ᵢ Fᵢⱼ.

Logo, a diferença entre as contas corresponde ao saldo de entrada e saída das relações externas de atribuição. A diagonal cancela no saldo, mas deve permanecer visível porque integra os volumes completos. No agregado, Σᵢ cᵢ = Σᵢ uᵢ: mudar a atribuição não reduz emissões físicas. Um saldo pequeno pode coexistir com grandes volumes de entrada e saída; o saldo sozinho não revela essa estrutura.

As identidades acima são propriedades contábeis a verificar, não achados empíricos ou hipóteses. A análise de redes acrescenta a distribuição dos pesos, as contrapartes e as ligações selecionadas. As arestas de F não representam transações diretas; concatená-las não reconstrói caminhos produtivos. A conta pela demanda inclui exportações e exclui emissões estrangeiras, portanto não equivale a uma pegada completa do consumo doméstico.

## 3. Pergunta e objetivos: formulação para validar

### Pergunta principal de trabalho

> Quais relações intersetoriais compõem as diferenças entre as emissões atribuídas pela produção e pela demanda na economia brasileira de 2015, e como essas relações se organizam em termos de volume, concentração e conectividade?

“Concentração” refere-se à distribuição ponderada dos vínculos de cada papel, medida na rede completa externa. “Conectividade” refere-se à existência de vínculos e à quantidade de ligações retidas no backbone, com a regra explicitada; não significa transmissão por caminhos. O filtro de disparidade identificará ligações localmente destacadas, condicionado à avaliação de seu modelo nulo. Relevância local não equivale a importância causal ou normativa. A comparação entre volume e concentração permanece como subquestão da pergunta principal.

### Questão de ligação com a dissertação

> Como esse diagnóstico relacional pode complementar a comparação entre produção e demanda na dissertação e orientar a seleção de relações a investigar em futuros cenários de mitigação?

### Objetivo geral

Caracterizar a estrutura das relações intersetoriais que conectam as atribuições de emissões pela produção e pela demanda, combinando volume, concentração e conectividade, e discutir suas implicações para identificar oportunidades de coordenação da mitigação.

### Objetivos específicos candidatos

1. Conferir F, as duas contas ambientais e a rede externa W, com significado explícito dos nós, pesos e diagonal.
2. Caracterizar densidade, forças e disparidade dos pesos em W e comparar volume com concentração dos perfis nos dois sentidos.
3. Avaliar o filtro de disparidade e interpretar graus de saída/entrada junto da cobertura de peso de cada perfil, distinguindo totais, volumes externos e pesos retidos.
4. Examinar a estabilidade das ligações, cobertura e posições diante das escolhas de filtragem, sem selecionar parâmetros para obter divergências ou figuras desejadas.
5. Decompor as diferenças entre produção e demanda em relações externas de entrada e saída, identificando contrapartes e contrastes de perfis; avaliar comunidades somente se acrescentarem informação robusta.
6. Discutir quais conjuntos de setores e demandas merecem investigação conjunta para mitigação, distinguindo diagnóstico relacional de avaliação de instrumentos de política.
7. Documentar limites ambientais e condições de aproveitamento na dissertação em SC/2018.

Esses objetivos são candidatos ao desenho final, não autorização para executar simultaneamente todas as análises.

## 4. Questões exploratórias e critérios de interpretação

O desenho é descritivo. As hipóteses do resumo inicial e as formulações posteriores H1/H2 são antecedentes da investigação; não constituem hipóteses confirmatórias pré-registradas. A expressão “não necessariamente” não oferece um critério estatístico de confirmação e deixa de organizar a análise.

A pergunta principal será desenvolvida em três questões operacionais:

1. **Contrapartes:** quais origens e destinos de atribuição compõem as diferenças entre produção e demanda, incluindo casos de saldos pequenos com grandes entradas e saídas?
2. **Distribuição dos pesos:** como os volumes externos se distribuem entre essas contrapartes e como a concentração se associa ao volume em cada perspectiva?
3. **Seleção de relações:** quais ligações o backbone seleciona e quanto peso essa seleção preserva globalmente e por atividade?

Na segunda questão, comparar c/u e forças externas com o número efetivo D₂ em W; informar também a diagonal. Spearman e postos com empates podem resumir associações descritivas, sem p-valores baseados em amostra IID nem corte arbitrário para “confirmar” divergência. Perfis externos nulos têm concentração indefinida, mantendo a identificação da atividade. Na terceira questão, graus de Bα serão lidos junto da cobertura e nunca como diversidade automática.

A identidade entre saldo externo e diferença das contas é propriedade contábil, não hipótese empírica. Associações fortes, perfis semelhantes e filtragem pouco informativa são resultados admissíveis. Comunidades permanecem uma extensão opcional, dependente de justificativa e estabilidade, sem número de grupos predeterminado.

## 5. Escolhas metodológicas abertas

### Desenho recomendado após as leituras, a validar antes do código

- **Contas completas:** F = ΦL diag(y), c = F1, u = Fᵀ1. Essas forças de F são identidades, não descobertas independentes.
- **Rede de relações externas:** 67 nós, um por atividade; Wᵢⱼ = Fᵢⱼ para i ≠ j, Wᵢᵢ = 0. Direção: origem emissora → produto destinado à demanda final. As forças de W são cᵢ − Fᵢᵢ e uᵢ − Fᵢᵢ.
- **Backbone Bα:** pesos originais de W nas arestas selecionadas; manter os 67 nós e identificar isolados. Graus contam relações retidas, não fornecedores/compradores diretos.
- **Tratamento da diagonal:** preservada nas contas; separada na rede externa. Examinar sua influência na seleção como sensibilidade, sem confundir contas completas com rede sem laços.
- **Filtro candidato:** disparidade dirigida, regra OU entre perspectiva de saída e de entrada; α = 0,05 como referência de literatura, 0,01/0,10 como sensibilidade proposta. Sem piso de uma tonelada importado automaticamente. Conferir derivação e casos de grau zero/um na fonte original antes de implementar.
- **Núcleo:** forças e disparidade em W, contas completas em F, graus e cobertura de Bα. O backbone destaca saliência, enquanto a concentração é avaliada antes de filtrar.
- **Comunidades:** extensão condicionada à utilidade e estabilidade, com modularidade dirigida ponderada e parâmetros explícitos. Não impor número de grupos ou qualidade desejada.
- **Não incluir no núcleo:** betweenness padrão sobre F, caminhos interpretados como etapas produtivas, efeitos causais de mitigação e intermediação não derivada.

A representação bipartida permanece alternativa didática, mas deixa de ser a recomendação analítica principal. As escolhas abaixo permanecem reversíveis mediante justificativa; não são uma lista de análises a executar.

| Escolha | Alternativas | Condição para decidir |
| --- | --- | --- |
| Objeto de rede | Atribuição total em F; relações produtivas diretas com extensão ambiental | Arestas devem corresponder à pergunta; mudar o objeto muda a interpretação |
| Nós | Recomendação: 67 atividades em rede dirigida; bipartida como alternativa | Validar interpretação dos dois papéis no mesmo nó, sem inferir transmissão por caminhos |
| Diagonal | Manter nas contas; tratamento separado na rede ou no desenho | Registrar efeito sobre forças, filtro, comunidades e cobertura |
| Redução de arestas | Disparity filter; limiar global como comparação; árvore máxima como síntese | Justificar pressupostos e o que o método preserva ou descarta |
| Importância local de uma aresta | Saída, entrada, ou combinação por regra OU/E | Definir qual perspectiva ambiental interessa e como a regra é implementada |
| Posição e perfil setorial | Força e disparidade em W; graus e cobertura do backbone | Não confundir concentração com quantidade de arestas selecionadas |
| Comunidades | Incluir ou não; modelo compatível com a rede | Fundamentar modularidade/modelo nulo e examinar estabilidade |
| Visualização | Rede com posições por forças, bipartida, matriz, Sankey | Avaliar legibilidade e tarefa de leitura; separar filtro analítico e corte gráfico |
| Base ambiental | Validar/reconstruir/substituir; cenário explicitamente exploratório | Fronteira, unidades, preços e correspondência setorial verificáveis |

Manter F como objeto de partida favorece a ligação com as duas atribuições, mas não obriga a conservar essa escolha se impedir a interpretação de redes desejada. Não aplicar betweenness, closeness, PageRank ou caminhos em F apenas porque estão disponíveis: a interpretação precisa considerar que F já incorpora todas as rodadas de produção.

### Candidata prioritária: extração de backbone

O filtro de disparidade compara a concentração local dos pesos com um modelo nulo. É uma técnica publicada de redes ponderadas, com aplicação próxima em Huang et al. (2019). Ainda não foi aprovado para nossa base.

A leitura crítica encontrou problemas que impedem copiar integralmente Huang: exemplos intermediários não equivalentes a F, descrição incorreta de Jᵢ, comunidades insuficientemente especificadas e limiar gráfico aparentemente inconsistente. Liang esclarece que somente (i,i) de Jᵢ é um; sua medida, porém, continua sendo passagem intermediária baseada em A/L, com contagem não exclusiva de emissões. A correção bibliográfica não autoriza incluí-la como centralidade de F.

Antes de implementá-lo, definir normalização de entrada/saída, grau considerado, casos de grau zero ou um, tratamento da diagonal, regra de retenção e parâmetro. Justificar a adequação do modelo nulo a pesos calculados por uma MIP. “Significância” sob o filtro não valida emissões físicas nem representa evidência causal.

Na normalização de saída, a intensidade direta da origem cancela para linhas positivas; na de entrada, a demanda final do destino cancela para colunas definidas. Portanto, os dois critérios descrevem composições diferentes. A regra OU combina essas perspectivas e deve ter seus resultados decompostos por origem da seleção. A derivação está na seção 5.2 da leitura crítica.

Antes de comparar posições, informar arestas, nós, peso retido, cobertura por origem/destino, isolados e componentes. A análise da rede reduzida não deve substituir as contas completas. Não escolher α para reproduzir os 93% de retenção do artigo. Para eventual partição, comparar sementes/resoluções e quantificar suas relações também em W completa.

Uma árvore máxima impõe conectividade e ausência de ciclos e não será o filtro principal. Um limiar global pode servir como comparação com tamanho ou peso retido semelhantes, não como seleção principal. Cobertura acumulada pode ser diagnóstico, mas não substitui a fundamentação do backbone.

### Disparidade e número efetivo: perfil antes da seleção

Para um perfil externo não nulo, definir p de saída por linha de W e p de entrada por coluna. Calcular Y = Σp², a medida de disparidade usada por Serrano, e reportar D₂ = 1/Y como número efetivo. Para k pesos iguais, D₂ = k; quando um domina, aproxima-se de um. Y e D₂ expressam a mesma informação em escalas inversas: não são dois resultados independentes. kY pode ser usado no diagnóstico frente ao modelo nulo, sem virar mais um ranking principal.

Não acumular Shannon, HHI, Gini e outros índices como se cada um fosse evidência adicional. O núcleo usa a disparidade por sua ligação com a literatura de redes e o filtro; Shannon do protótipo permanece exploratório, sem obrigação de reprodução na entrega.

**Exemplo conceitual:** com k > 1 e pesos iguais, cada cauda do filtro vale (1 − 1/k)^(k − 1). Em graus grandes, aproxima-se de 0,368, portanto não passa em α = 0,05 nessa extremidade. Um nó com 66 destinos iguais pode ter D₂ = 66 e nenhuma aresta selecionada por sua saída. Na regra OU, a outra extremidade ainda pode preservá-las. Logo, grau zero no backbone não significa perfil concentrado, emissão zero ou ausência de relação na matriz original.

### O que cada objeto sustenta

| Objeto | Indicadores principais | Leitura defensável |
| --- | --- | --- |
| F integral | c, u, diagonal e saldo | Onde se emite, a qual produto final se atribui e diferença de participação |
| W sem diagonal | Forças externas, disparidade/D₂, densidade | Volume e distribuição entre atividades distintas |
| Bα | Graus, forças retidas e cobertura por nó | Quantidade e volume de ligações selecionadas sob a regra |
| Rede agregada por eventual partição | Pesos internos e entre grupos em W e Bα | Organização mesoscópica, condicionada à partição |

### Conceitos de redes e sua função na pergunta

O conteúdo da disciplina estará no uso interpretado de redes dirigidas e ponderadas, força, distribuição dos pesos, disparidade, extração de backbone e grau. A densidade caracteriza o objeto inicial e ajuda a explicar por que o grau da rede completa pode distinguir pouco os setores. A força mede volume; a disparidade caracteriza sua concentração; o backbone seleciona relações conforme um modelo nulo; grau e cobertura descrevem o resultado dessa seleção. São funções diferentes e complementares.

O resultado esperado não é apenas um ranking: são perfis setoriais que combinem c, u, saldo, diagonal, forças externas, D₂ e principais contrapartes, acompanhados da interpretação das ligações do backbone. A definição final das tabelas e figuras fica para a etapa correspondente. Comunidades são opcionais; não é necessário acumular centralidades para demonstrar conteúdo de redes.

### Avaliação das ferramentas à luz das fontes

| Método | Decisão recomendada | Fundamentação e condição |
| --- | --- | --- |
| Forças de entrada/saída | Manter, distinguindo F/W/Bα | Conceito padrão; em F corresponde às contas, não é descoberta independente |
| Disparidade dos pesos | Incluir no núcleo | Serrano; distribuição completa antes de selecionar arestas |
| Disparity filter dirigido | Candidato principal ao backbone | Serrano e aplicação em Huang; entrada/saída separadas, regra OU e exceções explícitas |
| Grau do backbone | Manter com interpretação restrita | Número de ligações selecionadas; ler com D₂ e cobertura, nunca como diversidade automática |
| Comunidades | Complemento condicionado | Blondel fundamenta heurística não dirigida; extensão dirigida e estabilidade ainda precisam de referência e especificação |
| Rede agregada de comunidades | Avaliar depois da partição | Pode reduzir nós de forma analítica; não agrupar apenas para melhorar a figura |
| Árvore máxima/arborescência | Fora do núcleo e da seleção principal | Restrição de árvore não decorre da pergunta; guardar histórico |
| Betweenness/closeness de caminhos mínimos em F | Descartar neste desenho | Caminhos concatenados de atribuições não são etapas de produção |
| Intermediação SPA de Liang | Reservar para outra pergunta/extensão | Usa A/L, laços e múltiplas passagens; não conserva o total como c/u |
| PageRank de F | Não incluir | Exigiria justificar caminhada e teletransporte; fonte de del Río tem ambiguidades de fórmula e outro objeto |
| Pequeno mundo como teste de validade | Descartar | Não é pré-requisito de SNA; densidade torna caminhos curtos pouco informativos |
| Correlações temporais e competição | Fora do recorte | del Río exige séries; correlação não identifica causalidade |
| Intensidade por VAB multiplicando L | Não adotar | Ambiguidade em Li; usar emissão/produção bruta na extensão ambiental |

Essas decisões limitam o método ao que a pergunta permite interpretar; não afirmam que os métodos excluídos sejam inválidos para outros objetos.

## 6. Sequência de trabalho com pontos de validação

| Etapa | Produto para discutir | Critério antes de avançar |
| --- | --- | --- |
| 1. Leituras críticas — realizadas | [Huang](03_leitura_critica_huang_2019.md) e [cinco fontes](referencias/README.md) | Métodos e limites separados; suplementos externos e resultados empíricos não reproduzidos |
| 2. Fixação do problema | Uma pergunta operacional, contribuição de redes e objetivos enxutos | Concordância sobre o que a rede deve revelar além das duas contas |
| 3. Definição da rede | Especificação de nós, direção, pesos, diagonal e fronteira | Cada ligação ter significado inequívoco; representação aprovada |
| 4. Conferência da base | Alinhamento, unidades, preços, cobertura e identidades | Distinguir consistência computacional e validade ambiental; definir status dos resultados |
| 5. Diagnóstico da rede completa | Nós, arestas, densidade, pesos, forças e disparidade | Separar volume, distribuição ponderada e efeito mecânico da densidade |
| 6. Escolha e avaliação do filtro | Método, pressupostos e sensibilidade; nós, arestas e peso retidos | Evitar corte escolhido apenas pela estética ou para recuperar uma narrativa |
| 7. Protótipos visuais | Poucas alternativas do mesmo objeto já validado | Legibilidade, cobertura e interpretação; sem alterar silenciosamente a rede entre figuras |
| 8. Interpretação conjunta | Contas de produção/demanda, saldos, contrapartes, volume, D₂, graus e cobertura; eventual comunidade estável | Relacionar cada perfil à diferença entre as contas; não confundir perfil uniforme com ausência de conexões nem forçar divergência de rankings |
| 9. Discussão de política e redação | Oportunidades de coordenação, resposta à pergunta, limites e ponte com a dissertação | Separar diagnóstico de avaliação de políticas; conclusões proporcionais à validade dos dados e ao significado das arestas |

**Modo de condução:** apresentar e discutir uma etapa por vez. A existência do notebook protótipo não antecipa a aprovação das etapas. Não executar todo este planejamento de uma vez.

## 7. Aproveitamento na dissertação

O trabalho da disciplina pode mostrar se uma pegada elevada se concentra em poucas origens ou se distribui entre muitas, e se um grande emissor atende sobretudo a poucos destinos finais ou a perfis amplos. O backbone localiza ligações desproporcionais; não substitui essa leitura da distribuição completa. A diferença uᵢ − cᵢ continua sendo o saldo externo e explica a mudança de participação, sem constituir teste de hipótese. Eventuais grupos e código auditável podem complementar essa contribuição.

A dissertação permanece centrada na comparação das duas distribuições em SC/2018. A incorporação de uma seção de redes dependerá do valor explicativo demonstrado neste trabalho. Não se exige replicar todos os métodos nem transformar a dissertação em um estudo de redes.

O aproveitamento será principalmente metodológico: passar da comparação de totais setoriais à identificação das relações que compõem esses totais. A aplicação brasileira de 2015 pode fornecer uma demonstração auditável desse procedimento; seus setores prioritários e resultados numéricos não devem ser transferidos automaticamente para SC/2018. A aplicação regional exigirá conferir fronteiras, importações, exportações, correspondências setoriais e dados ambientais.

A ponte com políticas tem duas etapas distintas: este trabalho produz o diagnóstico das relações candidatas a investigação; uma etapa posterior da dissertação, se pertinente ao seu escopo, pode formular cenários explícitos de demanda ou tecnologia. Simular esses cenários não integra a implementação inicial da disciplina.

## 7.1. Implicações de política: interpretação prevista

**Pergunta de política associada:** quais setores emissores e demandas finais devem ser considerados conjuntamente ao investigar oportunidades de mitigação?

Os resultados podem ajudar a distinguir situações como as abaixo. São interpretações condicionais de padrões ainda não calculados, não recomendações antecipadas para setores específicos.

| Padrão que poderá ser observado | Implicação para investigação de política |
| --- | --- |
| Produto final com poucas emissões próprias, grande pegada e poucas origens emissoras dominantes | Investigar conjuntamente mudanças nos processos das origens e eficiência material ou especificações dos produtos finais associados |
| Pegada de uma demanda distribuída por muitas origens emissoras | Investigar alcance de medidas transversais e necessidade de coordenação mais abrangente; uma única origem pode representar parcela pequena da pegada |
| Setor emissor associado a muitas demandas finais | Investigar mudanças de intensidade de emissões na origem cujo efeito contábil alcance várias cadeias, sob as hipóteses do modelo |
| Emissões de uma origem fortemente associadas a poucas demandas finais | Investigar ações coordenadas nessas cadeias e instrumentos sobre os produtos finais associados |
| Saldo produção/demanda pequeno, mas grandes entradas e saídas externas | Evitar excluir a atividade apenas pelo saldo; examinar as relações brutas e suas contrapartes |

Por exemplo, **se** uma demanda final de construção apresentar pegada elevada concentrada em cimento e aço, o diagnóstico permitirá discutir tanto tecnologia e energia nas origens quanto projeto, eficiência material, reutilização e compras públicas na ponta de demanda. A matriz, por si só, não identifica contratos, compradores imediatos ou poder de negociação. A combinação de medidas ao longo das cadeias tem apoio no [IPCC, capítulo 11 do AR6/WGIII](https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-11/); instrumentos de demanda, incluindo compras públicas e requisitos de carbono incorporado, são discutidos pela [IEA para aço e cimento](https://www.iea.org/reports/demand-and-supply-measures-for-the-steel-and-cement-transition/executive-summary). Essas fontes contextualizam a discussão de instrumentos; não validam efeitos na nossa base.

**Critérios de interpretação:** combinar volume absoluto, concentração e contrapartes. Uma relação concentrada pode representar poucas emissões; uma aresta selecionada pelo filtro pode ser pequena no total nacional. Saldo positivo pela demanda não equivale a culpa, obrigação jurídica ou capacidade de intervenção. Não classificar automaticamente arestas retidas como prioridades de mitigação, nem arestas removidas como irrelevantes.

**O que o estudo permite concluir:** quais relações sustentam as diferenças de atribuição e quais conjuntos de atividades merecem investigação conjunta, dentro da fronteira e da qualidade dos dados.

**O que exige análise adicional:** eficácia e custo dos instrumentos, potencial de abatimento, substituição tecnológica, respostas comportamentais, efeitos distributivos e impactos sobre produção, emprego e preços. Uma comparação de contas ou uma filtragem não estima emissões evitadas. Para isso, seria necessário especificar uma intervenção e um cenário contrafactual apropriado.

Enquanto os coeficientes ambientais permanecerem exploratórios, a discussão será ilustrativa e metodológica. Recomendações setoriais substantivas dependem de sua validação ou substituição, conforme a [auditoria ambiental](../docs/auditoria_coeficientes_emissoes_2015.md).

## 8. Flexibilidade e limites do escopo

**Há flexibilidade** para ajustar a pergunta, dispensar hipóteses inadequadas, escolher representação unipartida ou bipartida, decidir por comunidades ou por análise de posições e colocar figuras no corpo ou no anexo. A preferência é preservar o tema e a ligação com produção/demanda.

**Não há flexibilidade** para tratar métodos propostos como aprovados, confundir atribuição total com transação direta, apresentar dados ambientais não validados como inventário observado, escolher métodos para obter resultados desejados ou substituir o conteúdo de redes por uma figura decorativa.

**Fora do escopo inicial:** regionalização microrregional, comparação com satélite/NO₂, modelos causais de choque, substituição tecnológica, otimização de políticas e novas camadas ou hipergrafos sem necessidade demonstrada.

## 9. Leituras prioritárias e acesso

As leituras efetivamente realizadas de Serrano, Blondel, Liang (2016), Li e del Río-Chanona estão reunidas no [índice local](referencias/README.md), com um parecer por artigo. Os itens abaixo incluem também referências ainda não lidas integralmente; não confundir esse levantamento com fontes já validadas. A próxima etapa não exige outra busca ampla de literatura.

1. **Huang et al. (2019).** *Carbon Communities and Hotspots for Carbon Emissions Reduction in China*. Sustainability, 11, 5508. [DOI](https://doi.org/10.3390/su11195508). [PDF aberto](https://opus.lib.uts.edu.au/bitstream/10453/138094/1/Carbon%20Communities%20and%20Hotspots%20for%20Carbon%20Emissions%20Reduction%20in%20China.pdf). Começar pelas seções 3.1–3.4. Usa rede dirigida com um nó por setor-região e matriz de forma equivalente a F; não obriga a representação bipartida.
2. **Serrano, Boguñá e Vespignani (2009).** *Extracting the multiscale backbone of complex weighted networks*. PNAS, 106, 6483–6488. [Texto aberto](https://pmc.ncbi.nlm.nih.gov/articles/PMC2672499/). Fundamenta o filtro; não é uma aplicação de emissões.
3. **Liang, Feng e Xu (2015).** *Structure of the Global Virtual Carbon Network: Revealing Important Sectors and Communities for Emission Reduction*. Journal of Industrial Ecology, 19, 307–320. [DOI](https://doi.org/10.1111/jiec.12242). Examinar a construção da rede e a interpretação dos caminhos antes de reutilizar indicadores.
4. **Hanaka et al. (2017).** *Finding environmentally critical transmission sectors, transactions, and paths in global supply chain networks*. Energy Economics, 68, 44–52. [DOI](https://doi.org/10.1016/j.eneco.2017.09.012). Distinguir intermediação adaptada à MIP da função padrão de caminhos mínimos.
5. **Du et al. (2018).** *A network analysis of indirect carbon emission flows among different industries in China*. Environmental Science and Pollution Research, 25, 24469–24487. [DOI](https://doi.org/10.1007/s11356-018-2533-x). Conferir equações e filtragem no texto integral.
6. **Pereira, Diele-Viegas e Ribeiro (2024).** *GHG emissions in Brazilian Agriculture and livestock sectors and the risk to Amazonia conservation*. The European Physical Journal B, 97, 94. [DOI](https://doi.org/10.1140/epjb/s10051-024-00720-5). Comparar fronteira de GEE e CO₂ e verificar metodologia integral.
7. **Rifki, Ono e Kagawa (2017).** *The robustest clusters in the input–output networks: global CO₂ emission clusters*. Journal of Economic Structures, 6, 3. [Texto aberto](https://doi.org/10.1186/s40008-017-0062-2). Apoio para discutir sensibilidade de agrupamentos.

Miller e Blair (2009), capítulos 2, 10 e 12, permanece como referência do modelo insumo-produto, da extensão ambiental e dos encadeamentos. O fundamento dos algoritmos de redes deve vir das respectivas referências, sem atribuí-los ao livro.

## 10. Próxima decisão

Validar a pergunta centrada nas diferenças entre produção e demanda, o núcleo **volume + disparidade na rede completa externa + backbone dirigido**, os 67 nós e a separação F/W/diagonal. A contribuição de política será o diagnóstico de oportunidades de coordenação; cenários e avaliação de instrumentos ficam fora da etapa inicial. A fonte original do filtro já foi lida; falta converter suas exceções em uma especificação operacional inequívoca e verificar um caso pequeno. Em seguida, avaliar a base e os diagnósticos completos antes de filtrar ou desenhar. Comunidades só entram após essa avaliação. Esta revisão altera somente o planejamento: nenhum notebook, cálculo, figura ou resultado foi implementado ou alterado.


## 11. Revisão de exposição baseada em Nikolov

A revisão editorial distingue recomendações de exposição de validação científica. Nikolov (2023), *Writing Tips for Crafting Effective Economics Research Papers*, seções I, IV–VIII e X–XIII, fundamenta clareza, pergunta antecipada, comparação com estudos próximos, definição das medidas e figuras compreensíveis. As recomendações causais da seção VII não serão impostas ao desenho descritivo; limites de páginas e convenções de apresentação não substituem a template e os objetivos da disciplina.

**Revisão aplicada:** introdução com pergunta no segundo parágrafo e contribuição delimitada em relação a Huang; seção de dados mais compacta com quadro de fontes; derivação preservada; exemplo conferido com os outputs e acompanhado de contas numéricas; questões exploratórias em lugar das formulações H1/H2. A base ambiental permanece exploratória: a revisão não resolve sua validade.

**Próximas entregas, uma por vez:** (1) seção 3.3, construção da rede e distinção F/W; (2) seção 3.4, forças e concentração; (3) seção 3.5, filtro, casos especiais e cobertura. Cada seção será discutida antes da seguinte e de sua implementação. Não executar novos métodos como consequência automática desta revisão. Resumo e resultados permanecem reservados.

**Critérios de aceite editorial:** pergunta até o terceiro parágrafo; contribuição sem novidade indevida; definições principais sem repetição extensa; derivação e unidades auditáveis; figura e tabela provenientes da mesma versão; identidades separadas de achados; implicações proporcionais à evidência; PDF sem referências indefinidas e com conferência visual. Não atribuir nota global nem classificar seções ainda não desenvolvidas como falhas.


## 12. Papel da MIP e status dos notebooks

O foco da disciplina é a análise de redes. A seção 3.1 da entrega limita-se à sequência A/L e demanda por atividade → extensão ambiental C → matriz de atribuição F, com significado e unidades. A construção detalhada produto–atividade e a expansão em rodadas de produção permanecem nos notebooks, sem transferência automática para apêndices. A seção 3.2 mantém a interpretação das atribuições e o exemplo.

Os notebooks são exploratórios e versões de trabalho, incluindo v2/v3/v4, protótipos visuais e análises anteriores. Podem conter alternativas, notações históricas e resultados não adotados. Não constituem uma implementação final aprovada por sua mera existência. A entrega deve indicar os insumos, métodos e resultados efetivamente utilizados; a validade ambiental continua condicionada à auditoria. O planejamento orienta o escopo e o texto registra as definições da entrega em elaboração.
