# Especificação acadêmica final — Brasil, MIP 2015

**Título provisório:** Emissões próprias de CO₂ e centralidade como fornecedor na rede produtiva brasileira: uma análise da MIP de 2015.

**Status:** fechamento da especificação após exploração e validação interna. Este documento fixa a pergunta, o objeto e a apresentação do estudo; não constitui pré-registro nem confirmação em dados independentes. Os resultados foram conferidos nos CSVs e nas definições dos notebooks existentes. Não foram introduzidas métricas nem alterados cálculos.

**Decisão central:** manter a média de S fora da diagonal como medida principal; usar L como robustez da normalização e A como contraste direto. Tratar HEM como análise complementar de encadeamentos, distinguindo efeito externo absoluto de efeito por unidade de produção. Essa decisão substitui, para a redação final, a classificação de HEM normalizada como robustez equivalente da centralidade feita na etapa anterior. A divergência encontrada permanece documentada.

## 1. Pergunta e subquestão

**Pergunta:** Em que medida os setores com maior participação nas emissões próprias estimadas de CO₂ ocupam posições centrais como fornecedores diretos e indiretos na rede produtiva brasileira de 2015?

**Subquestão:** Como essa associação se altera quando se considera a escala econômica dos setores, medida pelo valor da produção bruta?

A pergunta mantém o conteúdo econômico original. “Estimadas” explicita que os coeficientes ambientais não constituem um inventário observado de 2015. “Centrais” será operacionalizado como participação monetária média nos requerimentos das cadeias dos demais setores, não como essencialidade. A subquestão exige uma comparação descritiva, sem atribuir ao tamanho um mecanismo causal.

## 2. Hipóteses de trabalho

**H1 — A ordenação setorial por emissão própria não reproduz a ordenação por centralidade como fornecedor nas cadeias dos demais setores.**

Examinar concordância global por Spearman, diferenças de postos e contrastes setoriais, sem definir um corte ex post que transforme correlação em aprovação/rejeição binária. Uma ordenação fortemente coincidente e desvios pequenos enfraqueceriam H1. Não basta encontrar uma única inversão de postos para sustentar divergência substantiva. H1 permite associação positiva e não postula independência.

**H2 — A associação positiva entre emissão própria e centralidade como fornecedor é menor após o ajuste descritivo pela escala econômica setorial.**

Comparar correlação bruta e correlação parcial de postos, usando os mesmos setores. Ausência de redução ou inversão sistemática desse padrão nas especificações próximas enfraqueceria H2. A hipótese não afirma que tamanho “explica” uma fração causal da relação, nem que a associação residual é zero.

Essas formulações organizam evidência já conhecida. Não contêm valores de correlação ou nomes de setores como condições de sucesso. Sua avaliação nesta base é descritiva e posterior à exploração, não um teste confirmatório com nível de significância pré-fixado.

## 3. Dados e fronteira do estudo

A MIP do IBGE contém 127 produtos e 67 atividades. O sistema atividade × atividade é reconstruído a partir das tabelas de produção, usos nacionais e participação na produção. Os valores monetários estão em **R$ milhões de 2015**. A fronteira é a produção doméstica, incluindo a destinada às exportações; não cobre emissões estrangeiras incorporadas nas importações.

As intensidades de Sanguinet e Azzoni (2024) são utilizadas em Gg CO₂ por R$ milhão. O cenário central é:

$$
\gamma^{2015}=\frac{3\gamma^{2011}+4\gamma^{2018}}7.
$$

Os cenários de 2011 e 2018 aplicam seus coeficientes à **mesma estrutura de 2015**. São sensibilidades ambientais, não uma série temporal. A fonte inclui componentes de uso da terra: não chamar o objeto de CO₂ exclusivamente fóssil, nem de GEE/CO₂ equivalente.

A compatibilidade monetária permanece pendente: a fonte utiliza preços de 2018 e o projeto mantém fator monetário 1 ao aplicar os coeficientes à MIP de 2015. A interpolação não resolve essa incompatibilidade. Um fator comum de correção de γ preservaria participações e postos; ajustes setoriais poderiam alterá-los. A estabilidade entre cenários da mesma fonte não valida essa harmonização.

O total central, aproximadamente **683,696 Mt CO₂**, é uma estimativa condicionada a essas escolhas, não um total nacional observado independentemente. Priorizar participações e postos, sem apresentar isso como solução para possíveis erros setoriais da fonte.

## 4. Notação e construção da rede

| Símbolo | Definição e interpretação |
| --- | --- |
| V, U, D | Produção produto × atividade; uso intermediário nacional produto × atividade; participação atividade × produto. |
| x | Produção bruta por atividade, obtida pelas colunas de V. Não é valor adicionado. |
| Z = DU | Fornecimento intermediário doméstico: linha i fornecedora, coluna j compradora. |
| y | Demanda final por produtos nacionais atribuída às atividades, incluindo exportações. |
| A = Z diag(x)⁻¹ | Requerimentos diretos: Aᵢⱼ = Zᵢⱼ/xⱼ. |
| L = (I − A)⁻¹ | Requerimentos totais por unidade de demanda final. |
| γᵢ | Intensidade de emissão própria, em Gg CO₂/R$ milhão. |
| eᵢ = γᵢxᵢ | Volume estimado de emissão própria, em Gg CO₂. |
| sᵢᵉ = eᵢ/Σₖeₖ | Participação nas emissões próprias estimadas do sistema. |
| λⱼ = ΣₖLₖⱼ | Soma dos requerimentos monetários brutos da cadeia final j. |
| Sᵢⱼ = Lᵢⱼ/λⱼ | Participação de i nesses requerimentos. |
| S̄ᵢ = Σⱼ≠ᵢSᵢⱼ/(n−1) | Participação média nas cadeias dos outros 66 destinos. |

O balanço é x = Z1 + y = Ax + y = Ly. A direção da rede direta é **fornecedor i → comprador j**. Em L e S, j identifica o destino final da cadeia, não necessariamente um comprador imediato de i.

Quando a expansão converge, L = I + A + A² + … agrega todos os comprimentos de caminhos ponderados pelos coeficientes técnicos. Essa representação constitui o conteúdo de redes do estudo: relacionar a origem emissora à sua posição nos encadeamentos produtivos. Não é necessário adicionar algoritmos genéricos de centralidade ou visualizar um grafo quase completo.

O estudo usa e, não a pegada do destino final. H = diag(γ)L é intensidade incorporada; P = H diag(y) atribui emissões aos destinos e satisfaz P1 = e. H e P permanecem como objetos de auditoria, sem entrar como variáveis ambientais concorrentes no núcleo. Evitar a notação C/c, ambígua nos notebooks históricos.

## 5. Medida principal: escolha de S em relação a L

### Interpretação de L

Lᵢⱼ é a produção monetária bruta de i requerida por uma unidade monetária de demanda final pelos produtos de j, sob os coeficientes fixos da MIP. Por exemplo, Lᵢⱼ = 0,10 representa R$ 0,10 de produção de i por R$ 1 de demanda final de j, considerando fornecimento direto e indireto. Essa leitura contábil não prevê o efeito de uma falta de insumo.

A soma λⱼ acumula produção bruta de diferentes atividades e etapas. Não é valor adicionado, preço final ou quantidade física: valores intermediários aparecem em etapas sucessivas.

### Normalização e média

Dividir a coluna j por λⱼ transforma requerimentos monetários em composição relativa:

$$
\sum_i S_{ij}=\frac{\sum_iL_{ij}}{\lambda_j}=1,
\qquad
\bar S_i=\frac1{66}\sum_{j\ne i}\frac{L_{ij}}{\lambda_j}.
$$

**Definição verbal a usar:** participação monetária média do setor, como fornecedor direto e indireto, nos requerimentos brutos das cadeias de demanda final dos demais setores.

“Presença nas cadeias” é uma abreviação dessa definição. Não significa frequência de ocorrência: uma participação elevada em poucos destinos também pode elevar a média. S̄ᵢ = 0,02 significa participação média de 2% nos requerimentos agregados dessas cadeias; não que 2% da economia desapareceria sem i. A soma dos S̄ᵢ não precisa ser 1, pois as cadeias próprias são excluídas.

### Diagonal e pesos

O destino j = i sai da média, mas λⱼ mantém **todas** as origens, inclusive Lⱼⱼ. Excluir a origem do próprio destino também do denominador criaria uma participação condicional distinta. Tampouco confundir retirar a diagonal de L com usar L − I: a segunda operação preserva os circuitos que retornam ao setor.

Excluir o destino próprio não remove o setor dos caminhos que atendem aos outros destinos. Os circuitos internos que contribuem para Lᵢⱼ, com i ≠ j, continuam incorporados.

Cada destino recebe peso 1/66, independentemente do seu tamanho observado. A pergunta é sobre posição relativa entre cadeias setoriais padronizadas. Ela não pretende estimar a distribuição efetiva da demanda, vendas ou perdas econômicas agregadas. Dividir ou agregar atividades pode mudar o indicador; não foi demonstrada invariância à classificação setorial.

### Decisão conceitual

**Escolha definitiva: S principal e L como robustez.** Para comparar a presença relativa entre destinos, a normalização acrescenta uma interpretação clara. Com ℓᵢ = Σⱼ≠ᵢLᵢⱼ, temos ℓᵢ = Σⱼ≠ᵢλⱼSᵢⱼ: cadeias com maior requerimento bruto total contribuem mais à soma não normalizada. S padroniza esse total antes de fazer a média.

L também tem interpretação legítima: fornecimento agregado requerido por um conjunto de demandas finais unitárias nos demais setores. A escolha por S não decorre de melhor correlação ou maior destaque de Energia. Empiricamente, os postos de ℓ e S̄ têm Spearman **0,9978**, e seus top 10 coincidem. A normalização acrescenta transparência sobre o estimando, não uma descoberta independente.

S não elimina toda influência de tamanho, preços relativos ou agregação. Sua vantagem é comparabilidade relativa de colunas; sua contrapartida é dar igual peso a destinos pequenos e grandes. Não chamar S̄ de “dependência média” sem explicitar que se trata de participação em requerimentos monetários contábeis.

## 6. Papel de A, L e S

A medida direta é aᵢ = Σⱼ≠ᵢAᵢⱼ; a alternativa total é ℓᵢ = Σⱼ≠ᵢLᵢⱼ. Seus postos serão usados como diagnósticos secundários. A usa unidades de **produção bruta** dos compradores, enquanto L usa unidades de **demanda final** dos destinos: a diferença de magnitudes entre as somas não deve ser chamada, sem ressalva, de efeito indireto isolado.

As correlações de postos são 0,9853 entre a e ℓ; 0,9837 entre a e S̄; e 0,9978 entre ℓ e S̄. A compartilha nove dos dez primeiros fornecedores de L/S. Portanto, a inclusão dos encadeamentos indiretos não altera radicalmente a hierarquia dos principais fornecedores, embora modifique magnitudes e algumas posições. São transformações da mesma MIP, **não três evidências independentes**.

## 7. HEM: complemento, não teste equivalente de S

Manter a única definição já calculada: extração completa no fechamento de alocação de Ghosh. Seja B = diag(x)⁻¹Z, G = (I − B)⁻¹ = diag(x)⁻¹L diag(x) e r = x − Zᵀ1. O fechamento xᵀ = rᵀG inclui importações em r; r não é simplesmente VAB.

Retiram-se linha e coluna i de B e a entrada rᵢ, mantendo as entradas e coeficientes dos demais. Para j ≠ i:

$$
\Delta x_j^{(i)}=\frac{x_iG_{ij}}{G_{ii}},\qquad
F_i=\sum_{j\ne i}\Delta x_j^{(i)},\qquad
h_i=\frac{F_i}{x_i}.
$$

A perda própria xᵢ fica separada. **Fᵢ** mede o efeito externo absoluto desse contrafactual contábil, em R$ milhões. **hᵢ** mede efeito externo por unidade da produção do setor extraído, sem unidade monetária. Não é elasticidade ou percentual de perda nacional.

Como hᵢ = Σⱼ≠ᵢLᵢⱼxⱼ/(xᵢLᵢᵢ), mudam o peso dos destinos, o ajuste pelos retornos ao próprio setor e a escala da origem. HEM não reproduz a pergunta de S, mesmo antes da divisão por xᵢ. Normalizar tampouco equivale ao ajuste estatístico por tamanho utilizado em H2.

Os dados mostram ρ(S̄,F) = **0,9710**, mas ρ(S̄,h) = **0,5662**. Energia é 10ª em F e 37ª em h; Comércio, 1º e 41º. Isso delimita a interpretação: elevada presença média e elevado efeito externo absoluto não implicam elevado encadeamento externo por unidade do próprio tamanho. **Não significa que Energia “não é central segundo HEM”.**

Apresentar F e h juntos no suplemento e registrar esse contraste em um parágrafo do texto principal. A alta concordância de F não constitui confirmação independente, e a discordância de h não refuta a definição de S. Continua refutada a extrapolação de um ranking invariável sob todas as noções de importância intersetorial.

A extração é descritiva, com alocação fixa. Não prevê fechamento real, essencialidade, preços, substituição ou bem-estar. A fundamentação e as ressalvas já estão documentadas no notebook de validação a partir de Dietzenbacher, van der Linden e Steenge; Miller e Lahr; e Oosterhaven. Não se propõe outra extração nesta etapa.

## 8. Metodologia final em seis subseções

1. **Dados:** MIP 2015, correspondência das 67 atividades, coeficientes ambientais, unidades e limitações de preços. Conferir entradas e alinhamento pelo manifesto.
2. **Emissões próprias:** calcular e = γ ⊙ x e participações. Usar γ e x para interpretar a identidade, não como variáveis ambientais intercambiáveis. Resumir concentração em um parágrafo.
3. **Rede produtiva:** reconstruir Z, A e L; verificar balanços e concordância com as tabelas do IBGE. Explicitar a direção fornecedor → comprador/destino.
4. **Centralidade como fornecedor:** calcular S por normalização de colunas e S̄ pela média excluindo a cadeia própria. Justificar pesos e denominadores antes dos resultados.
5. **Relação ambiental–produtiva:** postos decrescentes com média em empates, Spearman, diferenças de postos, duas figuras e uma tabela de contrastes. Calcular correlação parcial dos postos após retirar de ambos a projeção linear sobre constante e posto de x. Usar os 67 setores, sem exclusão seletiva.
6. **Robustez e complemento:** comparar a e ℓ, repetir resultados principais com γ2011/γ2018 e resumir influência e forma funcional já disponíveis. Reservar HEM absoluta/normalizada a complemento com estimandos distintos. Sem novas métricas, cortes ou modelos.

A correlação parcial é Corr(uₑ,uₛ), em que uₑ e uₛ são os resíduos das regressões dos postos de e e S̄ sobre constante e posto de x. Ela remove uma associação **linear entre postos**, não controla todas as relações possíveis com tamanho. Os setores não são uma amostra IID; não usar p-valores convencionais como prova de validade.

## 9. Resultados centrais: sequência para a redação

1. **Concentração como contexto.** Os top 5 e top 10 emissores reúnem 30,30% e 48,28% do total estimado. Gini de e = 0,504 e de x = 0,534; na produção, top 5 = 34,94% e top 10 = 50,44%. Há desigualdade setorial, mas ela não é excepcionalmente superior à concentração econômica por esses indicadores. Não generalizar para todo indicador/cenário: o HHI se inverte ligeiramente com γ2018.
2. **Hierarquia produtiva relativamente estável.** A, L e S concordam fortemente na ordenação dos fornecedores. A normalização de cadeias altera a interpretação mais do que os postos. Não multiplicar a evidência contando cada transformação como confirmação independente.
3. **Associação sem coincidência.** Spearman(e,S̄) = **0,3964**; a mediana da diferença absoluta de postos é **16 posições**. Para a e ℓ, as correlações ambientais são 0,4011 e 0,3828. A associação é positiva e de magnitude intermediária, com divergências expressivas; não se conclui independência nem equivalência.
4. **Atenuação com escala econômica.** A parcial de postos por x é **0,1723**, enquanto ρ(S̄,x) = **0,5200** e ρ(S̄,γ) = **−0,1718**. A associação se reduz substancialmente quando se considera a escala. Não calcular uma “porcentagem explicada” pela diferença entre correlações. Em log–log, a correlação bruta de 0,4313 cai para 0,2690 após ajuste por log x, nos mesmos 66 setores com S̄ > 0. A associação residual não é invariavelmente próxima de zero.
5. **Sobreposições e contrastes.** Energia/utilidades e Comércio combinam posições ambientais e produtivas elevadas na definição principal. Água/resíduos e Construção têm posição ambiental muito superior à produtiva; Refino e Transporte terrestre apresentam o contraste oposto. Isso não delimita classes naturais nem demonstra que somente dois setores podem ser relevantes.
6. **Estabilidade delimitada.** Com coeficientes 2011/interpolados/2018, a correlação ambiental–S̄ é 0,3832/0,3964/0,4069 e a parcial é 0,1591/0,1723/0,2005. Energia mantém rank emissor 1; Comércio ocupa 5/7/8. Excluir simultaneamente Energia e Comércio mantém correlação bruta de 0,349 e parcial de 0,152. HEM por x mede outra dimensão e não sustenta destaque universal dos dois setores.

O ajuste exploratório log S̄ em log x tem R² = 0,168: descrever como ajuste dentro desta base, sem dizer que tamanho causa 16,8% da centralidade. Os detalhes logarítmicos e de influência ficam no suplemento; a exposição principal requer apenas a atenuação de postos.

## 10. Figuras que permanecem

**Figura 1 — Emissão própria e participação média nos requerimentos produtivos.** Reutilizar a [figura principal existente](../outputs/validacao_emissao_centralidade_2015/figura_1_principal.png), com participação emissora no eixo horizontal e 100S̄ no vertical. Manter os seis contrastes identificados e todos os 67 setores no cálculo. A dispersão é parte do resultado; não impor uma linha ajustada para reforçar visualmente a associação. Legenda: cada destino tem peso igual; o percentual vertical não é parcela da produção nacional.

**Figura 2 — Ranking ambiental × ranking de fornecedor.** Reutilizar os dados e rótulos do [gráfico existente](../outputs/validacao_emissao_centralidade_2015/figura_2_ranks.png), incluindo a diagonal de postos iguais e os maiores desvios. Os eixos existentes crescem de 1 a 67: posições mais altas nos rankings ficam próximas do canto inferior esquerdo; explicitar “1 = maior”. Para a composição final do artigo, preferir ambos os eixos de 67 para 1, de modo que posições maiores em relevância fiquem no canto superior direito. Inverter ambos preserva a diagonal de 45° e é apenas uma mudança de apresentação, não de postos. Não inverter apenas um eixo e manter uma diagonal ascendente como se nada tivesse mudado.

A versão com eixo emissivo logarítmico permanece somente no suplemento. Não incluir grafos, quadrantes com cortes ou fronteira de Pareto nas figuras principais. As imagens arquivadas permanecem intactas nesta etapa de especificação.

## 11. Única tabela setorial principal

Usar seis contrastes, sem apresentá-los como classificação exaustiva. Valores abaixo conferidos em `setores_completos.csv` e `tabela_principal.csv`. Rank 1 significa o maior valor; empates em intensidade recebem posto médio.

| Setor (código) | Emissões (%) | Rank e | Rank x | Rank γ | Rank S̄ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Energia e utilidades (3500) | 8,28 | 1 | 10 | 10 | 6 |
| Água e resíduos (3680) | 7,58 | 2 | 41 | 1 | 32 |
| Construção (4180) | 5,68 | 3 | 3 | 35 | 25 |
| Comércio (4580) | 3,91 | 7 | 1 | 60,5 | 1 |
| Refino de petróleo (1991) | 1,33 | 26 | 6 | 60,5 | 2 |
| Transporte terrestre (4900) | 0,77 | 37 | 7 | 65 | 3 |

Essa tabela substitui na redação final a tabela com quatro rankings de centralidade: torna visível e = γx e reduz redundância. A tabela anterior e os rankings completos continuam disponíveis. A/L, F/h, cenários e correlações detalhadas pertencem ao suplemento, não a novas tabelas principais.

## 12. Interpretação dos setores-chave

**Energia/utilidades:** combina escala e intensidade elevadas, ambas em décimo lugar. É primeira em emissão, sexta em S̄ e nona/sétima em a/ℓ. Sua presença média é aproximadamente 1,75% dos requerimentos brutos das demais cadeias. O código agrega eletricidade, gás natural e outras utilidades: não atribuir todo o resultado à eletricidade isoladamente. Rank 10 em F e 37 em h distingue efeito externo absoluto de efeito por unidade do próprio tamanho.

**Água/esgoto/resíduos:** segundo emissor com produção em 41º e intensidade em primeiro. O contraste é compatível principalmente com a intensidade elevada atribuída pela fonte, não com grande escala. Os postos 34/33/32 em a/ℓ/S̄ confirmam menor posição relativa como fornecedor. A plausibilidade ambiental dessa alocação precisa de validação externa; não deduzir daí baixa essencialidade dos serviços.

**Construção:** terceiro lugar tanto em emissão quanto em produção, mas intensidade intermediária (35º). É um caso compatível com escala elevada, sem posição equivalente no fornecimento às demais cadeias (25º em S̄). Sua relação com demanda final difere da de fornecedores intermediários. Não interpretar esse posto como irrelevância econômica ou capacidade de substituição.

**Comércio:** primeiro em produção e em S̄, sétimo emissor, com intensidade baixa relativamente aos demais. A escala é relevante para seu volume emissivo. Seu resíduo no ajuste log S̄–log x ocupa a oitava posição entre 66 atividades: a posição produtiva não se resume ao tamanho nesse diagnóstico. É outra sobreposição importante e impede apresentar Energia como única exceção. Rank 1 em F versus 41 em h preserva a distinção de estimandos.

**Refino/coquerias:** sexto em produção, segundo em S̄ e 26º em emissão, com intensidade em posto 60,5. O contraste acompanha a baixa intensidade própria da fonte, apesar da presença produtiva elevada. Emissão própria do refino não abrange automaticamente toda a combustão posterior dos combustíveis. Não inferir baixa relevância climática do ciclo de vida do petróleo.

**Transporte terrestre:** sétimo em produção, terceiro em S̄ e 37º em emissão, com intensidade em 65º. A divergência é condicionada ao coeficiente e à atribuição ambiental utilizados; não sustenta a afirmação geral de que transporte terrestre emite pouco. Sua alta posição produtiva também aparece em A/L. Os resíduos de Refino e Transporte no ajuste logarítmico ocupam quarto e quinto lugares, sem constituírem novas centralidades principais.

Essas leituras são descrições da identidade multiplicativa e dos postos. Rankings de x e γ não permitem atribuir percentuais causais da emissão a “escala” e “intensidade”.

## 13. O que sai do texto principal

| Destino editorial | Análises e motivo |
| --- | --- |
| Remover do argumento final | Afirmações de essencialidade, colapso, causalidade e “todos dependem dos maiores emissores”; grupos naturais definidos por top-k; Energia como única exceção; equivalência entre S̄ e h. Não são sustentadas. |
| Suplemento conciso | Rankings a/ℓ/S̄, cenários ambientais, versão log da figura, ajuste logarítmico e influência, F e h lado a lado. Qualificam diretamente a conclusão. |
| Documentação exploratória somente | PageRank, Katz, autovetor, betweenness, closeness, random walks, alcance binário, reachability, limiares 1%/5%/10%, similaridade de cosseno, clusters e projeções 3D. Não são necessários ao estimando final. |
| Documentação exploratória somente | Fronteira de Pareto, ranks compostos e curvas completas de top-k. Não identificam um grupo natural e a fronteira inclui o máximo emissor por construção. |
| Arquivo de validação, citado sem reproduzir integralmente | Muitas normalizações, variantes de diagonal, curvas de robustez redundantes e concentração extensa. Guardar a auditoria e as divergências; não alongar a exposição com resultados repetidos. |

“Remover” significa retirar da redação principal, **não apagar arquivos**. Os notebooks e relatórios históricos preservam decisões, resultados negativos e mudanças de interpretação, evitando apresentar uma escolha posterior à exploração como se tivesse sido fixada antes dela.

## 14. Limitações e vocabulário obrigatório

**Centralidade como fornecedor** designa posição na estrutura de fornecimento, operacionalizada aqui por S̄. **Presença nas cadeias** designa sua participação monetária média; não conta destinos. **Dependência contábil** refere-se aos requerimentos sob coeficientes fixos, sem demonstrar como compradores reagiriam à indisponibilidade de um insumo.

**Essencialidade** exigiria evidência de ausência de substitutos. **Importância sistêmica causal** exigiria modelar ou identificar respostas a choques, incluindo preços, estoques, capacidade, substituição e adaptação. A MIP utilizada não fornece isso. Não usar os dois termos como sinônimos de centralidade.

As conclusões também são limitadas por: uma única estrutura produtiva anual; agregação em 67 atividades; pesos iguais dos destinos; preços relativos e produção bruta somada entre etapas; coeficientes ambientais arredondados e interpolados; correspondência/alocação setorial da fonte; harmonização monetária pendente; e ausência de validação ambiental independente. A sensibilidade 2011/2018 não cobre essas incertezas integralmente.

Serviços domésticos têm S̄ = 0 e emissão positiva na fonte. Permanecem nos postos e nas análises principais; apenas especificações logarítmicas excluem esse zero e informam n = 66, sem adicionar constante. O pequeno lançamento negativo de Z foi preservado nas contas; sua sensibilidade já foi auditada. Não transformar a matriz em uma interpretação probabilística que ignore esses ajustes contábeis.

O fechamento fixa a especificação **para esta base**, não certifica seus níveis ambientais para publicação. Harmonização monetária e plausibilidade setorial devem ser resolvidas ou explicitamente assumidas como limitações materiais. Se uma correção de dados mudar resultados, registrar uma nova versão e recalcular esta mesma especificação; não procurar outra métrica para recuperar a narrativa.

## 15. Contribuição

Adotar **A como contribuição principal, qualificada**: demonstrar empiricamente que emissão própria e centralidade como fornecedor são atributos relacionados, mas não intercambiáveis, da estrutura setorial brasileira representada nesta base.

Usar **B como contribuição descritiva secundária**: identificar contrastes e sobreposições, especialmente Energia/utilidades e Comércio, sem criar um índice único de prioridade ou reivindicar exclusividade desses casos.

**C não será uma conclusão de política.** Os rankings sugerem que critérios de seleção baseados somente em emissão ou somente em presença produtiva geram ordenações diferentes. Não demonstram quais políticas seriam eficazes, seus custos, viabilidade ou efeitos indiretos. A contribuição é aplicada e estrutural; não é a invenção de uma nova centralidade nem uma alegação de ineditismo na literatura.

## 16. Conclusão em uma frase

Na base brasileira de 2015, emissão própria e presença como fornecedor se associam, mas seus rankings divergem, e a associação enfraquece após considerar a escala econômica.

## 17. Conclusão em um parágrafo

Na MIP brasileira de 2015, combinada aos coeficientes de CO₂ utilizados, os maiores emissores não coincidem sistematicamente com os fornecedores de maior participação média nos requerimentos das demais cadeias. A associação de postos é positiva e moderada (0,396), mas cai para 0,172 após ajuste descritivo pelo tamanho econômico. Energia/utilidades e Comércio combinam posições elevadas nas duas dimensões; Água/resíduos e Construção contrastam com Refino e Transporte terrestre. A concordância entre A, L e S sustenta a estabilidade da hierarquia na família de requerimentos produtivos, sem constituir evidência independente. Esses resultados descrevem relações contábeis condicionadas à base ambiental e não demonstram essencialidade nem efeitos causais de choques.

## 18. Conclusão completa

Os setores com maiores emissões próprias estimadas não são, de modo geral, os mesmos que ocupam as primeiras posições como fornecedores na rede produtiva brasileira de 2015. As duas dimensões apresentam associação positiva, mas diferenças expressivas de ordenação. Pela participação média nos requerimentos brutos das cadeias dos demais setores, a correlação de Spearman é 0,396 e a diferença absoluta mediana entre postos é de 16 posições. A contribuição do estudo está nessa combinação de associação e discordância, não em demonstrar independência.

A escala econômica acompanha parte desse padrão: a correlação entre presença produtiva e produção bruta é 0,520, e a associação ambiental–produtiva cai para 0,172 após o ajuste de postos por tamanho. A redução persiste nos cenários ambientais existentes e nos diagnósticos de influência. Entretanto, não equivale a uma decomposição causal, nem mostra que toda centralidade resulta de tamanho. A especificação logarítmica preserva associação residual maior, reforçando a necessidade de não declarar desaparecimento da relação.

Energia/utilidades combina escala e intensidade elevadas, enquanto Comércio combina grande escala com a primeira posição como fornecedor. Água/resíduos tem elevada emissão sobretudo em correspondência com a intensidade atribuída pela fonte; Construção combina grande escala e presença mais baixa como fornecedora às demais cadeias. Refino e Transporte terrestre apresentam forte presença produtiva e posições ambientais menores, condicionadas às intensidades próprias utilizadas. Esses casos ilustram atributos distintos e não constituem classes naturais ou uma lista definitiva de prioridades climáticas.

A hierarquia produtiva é semelhante em A, L e S, mas isso não autoriza um conceito universal de importância intersetorial. A extração hipotética distingue efeito externo absoluto de efeito por unidade da produção do setor, levando a posições diferentes para Energia e Comércio. O resultado final deve, portanto, permanecer restrito à presença monetária nos requerimentos produtivos. Agregação, interpolação e validade dos coeficientes, compatibilidade de preços e ausência de respostas comportamentais limitam a interpretação: o estudo não identifica insubstituibilidade, efeitos de paralisação ou políticas ótimas.

## 19. Estrutura sugerida do trabalho

1. **Introdução:** pergunta, relevância da distinção entre emissão própria e posição produtiva, H1/H2 e contribuição descritiva.
2. **Referencial:** redes de produção e requerimentos de Leontief; extensão ambiental; distinção entre centralidade contábil e efeitos causais. Aproveitar a revisão já realizada, sem catálogo de algoritmos.
3. **Dados e métodos:** as seis subseções da seção 8, com HEM delimitada brevemente e derivação no suplemento.
4. **Resultados:** contexto de concentração; figura 1; figura 2; tabela de seis contrastes; tamanho econômico e síntese de robustez.
5. **Discussão:** identidade e = γx, diferenças entre estimandos, limitações ambientais e alcance das conclusões.
6. **Conclusão:** resposta direta, contribuição e limites, sem converter centralidade em recomendação de intervenção.
7. **Suplemento:** diagnósticos próximos, HEM absoluta/normalizada e instruções de reprodução. O arquivo exploratório completo permanece no repositório.

## 20. Rastreabilidade e reprodução

Base documental: [exploração](../investigacao_redes_emissoes_2015.ipynb), [validação adversarial](../validacao_emissao_centralidade_2015.ipynb) e [roteiro de revisão](revisao_investigacao_2015.md), nos resultados publicados no commit `5b83a5f4dc9ea9538d431652db28f3a055a472eb`. Esta especificação revisa o enquadramento editorial do HEM, preservando as equações e os resultados daquela versão.

| Afirmação | Evidência auditável |
| --- | --- |
| Correlações brutas, por tamanho e logarítmicas | [associacoes.csv](../outputs/validacao_emissao_centralidade_2015/associacoes.csv) |
| Concordância A/L/S/h e sobreposição de postos | [convergencia_estrutural.csv](../outputs/validacao_emissao_centralidade_2015/convergencia_estrutural.csv), [sobreposicoes_estruturais.csv](../outputs/validacao_emissao_centralidade_2015/sobreposicoes_estruturais.csv) |
| Setores, escala, intensidade, F/h e resíduos | [setores_completos.csv](../outputs/validacao_emissao_centralidade_2015/setores_completos.csv) |
| Concordância de F com S e variantes | [variantes_definicao.csv](../outputs/validacao_emissao_centralidade_2015/variantes_definicao.csv) |
| Sensibilidade ambiental | [cenarios_associacoes.csv](../outputs/validacao_emissao_centralidade_2015/cenarios_associacoes.csv), [cenarios_ranks_pareto.csv](../outputs/validacao_emissao_centralidade_2015/cenarios_ranks_pareto.csv) — consultar postos, sem promover Pareto ao núcleo |
| Influência das observações | [influencia.csv](../outputs/validacao_emissao_centralidade_2015/influencia.csv) |
| Contexto de concentração | [concentracao.csv](../outputs/investigacao_redes_2015/concentracao.csv) |
| Derivações, R² e síntese anterior | [relatório da validação](../outputs/validacao_emissao_centralidade_2015/relatorio.html) |

Para reproduzir cálculos, executar da raiz o notebook de validação, seguindo suas células. As entradas canônicas e os resultados anteriores estão versionados; o notebook confere alinhamento, balanços e matrizes reconstruídas antes da análise. As versões e hashes estão nos JSONs de proveniência das duas etapas. O notebook permanece a entrada para cálculo; este documento é a entrada para redação e delimitação do argumento final.

As referências metodológicas e ambientais já utilizadas encontram-se nos notebooks e relatórios anteriores. A especificação não adiciona bibliografia nem reivindica uma nova revisão. A decisão final pode ser auditada sem aceitar a narrativa: ela identifica exatamente o que cada medida representa, os resultados que a sustentam e as extrapolações que devem ser abandonadas.
