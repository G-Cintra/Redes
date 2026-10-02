# Especificação acadêmica final — investigação de redes, MIP 2015

**Escopo:** fechamento de `outputs/investigacao_redes_2015/`; a validação posterior é material auxiliar. Esta revisão não altera outras análises, entradas ou resultados históricos do repositório.

**Título provisório:** Emissões próprias de CO₂ e centralidade como fornecedor na rede produtiva brasileira: uma análise da MIP de 2015.

**Status:** rede congelada após exploração e validação interna; auditoria ambiental concluída em 30/09/2026. A base ambiental foi classificada como **C — proxy exploratória**, sem validade suficiente para o resultado ambiental final. Consulte a [auditoria crítica](auditoria_coeficientes_emissoes_2015.md). Não é pré-registro nem validação em dados independentes. Os cálculos históricos foram preservados.

**Decisão central:** adotar $C_i^{sup}=\sum_{j\ne i}L_{ij}$ como medida estrutural principal; S̄ como robustez de normalização; A como contraste direto; HEM F e F/x somente como suplemento. A revisão não procura uma narrativa mais forte: a validade ambiental é uma questão separada da escolha da rede.

## 1. Pergunta e subquestão

**Pergunta:** Em que medida os setores com maior participação nas emissões próprias estimadas de CO₂ ocupam posições centrais como fornecedores diretos e indiretos na rede produtiva brasileira de 2015?

**Subquestão:** Como essa associação se altera quando se considera a escala econômica dos setores, medida pelo valor da produção bruta?

A pergunta mantém o conteúdo econômico original e permanece como objetivo da pesquisa. No estágio atual, os coeficientes ambientais permitem somente um cenário exploratório, e não uma resposta empírica final sobre emissões próprias de 2015. “Centrais” será operacionalizado como a soma dos requerimentos monetários diretos e indiretos do fornecedor nas demandas finais unitárias dos demais setores, sem interpretação de essencialidade. A subquestão exige uma comparação descritiva, sem atribuir ao tamanho um mecanismo causal.

## 2. Hipóteses de trabalho

**H1 — A ordenação setorial por emissão própria não reproduz a ordenação por centralidade como fornecedor nas cadeias dos demais setores.**

Examinar concordância global por Spearman, diferenças de postos e contrastes setoriais, sem definir um corte ex post que transforme correlação em aprovação/rejeição binária. Uma ordenação fortemente coincidente e desvios pequenos enfraqueceriam H1. Não basta encontrar uma única inversão de postos para sustentar divergência substantiva. H1 permite associação positiva e não postula independência.

**H2 — A associação positiva entre emissão própria e centralidade como fornecedor é menor após o ajuste descritivo pela escala econômica setorial.**

Comparar correlação bruta e correlação parcial de postos, usando os mesmos setores. Ausência de redução ou inversão sistemática desse padrão nas especificações próximas enfraqueceria H2. A hipótese não afirma que tamanho “explica” uma fração causal da relação, nem que a associação residual é zero.

Essas formulações organizam evidência já conhecida. Não contêm valores de correlação ou nomes de setores como condições de sucesso. Sua avaliação nesta base é descritiva e posterior à exploração, não um teste confirmatório com nível de significância pré-fixado.

## 3. Dados e fronteira do estudo

A MIP do IBGE contém 127 produtos e 67 atividades. O sistema atividade × atividade é reconstruído das tabelas de produção, usos nacionais e participação na produção. Os valores são produção bruta a preços básicos, em **R$ milhões de 2015**. A rede cobre produção doméstica, inclusive exportações, sem emissões estrangeiras incorporadas nas importações.

A Tabela 2 de Sanguinet e Azzoni (2024) fornece 67 intensidades declaradas como CO₂ por produção bruta, em Gg/R$ milhão, para 2011 e 2018. Os 134 valores dos CSVs conferem com a publicação. O cenário histórico é:

$$
\gamma^{2015}=\frac{3\gamma^{2011}+4\gamma^{2018}}7,\qquad e_i^{cen}=\gamma_i^{2015}x_i^{2015}.
$$

Os cenários 2011/2018 aplicam intensidades distintas à **mesma estrutura de 2015**; não são uma série temporal. O total central de **683,696 Mt** é o resultado desse cenário não harmonizado, não uma estimativa nacional validada.

**Decisão ambiental posterior à auditoria: categoria C.** A fonte informa ajuste pelo IPCA para dezembro de 2018, enquanto o projeto usa fator monetário 1. A correspondência nominal Tabela 2 → MIP é direta; os pesos de alocação EORA/EDGAR → SCN não foram recuperados. A descrição de LULUCF é contraditória no artigo: não afirmar inclusão confirmada. CO₂, CO₂e e GEE não são sinônimos.

A auditoria encontrou discrepâncias relevantes com componentes de processo do inventário oficial de 2015 em minerais não metálicos e siderurgia, além de alertas em resíduos, transporte e serviços. **A interpolação permanece somente como cenário; a base principal deve ser substituída ou reconstruída e validada.** Um fator comum de preços preservaria ranks, mas não resolveria as diferenças setoriais. A [auditoria](auditoria_coeficientes_emissoes_2015.md) contém a tabela das 67 atividades, fontes alternativas e critérios necessários antes da redação ambiental final.

## 4. Notação e construção da rede

| Símbolo | Definição e interpretação |
| --- | --- |
| V, U, D | Produção produto × atividade; uso intermediário nacional produto × atividade; participação atividade × produto. |
| x | Produção bruta por atividade, obtida pelas colunas de V. Não é valor adicionado. |
| Z = DU | Fornecimento intermediário doméstico: linha i fornecedora, coluna j compradora. |
| y | Demanda final por produtos nacionais atribuída às atividades, incluindo exportações. |
| A = Z diag(x)⁻¹ | Requerimentos diretos: Aᵢⱼ = Zᵢⱼ/xⱼ. |
| L = (I − A)⁻¹ | Requerimentos totais por unidade de demanda final. |
| Cᵢˢᵘᵖ = Σⱼ≠ᵢLᵢⱼ | Medida estrutural principal: centralidade como fornecedor pelos requerimentos totais dos demais destinos. |
| γᵢ | Intensidade direta declarada pela fonte, em Gg CO₂/R$ milhão; base ambiental e preços pendentes de validação. |
| eᵢ = γᵢxᵢ | Emissão do cenário exploratório, em Gg CO₂ segundo a unidade declarada; não inventário validado. |
| sᵢᵉ = eᵢ/Σₖeₖ | Participação nas emissões próprias estimadas do sistema. |
| λⱼ = ΣₖLₖⱼ | Soma dos requerimentos monetários brutos da cadeia final j. |
| Sᵢⱼ = Lᵢⱼ/λⱼ | Participação de i nesses requerimentos. |
| S̄ᵢ = Σⱼ≠ᵢSᵢⱼ/(n−1) | Participação média nas cadeias dos outros 66 destinos. |

O balanço é x = Z1 + y = Ax + y = Ly. A direção da rede direta é **fornecedor i → comprador j**. Em L e S, j identifica o destino final da cadeia, não necessariamente um comprador imediato de i.

Quando a expansão converge, L = I + A + A² + … agrega todos os comprimentos de caminhos ponderados pelos coeficientes técnicos. Essa representação constitui o conteúdo de redes do estudo: relacionar a origem emissora à sua posição nos encadeamentos produtivos. Não é necessário adicionar algoritmos genéricos de centralidade ou visualizar um grafo quase completo.

O estudo usa e, não a pegada do destino final. H = diag(γ)L é intensidade incorporada; P = H diag(y) atribui emissões aos destinos e satisfaz P1 = e. H e P permanecem como objetos de auditoria, sem entrar como variáveis ambientais concorrentes no núcleo. Evitar a notação C/c, ambígua nos notebooks históricos.

## 5. Medida principal: centralidade como fornecedor baseada em L

$$
C_i^{sup}=\sum_{j\ne i}L_{ij},\qquad L=(I-A)^{-1}.
$$

Lᵢⱼ representa a produção monetária bruta de i requerida por uma unidade monetária de demanda final de j, com os coeficientes fixos da MIP. Lᵢⱼ = 0,10 significa R$ 0,10 produzidos em i por R$ 1 de demanda final em j, somando fornecimento direto e indireto. Em x=Ly, a linha i reúne a produção de i necessária para atender cada destino j; por isso identifica o **fornecedor**. A coluna j descreve a cadeia demandada, não necessariamente um comprador imediato de i.

Somar os elementos fora da diagonal equivale a comparar a presença do fornecedor em um conjunto de demandas finais unitárias nos demais setores. Pela expansão L=I+A+A²+…, a medida incorpora todos os comprimentos de caminhos produtivos. Cada destino recebe a mesma unidade monetária de demanda final; não se pondera pela demanda efetiva. Dividir toda a soma por 66 apenas mudaria a escala e preservaria os postos.

Excluir j=i remove o destino final próprio do agregado, inclusive seus retornos em Lᵢᵢ. Não remove i dos caminhos que atendem a outros destinos. **Não equivale a L−I**, que preservaria retornos na diagonal. A soma agrega produção bruta entre etapas; não é valor adicionado, participação no PIB ou porcentagem de perda nacional.

### Fundamentação e limites da terminologia

A expressão *supplier centrality* é utilizada para a importância de um fornecedor nos requerimentos diretos e indiretos. Blackburn e Moreno-Cruz (2019), *Energy Efficiency in General Equilibrium with Input-Output Linkages*, definição 4 e equação 11, usam Mα, ponderando pelo consumo final; **não é exatamente o nosso indicador**. [Texto dos autores, CESifo 8007, pp. 14–15](https://www.ifo.de/DocDL/cesifo1_wp8007.pdf).

Ghassibe e Nakov (2025), *Business Cycles with Pricing Cascades*, equação 33, usam uma média de elementos da inversa associada ao fornecedor (coluna na orientação deles), incluindo a diagonal. Nossa orientação tem fornecedor na linha, e excluímos o destino próprio. Essa referência sustenta a família de interpretação, não uma equivalência exata entre especificações ou a importação de resultados causais. [Manuscrito de julho de 2025, pp. 20–21 e 27](https://www.cerge.cuni.cz/pdf/events/papers/GN_latest.pdf).

Usar, portanto, **“centralidade como fornecedor baseada nos requerimentos de Leontief, com pesos unitários e sem destino próprio”**. É uma operacionalização explícita de posição estrutural. Não é a medida ponderada de equilíbrio de toda a literatura, uma nova centralidade independente, nem efeito causal de retirar um setor. Essencialidade e insubstituibilidade exigiriam informação sobre substitutos, estoques, preços e adaptação que a MIP não fornece.

### S como robustez de normalização

$$
S_{ij}=\frac{L_{ij}}{\lambda_j},\qquad
\lambda_j=\sum_k L_{kj},\qquad
\bar S_i=\frac1{66}\sum_{j\ne i}S_{ij}.
$$

S normaliza cada coluna e S̄ mede a **presença relativa média do fornecedor em cadeias padronizadas**. O denominador mantém todas as origens, inclusive Lⱼⱼ. Cada destino recebe igual peso na média, independentemente do total dos seus requerimentos brutos. S̄=0,02 significa presença relativa média de 2% nessas cadeias, não parcela da produção nacional ou fração perdida sem i.

Como Cᵢˢᵘᵖ=Σⱼ≠ᵢλⱼSᵢⱼ, a normalização pergunta se o ranking depende excessivamente de cadeias com maior total de requerimentos brutos. **Muda o estimando**: requerimento agregado versus composição relativa média. Não é uma segunda evidência independente de L.

Reconfirmados **ρ(L,S)=0,997765≈0,998** e **top 10 coincidentes**. A normalização das cadeias altera pouco a hierarquia setorial. Ambas as medidas dependem da classificação, dos preços relativos e da convenção sobre destinos; não se demonstrou invariância a uma nova agregação. A adoção de L prioriza a leitura direta dos requerimentos; não foi escolhida para elevar a correlação ambiental, que inclusive é ligeiramente menor.

## 6. Papel de A, L e S

| Papel | Objeto |
| --- | --- |
| Principal | Cᵢˢᵘᵖ=Σⱼ≠ᵢLᵢⱼ |
| Robustez de normalização | S̄ᵢ=Σⱼ≠ᵢSᵢⱼ/66 |
| Contraste de vínculos diretos | Cᵢᵈⁱʳ=Σⱼ≠ᵢAᵢⱼ |
| Suplemento com outra pergunta | HEM Fᵢ e Fᵢ/xᵢ |

A usa unidades de **produção bruta** dos compradores; L usa unidades de **demanda final** dos destinos. A diferença numérica das somas não isola, sem ressalva, um efeito indireto. As correlações de postos são 0,985314 entre A e L, 0,983678 entre A e S, e 0,997765 entre L e S. A compartilha nove dos top 10 de L/S.

A hierarquia dos principais fornecedores já é bastante visível na estrutura direta e permanece quando os encadeamentos indiretos são incorporados pela inversa de Leontief. São transformações da mesma MIP, **não três validações independentes**. Essa robustez estrutural não se transfere aos coeficientes ambientais.

## 7. HEM: suplemento com estimando distinto de L

Manter como suplemento a extração completa no fechamento de alocação de Ghosh já calculada na investigação. A extração de demanda também existente permanece no histórico, sem desenvolver novos HEMs. Seja B = diag(x)⁻¹Z, G = (I − B)⁻¹ = diag(x)⁻¹L diag(x) e r = x − Zᵀ1. O fechamento xᵀ = rᵀG inclui importações em r; r não é simplesmente VAB.

Retiram-se linha e coluna i de B e a entrada rᵢ, mantendo as entradas e coeficientes dos demais. Para j ≠ i:

$$
\Delta x_j^{(i)}=\frac{x_iG_{ij}}{G_{ii}},\qquad
F_i=\sum_{j\ne i}\Delta x_j^{(i)},\qquad
h_i=\frac{F_i}{x_i}.
$$

A perda própria xᵢ fica separada. **Fᵢ** mede o efeito externo absoluto desse contrafactual contábil, em R$ milhões. **hᵢ** mede efeito externo por unidade da produção do setor extraído, sem unidade monetária. Não é elasticidade ou percentual de perda nacional.

Como hᵢ = Σⱼ≠ᵢLᵢⱼxⱼ/(xᵢLᵢᵢ), mudam o peso dos destinos, o ajuste pelos retornos ao próprio setor e a escala da origem. HEM não reproduz a pergunta principal de L, mesmo antes da divisão por xᵢ. Normalizar tampouco equivale ao ajuste estatístico por tamanho utilizado em H2.

Os dados mostram ρ(S̄,F) = **0,9710**, mas ρ(S̄,h) = **0,5662**. Energia é 10ª em F e 37ª em h; Comércio, 1º e 41º. Isso delimita a interpretação: elevada presença média e elevado efeito externo absoluto não implicam elevado encadeamento externo por unidade do próprio tamanho. **A queda de Energia em h não invalida sua posição na centralidade de fornecedor baseada em L.**

Apresentar F e h juntos no suplemento e registrar esse contraste em um parágrafo do texto principal. A alta concordância de F não constitui confirmação independente, e a discordância de h não refuta a centralidade de fornecedor baseada em L. Continua refutada a extrapolação de um ranking invariável sob todas as noções de importância intersetorial.

A extração é descritiva, com alocação fixa. Não prevê fechamento real, essencialidade, preços, substituição ou bem-estar. A fundamentação e as ressalvas já estão documentadas no notebook de validação a partir de Dietzenbacher, van der Linden e Steenge; Miller e Lahr; e Oosterhaven. Não se propõe outra extração nesta etapa.

## 8. Metodologia final em seis subseções

1. **Dados:** MIP 2015, correspondência das 67 atividades, coeficientes ambientais, unidades e limitações de preços. Conferir entradas e alinhamento pelo manifesto.
2. **Emissões próprias:** após validar a base ambiental, calcular e = γ ⊙ x e participações. Até lá, apresentar somente o cenário exploratório. Usar γ e x para interpretar a identidade, não como variáveis ambientais intercambiáveis. Resumir concentração em um parágrafo.
3. **Rede produtiva:** reconstruir Z, A e L; verificar balanços e concordância com as tabelas do IBGE. Explicitar a direção fornecedor → comprador/destino.
4. **Centralidade como fornecedor:** somar L por linha fora da diagonal. Justificar demandas finais unitárias e exclusão do destino próprio; calcular S̄ somente como robustez de normalização.
5. **Relação ambiental–produtiva:** postos decrescentes com média em empates, Spearman, diferenças de postos, duas figuras e uma tabela de contrastes. Calcular correlação parcial dos postos após retirar de ambos a projeção linear sobre constante e posto de x. Usar os 67 setores, sem exclusão seletiva.
6. **Robustez e complemento:** separar robustez estrutural (S e contraste A) de sensibilidade ambiental (fonte, preços e alocação). Repetir o cenário histórico com γ2011/γ2018 e resumir influência, sem chamar isso de validação ambiental independente. Reservar HEM absoluta/normalizada a complemento com estimandos distintos. Sem novas métricas, cortes ou modelos.

A correlação parcial é Corr(uₑ,uₛ), em que uₑ e uₛ são os resíduos das regressões dos postos de e e Cˢᵘᵖ sobre constante e posto de x. Ela remove uma associação **linear entre postos**, não controla todas as relações possíveis com tamanho. Os setores não são uma amostra IID; não usar p-valores convencionais como prova de validade.

## 9. Resultados conferidos: rede e cenário exploratório separados

1. **Concentração do cenário:** top 5/top 10 emissores reúnem 30,30%/48,28%; Gini de e=0,504 e de x=0,534. São números condicionados ao vetor não validado, sem interpretação de concentração nacional observada.
2. **Hierarquia estrutural:** Comércio, Refino, Transporte terrestre, Intermediação financeira, Agricultura, Atividades jurídicas/consultoria, Energia/utilidades, Químicos, Serviços administrativos e Extração de petróleo/gás são os top 10 de L, nessa ordem. A normalização S preserva o conjunto, com pequenas mudanças de postos.
3. **Associação no cenário:** Spearman(e,L)=**0,382792**; a mediana da diferença absoluta de postos é **16**. Para S e A, as correlações são 0,396440 e 0,401109. A mudança de S para L não altera a leitura descritiva de associação positiva com discordâncias.
4. **Ajuste por escala:** parcial de postos e–L por x=**0,158212**; ρ(L,x)=0,512371 e ρ(L,γ)=−0,182198. Em log–log, a correlação bruta 0,417357 cai para 0,254480, nos mesmos 66 setores com L fora da diagonal positivo. Não significa desaparecimento nem decomposição causal da relação.
5. **Sensibilidade interna:** para γ2011/γ2015/γ2018, ρ(e,L)=0,370820/0,382792/0,392729; parcial=0,146822/0,158212/0,185561. Excluir Energia e Comércio dá 0,335490/0,137958; excluir Água dá 0,390586/0,156806. Não há domínio de um único ponto dentro deste cenário.
6. **Validade ambiental:** esses números não têm validação externa suficiente do numerador físico; as comparações disponíveis levantaram discrepâncias materiais. Não afirmar que a estabilidade interna confirma o ranking dos maiores emissores brasileiros. A conclusão conjunta permanece frágil até a substituição/validação de γ.

Os números foram conferidos diretamente nos [inputs alinhados](../outputs/investigacao_redes_2015/entradas_alinhadas.csv), nas [métricas setoriais](../outputs/investigacao_redes_2015/metricas_setoriais.csv) e nos [cenários](../outputs/investigacao_redes_2015/cenarios_coeficientes.csv) da investigação. O código de reprodução dos diagnósticos adicionais está na seção 11 da [auditoria](auditoria_coeficientes_emissoes_2015.md).

## 10. Figuras da apresentação final

**Figura 1 — Emissão e centralidade de fornecedor:** usar participação emissora no eixo horizontal e Cˢᵘᵖ no vertical, sem apresentar este último como percentual. Identificar os seis contrastes, manter todos os setores e explicitar o caráter de cenário até validar γ.

**Figura 2 — Ranking ambiental × ranking em L:** comparar os postos das mesmas duas variáveis, com 1=maior e a diagonal de igualdade. Na versão final, preferir ambos os eixos de 67 para 1, preservando a diagonal. A coluna `L_saida` das [métricas setoriais](../outputs/investigacao_redes_2015/metricas_setoriais.csv) fornece a medida; ordenar de forma decrescente, com média em empates.

As imagens e tabelas do [relatório histórico da investigação](../outputs/investigacao_redes_2015/relatorio.html) permanecem como registro da etapa anterior. **Não basta trocar suas legendas para L**: valores, postos e estatísticas dos eixos precisam corresponder à métrica. A presente rodada fixa a especificação e audita a base; não produz figuras ambientais como resultado final validado.

S, versão logarítmica e HEM permanecem no suplemento. Não introduzir grafos, quadrantes ou Pareto para compensar a incerteza ambiental.

## 11. Tabela setorial do cenário histórico

Os seis contrastes são preservados, com a coluna principal atualizada para L. Não são uma classificação exaustiva nem conclusões ambientais validadas. Rank 1=maior; empates em γ recebem posto médio.

| Setor (código) | Emissões do cenário (%) | Rank e | Rank x | Rank γ | Rank L |
| --- | ---: | ---: | ---: | ---: | ---: |
| Energia e utilidades (3500) | 8,28 | 1 | 10 | 10 | 7 |
| Água e resíduos (3680) | 7,58 | 2 | 41 | 1 | 33 |
| Construção (4180) | 5,68 | 3 | 3 | 35 | 27 |
| Comércio (4580) | 3,91 | 7 | 1 | 60,5 | 1 |
| Refino de petróleo (1991) | 1,33 | 26 | 6 | 60,5 | 2 |
| Transporte terrestre (4900) | 0,77 | 37 | 7 | 65 | 3 |

Fonte: [métricas setoriais da investigação](../outputs/investigacao_redes_2015/metricas_setoriais.csv); postos em L recalculados da coluna `L_saida`. A tabela não deve ser apresentada como ranking observado de emissões em 2015. Sua eventual substituição exige novo γ, mantendo a métrica estrutural.

## 12. Interpretação dos setores-chave após a auditoria

**Energia/utilidades:** 7ª em L, 6ª em S e 9ª no contraste A. O primeiro posto ambiental pertence ao cenário atual, sem confirmação independente. O código não isola eletricidade. A posição em h=37 não invalida seu papel de fornecedor em L.

**Água/esgoto/resíduos:** 33ª em L e segunda emissora no cenário por intensidade atribuída elevada. A discrepância com a composição por gases e as categorias do inventário exige conciliação. Sua exclusão altera pouco a correlação global, mas isso não valida o contraste ambiental setorial.

**Construção:** 27ª em L; terceiro output e terceira emissão no cenário. Não confundir emissões próprias com a pegada do cimento e aço adquiridos. Não interpretar a posição produtiva como baixa essencialidade.

**Comércio:** primeiro output e primeiro fornecedor em L; sétima emissão no cenário. Grande escala contribui para γx, mas a posição ambiental depende do coeficiente e do denominador comercial correto. Mesmo o arredondamento permite postos ambientais 4–10; não chamar o rank de certificado pela escala.

**Refino:** segundo em L, 26º emissor no cenário. Emissão própria exclui automaticamente a ideia de atribuir ao refino toda a combustão posterior de seus produtos; a intensidade atual, contudo, requer validação física e monetária.

**Transporte terrestre:** terceiro em L, 37º emissor no cenário, com intensidade 65ª. A ponte entre transporte territorial e atividade SCN precisa separar famílias e transporte por conta própria. O contraste não permite concluir que o setor brasileiro emita pouco.

**Minerais não metálicos e siderurgia:** a auditoria encontrou totais do cenário inferiores aos componentes de processo do cimento e do ferro/aço no inventário de 2015. São contraevidências à validade ambiental, não novos contrastes escolhidos para fortalecer a narrativa.

Rankings de x e γ não atribuem percentuais causais a escala/intensidade. Nenhuma dessas leituras autoriza escolher outra rede para compensar problemas dos dados ambientais.

## 13. O que sai do texto principal

| Destino editorial | Análises e motivo |
| --- | --- |
| Remover do argumento final | Afirmações de essencialidade, colapso, causalidade e “todos dependem dos maiores emissores”; grupos naturais definidos por top-k; Energia como única exceção; equivalência entre S̄ e h. Não são sustentadas. |
| Suplemento conciso | Contraste a e robustez S̄, cenários ambientais, versão log da figura, ajuste logarítmico e influência, F e h lado a lado. Qualificam diretamente a conclusão. |
| Documentação exploratória somente | PageRank, Katz, autovetor, betweenness, closeness, random walks, alcance binário, reachability, limiares 1%/5%/10%, similaridade de cosseno, clusters e projeções 3D. Não são necessários ao estimando final. |
| Documentação exploratória somente | Fronteira de Pareto, ranks compostos e curvas completas de top-k. Não identificam um grupo natural e a fronteira inclui o máximo emissor por construção. |
| Arquivo de validação, citado sem reproduzir integralmente | Muitas normalizações, variantes de diagonal, curvas de robustez redundantes e concentração extensa. Guardar a auditoria e as divergências; não alongar a exposição com resultados repetidos. |

“Remover” significa retirar da redação principal, **não apagar arquivos**. Os notebooks e relatórios históricos preservam decisões, resultados negativos e mudanças de interpretação, evitando apresentar uma escolha posterior à exploração como se tivesse sido fixada antes dela.

## 14. Limitações e vocabulário obrigatório

**Centralidade como fornecedor** designa posição nos requerimentos produtivos, operacionalizada por Cˢᵘᵖ=Σⱼ≠ᵢLᵢⱼ. **Presença relativa média nas cadeias padronizadas** é a interpretação de S̄, usada como robustez; não conta destinos. **Dependência contábil** refere-se aos requerimentos sob coeficientes fixos, sem demonstrar como compradores reagiriam à indisponibilidade de um insumo.

**Essencialidade** exigiria evidência de ausência de substitutos. **Importância sistêmica causal** exigiria modelar ou identificar respostas a choques, incluindo preços, estoques, capacidade, substituição e adaptação. A MIP utilizada não fornece isso. Não usar os dois termos como sinônimos de centralidade.

As conclusões também são limitadas por: uma única estrutura produtiva anual; agregação em 67 atividades; pesos iguais dos destinos; preços relativos e produção bruta somada entre etapas; coeficientes ambientais arredondados e interpolados; correspondência/alocação setorial da fonte; harmonização monetária pendente; e ausência de validação ambiental independente. A sensibilidade 2011/2018 não cobre essas incertezas integralmente.

Serviços domésticos têm Cˢᵘᵖ = 0 e S̄ = 0 e emissão positiva na fonte. Permanecem nos postos e nas análises principais; apenas especificações logarítmicas excluem esse zero e informam n = 66, sem adicionar constante. O pequeno lançamento negativo de Z foi preservado nas contas; sua sensibilidade já foi auditada. Não transformar a matriz em uma interpretação probabilística que ignore esses ajustes contábeis.

O fechamento fixa a especificação **para esta base**, não certifica seus níveis ambientais para publicação. Após a classificação C, uma ressalva textual não basta: a base ambiental precisa ser substituída ou reconstruída e validada antes das conclusões finais. Se uma correção de dados mudar resultados, registrar uma nova versão e recalcular esta mesma especificação; não procurar outra métrica para recuperar a narrativa.

## 15. Contribuição e limite atual

A contribuição estrutural é uma implementação transparente da posição dos fornecedores na MIP de 2015. O cenário ambiental demonstra como comparar atributos ambientais e produtivos, mas ainda não estabelece empiricamente os maiores emissores brasileiros nem uma divergência robusta sob dados ambientais independentes.

Os contrastes preservados são hipóteses descritivas condicionais, sem índice único de prioridade. Não se reivindica nova centralidade ou política ótima. A principal limitação passa a ser a validade do numerador ambiental e de sua atribuição setorial, além dos preços; a interpretação da rede está congelada.

## 16. Conclusão em uma frase

A hierarquia de fornecedores da MIP de 2015 é estável em A/L/S; a divergência com o ranking ambiental é reproduzível no cenário atual, mas permanece frágil como conclusão sobre emissões próprias de 2015 devido à qualidade dos coeficientes.

## 17. Conclusão em um parágrafo

Na MIP de 2015, a centralidade como fornecedor baseada na soma de L fora da diagonal apresenta hierarquia quase idêntica à de S normalizada. Com os coeficientes atuais, emissão e centralidade têm Spearman 0,383, reduzido a 0,158 após ajuste descritivo por tamanho, com diferenças expressivas de postos. A troca de S por L não muda essa narrativa condicional. Contudo, a auditoria ambiental classificou a base como proxy exploratória: preços não harmonizados, alocação original não recuperada, fronteira ambígua e discrepâncias com processos industriais inventariados impedem apresentar o ranking ambiental e os contrastes conjuntos como resultados finais validados.

## 18. O que pode ser defendido perante a banca

**Resultado estrutural — robusto:** as matrizes foram reconstruídas do IBGE e os principais fornecedores identificados por L permanecem quase os mesmos sob a normalização S e o contraste direto A. Essa é uma posição contábil sob coeficientes fixos, não uma medida de essencialidade ou efeito causal de retirada.

**Resultado ambiental — não sustentado como ranking real de 2015:** a transcrição correta e as identidades contábeis não validam o numerador físico. A estimativa atual de γx é apenas um cenário; a auditoria encontrou problemas suficientes para exigir outra base principal ou reconstrução verificável.

**Resultado conjunto — frágil:** associação moderada e atenuação por tamanho resistem aos dois vetores da mesma fonte e ao leave-one-out. Isso não demonstra sobrevivência a preços setoriais e alocação ambiental corrigidos. Energia, Água, Construção, Comércio, Refino e Transporte não recebem confirmação ambiental apenas por manterem seus postos entre 2011/interpolação/2018.

Preservar a pergunta e a métrica, substituir ou validar γ, recalcular os mesmos resultados e aceitar eventual mudança da conclusão. HEM permanece como suplemento que ilustra diferentes noções de importância intersetorial, sem confirmar nem refutar L de forma independente.

## 19. Estrutura sugerida do trabalho

1. **Introdução:** pergunta, relevância da distinção entre emissão própria e posição produtiva, H1/H2 e contribuição descritiva.
2. **Referencial:** redes de produção e requerimentos de Leontief; extensão ambiental; distinção entre centralidade contábil e efeitos causais. Aproveitar a revisão já realizada, sem catálogo de algoritmos.
3. **Dados e métodos:** as seis subseções da seção 8, com HEM delimitada brevemente e derivação no suplemento.
4. **Resultados:** contexto de concentração; figura 1; figura 2; tabela de seis contrastes; tamanho econômico e síntese de robustez.
5. **Discussão:** identidade e = γx, diferenças entre estimandos, limitações ambientais e alcance das conclusões.
6. **Conclusão:** resposta direta, contribuição e limites, sem converter centralidade em recomendação de intervenção.
7. **Suplemento:** diagnósticos próximos, HEM absoluta/normalizada e instruções de reprodução. O arquivo exploratório completo permanece no repositório.

## 20. Rastreabilidade e reprodução

O objeto desta revisão é a investigação publicada em [outputs/investigacao_redes_2015](../outputs/investigacao_redes_2015/), gerada pelo [notebook de investigação](../investigacao_redes_emissoes_2015.ipynb). O [roteiro de revisão](revisao_investigacao_2015.md) e a validação posterior documentam o histórico. Os relatórios e notebooks anteriores conservam as escolhas de suas respectivas etapas; a orientação vigente para a redação é a presente especificação, com L principal e base ambiental C.

| Afirmação | Evidência da investigação |
| --- | --- |
| Coeficientes, output e emissões | [entradas_alinhadas.csv](../outputs/investigacao_redes_2015/entradas_alinhadas.csv) |
| Medidas L/S/A e extrações históricas | [metricas_setoriais.csv](../outputs/investigacao_redes_2015/metricas_setoriais.csv): `L_saida`, `S_media`, `A_saida`, `HEM_alocacao_abs`, `HEM_alocacao_por_x` |
| Matrizes e normalização | [matriz_L.csv](../outputs/investigacao_redes_2015/matriz_L.csv), [matriz_S.csv](../outputs/investigacao_redes_2015/matriz_S.csv), [matriz_A.csv](../outputs/investigacao_redes_2015/matriz_A.csv) |
| Cenários ambientais e parcial em L | [cenarios_coeficientes.csv](../outputs/investigacao_redes_2015/cenarios_coeficientes.csv) |
| Concentração | [concentracao.csv](../outputs/investigacao_redes_2015/concentracao.csv) |
| Integridade das entradas e ambiente histórico | [reproducibilidade.json](../outputs/investigacao_redes_2015/reproducibilidade.json), [manifesto](../raw/manifesto.csv) |
| Correspondência de 67 atividades, validação externa, influência em L e limites de arredondamento | [auditoria ambiental](auditoria_coeficientes_emissoes_2015.md), com código focal de reprodução na seção 11 |

Para reconstruir toda a investigação, executar seu notebook da raiz; ele regrava sua pasta de outputs. Para conferir somente esta revisão, executar o trecho da seção 11 da auditoria, que apenas lê os CSVs. Não foi necessário criar outro notebook, modificar módulos ou regravar as saídas históricas. As fontes metodológicas específicas estão na seção 5 e as ambientais no relatório de auditoria.
