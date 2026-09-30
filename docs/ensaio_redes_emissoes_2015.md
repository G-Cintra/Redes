# Emissões e centralidade como fornecedor na economia brasileira de 2015

**Ensaio exploratório para discussão acadêmica.** Resultados baseados na investigação da MIP brasileira de 2015. Os valores ambientais são cenários calculados com coeficientes cuja validade final permanece pendente; não constituem um inventário observado das emissões setoriais.

## Resumo

Este ensaio examina a relação entre emissão própria e centralidade como fornecedor nas 67 atividades da Matriz de Insumo-Produto brasileira de 2015. A centralidade é definida pela soma dos elementos de cada linha da inversa de Leontief, excluindo a diagonal, e expressa os requerimentos diretos e indiretos do fornecedor para demandas finais unitárias dos demais setores. O cenário ambiental resulta da aplicação de intensidades interpoladas de 2011 e 2018 à produção bruta de 2015. Quatro figuras articulam concentração, hierarquia produtiva, associação ambiental–estrutural e ajuste por escala econômica. Os dez maiores emissores reúnem 48,3% das emissões do cenário, frente a 50,4% da produção nos dez maiores produtores. A hierarquia de fornecedores é estável sob normalização das cadeias. Emissão e centralidade têm correlação de postos de 0,383, que se reduz a 0,158 após ajuste descritivo por produção bruta. Há associação positiva e diferenças relevantes de ordenação. Entretanto, problemas de compatibilidade monetária, fronteira e alocação dos coeficientes limitam a conclusão ambiental. O resultado estrutural é defensável dentro da MIP; a interpretação conjunta permanece exploratória até a reconciliação da extensão ambiental.

**Palavras-chave:** insumo-produto; redes de produção; emissões setoriais; centralidade de fornecedor; economia brasileira.

## A pergunta sobre emissão e posição produtiva

O volume de emissão de uma atividade e sua posição na organização da produção descrevem aspectos diferentes da economia. Uma atividade pode apresentar grande emissão por operar em grande escala, por emitir muito por unidade produzida ou por combinar essas características. Sua posição como fornecedora, por sua vez, depende dos insumos requeridos pelas outras atividades e dos encadeamentos que conectam os diferentes estágios de produção. Não há razão contábil para que as duas ordenações sejam idênticas.

A distinção é relevante para interpretar listas de setores ambientalmente importantes. Identificar os maiores emissores informa onde um dado inventário atribui emissões. Identificar fornecedores centrais informa quais atividades aparecem com maior peso nos requerimentos produtivos das demais cadeias. Nenhuma dessas informações, isoladamente, demonstra quais setores seriam insubstituíveis, quais paralisações teriam os maiores efeitos ou quais intervenções ambientais seriam mais eficazes.

O ensaio pergunta em que medida os setores com maior emissão própria também ocupam posições centrais como fornecedores diretos e indiretos na economia brasileira de 2015. A subquestão é como essa associação se modifica quando se considera a escala econômica, medida pela produção bruta. A análise é descritiva: não identifica efeitos causais e não trata as 67 atividades como uma amostra aleatória de setores independentes.

O argumento desenvolvido é que emissão e posição produtiva se associam, mas não são atributos intercambiáveis. Esse argumento tem, neste estágio, uma delimitação empírica importante. A estrutura de produção é obtida da MIP; o vetor ambiental é um cenário construído com intensidades de outra fonte e outros anos. A auditoria dos coeficientes permite utilizá-lo para exploração metodológica, mas ainda não sustenta seus postos como um ranking validado das emissões próprias brasileiras de 2015.

## Dados e definição dos objetos

A análise usa a MIP do IBGE de 2015, no nível de 67 atividades e 127 produtos. A matriz de fornecimento intermediário doméstico entre atividades, Z, é obtida pela combinação dos usos nacionais com as participações das atividades na produção de cada produto. A linha i identifica o fornecedor e a coluna j, o comprador. O vetor x contém a produção bruta em milhões de reais de 2015; a demanda final doméstica por produção nacional inclui exportações, sem incorporar emissões estrangeiras de produtos importados. As entradas e sua integridade estão registradas no [manifesto do projeto](../raw/manifesto.csv).

Os coeficientes técnicos e os requerimentos totais são definidos por:

$$
A=Z\operatorname{diag}(x)^{-1},\qquad L=(I-A)^{-1}.
$$

O elemento Lᵢⱼ representa a produção monetária bruta da atividade i requerida por uma unidade monetária de demanda final pelos produtos de j. Como x = Ly, a linha i reúne os requerimentos do fornecedor para os diferentes destinos finais. A medida principal é:

$$
C_i^{sup}=\sum_{j\ne i}L_{ij}.
$$

Essa soma atribui a mesma unidade monetária de demanda final a cada um dos demais destinos. Ela agrega fornecimento direto e indireto, sem ponderar pela demanda final observada. A exclusão da diagonal retira o destino próprio do agregado; não elimina os circuitos produtivos que participam do atendimento aos outros destinos. A medida não é uma parcela do PIB, nem a perda econômica que ocorreria com a retirada do setor.

A interpretação como centralidade de fornecedor aproxima-se da família de medidas baseadas nos requerimentos de produção discutida por [Blackburn e Moreno-Cruz (2019)](https://www.ifo.de/DocDL/cesifo1_wp8007.pdf) e [Ghassibe e Nakov (2025)](https://www.cerge.cuni.cz/pdf/events/papers/GN_latest.pdf). As convenções não são idênticas: a primeira referência usa ponderação pelo consumo final, enquanto a segunda inclui o termo próprio e apresenta orientação matricial diferente. Aqui se explicita uma medida com destinos unitários e exclusão da diagonal, sem importar os resultados causais dos modelos dessas referências.

Como robustez de normalização, utiliza-se:

$$
S_{ij}=\frac{L_{ij}}{\sum_kL_{kj}},\qquad
\bar S_i=\frac{1}{66}\sum_{j\ne i}S_{ij}.
$$

S̄ mede a presença relativa média do fornecedor em cadeias cujo total de requerimentos foi padronizado. O denominador de cada coluna mantém todas as origens, inclusive a origem do próprio destino. O contraste direto é a soma de A por linha fora da diagonal. Como A divide transações pela produção bruta do comprador e L se refere à demanda final, a diferença de suas somas não constitui automaticamente um efeito indireto isolado.

O cenário ambiental usa a Tabela 2 de [Sanguinet e Azzoni (2024)](https://doi.org/10.1016/j.rspp.2024.100015), com intensidades declaradas como CO₂ por produção bruta, em Gg por milhão de reais. A transformação é:

$$
\gamma_i^{cen}=\frac{3\gamma_i^{2011}+4\gamma_i^{2018}}{7},\qquad
e_i^{cen}=\gamma_i^{cen}x_i^{2015}.
$$

Os 134 coeficientes anuais conferem com a publicação. A interpolação localiza 2015 entre os dois anos, mas não observa sua tecnologia ou emissão física. Além disso, o ajuste monetário da fonte e a produção de 2015 não foram reconciliados. Por isso, eᶜᵉⁿ é denominado emissão do cenário ao longo do texto. A intenção conceitual é emissão própria, distinta da emissão incorporada nos insumos comprados ou da pegada de consumo. CO₂, CO₂e e GEE não são usados como sinônimos.

## Concentração ambiental e concentração econômica

A primeira figura estabelece o contexto distributivo. Emissão e produção apresentam concentração setorial: uma parcela relativamente pequena das atividades responde por uma parcela importante de cada agregado. Entretanto, os indicadores do cenário central não mostram uma concentração ambiental excepcionalmente superior à econômica.

![Figura 1 Concentração das emissões do cenário e da produção bruta](../outputs/investigacao_redes_2015/ensaio/figura_1_concentracao.png)

**Figura 1. Concentração setorial das emissões do cenário e da produção bruta.** Curvas de Lorenz das 67 atividades, ordenadas separadamente em cada variável. A linha pontilhada representa distribuição igualitária. Fonte: outputs da investigação, MIP/IBGE e coeficientes Sanguinet–Azzoni. Emissões calculadas com o vetor interpolado, sem harmonização monetária final.

Os dez maiores emissores concentram 48,3% da emissão calculada, enquanto os dez maiores produtores concentram 50,4% da produção. O Gini é 0,504 para emissão e 0,534 para produção. A comparação qualifica a percepção de concentração: a emissão é desigual entre atividades, mas a desigualdade econômica também é expressiva.

Esses resultados não implicam que os setores nos primeiros lugares sejam os mesmos. As curvas ordenam cada distribuição de forma independente. Tampouco se afirma que a concentração ambiental seja menor sob qualquer medida: os cenários e indicadores da investigação apresentam diferenças, incluindo inversão da comparação por HHI quando se aplicam os coeficientes de 2018. A figura fornece contexto, sem escolher um limiar que defina um grupo natural de emissores.

Passar da concentração agregada à posição de cada atividade exige examinar as relações de fornecimento. Uma economia pode ter distribuições de produção e emissão semelhantes e, ainda assim, atribuir posições diferentes aos mesmos setores em cada dimensão.

## A hierarquia dos fornecedores

A segunda figura apresenta os dez setores com maior centralidade em L. Comércio, Refino de petróleo e Transporte terrestre ocupam as primeiras posições, seguidos por Intermediação financeira e Agricultura. A presença de serviços entre os fornecedores centrais é coerente com uma medida monetária de requerimentos produtivos: a rede não descreve apenas materiais ou energia física.

![Figura 2 Principais fornecedores em L com comparação dos postos em S e A](../outputs/investigacao_redes_2015/ensaio/figura_2_fornecedores.png)

**Figura 2. Centralidade como fornecedor nos requerimentos de Leontief.** Barras representam Cˢᵘᵖ; as colunas laterais mostram postos em S̄ e na soma direta de A, calculados entre as 67 atividades, com 1 indicando a maior centralidade. Fonte: MIP/IBGE e cálculos da investigação. A figura independe da extensão ambiental.

A correlação de postos entre L e S é 0,9978, e seus conjuntos de dez primeiros setores coincidem. A normalização do total requerido por cada cadeia altera pouco a hierarquia geral. Entre A e L, a correlação é 0,9853, com nove setores comuns nos dez primeiros. Assim, grande parte da hierarquia já é visível nos vínculos diretos e permanece quando os encadeamentos indiretos são incorporados.

Há mudanças localizadas relevantes. Refino ocupa o sexto posto no contraste direto e o segundo em L. Extração de petróleo e gás passa do 27º ao décimo. Esses exemplos impedem interpretar a elevada correlação global como equivalência exata entre medidas. Cada objeto preserva sua definição, e a normalização S muda o estimando para uma presença relativa média.

A concordância é uma propriedade interna da estrutura produtiva representada pela MIP. A, L e S não oferecem três evidências independentes, porque derivam da mesma base e estão relacionados matematicamente. O resultado defensável é mais delimitado: a identificação dos principais fornecedores não depende fortemente da padronização das cadeias adotada neste exercício. Isso não demonstra invariância a outras agregações, outros preços relativos ou respostas comportamentais.

## Associação positiva e diferenças setoriais

A terceira figura confronta a posição produtiva com a participação nas emissões do cenário. Cada ponto representa uma atividade, com a mesma área visual; os seis destaques retomam os contrastes discutidos na investigação. A centralidade no eixo vertical é a soma de L fora da diagonal, e não um percentual da produção nacional.

![Figura 3 Emissões do cenário e centralidade como fornecedor](../outputs/investigacao_redes_2015/ensaio/figura_3_emissao_centralidade.png)

**Figura 3. Participação emissora e centralidade como fornecedor.** Dispersão das 67 atividades em escala linear. Spearman é calculado com postos médios em empates. Fonte: outputs da investigação. As posições ambientais são condicionadas aos coeficientes atuais, cuja alocação e compatibilidade monetária ainda não estão validadas.

A correlação de Spearman é 0,383. Portanto, existe associação positiva, mas a ordenação ambiental não reproduz a hierarquia produtiva. A diferença absoluta mediana entre os postos é de 16 posições. A interpretação adequada combina esses dois elementos: associação e discordância. Não se conclui independência entre emissão e posição produtiva.

Energia/utilidades aparece como primeiro emissor do cenário e sétimo fornecedor em L. O setor combina intensidade e produção elevadas, ambas no décimo posto, mas agrega eletricidade, gás natural e outras utilidades. Seu resultado não pode ser atribuído exclusivamente à geração elétrica. Comércio ocupa o primeiro posto estrutural e o sétimo ambiental. Sua grande produção, combinada com intensidade relativamente baixa, gera volume emissivo relevante no cenário; no comércio, produção deve ser entendida como o serviço comercial, não como vendas brutas das mercadorias.

Água/esgoto/resíduos e Construção apresentam outra configuração. São o segundo e o terceiro emissores do cenário, mas ocupam os postos 33 e 27 em L. No primeiro caso, a posição ambiental acompanha principalmente a intensidade atribuída pela fonte: o setor é apenas o 41º em produção. Construção, por sua vez, é terceira em produção e tem intensidade intermediária. Essa leitura decorre da identidade e = γx, sem atribuir percentuais causais a cada componente.

Refino e Transporte terrestre constituem o contraste inverso. Ocupam os postos dois e três em L, mas 26 e 37 em emissão. A emissão própria de Refino não abrange toda a combustão posterior dos combustíveis vendidos; a de Construção não deve receber automaticamente as emissões de fabricação do cimento e do aço adquiridos. Para Transporte, a ponte entre combustão territorial e atividade econômica precisa separar famílias e frotas próprias de outros setores. Essas distinções são essenciais para interpretar os pontos.

Os contrastes não constituem classes naturais nem uma lista de prioridades climáticas. Em particular, a alta intensidade de Água/resíduos e a baixa intensidade de Transporte terrestre exigem validação externa. A figura mostra fielmente o cenário calculado, mas sua precisão gráfica não elimina a incerteza do vetor ambiental.

## O ajuste descritivo pela escala econômica

A associação entre emissão e centralidade pode acompanhar a escala econômica dos setores. Pela identidade e = γx, maior produção implica maior emissão quando se mantém a intensidade. Ao mesmo tempo, a produção bruta apresenta correlação de postos de 0,512 com a centralidade em L. Isso motiva um ajuste descritivo por tamanho, sem pressupor uma relação causal entre as variáveis.

Para cada uma das variáveis emissão e centralidade, seus postos são projetados sobre uma constante e o posto de x. A correlação entre os dois vetores de resíduos constitui a correlação parcial de postos. Os mesmos 67 setores permanecem nos dois painéis da quarta figura, inclusive Serviços domésticos, cuja centralidade fora da diagonal é zero. Não se adiciona constante à medida nem se selecionam observações para fortalecer a associação.

![Figura 4 Associação antes e depois do ajuste pelo tamanho econômico](../outputs/investigacao_redes_2015/ensaio/figura_4_ajuste_tamanho.png)

**Figura 4. Associação de postos e ajuste pela produção bruta.** O painel A usa postos crescentes, com 67 indicando o maior valor. O painel B mostra resíduos após projeção linear dos postos de emissão e centralidade sobre constante e posto da produção. Sua correlação de Pearson é a parcial de postos; os resíduos não são ranqueados novamente. As cores identificam os mesmos seis contrastes da figura 3. Fonte: outputs da investigação, cenário ambiental exploratório.

A correlação cai de 0,383 para 0,158. A redução mostra que a associação linear entre os postos de tamanho e os outros dois conjuntos de postos participa do padrão observado. Não autoriza afirmar que tamanho “explica” uma porcentagem calculada pela diferença entre correlações, nem que a relação residual seja nula. Tampouco transforma os resíduos em uma nova medida de importância produtiva.

O resultado permanece dependente da forma de descrição. O diagnóstico logarítmico já documentado na auditoria, usando as 66 atividades com centralidade positiva, preserva associação residual maior, de aproximadamente 0,254. Essa diferença reforça que o ajuste de postos não remove todas as relações possíveis com escala.

Nos cenários que aplicam as intensidades de 2011 e 2018 à mesma MIP de 2015, a correlação bruta em L é, respectivamente, 0,371 e 0,393; as parciais são 0,147 e 0,186. Excluir simultaneamente Energia e Comércio mantém associação bruta de 0,335 e parcial de 0,138. Esses diagnósticos indicam que a atenuação não depende exclusivamente de um dos dois vetores anuais ou da presença desses dois setores. São sensibilidades internas, não validação ambiental independente.

## O alcance ambiental dos resultados

A principal restrição do ensaio está na interpretação do vetor ambiental. A [auditoria dos coeficientes](auditoria_coeficientes_emissoes_2015.md) classificou a base como **C, útil apenas como proxy exploratória**. Essa decisão distingue a correção da implementação da validade do insumo: os números publicados foram transcritos corretamente, mas não foram recuperados os numeradores físicos e os pesos de alocação que os produziram.

A compatibilidade monetária também permanece material. A fonte informa ajuste da estrutura de 2011 para preços de dezembro de 2018, enquanto a investigação usa produção monetária de 2015 com fator de conversão igual a um. Um multiplicador comum positivo preservaria os postos por identidade, mas não demonstraria que a correção efetivamente necessária seja igual entre atividades. A interpolação não resolve esse problema, nem representa mudanças observadas na tecnologia, na composição energética ou nos preços setoriais de 2015.

Há ainda ambiguidade sobre a fronteira ambiental implementada. O artigo apresenta descrições contraditórias sobre a inclusão de emissões associadas ao uso da terra. Sua declaração de CO₂ não permite tratar os coeficientes como CO₂e ou como todos os gases de efeito estufa. A agregação água/esgoto/resíduos merece atenção especial porque uma parcela importante das emissões de resíduos em inventários corresponde a gases distintos do CO₂.

A comparação com o inventário brasileiro reforça a necessidade de conciliação. No cenário, minerais não metálicos e siderurgia apresentam, respectivamente, cerca de 4,99 e 4,06 Mt. O inventário de 2015 registra aproximadamente 23,90 Mt somente no processo de fabricação de cimento e 43,39 Mt nos processos de ferro/aço. Esses componentes maiores que os totais setoriais calculados levantam uma discrepância material para a interpretação abrangente de emissão própria. As fontes, as páginas e os limites dessa comparação estão documentados na auditoria, com base no [BUR5 do Brasil](https://unfccc.int/sites/default/files/resource/BRA_BUR5_EN.pdf), cuja [cópia consultada](https://cdn.climatepolicyradar.org/navigator/BRA/2024/brazil-biennial-update-report-bur5_a3a92935f0bfdb543d96efe03ba6771e.pdf) está identificada por hash.

Para Água/resíduos e Transporte, diferenças de classificação impedem uma substituição direta por totais de inventário. A inexistência de uma correspondência imediata não valida os coeficientes atuais: define o trabalho necessário para validá-los. Do mesmo modo, a pouca mudança na correlação após excluir Água não torna confiável seu contraste setorial. Influência estatística dentro de um cenário e confiabilidade do dado são problemas diferentes.

A robustez estrutural, portanto, está em estágio mais avançado que a ambiental. As extrações hipotéticas já calculadas ficam como complemento: efeito externo absoluto e efeito por unidade da produção respondem a perguntas distintas da centralidade em L. Sua divergência não deve ser usada para escolher uma métrica que preserve ou amplifique a narrativa ambiental.

## Conclusão

A investigação distingue concentração, escala e posição nas cadeias produtivas. No cenário analisado, a concentração das emissões é próxima da concentração econômica; os principais fornecedores apresentam hierarquia estável na família A/L/S; emissão e centralidade têm associação positiva com diferenças relevantes de ordenação; e a associação se reduz após ajuste descritivo pela produção bruta. As quatro figuras tornam visível essa sequência sem recorrer a novas centralidades ou a grupos setoriais definidos por cortes arbitrários.

O resultado estrutural pode ser defendido como uma descrição da MIP de 2015 sob as convenções adotadas. A conclusão ambiental–produtiva exige maior cautela: sua reprodução interna não basta para confirmar que os coeficientes representam adequadamente as emissões próprias daquele ano. Os contrastes identificados permanecem hipóteses descritivas condicionadas à extensão utilizada.

A contribuição atual do ensaio é estabelecer uma comparação transparente entre atributos ambientais e produtivos e mostrar onde essa comparação depende de dados ainda não validados. O próximo passo empírico é obter uma extensão física de 2015, reconciliá-la com as atividades e com o denominador monetário e repetir a mesma especificação de rede. A nova base poderá preservar ou modificar os contrastes. O argumento final deve acompanhar essa evidência.

## Referências e reprodução

Blackburn, C. J.; Moreno-Cruz, J. (2019). *Energy Efficiency in General Equilibrium with Input-Output Linkages*. CESifo Working Paper 8007. [Texto](https://www.ifo.de/DocDL/cesifo1_wp8007.pdf). Definição 4 e equação 11.

Ghassibe, M.; Nakov, A. (2025). *Business Cycles with Pricing Cascades*. Manuscrito de julho de 2025. [Texto](https://www.cerge.cuni.cz/pdf/events/papers/GN_latest.pdf). Equação 33.

IBGE. *Matriz de Insumo-Produto Brasil 2015*. Tabelas de 127 produtos e 67 atividades. Arquivo canônico e SHA-256 identificados no [manifesto](../raw/manifesto.csv).

MCTI (2024). *Fifth Biennial Update Report of Brazil*. Apêndice I, coluna 2015, páginas impressas 93–96. [UNFCCC](https://unfccc.int/sites/default/files/resource/BRA_BUR5_EN.pdf).

Sanguinet, E. R.; Azzoni, C. R. (2024). *Carbon emissions drivers in Brazilian regional production chains: Value-added and consumption-based approaches*. Regional Science Policy & Practice, 16, 100015. [DOI](https://doi.org/10.1016/j.rspp.2024.100015). Tabela 2.

Os cálculos provêm de [outputs/investigacao_redes_2015](../outputs/investigacao_redes_2015/), com definições no [notebook original](../investigacao_redes_emissoes_2015.ipynb). As quatro figuras são reproduzidas pelo [notebook do ensaio](../outputs/investigacao_redes_2015/ensaio/figuras_ensaio.ipynb), que registra versões, hashes e conferências numéricas. Os arquivos estão disponíveis em PNG, SVG e PDF. A [especificação final](especificacao_final_pesquisa_2015.md) e a [auditoria ambiental](auditoria_coeficientes_emissoes_2015.md) documentam as decisões e os diagnósticos suplementares. Nenhum resultado histórico foi sobrescrito para preparar este ensaio.
