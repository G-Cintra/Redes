# Referências para comparar emissões e consumo no Brasil

Este documento registra somente resultados e métodos publicados nos três PDFs arquivados. Seu objetivo é orientar a comparação com as contas de produção, consumo e renda do notebook.

## Leitura correta das três medidas

| Referência | Medida atribuída ao Brasil | Abordagens publicadas |
| --- | --- | --- |
| Marques et al. (2012) | Emissões diretas, incorporadas na demanda e habilitadas pela renda, com comércio internacional | Produção, consumo e renda |
| Montoya et al. (2026) | Pegada de carbono da demanda brasileira, separada em origem interna e importada | Consumo; não estima renda/Ghosh |
| Sanguinet e Azzoni (2024) | CO2 ligado à demanda e ao valor adicionado nas cadeias inter-regionais brasileiras | Demanda/consumo e oferta/renda; também intensidades diretas |

Somente Marques publica os três critérios para o Brasil. Sanguinet é o benchmark operacional mais próximo do notebook, porque usa 67 setores compatíveis com a classificação da MIP do IBGE. Montoya é o benchmark para pegada de consumo com importações e para renovabilidade, não para renda.

## Ordem de grandeza: notebook e referências

**Conversão usada nesta seção:** `1 Mt CO2 = 1.000 Gg CO2`. Os valores do notebook abaixo são resultados reproduzíveis da MIP brasileira de 2015: as intensidades de 2011 e 2018 são aplicadas à estrutura monetária de 2015. Logo, os anos indicam o vetor de intensidade, não um inventário observado naqueles anos.

| Fonte e método | Ano | Valor publicado/calculado | Equivalente em Mt CO2 | Comparabilidade |
| --- | ---: | ---: | ---: | --- |
| **Notebook — produção territorial** | intensidade 2011 | 692.368,19 Gg CO2 | 692,37 | Brasil, MIP 2015; emissões diretas por atividade |
| **Notebook — consumo com exterior representativo** | intensidade 2011 | 695.566,25 Gg CO2 | 695,57 | Demanda doméstica + importações finais/intermediárias; `gamma_EXT = gamma_BR` e `L_EXT = L_BR` |
| **Notebook — renda doméstica** | intensidade 2011 | 692.368,19 Gg CO2 | 692,37 | Sistema doméstico fechado; ainda não é renda internacional de Marques |
| **Sanguinet — demanda/consumo** | 2011 | 589.974 Gg CO2 | 589,97 | IRIO de 27 UFs × 67 setores |
| **Sanguinet — oferta/renda** | 2011 | 503.523 Gg CO2 | 503,52 | IRIO de 27 UFs × 67 setores |
| **Notebook — produção territorial** | intensidade 2018 | 677.191,93 Gg CO2 | 677,19 | Brasil, MIP 2015; emissões diretas por atividade |
| **Notebook — consumo com exterior representativo** | intensidade 2018 | 675.133,24 Gg CO2 | 675,13 | Demanda doméstica + importações finais/intermediárias; `gamma_EXT = gamma_BR` e `L_EXT = L_BR` |
| **Notebook — renda doméstica** | intensidade 2018 | 677.191,93 Gg CO2 | 677,19 | Sistema doméstico fechado; ainda não é renda internacional de Marques |
| **Sanguinet — demanda/consumo** | 2018 | 783.654 Gg CO2 | 783,65 | IRIO de 27 UFs × 67 setores |
| **Sanguinet — oferta/renda** | 2018 | 639.057 Gg CO2 | 639,06 | IRIO de 27 UFs × 67 setores |
| **Marques — produção** | 2004 | 234,81 Mt CO2 | 234,81 | MRIO global; Brasil agregado |
| **Marques — consumo** | 2004 | 215,53 Mt CO2 | 215,53 | MRIO global; inclui comércio internacional |
| **Marques — renda** | 2004 | 241,66 Mt CO2 | 241,66 | MRIO global; inclui comércio internacional |
| **Montoya — pegada nacional de carbono** | 2000 | 543.440,307 na escala impressa | não converter | Tabela 5: escala/unidade deve ser confirmada no dataset dos autores |
| **Montoya — pegada nacional de carbono** | 2015 | 762.459,242 na escala impressa | não converter | Tabela 5: escala/unidade deve ser confirmada no dataset dos autores |

### Leitura dos números

- **Sanguinet:** o notebook e o artigo estão na mesma ordem de grandeza, entre aproximadamente **0,5 e 0,8 Gt CO2** (500–800 Mt CO2). A diferença é esperada: Sanguinet usa MIPs inter-regionais de 2011 e 2018; o notebook mantém a estrutura nacional de 2015 e muda apenas o vetor de intensidade.
- **Marques:** seus valores brasileiros estão na ordem de **0,2 Gt CO2**, inferior à escala atual do notebook e de Sanguinet. Não é uma divergência de implementação por si só: trata-se de 2004, MRIO global e um inventário/fonte de emissões distintos. A comparação útil é conceitual, principalmente a diferença entre produção, consumo e renda.
- **Montoya:** os valores são explicitamente registrados acima, mas não são usados para teste de ordem de grandeza até que a escala numérica da Tabela 5 seja confirmada nos dados dos autores. Além disso, é uma pegada de CO2eq, não necessariamente CO2 estrito.
- **Renda no notebook:** coincidir com produção é consequência do fechamento do sistema doméstico. Não deve ser interpretado como confirmação do resultado de renda de Sanguinet ou Marques.

Como diagnóstico adicional, as emissões territoriais brasileiras associadas às exportações calculadas no notebook são 109.439,08 Gg CO2 (109,44 Mt) com a intensidade de 2011 e 105.408,13 Gg CO2 (105,41 Mt) com a intensidade de 2018. Elas são excluídas da conta de consumo brasileira.

## Marques, Rodrigues, Lenzen e Domingos (2012)

Fonte: [artigo na editora](https://doi.org/10.1016/j.ecolecon.2012.09.010).

### Método e dimensões

- MRIO global construído com GTAP 7.1, ano **2004**, cobrindo **112 países/regiões** (seção 6.1, p. 62).
- Parte de emissões diretas setoriais (`e`), transações (`Z`), demanda final (`y`), valor adicionado (`v`) e produção (`x`).
- Produção: emissão direta territorial. Consumo: emissão a montante da demanda final, pela inversa de Leontief. Renda: emissão a jusante habilitada por fornecedores de fatores primários, pela inversa de Ghosh.
- A equação de renda é `d = v_hat (I - x_hat^-1 Z)^-1 x_hat^-1 e` (Eq. 2, p. 62).
- O Brasil é a soma dos setores no MRIO. O artigo **não publica resultados setoriais brasileiros**: a tabela empírica é agregada por país/região.

### Resultados para o Brasil

Tabela 2 (p. 61), **Mt CO2**, 2004:

| Produção | Consumo | Renda |
| ---: | ---: | ---: |
| 234,81 | 215,53 | 241,66 |

A ordenação é **consumo < produção < renda**. Em relação à produção, consumo é 19,28 Mt CO2 menor (-8,2%) e renda é 6,85 Mt CO2 maior (+2,9%). São diferenças de atribuição e comércio, não de emissão física mundial.

### Comparação com o projeto

É a referência conceitual para as três contas. Não deve ser comparada em nível com o notebook: usa 2004, MRIO global, classificação setorial própria e Mt CO2. O sinal relativo brasileiro só é comparável qualitativamente depois de incluir importações e exportações de forma consistente.

## Montoya, Bertussi, Allegretti e Talamini (2026)

Fonte: [artigo na editora](https://doi.org/10.1007/s10668-024-05251-8).

### Método e dimensões

- Modelo ecológico de insumo-produto para **2000, 2005, 2010 e 2015** (seção 2, pp. 6728–6733).
- Combina MIPs do IBGE, Balanço Energético Nacional/EPE, fatores de carbono IPCC e WIOD para o componente externo.
- A pegada de consumo é dividida em parcela **interna** e **externa**; a externa é o conteúdo incorporado nas importações usadas na demanda brasileira. Exportações não pertencem à pegada brasileira de consumo.
- As matrizes foram compatibilizadas em **40 setores** (p. 6733). O recorte é nacional, com comércio internacional, sem resultados por UF.
- Não usa Ghosh nem calcula responsabilidade baseada em renda.

### Resultados nacionais

Tabela 5 (p. 6740), valores na escala impressa (`t CO2eq ano^-1`):

| Ano | Pegada nacional | Interna | Externa |
| --- | ---: | ---: | ---: |
| 2000 | 543.440,307 | 317.444,181 (58,4%) | 225.996,126 (41,6%) |
| 2005 | 508.709,048 | 335.804,092 (66,0%) | 172.904,956 (34,0%) |
| 2010 | 818.728,960 | 460.066,894 (56,2%) | 358.662,067 (43,8%) |
| 2015 | 762.459,242 | 467.966,283 (61,4%) | 294.492,959 (38,6%) |

O texto também descreve os extremos como 543,4 e 762,4 “thousand tonnes”, enquanto a tabela usa os valores acima com separador de milhares. Antes de converter a Gg ou Mt, a escala deve ser confirmada no dataset dos autores (Montoya et al., 2021); este relatório preserva a unidade impressa.

Resultados setoriais publicados:

- Na média de 2000–2015, indústria, serviços e agroindústria respondem por 42,4%, 34,5% e 17,1% da pegada de carbono total (Tabela 6, p. 6741).
- Transporte, indústria química e alimentos processados respondem juntos por 49,8% do CO2eq (pp. 6743–6745).
- A parcela renovável da pegada de carbono cresce de 21,6% em 2000 para 26,5% em 2015; em 2015, 96,2% da parcela externa não renovável decorre de importações (Tabela 5 e p. 6738).

### Comparação com o projeto

É adequado para comparar 2015 após uma concordância **40 setores ↔ 67 atividades**. O notebook agora inclui importações finais e intermediárias, sob a hipótese simplificadora de que o exterior tem a mesma tecnologia e intensidade setorial do Brasil; Montoya usa um componente externo baseado na WIOD. Portanto, os totais continuam não diretamente comparáveis. O artigo não valida a coluna `renda`.

## Sanguinet e Azzoni (2024)

Fonte: [artigo na editora](https://doi.org/10.1016/j.rspp.2024.100015).

### Método e dimensões

- MIP inter-regional de **27 UFs e 67 setores** para **2011 e 2018**; estrutura estimada pelo NEREUS-USP e atualizada/balanceada com RAS e Contas Regionais do IBGE (seção 2.3, p. 3).
- Intensidade direta `gamma_j = p_j/x_j`, compatibilizada de EORA e EDGAR, em **Gg por R$ milhão de produção bruta** (seção 2.1, p. 2; Tabela 2, p. 5).
- Demanda: `C = gamma_hat L y`, pela inversa de Leontief. Oferta/renda: `F = v G gamma_hat`, pela inversa de Ghosh.
- Decomposição estrutural bipolar 2011–2018: demanda (intensidade, estrutura produtiva, demanda doméstica, exportações); renda (atividade econômica, estrutura econômica, alocação, intensidade).
- Limitação declarada: a intensidade de cada setor é a mesma em todas as UFs; o recorte regional varia por estrutura e encadeamentos, não por fator de emissão estadual.

### Resultados nacionais e regionais

Tabela 3 (p. 7), **Gg CO2**:

| Conta | 2011 | 2018 | Variação |
| --- | ---: | ---: | ---: |
| Demanda/consumo | 589.974 | 783.654 | +32,8% |
| Oferta/renda | 503.523 | 639.057 | +26,9% |

- São Paulo é a maior UF: demanda de 208.014 para 250.606 Gg e renda de 174.804 para 206.733 Gg.
- Em 2018, Rio de Janeiro e Minas Gerais vêm a seguir: demanda 76.843 e 70.368 Gg; renda 65.874 e 54.759 Gg.
- No lado da demanda, estrutura produtiva, exportações e demanda doméstica explicam o aumento. No lado da renda, estrutura de alocação e atividade econômica se destacam; a primeira explica aproximadamente 87% do aumento do lado da oferta (pp. 6–8).

### Resultados por atividade

A Tabela 2 contém as 67 **intensidades diretas**, e não uma tabela de responsabilidades nacionais por atividade. Exemplos (Gg/R$ milhão):

| Atividade | 2011 | 2018 | Variação |
| --- | ---: | ---: | ---: |
| Fabricação e refino de açúcar | 0,42 | 0,58 | +40,0% |
| Eletricidade, gás natural e outras utilidades | 0,16 | 0,26 | +65,8% |
| Água, esgoto e gestão de resíduos | 0,55 | 1,03 | +85,7% |
| Alojamento | 0,32 | 0,29 | -8,9% |
| Intermediação financeira, seguros e previdência | 0,04 | 0,02 | -43,1% |

Os resultados setoriais da decomposição são remetidos ao material suplementar. Logo, o CSV deste repositório reproduz um insumo (a Tabela 2), não uma tabela publicada de responsabilidade por atividade.

### Comparação com o projeto

É a referência principal para o notebook: mesma ordem de 67 atividades, mesma unidade das intensidades e mesmas contas econômicas. Ainda não há comparação válida de totais: o notebook combina MIP nacional de **2015** com intensidades de 2011/2018, enquanto o artigo usa MIPs inter-regionais dos próprios anos. A sequência correta é comparar intensidades por setor e, depois, reproduzir o recorte temporal e regional.

## Matriz de comparabilidade

| Dimensão | Notebook atual | Marques | Montoya | Sanguinet |
| --- | --- | --- | --- | --- |
| Ano | Estrutura 2015; intensidades 2011/2018 | 2004 | 2000, 2005, 2010, 2015 | 2011, 2018 |
| Espaço | Brasil nacional | MRIO global; Brasil agregado | Brasil com importações | 27 UFs brasileiras |
| Atividades | 67 | Não publicadas para Brasil | 40 | 67 |
| Produção | Sim | Sim | Não como conta comparável | Intensidades diretas |
| Consumo | Sim, com exterior representativo de mesma tecnologia/intensidade | Sim, comércio internacional | Sim, interna + importada | Sim, demanda e exportações |
| Renda/Ghosh | Sim | Sim | Não | Sim |

## Protocolo para comparações futuras

1. Não comparar totais sem harmonizar ano, unidade, fronteira comercial e agregação setorial.
2. Usar Sanguinet para conferir os 67 coeficientes e as fórmulas Leontief/Ghosh; registrar sempre que aplicar intensidades de 2011/2018 à MIP 2015 é uma simulação.
3. Usar Marques para testar a lógica das três atribuições; a conta de consumo já incorpora comércio exterior sob hipótese de exterior representativo, mas a conta de renda ainda não.
4. Usar Montoya para avaliar a hipótese externa da conta de consumo, construir uma concordância 67→40 e confirmar a escala da Tabela 5 no dataset dos autores.
