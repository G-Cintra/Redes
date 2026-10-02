# Auditoria dos coeficientes de emissões — investigação de redes, MIP 2015

**Escopo:** avaliação de `outputs/investigacao_redes_2015/`, sua interpretação e sua especificação acadêmica. As entradas brutas, a literatura e a validação posterior são evidências auxiliares. Este parecer não altera outras análises do repositório, não reabre a exploração de centralidades e não substitui os outputs históricos. Data da conferência: 30/09/2026.

## 1. Resumo executivo

1. **Base ambiental: C — útil apenas como proxy exploratória.**
2. A transcrição dos 134 coeficientes da Tabela 2 está correta; a validade ambiental é uma questão diferente.
3. A correspondência nominal com as 67 atividades é direta; a alocação EORA/EDGAR anterior à tabela não foi recuperada.
4. O artigo declara intensidade direta de CO₂ por produção bruta, mas não documenta suficientemente a fronteira efetivamente implementada.
5. Há contradição sobre uso da terra e falta harmonização dos preços da fonte com os preços de 2015.
6. Comparações com processos industriais do inventário oficial levantam discrepâncias materiais de magnitude.
7. A interpolação 2011–2018 permanece somente como cenário, não como estimativa validada de 2015.
8. A rede fica fixada em L fora da diagonal; S é robustez, A é contraste direto e HEM é suplemento.
9. O resultado estrutural é robusto dentro dessa família; o ranking ambiental não está sustentado e a conclusão conjunta é frágil.
10. Não defenderia os volumes atuais como emissões próprias setoriais de 2015 perante uma banca sem reconstruir/validar ou substituir a base.

## 2. Fonte ambiental atual

Sanguinet, Eduardo Rodrigues; Azzoni, Carlos Roberto (2024). *Carbon emissions drivers in Brazilian regional production chains: Value-added and consumption-based approaches*. Regional Science Policy & Practice, 16, 100015. [Artigo e DOI](https://doi.org/10.1016/j.rspp.2024.100015).

A **Tabela 2, p. 5**, publica 67 intensidades de 2011 e 2018, em **Gg CO₂/BRL milhão**, com duas casas decimais. A seção 2.1 define a intensidade pela divisão da emissão setorial pela produção bruta. Ela é o insumo direto da extensão ambiental, antes de multiplicar pela inversa de Leontief. As contas de consumo e renda calculadas depois no artigo não são os coeficientes transcritos pelo projeto. O denominador declarado não é VAB, consumo final nem pegada.

A fonte usa um sistema inter-regional com 27 UFs e 67 setores e aplica a mesma intensidade de cada atividade às UFs. Não há 27 vetores regionais observados na Tabela 2. A menção a 68 indústrias na notação geral da seção 2.1 não autoriza inventar um 68º coeficiente: a base empírica declarada e a tabela utilizada têm 67.

Nos [inputs alinhados da investigação](../outputs/investigacao_redes_2015/entradas_alinhadas.csv), `setor_fonte`, `gamma2011`, `gamma2018`, `gamma2015`, `x` e `e` tornam a transformação local inspecionável. Os valores foram reconferidos com os CSVs de `raw/` e com a Tabela 2: **134 de 134 coincidem**. Não foi demonstrado erro de digitação ou deslocamento de linha.

## 3. Proveniência

| Etapa | O que está documentado | O que não foi recuperado e consequência |
| --- | --- | --- |
| EORA/EDGAR → emissões por atividade | Seção 2.3 menciona EORA e harmonização das indústrias de EDGAR com IBGE. | Versão original, arquivos, linhas do satélite, emissões físicas de origem e pesos de alocação. Não é possível recalcular o numerador. |
| Emissões/produção → intensidade original | γ = p/x; denominador declarado como produção bruta. | Vetores p e x usados para obter cada intensidade não arredondada; conversões intermediárias de unidade/moeda. |
| Preços da IRIO | Seção 2.3 informa ajuste da IRIO 2011 pelo IPCA para dezembro de 2018; nota da Tabela 1 confirma a base. | Fatores numéricos, convenção anual versus mensal e aplicação exata aos denominadores da Tabela 2. |
| Intensidade → Tabela 2 | 67 setores SCN, 2011/2018, Gg/R$ milhão, duas casas. | Valores não arredondados; percentuais de variação impressos não bastam para recuperá-los univocamente. |
| Tabela 2 → CSVs em raw | Transcrição de S1…S67, mesma ordem e nomes. | Nenhuma divergência numérica encontrada nesta etapa. |
| CSVs → atividades MIP | Correspondência nominal direta, explicitada nas 67 linhas da seção 6. | A igualdade dos nomes não certifica a alocação ambiental anterior. |
| γ2011/γ2018 → γ2015 | (3γ2011 + 4γ2018)/7, fator monetário 1. | Nenhuma observação física de 2015 entra nessa interpolação. |
| γ2015 × x2015 → e | Produção bruta da MIP em R$ milhões de 2015; resultados conferidos nos outputs. | A aplicação não harmoniza o denominador monetário nem resolve a fronteira ambiental. |

Portanto, a cadeia é: **EORA/EDGAR (alocação não recuperada) → p/x (p e x originais ausentes) → preços declarados na fonte → Tabela 2 arredondada → transcrição exata → correspondência nominal direta → interpolação → multiplicação pelo output de 2015 sem conversão monetária**. Marcar uma etapa como desconhecida é necessário para a auditabilidade; não é evidência de que ela foi feita corretamente ou incorretamente.

O artigo remete a harmonização ao anexo, mas o anexo do PDF principal consultado contém a relação das UFs, não a matriz de pesos ambientais. O suplemento da editora não foi recuperado nas tentativas de acesso. Logo, a reconstrução completa da fonte permanece impedida exatamente na alocação física e nos denominadores originais. Não se atribuiu silenciosamente uma concordância de outra versão da EORA aos autores.

As entradas utilizadas são identificadas pelo [manifesto](../raw/manifesto.csv) e pela [proveniência da investigação](../outputs/investigacao_redes_2015/reproducibilidade.json). Os hashes das cinco entradas desta investigação conferem. PDFs consultados: Sanguinet–Azzoni, SHA-256 `449ef03b89626f339c7c62f5e7b42b5ac50205320c7acdd92b3cfbd6b3d3bbc9`; BUR5, `d27e8912204ff57c300f8a523fc790cb67acfea10e1a029d16e8512978ffd3fb`.

## 4. Unidades e fronteira ambiental

**Interpretação pretendida pela fonte:** emissão direta de CO₂ atribuída ao setor por unidade de produção bruta. Nesse sentido formal, γx é emissão própria e não pegada de consumo. Multiplicar por L transforma a intensidade direta em intensidade incorporada; somar esta última como se fosse emissão própria introduziria outra variável. A investigação mantém corretamente essa distinção entre e, H e P.

**Interpretação efetivamente defensável dos resultados atuais:** volume do cenário calculado com a intensidade direta *declarada* pela fonte, aplicado ao output da MIP de 2015. Não é emissão observada nem inventário validado das 67 atividades.

| Questão | Parecer |
| --- | --- |
| CO₂ ou CO₂e? | A tabela declara CO₂. Não há documentação suficiente para afirmar soma de CH₄/N₂O convertidos por GWP. Não renomear como CO₂e ou GEE. |
| Combustão e processos? | A descrição sugere emissões por atividade, mas as categorias efetivamente selecionadas não são reproduzíveis. Não certificar cobertura integral de ambos; a comparação de processos é problemática. |
| LULUCF? | Seção 2.3, p. 3, descreve inclusão de desmatamento e outras categorias de uso da terra. Seção 5.3, pp. 13–14, descreve exclusão/não incorporação explícita. **Inclusão não confirmada.** |
| Territorial ou residência? | Atribuição à produção brasileira é o objetivo; não foi recuperada a ponte entre inventário territorial e atividades econômicas, incluindo famílias e transporte. |
| Biomassa? | Separação entre CO₂ fóssil, biogênico e uso da terra não verificável nos coeficientes publicados. Não somar itens de memória automaticamente. |
| Produção ou consumo? | γ é direto; e é calculado pela produção. As emissões estrangeiras não integram esse vetor. Exportações de produção doméstica estão incluídas. |

A afirmação categórica de inclusão de uso da terra presente na narrativa histórica da investigação deve ser substituída, na especificação final, por **fronteira não resolvida**. Preservar o relatório histórico não significa endossar essa afirmação após a auditoria.

A conversão dimensional local está correta: Gg/(R$ milhão) × R$ milhão = Gg; 1.000 Gg = 1 Mt. Numericamente, 1 Gg/R$ milhão = 1 kg/R$. O resultado elevado de água/resíduos não é explicado por um erro de fator mil nessa multiplicação.

## 5. Compatibilidade monetária

O x da investigação é produção bruta a preços básicos de 2015. A fonte relata atualização monetária para dezembro de 2018. A Tabela 2 não fornece seus denominadores originais, de modo que **não está justificado multiplicar diretamente seus coeficientes por x2015 com fator 1**. O fato de ambos usarem reais e milhões não basta: o poder de compra, os preços relativos e a definição da produção precisam coincidir.

Se a intensidade física de um dado período estivesse expressa em preços de 2018 e fosse possível definir dᵢ = pᵢ2018/pᵢ2015 para a mesma cesta e conceito de produção, então:

$$
x_i^{(preços\ 2018)}=d_i x_i^{(preços\ 2015)},\qquad
e_i=\gamma_i^{(preços\ 2018)}d_i x_i^{(preços\ 2015)}.
$$

Ou seja, para mudar o denominador da intensidade para preços de 2015, multiplicar γ por d; não inverter esse fator por intuição. **Isso corrige somente a unidade monetária**, sob as hipóteses explicitadas, e não transforma a tecnologia/emissão física de 2011 ou 2018 em observação de 2015. Antes de aplicar qualquer fator, é preciso recuperar o ajuste realmente empregado pelos autores e verificar preços básicos versus outra valoração, média anual versus dezembro e composição setorial.

Um fator comum positivo preserva postos e participações por identidade, mas não demonstra que a discrepância verdadeira seja comum. O IPCA mede uma cesta de consumo, não os preços de produção das 67 atividades. Como evidência concreta de heterogeneidade, o [IPP/IBGE de outubro de 2018](https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Produtor/Fasciculo_Indicadores_IBGE/2018/ipp_201810_Publicacao.pdf) registra, em 12 meses, 35,50% em refino/álcool, 19,18% em metalurgia e 15,12% na indústria geral. Esses números **não são deflatores de 2015–2018** e não foram aplicados aos outputs. O IPP também não cobre todas as atividades de serviços e agropecuária.

Há ainda uma questão de conceito: no comércio, produção mede o serviço/margem comercial, não as vendas brutas das mercadorias. Um coeficiente construído com faturamento de mercadorias produziria incompatibilidade mesmo com o ano monetário correto. A definição geral de output na fonte é favorável à compatibilidade, mas os valores originais precisam ser verificados.

A solução preferível é obter pᵢ2015 físico, reconciliá-lo com as atividades MIP e calcular γᵢ2015 = pᵢ2015/xᵢ2015. Evita transportar um coeficiente monetário entre bases. Uma correção só pelo IPCA, sem reconciliar a atribuição ambiental, é insuficiente para promover a base à categoria B.

## 6. Correspondência setorial

**D+I** = correspondência nominal direta Tabela 2 → MIP, seguida da interpolação 3/7 e 4/7, sem conversão monetária. A fonte já possui os agregados de 67 atividades; não houve agregação, desagregação, média simples ou proxy adicionada localmente. Quando a origem física EORA/EDGAR exigiu tais operações, seus pesos não foram recuperados: a classificação dessa etapa é **correspondência incerta** para todas as atividades.

**N alta / A ind.** = confiança nominal alta; confiança na alocação ambiental original indeterminada. Não é uma probabilidade nem certificação de qualidade ambiental. Todos os γ estão em Gg/R$ milhão segundo a unidade declarada; seis casas em 2015 mostram o cálculo, não precisão adicional da fonte.

| MIP 2015 (código e atividade) | Setor da fonte (Tabela 2) | Transformação | γ2011 | γ2018 | γ2015 | Confiança | Observação |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 0191 — Agricultura, inclusive o apoio à agricultura e a pós-colheita | S1 — Agriculture, including support for agriculture and post-harvest | D+I | 0.04 | 0.03 | 0.034286 | N alta / A ind. | CO2 não cobre CH4/N2O agropecuários; atribuição de LULUCF não resolvida. |
| 0192 — Pecuária, inclusive o apoio à pecuária | S2 — Livestock, including support for livestock | D+I | 0.05 | 0.04 | 0.044286 | N alta / A ind. | Emissão baixa de CO2 não significa baixa emissão de GEE; LULUCF não resolvido. |
| 0280 — Produção florestal; pesca e aquicultura | S3 — Forest production; fishing and aquaculture | D+I | 0.19 | 0.17 | 0.178571 | N alta / A ind. | Agregado já existente na fonte: floresta, pesca e aquicultura; não separar LULUCF por suposição. |
| 0580 — Extração de carvão mineral e de minerais não metálicos | S4 — Extraction of coal and non-metallic minerals | D+I | 0.07 | 0.08 | 0.075714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 0680 — Extração de petróleo e gás, inclusive as atividades de apoio | S5 — Oil and gas extraction, including support activities | D+I | 0.01 | 0.01 | 0.010000 | N alta / A ind. | Coeficientes 0,01: erro relativo de arredondamento pode chegar a 50%. |
| 0791 — Extração de minério de ferro, inclusive beneficiamentos e a aglomeração | S6 — Iron ore extraction, including beneficiation and agglomeration | D+I | 0.02 | 0.02 | 0.020000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 0792 — Extração de minerais metálicos não ferrosos, inclusive beneficiamentos | S7 — Extraction of non-ferrous metallic minerals, including beneficiation | D+I | 0.13 | 0.10 | 0.112857 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1091 — Abate e produtos de carne, inclusive os produtos do laticínio e da pesca | S8 — Slaughter and meat products, including dairy and fish products | D+I | 0.14 | 0.10 | 0.117143 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1092 — Fabricação e refino de açúcar | S9 — Sugar manufacturing and refining | D+I | 0.42 | 0.58 | 0.511429 | N alta / A ind. | Intensidade alta; distinguir combustão de biomassa, CO2 fóssil e LULUCF. |
| 1093 — Outros produtos alimentares | S10 — Other food products | D+I | 0.14 | 0.09 | 0.111429 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1100 — Fabricação de bebidas | S11 — Beverage manufacturing | D+I | 0.41 | 0.38 | 0.392857 | N alta / A ind. | 4º emissor no cenário; intensidade muito alta requer numerador físico verificável. |
| 1200 — Fabricação de produtos do fumo | S12 — Manufacture of tobacco products | D+I | 0.05 | 0.06 | 0.055714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1300 — Fabricação de produtos têxteis | S13 — Manufacture of textile products | D+I | 0.07 | 0.08 | 0.075714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1400 — Confecção de artefatos do vestuário e acessórios | S14 — Manufacture of garments and accessories | D+I | 0.06 | 0.07 | 0.065714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1500 — Fabricação de calçados e de artefatos de couro | S15 — Manufacture of footwear and leather goods | D+I | 0.05 | 0.06 | 0.055714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1600 — Fabricação de produtos da madeira | S16 — Manufacture of wood products | D+I | 0.06 | 0.06 | 0.060000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1700 — Fabricação de celulose, papel e produtos de papel | S17 — Manufacture of pulp, paper and paper products | D+I | 0.05 | 0.04 | 0.044286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1800 — Impressão e reprodução de gravações | S18 — Printing and playing back recordings | D+I | 0.15 | 0.20 | 0.178571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 1991 — Refino de petróleo e coquerias | S19 — Oil refining and coke ovens | D+I | 0.03 | 0.02 | 0.024286 | N alta / A ind. | Refino próprio não é combustão posterior; numerador físico e alocação pendentes. |
| 1992 — Fabricação de biocombustíveis | S20 — Biofuel manufacturing | D+I | 0.05 | 0.03 | 0.038571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2091 — Fabricação de químicos orgânicos e inorgânicos, resinas e elastômeros | S21 — Manufacture of organic and inorganic chemicals, resins and elastomers | D+I | 0.07 | 0.05 | 0.058571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2092 — Fabricação de defensivos, desinfestantes, tintas e químicos diversos | S22 — Manufacture of pesticides, disinfectants, paints and various chemicals | D+I | 0.05 | 0.04 | 0.044286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2093 — Fabricação de produtos de limpeza, cosméticos/perfumaria e higiene pessoal | S23 — Manufacture of cleaning products, cosmetics/perfumery and personal hygiene | D+I | 0.10 | 0.07 | 0.082857 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2100 — Fabricação de produtos farmoquímicos e farmacêuticos | S24 — Manufacture of pharmochemicals and pharmaceuticals | D+I | 0.10 | 0.07 | 0.082857 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2200 — Fabricação de produtos de borracha e de material plástico | S25 — Manufacture of rubber and plastic material products | D+I | 0.07 | 0.06 | 0.064286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2300 — Fabricação de produtos de minerais não metálicos | S26 — Manufacture of non-metallic mineral products | D+I | 0.05 | 0.06 | 0.055714 | N alta / A ind. | 4,99 Mt no cenário versus 23,903 Mt só de processos de cimento no BUR5. |
| 2491 — Produção de ferro gusa/ferroligas, siderurgia e tubos de aço sem costura | S27 — Production of pig iron / ferroalloys, steel and seamless steel tubes | D+I | 0.04 | 0.04 | 0.040000 | N alta / A ind. | 4,06 Mt no cenário versus 43,391 Mt só de processos de ferro/aço no BUR5. |
| 2492 — Metalurgia de metais não ferosos e a fundição de metais | S28 — Metallurgy of non-ferrous metals and metal smelting | D+I | 0.05 | 0.04 | 0.044286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2500 — Fabricação de produtos de metal, exceto máquinas e equipamentos | S29 — Manufacture of metal products, except machinery and equipment | D+I | 0.05 | 0.05 | 0.050000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2600 — Fabricação de equipamentos de informática, produtos eletrônicos e ópticos | S30 — Manufacture of computer equipment, electronic and optical products | D+I | 0.12 | 0.11 | 0.114286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2700 — Fabricação de máquinas e equipamentos elétricos | S31 — Manufacture of electrical machinery and equipment | D+I | 0.07 | 0.07 | 0.070000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2800 — Fabricação de máquinas e equipamentos mecânicos | S32 — Manufacture of machinery and mechanical equipment | D+I | 0.05 | 0.06 | 0.055714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 2991 — Fabricação de automóveis, caminhões e ônibus, exceto peças | S33 — Manufacture of automobiles, trucks and buses, except for parts | D+I | 0.01 | 0.01 | 0.010000 | N alta / A ind. | Coeficientes 0,01: erro relativo de arredondamento pode chegar a 50%. |
| 2992 — Fabricação de peças e acessórios para veículos automotores | S34 — Manufacture of parts and accessories for motor vehicles | D+I | 0.04 | 0.04 | 0.040000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 3000 — Fabricação de outros equipamentos de transporte, exceto veículos automotores | S35 — Manufacture of other transport equipment, except motor vehicles | D+I | 0.05 | 0.06 | 0.055714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 3180 — Fabricação de móveis e de produtos de indústrias diversas | S36 — Manufacture of furniture and products of various industries | D+I | 0.08 | 0.07 | 0.074286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 3300 — Manutenção, reparação e instalação de máquinas e equipamentos | S37 — Maintenance, repair and installation of machinery and equipment | D+I | 0.05 | 0.04 | 0.044286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 3500 — Energia elétrica, gás natural e outras utilidades | S38 — Electricity, natural gas and other utilities | D+I | 0.16 | 0.26 | 0.217143 | N alta / A ind. | Energia/utilidades é agregado; mistura elétrica e preços variam entre anos. |
| 3680 — Água, esgoto e gestão de resíduos | S39 — Water, sewage and waste management | D+I | 0.55 | 1.03 | 0.824286 | N alta / A ind. | 51,80 Mt CO2 no cenário; resíduos do inventário têm 1,153 Mt CO2 e muito CH4. Fronteiras diferem. |
| 4180 — Construção | S40 — Construction | D+I | 0.05 | 0.07 | 0.061429 | N alta / A ind. | Não atribuir automaticamente emissões de cimento/aço à construção; emissão própria não é pegada. |
| 4580 — Comércio por atacado e varejo | S41 — Wholesale and retail trade | D+I | 0.03 | 0.02 | 0.024286 | N alta / A ind. | Output do comércio mede serviço/margem; verificar denominador, não usar vendas brutas de mercadorias. |
| 4900 — Transporte terrestre | S42 — Ground transportation | D+I | 0.01 | 0.02 | 0.015714 | N alta / A ind. | Intensidade muito baixa; transporte territorial inclui famílias e transporte por conta própria. |
| 5000 — Transporte aquaviário | S43 — Water transportation | D+I | 0.18 | 0.13 | 0.151429 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 5100 — Transporte aéreo | S44 — Air transport | D+I | 0.08 | 0.07 | 0.074286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 5280 — Armazenamento, atividades auxiliares dos transportes e correio | S45 — Storage, auxiliary transport and mail activities | D+I | 0.03 | 0.04 | 0.035714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 5500 — Alojamento | S46 — Accommodation | D+I | 0.32 | 0.29 | 0.302857 | N alta / A ind. | Intensidade alta; separar combustão própria de eletricidade adquirida e de pegada. |
| 5600 — Alimentação | S47 — Food | D+I | 0.04 | 0.03 | 0.034286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 5800 — Edição e edição integrada à impressão | S48 — Print-integrated editing and editing | D+I | 0.35 | 0.24 | 0.287143 | N alta / A ind. | Intensidade alta em edição; nenhum numerador físico recuperado. |
| 5980 — Atividades de televisão, rádio, cinema e  gravação/edição de som e imagem | S49 — Television, radio, film and sound and image recording/editing activities | D+I | 0.26 | 0.30 | 0.282857 | N alta / A ind. | Intensidade alta em audiovisual; alocação original não demonstrada. |
| 6100 — Telecomunicações | S50 — Telecommunications | D+I | 0.06 | 0.08 | 0.071429 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 6280 — Desenvolvimento de sistemas e outros serviços de informação | S51 — Development of systems and other information services | D+I | 0.11 | 0.08 | 0.092857 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 6480 — Intermediação financeira, seguros e previdência complementar | S52 — Financial intermediation, insurance and supplementary pensions | D+I | 0.04 | 0.02 | 0.028571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 6800 — Atividades imobiliárias | S53 — Real estate activities | D+I | 0.04 | 0.03 | 0.034286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 6980 — Atividades jurídicas, contábeis, consultoria e sedes de empresas | S54 — Legal, accounting, consulting and company headquarters | D+I | 0.08 | 0.06 | 0.068571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 7180 — Serviços de arquitetura, engenharia, testes/análises técnicas e P & D | S55 — Architectural, engineering, technical testing/analysis and R&D services | D+I | 0.16 | 0.19 | 0.177143 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 7380 — Outras atividades profissionais, científicas e técnicas | S56 — Other professional, scientific and technical activities | D+I | 0.12 | 0.13 | 0.125714 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 7700 — Aluguéis não imobiliários e gestão de ativos de propriedade intelectual | S57 — Non-real estate rentals and intellectual property asset management | D+I | 0.32 | 0.24 | 0.274286 | N alta / A ind. | Intensidade alta em aluguel/ativos; não atribuir automaticamente emissões do usuário ao proprietário. |
| 7880 — Outras atividades administrativas e serviços complementares | S58 — Other administrative activities and complementary services | D+I | 0.07 | 0.06 | 0.064286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 8000 — Atividades de vigilância, segurança e investigação | S59 — Surveillance, security and investigation activities | D+I | 0.32 | 0.34 | 0.331429 | N alta / A ind. | Intensidade maior que utilidades; alocação ambiental não demonstrada. |
| 8400 — Administração pública, defesa e seguridade social | S60 — Public administration, defense and social security | D+I | 0.04 | 0.03 | 0.034286 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 8591 — Educação pública | S61 — Public education | D+I | 0.02 | 0.02 | 0.020000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 8592 — Educação privada | S62 — Private education | D+I | 0.05 | 0.03 | 0.038571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 8691 — Saúde pública | S63 — Public health | D+I | 0.02 | 0.02 | 0.020000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 8692 — Saúde privada | S64 — Private health | D+I | 0.04 | 0.02 | 0.028571 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 9080 — Atividades artísticas, criativas e de espetáculos | S65 — Artistic, creative and entertainment activities | D+I | 0.32 | 0.29 | 0.302857 | N alta / A ind. | Intensidade alta em artes; alocação ambiental não demonstrada. |
| 9480 — Organizações associativas e outros serviços pessoais | S66 — Membership organizations and other personal services | D+I | 0.07 | 0.07 | 0.070000 | N alta / A ind. | Não há inventário físico de origem nem pesos de alocação verificáveis. |
| 9700 — Serviços domésticos | S67 — Domestic services | D+I | 0.18 | 0.16 | 0.168571 | N alta / A ind. | Serviços domésticos não equivalem às emissões residenciais de todas as famílias. |

Não há subconjunto certificado de alta confiança ambiental que permita resolver a auditoria simplesmente excluindo os demais setores. As observações distinguem alertas substantivos, não inventam qualidade superior para as linhas sem um alerta específico.

## 7. Interpolação 2011–2018

Os pesos 3/7 e 4/7 são temporalmente corretos para localizar 2015 entre 2011 e 2018. Isso prova a correção aritmética, não a trajetória da intensidade. γ = p/x é uma razão: interpolar a razão não equivale a interpolar separadamente emissões físicas e produção, nem a controlar preços.

Mudam tecnologia, composição interna de cada atividade, preços e utilização de capacidade; eletricidade também depende da hidrologia e do despacho térmico. O [BEN 2016, ano-base 2015, da EPE](https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-126/topico-92/Relat%C3%B3rio_S%C3%ADntese_2016.pdf) documenta a composição energética daquele ano. Suas estimativas agregadas de emissões são apresentadas em CO₂e e não foram tratadas como CO₂ puro para preencher o vetor atual. Uso da terra, se incluído, acrescentaria volatilidade que uma interpolação linear não valida.

**Decisão:** manter a interpolação apenas como cenário histórico de demonstração; substituir como estimativa principal por uma extensão com ano físico 2015. Se os autores fornecerem dados completos, uma reconstrução reconciliada poderá ser avaliada. A estabilidade dos três cenários da mesma fonte não mede erros comuns de alocação ou de fronteira.

## 8. Outliers

Maiores intensidades interpoladas, calculadas das entradas da investigação:

| Atividade | γ interpolado | Emissão do cenário (Mt) | Rank e |
| --- | ---: | ---: | ---: |
| 3680 — Água, esgoto e gestão de resíduos | 0.824286 | 51.802 | 2 |
| 1092 — Fabricação e refino de açúcar | 0.511429 | 24.582 | 9 |
| 1100 — Fabricação de bebidas | 0.392857 | 30.032 | 4 |
| 8000 — Atividades de vigilância, segurança e investigação | 0.331429 | 13.242 | 13 |
| 5500 — Alojamento | 0.302857 | 7.266 | 29 |
| 9080 — Atividades artísticas, criativas e de espetáculos | 0.302857 | 10.488 | 22 |
| 5800 — Edição e edição integrada à impressão | 0.287143 | 5.882 | 35 |
| 5980 — Atividades de televisão, rádio, cinema e  gravação/edição de som e imagem | 0.282857 | 12.277 | 17 |
| 7700 — Aluguéis não imobiliários e gestão de ativos de propriedade intelectual | 0.274286 | 12.523 | 16 |
| 3500 — Energia elétrica, gás natural e outras utilidades | 0.217143 | 56.621 | 1 |

**Água/esgoto/resíduos (3680).** γ = 0,824286, o maior da base; x = R$ 62.845 milhões, 41º em produção; e = 51,802 Mt, 2º no ranking. A intensidade elevada não foi criada por ordenação incorreta ou unidade mil vezes maior. Entretanto, não foi recuperado o numerador físico original que permitiria separar emissão elevada de denominador pequeno na fonte. O agregado mistura água, esgoto e resíduos; comparar automaticamente com a categoria “resíduos” de um inventário é incorreto. A importância de CH₄ nos resíduos torna especialmente inadequado inferir plausibilidade de CO₂ a partir de números totais de CO₂e. O arredondamento permitiria apenas cerca de ±0,61% nesse coeficiente: não explica a dúvida de magnitude/alocação.

**Energia/utilidades (3500).** Primeira emissão no cenário, intensidade e tamanho em 10º. O agregado não equivale exclusivamente à geração elétrica, nem à categoria “Energia” inteira do inventário. Variação de matriz elétrica e preços é material; o primeiro posto persiste sob arredondamento e nos cenários publicados, mas não está validado por outro vetor setorial.

**Construção (4180).** Terceira em emissão e produção; intensidade intermediária. É indispensável separar combustão própria das emissões de fabricação do cimento e do aço que compra. Atribuir estas últimas à construção mudaria o objeto para emissão incorporada e violaria a pergunta.

**Comércio (4580).** Grande volume resulta da escala aplicada a γ baixo. Permanece top 10 sob os limites de arredondamento, mas isso não valida seu denominador ou suas emissões físicas. Alterações setoriais de alocação poderiam mudar sua posição ambiental; a primeira posição estrutural independe disso.

**Refino (1991) e transporte terrestre (4900).** Intensidades 0,024286 e 0,015714, respectivamente. É correto excluir do refino a combustão posterior dos combustíveis vendidos; não é correto usar isso para certificar o valor de suas operações próprias. Transporte terrestre gera somente 5,231 Mt no cenário: comparação com combustão de todo o transporte exige retirar famílias e realocar frotas próprias de outras atividades. O contraste de transporte como fornecedor central é sólido; sua baixa posição emissora continua dependente de um coeficiente não validado.

**Minerais não metálicos (2300) e siderurgia (2491).** Volumes 4,990 e 4,064 Mt são inferiores até a componentes de processos industriais correspondentes no inventário oficial (seção 9). É um alerta mais específico que simplesmente comparar a ordenação com expectativas intuitivas.

**Agropecuária (0191/0192).** CO₂ não representa toda a contribuição climática dessas atividades: CH₄ e N₂O são relevantes e distintos. A intensidade relativamente baixa não prova baixa emissão de GEE. Alocar LULUCF aos setores sem regra explícita pode alterar radicalmente seus postos.

**Açúcar, bebidas e serviços.** Açúcar tem γ = 0,511429; é necessário identificar tratamento de combustão de biomassa. Bebidas tem γ = 0,392857 e ocupa o 4º posto emissor, exigindo numerador verificável. Segurança, alojamento, artes, edição, audiovisual e aluguéis têm intensidades superiores a utilidades. Isso é um sinal para investigar alocação e fronteira, não demonstração isolada de erro. Serviços domésticos não equivalem a todas as emissões residenciais das famílias.

No extremo inferior, extração de petróleo e fabricação de veículos têm γ = 0,01; transporte terrestre, 0,015714; minério de ferro, educação e saúde públicas, 0,02. Valores tão arredondados têm incerteza relativa importante. Não foi encontrada mudança de classificação local que explicasse os extremos. A falta dos p/x originais impede escolher, entre numerador, denominador e alocação, uma causa factual para cada outlier.

## 9. Validação externa

Referência independente principal: **MCTI (2024), Fifth Biennial Update Report of Brazil (BUR5)**, Apêndice I, páginas impressas 93–96, coluna **2015** (páginas PDF 94–97). [Endereço oficial UNFCCC](https://unfccc.int/sites/default/files/resource/BRA_BUR5_EN.pdf); [cópia do documento primário efetivamente consultada](https://cdn.climatepolicyradar.org/navigator/BRA/2024/brazil-biennial-update-report-bur5_a3a92935f0bfdb543d96efe03ba6771e.pdf). O acesso ao endereço oficial falhou; a cópia é do relatório do MCTI, não uma estimativa produzida pelo espelho.

Os valores são originalmente kt do gás, numericamente iguais a Gg, convertidos abaixo por 1.000. As categorias são fontes de emissão, não atividades SCN. Subcategorias não devem ser somadas novamente aos totais.

| Categoria BUR5, ano 2015 | Mt CO₂ | Limite da comparação |
| --- | ---: | --- |
| Total nacional líquido | 876,747 | Inclui LULUCF líquido; não confrontar como total equivalente aos 683,696 do cenário. |
| Energia | 431,970 | Inclui transportes e combustão industrial; não é apenas setor MIP 3500. |
| Indústrias energéticas | 101,467 | Agregado mais amplo que eletricidade; inclui outras transformações energéticas. |
| Combustão: indústria/construção | 75,201 | Distribuição por atividades necessária; não soma à emissão própria industrial sem conferir processos. |
| Transportes | 200,086 | Famílias, transporte por conta própria e fronteiras de inventário. |
| Rodoviário + ferroviário | 183,673 | Não substituir diretamente o setor MIP 4900 por esse total. |
| Processos industriais e uso de produtos | 88,253 | Distintos da combustão energética. |
| Processo: cimento | 23,903 | Componente associado à fabricação de minerais não metálicos. |
| Processo: ferro/aço | 43,391 | Componente associado à siderurgia. |
| Agropecuária: CO₂ de calagem/ureia | 17,538 | Não contém CH₄/N₂O da agropecuária. |
| LULUCF líquido | 337,834 | Emissões e remoções; não atribuir por setor sem concordância. |
| Resíduos | 1,153 | CO₂ somente, categoria distinta do agregado água/esgoto/resíduos da MIP. |
| Biomassa, item de memória | 323,206 | Não somar novamente ao total nacional. |

O mesmo inventário registra **14,5304 Mt de CH₄ na agropecuária** e **2,7559 Mt de CH₄ nos resíduos**. São massas de metano, não CO₂ e não CO₂e. Não somá-las à coluna acima nem aplicar GWP sem estabelecer outro objeto ambiental.

Comparações substantivas:

- **Minerais não metálicos:** cenário 4,990 Mt versus 23,903 Mt apenas de processo do cimento (4,79 vezes). Se e pretende cobrir toda a emissão direta do setor, um componente físico do mesmo ano já é maior que o total estimado. Reconciliar fontes e atribuição é obrigatório.
- **Siderurgia:** cenário 4,064 Mt versus 43,391 Mt de processos de ferro/aço (10,68 vezes), antes de considerar a combustão classificada em Energia. É forte incompatibilidade com a interpretação abrangente de emissão própria. Não usar o quociente como fator pronto de correção.
- **Água/resíduos:** 51,802 Mt no cenário versus 1,153 Mt de CO₂ dos resíduos. Universos não idênticos: o setor econômico também tem outras operações/combustões. Não afirmar erro exato de 45 vezes, mas exigir explicação física para a magnitude e para o tratamento dos gases.
- **Transporte:** 5,231 Mt no cenário versus 183,673 Mt rodoviário/ferroviário. A diferença pode incluir realocação a famílias e outras atividades; não prova subestimação nessa razão. Tampouco confirma a baixa intensidade usada na pesquisa.

Esses testes não fornecem uma concordância integral de 67 setores nem um ranking alternativo validado. Evidenciam que a consistência interna dos outputs não é suficiente para a interpretação ambiental pretendida. Uma diferença de unidade monetária comum não resolve, por si, problemas distintos de subcobertura industrial, alocação de transporte e composição dos resíduos.

## 10. Fontes alternativas

| Fonte | Possibilidade para 2015 | Viabilidade e trabalho necessário |
| --- | --- | --- |
| MCTI/SIRENE, inventário nacional e BUR5 | Valores por gás e fontes físicas de 2015; primeira prioridade para validação. | Construir concordância de fontes com SCN, separar famílias, residência/território e processos; não há vetor pronto de 67 coeficientes verificado nesta auditoria. |
| [SEEG — dados](https://seeg.eco.br/dados/) e [metodologia](https://seeg.eco.br/metodologia/) | Candidato a séries anuais e desagregação de fontes. | Verificar versão, gás, métrica GWP e fronteira. Não foi validado aqui um download completo compatível; acesso às páginas apresentou falhas. |
| [BEN/EPE 2016](https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-126/topico-92/Relat%C3%B3rio_S%C3%ADntese_2016.pdf) | Energia física por setores e combustíveis em 2015. | Cruzar com fatores de emissão e atividades; acrescentar processos; definir biomassa e transporte próprio. Não cobre sozinho a emissão direta total. |
| [EDGAR_2025_GHG](https://edgar.jrc.ec.europa.eu/dataset_ghg2025) | Série anual 1970–2024, incluindo 2015, separada por gás, país e categorias de fonte. | CO₂ fóssil/processos e biogênico separados; LULUCF excluído desse conjunto. Requer concordância com SCN. Tem ancestralidade comum à fonte atual, portanto não é validação inteiramente independente. |
| [WIOD 2016](https://www.rug.nl/ggdc/valuechain/wiod/wiod-2016-release?lang=en) e [contas ambientais JRC](https://op.europa.eu/en/publication-detail/-/publication/df9c194b-81ba-11e9-9f05-01aa75ed71a1/language-en) | As WIOT terminam em 2014, mas as extensões ambientais JRC anunciadas cobrem 2000–2016. | Não descartar 2015 por confundir intervalo da WIOT com o das extensões. Confirmar acesso, numeradores brasileiros e agregação; não aplicar intensidade em moeda externa a x em reais. |
| [EXIOBASE 3.8.1](https://zenodo.org/records/4588235) | Há arquivos de 2015, satélites físicos e Brasil em outra classificação. | Usar emissões diretas do satélite, não pegada ou multiplicadores. Distinguir dados observados/estimados: a documentação informa anos finais diferentes entre extensões e uso de projeções. Reconciliar atividades antes de dividir por x da MIP. |
| [OECD Air Emissions Accounts](https://www.oecd.org/en/data/datasets/air-emissions-accounts.html) e [indicadores de pegadas/ICIO](https://www.oecd.org/en/data/datasets/greenhouse-gas-footprint-indicators.html) | Contas por atividade e extensões de emissões podem apoiar reconciliação. | Conferir disponibilidade efetiva para Brasil/2015, princípio de residência, agregação e gás. Indicador de pegada de consumo não substitui emissão própria. |
| [EORA — documentação](https://worldmrio.com/documentation/) | Recuperar a versão exata usada pelos autores pode permitir reconstrução. | Exigir linhas selecionadas, p/x e concordância. Uma versão atual ou Eora26 não reproduz automaticamente a base original. |
| [IBGE, contas de energia da biomassa 2015–2018](https://loja.ibge.gov.br/contas-economicas-ambientais-de-energia-produtos-da-biomassa-brasil-2015-2018.html) | Complemento físico e conceitual para biomassa. | Não constitui sozinho inventário de CO₂ das 67 atividades. |

**Avaliação de viabilidade:** há numeradores físicos de 2015 e caminhos defensáveis para abandonar a interpolação, mas não foi identificado e validado um vetor pronto que se possa inserir sem reconciliação. A rota preferida é inventário oficial + energia + processos, com concordância explícita. Estimar partes desconhecidas por participações de output deve ser identificado como proxy, não como observação. Nenhuma reconstrução extensa nem substituição parcial seletiva foi implementada nesta rodada.

## 11. Sensibilidade do resultado

### Rede congelada

Adotar **Cᵢˢᵘᵖ = Σⱼ≠ᵢ Lᵢⱼ**. Lᵢⱼ é a produção monetária bruta de i requerida por uma unidade monetária de demanda final de j sob os coeficientes fixos da MIP. Como x = Ly, a linha i representa o fornecedor, e a coluna j o destino final. Somar a linha fora da diagonal agrega sua participação direta e indireta nos demais destinos com demandas finais unitárias. Não pondera pela demanda observada, não remove fisicamente o setor nem prevê uma paralisação. Excluir Lᵢᵢ não equivale a L−I e não apaga os circuitos que integram caminhos para outros destinos.

O termo *supplier centrality* tem respaldo em medidas de requerimentos/Bonacich, mas a convenção desta pesquisa deve ficar explícita. [Blackburn e Moreno-Cruz (2019), definição 4 e eq. 11, pp. 14–15](https://www.ifo.de/DocDL/cesifo1_wp8007.pdf), usam Mα, com pesos de consumo final e termo próprio. [Ghassibe e Nakov (2025), eq. 33, pp. 20–21](https://www.cerge.cuni.cz/pdf/events/papers/GN_latest.pdf), usam média de coluna da inversa em sua orientação comprador–fornecedor, incluindo a diagonal. Aqui a orientação é transposta, os destinos têm peso uniforme e excluímos o próprio destino. Logo, usar **centralidade como fornecedor baseada em requerimentos de Leontief**, sem alegar replicação exata desses modelos ou importar seus efeitos causais.

Sᵢⱼ = Lᵢⱼ/ΣₖLₖⱼ padroniza cada coluna; S̄ᵢ = Σⱼ≠ᵢSᵢⱼ/66 é a presença relativa média em cadeias padronizadas. O denominador mantém a diagonal da coluna. S muda o estimando e testa dependência do ranking em relação ao total bruto requerido por cada cadeia. A soma direta de A usa produção bruta do comprador como denominador, diferentemente da demanda final unitária de L; não subtrair somas para chamar o resultado de “efeito indireto puro”.

Recalculados diretamente das matrizes da investigação: **ρ(L,S) = 0,997765**, **ρ(A,L) = 0,985314**, **ρ(A,S) = 0,983678**. Os top 10 L/S coincidem; A compartilha nove. A normalização altera pouco a hierarquia. A estrutura direta já contém grande parte dessa hierarquia, mantida quando se incorporam encadeamentos indiretos. São transformações da mesma base, não três confirmações independentes.

Top 10 de L: Comércio; Refino; Transporte terrestre; Intermediação financeira; Agricultura; Atividades jurídicas/contábeis/consultoria; Energia/utilidades; Químicos orgânicos/inorgânicos; Outras atividades administrativas; Extração de petróleo/gás.

HEM fica no suplemento, sem novo cálculo de extração. No fechamento de alocação já usado, Fᵢ é efeito externo absoluto e hᵢ = Fᵢ/xᵢ efeito por unidade do tamanho do setor. O primeiro não confirma L de forma independente; o segundo não refuta L. A queda de Energia em h responde a outra pergunta. As outras extrações históricas permanecem documentadas, sem escolher entre elas para recuperar uma narrativa.

### Cenários ambientais com L fixa

Recalculados das [entradas alinhadas](../outputs/investigacao_redes_2015/entradas_alinhadas.csv), com concordância aos [cenários já publicados](../outputs/investigacao_redes_2015/cenarios_coeficientes.csv):

| Coeficientes aplicados ao x2015 | Total do cenário (Mt) | ρ(e,L) | Parcial de postos por x |
| --- | ---: | ---: | ---: |
| 2011 | 692,368 | 0,370820 | 0,146822 |
| Interpolação 2015 | 683,696 | 0,382792 | 0,158212 |
| 2018 | 677,192 | 0,392729 | 0,185561 |

No cenário central, ρ(L,x) = 0,512371, ρ(L,γ) = −0,182198 e a mediana de |rank(e)−rank(L)| é 16. A atenuação por tamanho e as diferenças de postos existem nesse cenário. Não provam validade do ranking ambiental brasileiro real.

### Influência dos setores

Postos recalculados em cada subconjunto; L setorial permanece fixa, sem reconstrução de uma economia extraída:

| Exclusão | n | ρ(e,L) | Parcial por x |
| --- | ---: | ---: | ---: |
| Nenhuma | 67 | 0,382792 | 0,158212 |
| Energia | 66 | 0,358898 | 0,145053 |
| Água/resíduos | 66 | 0,390586 | 0,156806 |
| Comércio | 66 | 0,361111 | 0,152228 |
| Energia e Comércio | 65 | 0,335490 | 0,137958 |
| Energia, Água/resíduos e Comércio | 64 | 0,341850 | 0,135973 |
| Seis contrastes históricos | 61 | 0,342464 | 0,172523 |
| Minerais não metálicos e siderurgia | 65 | 0,399476 | 0,177893 |

Leave-one-out completo: ρ de **0,356142 a 0,417472**; parcial de **0,087161 a 0,196290**. Água não domina a associação global, embora seja decisiva para um contraste substantivo. Energia e Comércio contribuem para a associação, mas sua retirada não a elimina. Retirar os setores industriais questionados tampouco valida o restante: erros de alocação podem redistribuir emissões entre muitas linhas e não são simulados por excluir uma observação.

### Arredondamento e fatores comuns

Foi verificado que multiplicar todos os coeficientes por um fator positivo comum preserva postos e Spearman. Isso é identidade, não correção empírica de preços.

Sob arredondamento ao centésimo mais próximo, cada coeficiente original admite ±0,005; a interpolação convexa conserva esse limite. Calculam-se e⁻ᵢ = max(γᵢ−0,005,0)xᵢ e e⁺ᵢ = (γᵢ+0,005)xᵢ. Os limites conservadores dos postos comparam intervalos de cada setor com todos os demais. Não se atribui distribuição de probabilidade, e os intervalos não representam incerteza total.

| Setor | Erro relativo máximo de arredondamento | Limites conservadores de rank e |
| --- | ---: | ---: |
| Energia | 2,30% | 1–1 |
| Água/resíduos | 0,61% | 2–2 |
| Construção | 8,14% | 3–3 |
| Comércio | 20,59% | 4–10 |
| Refino | 20,59% | 20–32 |
| Transporte terrestre | 31,82% | 29–51 |

Não foi usado Monte Carlo adicional. A estabilidade de Água nesse teste apenas afasta arredondamento como explicação de sua posição. Não afasta erro na fonte. Os contrastes de Refino e Transporte não foram validados sob outra extensão ambiental completa; isso permanece **não demonstrado**, apesar de sua centralidade estrutural alta.

### Reprodução focal dos diagnósticos

O [notebook histórico](../investigacao_redes_emissoes_2015.ipynb) continua sendo a entrada da investigação. O trecho abaixo reproduz os diagnósticos novos lendo seus outputs, sem regravar resultados ou adicionar dependências. Execute da raiz com o ambiente do projeto. Postos médios em empates; sem p-valores de amostra IID.

```python
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

p = Path('outputs/investigacao_redes_2015')
t = pd.read_csv(p/'entradas_alinhadas.csv', dtype={'atividade': str}).set_index('atividade')
m = pd.read_csv(p/'metricas_setoriais.csv', dtype={'atividade': str}).set_index('atividade').loc[t.index]
L = pd.read_csv(p/'matriz_L.csv', index_col=0, dtype=str)
assert list(L.index) == list(t.index) == list(L.columns)
L = L.astype(float).to_numpy()
c = L.sum(axis=1) - np.diag(L)
x = t.x.to_numpy()
e = t.e.to_numpy()
g = (3*t.gamma2011.to_numpy() + 4*t.gamma2018.to_numpy())/7
np.testing.assert_allclose(c, m.L_saida, atol=1e-12)
np.testing.assert_allclose(e, g*x, atol=1e-8)

def parcial(e, c, x):
    r = pd.DataFrame({'e': e, 'c': c, 'x': x}).rank(method='average')
    X = np.column_stack([np.ones(len(r)), r.x])
    U = r[['e', 'c']].to_numpy() - X @ np.linalg.lstsq(X, r[['e', 'c']], rcond=None)[0]
    return np.corrcoef(U.T)[0, 1]

for ano, gamma in [('2011', t.gamma2011.to_numpy()), ('2015', g), ('2018', t.gamma2018.to_numpy())]:
    print(ano, (gamma*x).sum()/1000, spearmanr(gamma*x, c).statistic, parcial(gamma*x, c, x))
grupos = [[], ['3500'], ['3680'], ['4580'], ['3500', '4580'],
          ['3500', '3680', '4580'], ['3500', '3680', '4180', '4580', '1991', '4900'],
          ['2300', '2491']]
for grupo in grupos:
    k = ~t.index.isin(grupo)
    print(grupo, k.sum(), spearmanr(e[k], c[k]).statistic, parcial(e[k], c[k], x[k]))
loo = []
for setor in t.index:
    k = t.index != setor
    loo.append([spearmanr(e[k], c[k]).statistic, parcial(e[k], c[k], x[k])])
print('LOO min/max:', np.min(loo, axis=0), np.max(loo, axis=0))
lo, hi = np.maximum(g-.005, 0)*x, (g+.005)*x
limites = pd.DataFrame({'melhor': [1+(lo > hi[i]).sum() for i in range(len(t))],
                       'pior': [len(t)-(hi < lo[i]).sum() for i in range(len(t))]}, index=t.index)
print(limites.loc[['3500', '3680', '4180', '4580', '1991', '4900']])
```

## 12. Classificação da base

**C — útil apenas como proxy exploratória.** A multiplicação e a transcrição são reproduzíveis, e o conceito formal de intensidade direta é adequado à pergunta. Contudo, a incerteza não se limita a um deflator conhecido ou a uma concordância local corrigível: faltam os numeradores originais e os pesos ambientais; há fronteira contraditória e discrepâncias de magnitude que afetam setores substantivos.

Não é A, pois a interpretação final não está validada. Não é B, porque ainda não há correção monetária/setorial demonstrada que resolva o conjunto de problemas. Não é necessário classificar como D: não se demonstrou que a Tabela 2 seja uma pegada incorporada usada indevidamente, e o cenário continua útil para mostrar o método. **C não autoriza publicar seus postos como ranking confiável dos emissores de 2015.**

## 13. Correções obrigatórias

1. Fixar a fronteira ambiental: CO₂ por atividade; separar fóssil, processos e biomassa; declarar tratamento de LULUCF, famílias e território/residência. Não trocar para CO₂e para acomodar uma base disponível.
2. Recuperar os dados e a concordância usados pelos autores, ou selecionar outra extensão física de 2015. Exigir versões, categorias, pesos e numeradores, não somente o vetor final.
3. Reconciliar as atividades e confrontar explicitamente cimento/siderurgia, água/resíduos, transporte, energia e os serviços com intensidades elevadas. Documentar incertezas e agregações irredutíveis.
4. Harmonizar os denominadores: produção bruta compatível, preços básicos e ano monetário. Preferir dividir o numerador físico reconciliado por x2015.
5. Recalcular **a mesma especificação de L**, associações e contrastes com a extensão validada. Preservar esta versão como cenário e registrar qualquer mudança substantiva; não procurar outra centralidade para manter conclusões.
6. Só então finalizar figuras, conclusões ambientais e redação empírica. Os gráficos históricos em S não podem ser relabelados como L sem recalcular seus eixos.

As pendências de fonte não foram resolvidas por suposição. Não houve comunicação com autores, aquisição de dados ou substituição parcial dos coeficientes.

## 14. Impacto sobre a pergunta de pesquisa

| Resultado | Classificação | Fundamentação |
| --- | --- | --- |
| Identificação dos fornecedores centrais em L | **Robusta**, dentro da MIP e das convenções adotadas | Independente de γ; forte concordância A/L/S. Não implica causalidade, essencialidade ou invariância à agregação. |
| Ranking dos maiores emissores brasileiros de 2015 | **Não sustentada** | O ranking computacional está correto para o cenário; sua interpretação como ranking físico real não está validada. |
| Divergência emissão própria × supplier centrality | **Frágil**, como conclusão substantiva sobre o Brasil | Existe no cenário e resiste a exclusões, mas não foi testada com uma alocação ambiental independente reconciliada. |

O problema atual não é “qual centralidade funciona melhor”. É se a variável ambiental representa o objeto prometido. A contribuição metodológica e a posição estrutural dos setores permanecem defensáveis. As hipóteses ambientais podem ser mantidas como perguntas, sem apresentá-las como empiricamente confirmadas.

## 15. Recomendação final

**Substituir a base como insumo principal, ou reconstruí-la e validá-la antes do uso final; conservar os coeficientes atuais apenas como cenário exploratório.** Não basta aplicar inflação comum nem refinar arredondamentos. Priorizar o numerador físico de 2015 e uma concordância auditável; manter L fixa durante essa correção.

Respostas aos dez critérios de sucesso:

1. **Medida:** soma da linha de L fora da diagonal, com S como robustez de normalização, A como contraste e HEM como suplemento.
2. **O que mede:** requerimentos monetários do fornecedor, diretos e indiretos, para demandas finais unitárias dos demais setores; não retirada causal.
3. **Origem de cada γ:** linha nominalmente correspondente da Tabela 2, dois anos transcritos e interpolação explícita na tabela de 67 atividades. A alocação física anterior não foi recuperada.
4. **Conceito:** intensidade direta declarada de CO₂/produção bruta; fronteira implementada não certificada, especialmente LULUCF/biomassa.
5. **Multiplicação por x2015:** correta dimensionalmente, mas monetária e ambientalmente não validada com fator 1.
6. **Interpolação:** defensável apenas como cenário transparente, não como melhor estimativa de 2015 já demonstrada.
7. **Contrastes independentes:** não foram confirmados por vetor alternativo compatível; comparações de processos levantam problemas materiais.
8. **Conclusão conjunta:** válida como descrição condicional do cenário, frágil como afirmação empírica sobre emissões de 2015.
9. **Limitação principal:** validade/alocação/fronteira dos coeficientes e compatibilidade monetária; não a estabilidade da hierarquia de rede.
10. **Pronto para versão acadêmica final?** A especificação estrutural está fechada; o conjunto ambiental ainda não.

**Conferência desta entrega:** os cálculos da seção 11 foram executados diretamente dos outputs da investigação; os 134 coeficientes foram cotejados com o PDF original. A auditoria confere alinhamento, identidades A/L/S/Z/H/P, cenários, influência e limites de arredondamento. Os arquivos históricos da pasta de investigação foram preservados byte a byte. Passaram os 4 testes de investigação, 6 de consistência e 5 de validação de centralidade, totalizando 15. Esses testes verificam os cálculos, não certificam a validade ambiental da fonte.
