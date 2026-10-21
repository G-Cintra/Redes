# Li et al. (2017): leitura crítica

18/10/2026. Fonte: [manuscrito aceito consultado](li_2017_sna_io_china_japan_manuscrito.pdf), 35 páginas, PolyU. [Publicação](https://doi.org/10.1016/j.jclepro.2017.05.200). Paginação do manuscrito, diferente da versão editorial. Leitura do texto principal, método e discussão; equação ambiental conferida visualmente na p. 13. Não auditamos os dados nem reproduzimos os resultados. O parecer se refere à versão obtida; eventuais correções editoriais não foram verificadas.

## 1. Desenho do artigo

Compara mudanças na estrutura produtiva da China (2002/2007/2012) e Japão (2000/2005/2011), compatibilizando atividades em 37 setores (seção 2.1). Combina dois componentes: rede dirigida de relações econômicas e avaliação ambiental insumo-produto. Retira autofornecimento da rede e examina densidade, distâncias, agrupamento e centralidades.

O componente ambiental trata CO₂, CH₄ e N₂O em CO₂ equivalente e inclui análise da eletricidade/calor. Portanto, nem o objeto de rede nem a fronteira de gases são iguais aos nossos F e CO₂.

## 2. O que o artigo acrescenta

Mostra uma alternativa em que a análise de redes está na estrutura produtiva e a conta ambiental é associada posteriormente. Isso é útil se nossa pergunta passar a ser posição produtiva versus emissão. Porém, essa escolha não pode ser apresentada como a mesma análise do backbone de atribuições finais.

O esforço de correspondência setorial também é relevante para uma aplicação futura em SC: classificações diferentes precisam ser harmonizadas antes de comparar métricas. A comparação de redes exige denominadores e universo de setores consistentes.

## 3. Problemas metodológicos que impedem reprodução acrítica

### Pequeno mundo não é condição de validade de SNA

As seções 2.1 e 2.1.1 (pp. 7–9) apresentam pequeno mundo como pré-requisito para aplicar análise de redes. Essa afirmação não é uma condição geral: redes desconectadas, árvores ou redes bipartidas continuam sendo objetos legítimos de análise. Não usar esse diagnóstico para aprovar ou rejeitar nosso projeto.

Em redes muito densas, distâncias próximas de um e agrupamento elevado podem decorrer mecanicamente da presença de muitas arestas. Uma caracterização de pequeno mundo exige comparação apropriada, não apenas valores aparentemente altos/baixos. Além disso, a fórmula de agrupamento impressa usa o denominador de pares não dirigidos, apesar da declaração de rede dirigida; a convenção não fica suficientemente clara.

### Grau, força e dimensão monetária

As equações (4)–(6), p. 11, somam xᵢⱼ e dividem por n − 1, chamando o resultado de grau ponderado. Se x representa transações monetárias, trata-se de força normalizada, não contagem de parceiros. Dividir por n − 1 não elimina escala econômica, preços ou unidade monetária. Comparações temporais exigem harmonização de preços; a equação sozinha não a resolve.

A fórmula de intermediação apresentada usa contagem de caminhos e uma normalização associada a pares não ordenados, sem esclarecer completamente direção, fração dos caminhos mínimos e transformação dos pesos em distâncias. Não é suficiente para transportar a implementação à nossa matriz.

### Denominador ambiental e dimensão da matriz

A equação (9), p. 12, define intensidade por GDPᵢ, explicitado como valor adicionado. Na p. 13, a equação (11) aplica essa intensidade à produção requerida por Leontief. No modelo usual, a intensidade que multiplica L deve ser emissão/produção bruta, não emissão/VAB. A unidade monetária compatível não torna os denominadores conceitualmente equivalentes. É preciso esclarecer se houve conversão nos dados; ela não está resolvida nas definições consultadas.

Na mesma página, o texto chama Y de vetor coluna e a equação (11) usa Y diagonalizada para obter uma matriz. A leitura matricial é possível pelo acento, mas a definição textual é ambígua. RLY produz um vetor se Y for coluna; RL diag(y) produz a matriz origem/destino. Não corrigir silenciosamente a notação e afirmar reprodução do artigo.

### Inferências econômicas excessivas

Maior densidade não demonstra maiores lucros; menor distância não identifica eficiência física, circulação de informação ou ausência de substitutos. O artigo associa propriedades de rede a interpretações de desenvolvimento e política que não foram causalmente identificadas pelas métricas. Também não basta remover uma aresta para inferir paralisação real do sistema.

## 4. Adaptação para nosso trabalho

- Usar como comparação entre **rede econômica direta** e **rede de atribuição ambiental total**.
- Manter φ = emissão/produção bruta e documentar separadamente qualquer razão por VAB.
- Separar grau binário, força e distância, com definição explícita de cada peso.
- Não acrescentar pequeno mundo como requisito nem betweenness convencional sobre F.
- Preservar diagonal nas contas econômicas e ambientais; sua retirada em W é uma escolha sobre relações entre atividades, não correção da MIP.
- Não importar a dimensão temporal: temos um único sistema econômico de 2015.

## 5. Consequência para pergunta e dissertação

A fonte não justifica mudar agora para uma pergunta de evolução da estrutura industrial. Essa mudança exigiria outras bases e aumentaria o escopo. Reforça, porém, a necessidade de escolher se estudamos relações diretas de produção ou atribuições finais e de não alternar entre elas nas interpretações.

Na dissertação, o maior aproveitamento é o cuidado com compatibilização setorial, fronteiras de gases e denominadores. **Parecer:** referência comparativa secundária; não adotar suas fórmulas como especificação principal da nossa análise.
