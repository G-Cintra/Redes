# Handover da entrega e avaliação de mérito

Registro atualizado em 29/10/2026 para continuar o trabalho em outro computador ou com outro agente. A versão de referência é o artigo atual, incluindo a introdução revisada pelo usuário e a integração das implicações de mitigação descrita a seguir. Os registros de 28/10 e o histórico de conciliação de versões permanecem documentados nas seções posteriores; não confundir recomendações históricas com o estado atual.

## Integração das implicações de mitigação em 29/10/2026

O usuário aprovou incorporar a discussão baseada em Rissman et al. (2020), com mudanças localizadas e sem desfigurar o trabalho. Na introdução, autorizou alterar **apenas o último parágrafo**. Foi usada como base a introdução que o próprio usuário revisou em 29/10, incluindo a pergunta sobre a distribuição das emissões nas relações entre atividades emissoras e setores de produtos finais. Todo o trecho anterior ao último parágrafo foi preservado byte a byte. Não restaurar a introdução de 28/10 com base no hash histórico registrado adiante.

- **Resultados:** foi explicitado que outras atividades geram cerca de 39,5% das emissões atribuídas aos produtos finais da construção e que 60,5% permanece na diagonal. A proporção foi conferida nas saídas já existentes do notebook: construção tem 59.397,0619 Gg pela demanda, 23.483,7571 Gg de entrada externa e 35.913,3049 Gg na diagonal. Não houve novo indicador ou mudança de cálculo. As cinco tabelas e as nove figuras foram preservadas integralmente.
- **Discussão:** os quatro primeiros parágrafos foram mantidos. A passagem genérica sobre mitigação foi desenvolvida em três parágrafos, relacionando a composição da conta da construção a eficiência material e critérios de emissões incorporadas nos projetos; informação verificável sobre materiais e compras públicas de produtos de menor emissão; e a distribuição das atribuições associadas a uma redução da intensidade emissora de energia, com estrutura produtiva e demanda fixas. As citações usam as seções 5.1 e 6.4, 6.6 e 6.7, e 4.2 e 7.2 de Rissman, respectivamente.
- **Alcance:** a revisão fundamenta a pertinência de discutir essas estratégias com o diagnóstico intersetorial, sem atribuir ao estudo uma avaliação de eficácia, custo ou tecnologia ótima. A matriz não identifica contratos, poder de negociação ou participação governamental na demanda da construção. Essa participação não é medida pelo nó de administração pública. Informações de fornecedores e avaliação de ciclo de vida continuam necessárias à especificação de materiais. A limitação dos coeficientes ambientais foi mantida.
- **Sínteses:** o último parágrafo da introdução passou a apresentar o setor da construção, a parcela de 39,5% e a ligação com as estratégias de mitigação. O resumo e o encerramento da conclusão foram alinhados. A análise de concentração, os casos de energia e água/resíduos e a avaliação do backbone permanecem no trabalho. A metodologia, os dados, as referências e o notebook não foram alterados.
- **Backup:** `entrega/backup/mitigacao_rissman_20261029_085224_853476/`, com os fontes afetados, o PDF e o handover anteriores, além do manifesto de integridade e da verificação final. O manifesto registra o comprimento e o hash do trecho protegido da introdução.
- **Verificação:** compilação LaTeX/Biber concluída, com 29 páginas, sem referências indefinidas ou caixas excedentes. As 29 páginas foram inspecionadas em visão geral; resumo, discussão e conclusão foram conferidos em detalhe. Foi ajustada uma quebra de página na discussão para evitar uma linha de abertura de parágrafo isolada. Não foram executados novamente cálculos nem testes analíticos, pois não houve alteração de código, dados ou método. Nesta etapa não foi solicitado novo commit ou push.

No ajuste seguinte do fechamento, a abertura passou a retomar a produção nacional e a frase final afirma diretamente a ligação com as estratégias de mitigação. Foram retiradas desse parágrafo as ressalvas repetidas. A mudança permanece limitada ao último parágrafo. Backup anterior: `entrega/backup/fechamento_introducao_20261029_091042_566505/`.

## Leitura crítica e ajustes de 28/10/2026 (histórico)

Pedido expresso do usuário para o próximo agente:

> Faça uma leitura crítica da versão revisada, seguindo Booth e Nikolov. A análise de redes e o diálogo com a dissertação ficaram integrados de forma orgânica? Preserve a introdução.

**A leitura crítica foi realizada e o usuário autorizou implementar seus ajustes.** O diagnóstico foi favorável à integração substantiva das redes e ao diálogo com a dissertação, com necessidade de explicitar a síntese das diferenças entre as contas, desenvolver as consequências dos achados na discussão, aproximar figuras e interpretação e distinguir emissões próprias da parcela da diagonal. A introdução aprovada permanece integralmente preservada.

Foram ajustados os resultados, a discussão e a conclusão para relacionar explicitamente os saldos aos perfis de saída e entrada, explicar as consequências da importância assimétrica e desenvolver a aplicação estadual sem linguagem de relatório de andamento. A figura de indicadores passou a acompanhar a comparação de volume e concentração; os painéis da matriz e do backbone receberam interpretações mais específicas. Todas as nove figuras e seus blocos de inclusão foram preservados. Uma opção de posicionamento de tabela e algumas quebras de página foram ajustadas para aproximar texto e evidência.

Também foi condensada a exposição de MIP após conferir **Marques et al. (2012), seção 6.1, pp. 61–62**, e **Sanguinet e Azzoni (2024), seção 2.1, p. 2**. Marques apresenta as contas em poucas equações e remete as derivações à literatura; Sanguinet explicita o balanço de Leontief, as intensidades e a extensão ambiental antes da decomposição. O texto atual reúne a base de MIP e as contas em uma subseção, mantendo definições, unidades, hipóteses, emissões por unidade de demanda, volumes atribuídos, conservação, saldo e exemplo didático. A exposição não incorpora o modelo de Ghosh, a conta pela renda ou a decomposição estrutural daqueles artigos. Na contagem de texto do arquivo `modelo_atribuicao.tex`, a exposição passou de 430 para 331 palavras; o objetivo foi eliminar repetição, não impor uma meta.

**Backup anterior às alterações:** `entrega/backup/ajustes_argumento_metodologia_20261028_210722_847479/`, com os fontes afetados, PDF anterior, handover anterior, README e manifesto de integridade. A introdução, os dados, a bibliografia, o notebook e os nove arquivos de figuras mantêm seus hashes; os valores, as legendas e as notas das cinco tabelas dos resultados foram preservados. As equações dos métodos de rede permanecem idênticas. Na parte de MIP, foram reunidas apresentações equivalentes das contas e colocadas expressões simples no texto, sem mudar as operações.

**Verificação da revisão argumentativa:** LaTeX/Biber compilados com sucesso, PDF final de 30 páginas, sem referências indefinidas ou caixas excedentes no log. As 30 páginas foram conferidas em visão geral e as equações e tabelas relevantes, em detalhe. Não foram reexecutados cálculos nem testes analíticos, pois não houve alteração de código, dados ou método. A leitura crítica está concluída; a nova redação aguarda a avaliação pessoal do usuário. Esta revisão não foi objeto de um novo pedido de commit ou push.

O foco do diálogo com a dissertação permanece na explicação das diferenças entre as contas pela produção e pela demanda. Não foi solicitado acrescentar um teste de sua hipótese sobre intensidade de emissão e orientação das vendas.

## Simplificação posterior da apresentação dos dados

Por solicitação do usuário, a subseção de fontes foi reduzida aos dois parágrafos sobre a MIP e as intensidades ambientais. Foram retiradas a tabela de fontes e dimensões, a menção ao número da tabela do artigo de Sanguinet e Azzoni e a equação de interpolação. Permanecem a descrição da interpolação linear e sua hipótese, sem observação física de 2015. A subseção de fronteira e validade ambiental foi preservada. Os detalhes operacionais continuam no notebook e na documentação do repositório; não houve mudança de dados ou cálculos.

Backup anterior: `entrega/backup/simplificacao_dados_20261028_212827_147240/`, com dados, PDF e handover anteriores e hashes dos arquivos preservados. Introdução, metodologia, resultados, apêndices, figuras e notebook não foram alterados nesta simplificação. LaTeX/Biber recompilados com sucesso; PDF atual de **29 páginas**, sem referências indefinidas ou caixas excedentes. Conferidas visualmente a seção de dados e a renumeração de equações e tabelas. A antiga tabela de fontes foi excluída; a tabela de contas setoriais passou a ser a Tabela 1. A numeração dos resultados muda automaticamente, sem alterar valores.

## Ajuste da abertura da seção 3.1

A abertura passou a apresentar as relações de fornecimento e demanda final descritas pela MIP antes dos coeficientes técnicos e da matriz A. Em seguida, apresenta produção bruta, usos intermediários, demanda final e requisitos diretos e indiretos, associados a x, y e L. Foi explicitado que I é a matriz identidade. O ajuste acrescentou 40 palavras; as equações e o restante da explicação foram preservados.

Backup anterior: `entrega/backup/abertura_metodologia_20261028_214021_599595/`. A figura didática conserva arquivo, dimensões, conteúdo e legenda; mudou somente sua opção de posicionamento para acompanhar a continuação da explicação na mesma página. Introdução, dados, resultados, demais figuras, apêndices e notebook permanecem intactos. LaTeX/Biber compilados com sucesso: PDF de 29 páginas, sem referências indefinidas ou caixas excedentes; abertura e continuidade com a figura conferidas visualmente.

## Últimas decisões de apresentação e extensão

- **Título definido pelo usuário:** “Rede de emissões de CO₂ no Brasil”. Usar título único, sem o subtítulo anterior. A fronteira das emissões é explicada no texto.
- **Paginação:** cada seção principal, de 1 a 6, e as referências devem começar em nova página. A quebra anterior à introdução está em `main.tex`, sem editar `introducao.tex`.
- **Apêndices:** identificar os cabeçalhos e as referências como “Apêndice A” e “Apêndice B”; a versão atual possui dois apêndices. A subseção B.1 mantém sua numeração. Não criar um terceiro apêndice apenas pela menção genérica a “A B C” na conversa.
- **Extensão desejável:** 2.500–3.000 palavras de corpo, como preferência flexível. O usuário aceita um texto maior. A clareza, a correção e a preservação das explicações necessárias continuam prioritárias; esta passagem não realizou cortes para atingir uma meta.
- **Localização nesta revisão:** repositório em `C:/GitHub/Redes-1`; dissertação em `C:/GitHub/Mestrado/0-Projeto de Dissertação`. No computador da retomada anterior, os repositórios estavam em `C:/Users/acarm/GitHub/Redes` e `C:/Users/acarm/GitHub/Mestrado`. Localizar os documentos pela estrutura relativa.
- **PDF atual:** `entrega/main.pdf`, com 29 páginas após a integração das implicações de mitigação. As seções principais continuam começando em nova página. A introdução atual é a versão revisada pelo usuário em 29/10, com alteração autorizada apenas no último parágrafo nesta etapa; o hash de 28/10 é histórico.
- **Backup anterior ao título e à paginação:** `entrega/backup/titulo_handover_20261028_145242175/`, com os fontes afetados, PDF, handover e README anteriores, além do script e do registro de contagem daquela etapa.
- **Sincronização anterior:** o commit `1eadced` contém o aprofundamento feito no outro computador. A revisão argumentativa e metodológica registrada acima é posterior; sincronização e aprovação pessoal do conteúdo são etapas distintas.
- **Temporários locais:** scripts de diagnóstico, logs adicionais e imagens de conferência foram preservados em `outputs/entrega_redes_2015/revisao_editorial_20261028/`, pasta ignorada pelo Git. A remoção havia sido bloqueada pela revisão automática; os arquivos foram organizados sem exclusão. As evidências necessárias à retomada estão no artigo, nas saídas do notebook e nos backups versionados, sem depender dessa pasta local.

### Contagem atual de palavras do corpo

**4.402 palavras**, segundo TeXcount, com peso apenas para `Words in text`. Excluídos títulos e subtítulos, abstract, palavras-chave, referências bibliográficas, apêndices, figuras e tabelas completas (incluindo legendas, fontes e notas), notas de rodapé e fórmulas. Com as 59 palavras das notas de rodapé, seriam **4.461 palavras**. Essa contagem inclui a introdução revisada pelo usuário e os ajustes de mitigação. As contagens anteriores registradas no histórico não representam a versão atual.

| Parte | Palavras do corpo |
| --- | ---: |
| Introdução | 520 |
| Dados e recorte | 308 |
| Metodologia | 1.085 |
| Resultados | 1.533 |
| Discussão | 742 |
| Conclusões | 214 |
| **Total** | **4.402** |

Procedimento: expandir os quatro arquivos incluídos no corpo de `main.tex`, da introdução até as conclusões; excluir o material anterior à introdução e posterior às conclusões, além dos ambientes completos de figura e tabela; preservar o preâmbulo para reconhecer as regras de biblatex; executar `texcount -utf8 -sub=section -sum=1,0,0,0,0,0,0` sobre esse fonte temporário. A convenção de contagem é a do TeXcount; não se convertem manualmente citações e referências cruzadas em palavras. Uma cópia histórica do script está em `entrega/backup/titulo_handover_20261028_145242175/contar_corpo_revisado.py`. A contagem atual adapta sua verificação de 11 para 10 ambientes de figuras e tabelas, devido à retirada da tabela de fontes, sem editar o script guardado no backup. Executar a partir da raiz do repositório.

## Esclarecimento sobre a validação ambiental pendente

Essa limitação já constava na seção 2.2 do artigo e na auditoria ambiental anterior; não é uma nova falha identificada pela última revisão. Os cálculos verificam a aplicação das fórmulas e a consistência das contas para os dados utilizados. Validar a base ambiental exige conferir se as intensidades de emissão correspondem às emissões e aos denominadores necessários à aplicação:

1. **Ano físico:** os coeficientes publicados são de 2011 e 2018; o vetor de 2015 é uma interpolação, sem observação física de 2015 incorporada ao cálculo.
2. **Preços e denominadores:** a fonte relata atualização monetária para dezembro de 2018, enquanto a MIP utilizada está a preços de 2015. Falta reconciliar os denominadores dos coeficientes com esses valores monetários.
3. **Cobertura e alocação:** não foram recuperados os numeradores físicos e os procedimentos completos de atribuição aos setores; a documentação da fonte também apresenta descrições divergentes sobre uso da terra.

O fechamento das contas e os testes do filtro não resolvem essas questões. Os resultados continuam sendo um cenário exploratório, condição já declarada na introdução aprovada e na seção de dados. Isso permite avaliar a aplicação metodológica e a interpretação do cenário, mas não certifica os volumes e as posições como um inventário observado e validado do Brasil de 2015. A força das conclusões empíricas deve ser avaliada na leitura crítica. Reconstruir ou substituir a extensão ambiental não foi solicitado nesta passagem. A [auditoria](../docs/auditoria_coeficientes_emissoes_2015.md) documenta a investigação anterior; seus outros objetos e notações não substituem os da entrega atual.

## Aprofundamento anterior em 28/10/2026 (histórico)

Na primeira etapa da retomada, o usuário autorizou aprofundar as análises existentes e revisar resultados e discussão, preservando a introdução e criando backup antes da reescrita. O objetivo acordado é um bom artigo acadêmico para a disciplina de redes, seguindo as diretrizes qualitativas do AGENTS, com valor metodológico para a dissertação. O diálogo se concentra na explicação das diferenças entre as contas, sem acrescentar um teste da hipótese da dissertação.

- **Base preservada:** revisão local de 28/10; não foi restaurada a versão antiga. A introdução mantém o SHA-256 registrado neste documento. Entradas, células de código anteriores, matrizes e especificação do filtro permanecem intactas, assim como as nove figuras existentes.
- **Aprofundamento implementado:** seção 25 do notebook, com cinco perfis completos (saídas de energia e água/resíduos, entradas de construção e as direções inversas de energia e construção), posição dos casos no conjunto, composição das contrapartes e sensibilidade das interpretações nos três parâmetros. As cinco novas células foram executadas. As saídas estão no notebook; cinco tabelas CSV sem arredondamento são reproduzíveis em `outputs/entrega_redes_2015/aprofundamento/`, pasta ignorada pelo Git.
- **Texto revisado:** resultados desenvolvem volume, concentração, composição e importância local nas duas extremidades. Foram acrescentadas a tabela das contrapartes completas e a sensibilidade dos casos no anexo. A discussão explicita o ganho da análise de redes para interpretar as contas e seu aproveitamento em SC/2018. Resumo e conclusão foram alinhados; a metodologia recebeu apenas a descrição do detalhamento dos perfis.
- **Evidências centrais:** cinco maiores destinos reúnem 40,45% das saídas de energia e 52,35% das de água/resíduos; administração pública representa 27,22% do segundo perfil. As cinco maiores origens somam 38,71% das entradas externas da construção. Produtos de metal → construção representa 32,57% das saídas externas da origem e 4,42% das entradas externas do destino. Energia → construção permanece pelos dois testes nos três parâmetros; água/resíduos → construção é omitida em alfa 0,01.
- **Verificações:** executadas as células do núcleo numérico até a avaliação do filtro e as cinco células novas, com verificações de conservação e preservação das matrizes; passaram os 12 testes de `test_indicadores_entrega.py`. Conferidas as 325 relações dos perfis, sua concentração e fechamento, a transcrição da tabela de contrapartes, as chaves bibliográficas e as referências internas. LaTeX/Biber compilados com sucesso; PDF de 27 páginas inspecionado visualmente, sem alertas de referências ou caixas excedentes no log final. As células de desenho e exportação das figuras anteriores não foram reexecutadas.
- **Backup anterior à reescrita:** `entrega/backup/aprofundamento_redes_20261028_142940142/`, contendo os fontes afetados, notebook, PDF anterior, este handover anterior à atualização e hash da introdução.

As recomendações e o estado descritos nas seções seguintes são históricos e devem ser lidos à luz desta atualização. A comparação com fornecedores e a recuperação da figura completa de F não foram incorporadas. A validade ambiental permanece pendente conforme a seção de dados; a revisão não resolveu essa limitação. As alterações desta retomada ainda dependem da leitura pessoal do usuário; não equivalem à aprovação da redação revista.

## Retomada

1. Ler o `AGENTS.md` da raiz e o [AGENTS.md da entrega](entrega/AGENTS.md).
2. Usar como ponto de partida o [artigo atual](entrega/main.tex), o [notebook da entrega](analise_redes_2015.ipynb) e este registro. O [planejamento anterior](02_planejamento_academico.md) contém decisões e questões históricas; conferir seu estado contra a implementação e o texto atuais.
3. Preservar a introdução. O último escopo de revisão do artigo excluía alterações nela. Sua integridade está registrada abaixo.
4. Distinguir as recomendações desta avaliação das mudanças já autorizadas e executadas. Não recuperar automaticamente a versão antiga nem acrescentar indicadores só porque existem no histórico.
5. A leitura crítica e sua implementação estão registradas no início deste handover. Aguardar a avaliação do usuário sobre a nova redação antes de presumir aprovação ou ampliar o escopo.

## Contexto acadêmico e fontes

O trabalho é para a disciplina **Desigualdade, Diversidade e Redes**, CNM410028, PPGEco/UFSC, professor Dominik Hartmann, 2026.2. O usuário quer relacionar o conteúdo da disciplina ao projeto de dissertação.

O plano preliminar consultado está no repositório irmão `Mestrado`, em `Redes/0 Desigualdade, Diversidade, Redes - Plano de ensino preliminar.pdf`. Neste computador, o caminho é `C:/GitHub/Mestrado/Redes/0 Desigualdade, Diversidade, Redes - Plano de ensino preliminar.pdf`. O plano permite um trabalho empírico próprio no terceiro eixo do projeto aplicado e inclui análise de redes e medidas de diversidade. O projeto e o seminário final correspondem, conjuntamente, a 40% da nota. Não foi encontrada nesse plano uma exigência de centralidades específicas nem um limite de 2.500 palavras. Orientações posteriores do professor podem existir; não transformar a ausência no plano preliminar em confirmação de ausência de requisitos posteriores.

As instruções do professor em `Mestrado/Redes/Critica Construtiva/instruções do professor.txt` destacam tópico e relevância, questão específica, dados e métodos, resultados e implicações políticas; também pedem clareza, figuras bem utilizadas e críticas que indiquem melhorias. O arquivo vizinho `criterios.txt` contém comentários de avaliação de outro trabalho: não tratar suas observações particulares, por exemplo sobre impacto causal, como exigência universal desta entrega.

A introdução atual da dissertação foi conferida em `Mestrado/0-Projeto de Dissertação/secoes/01_introdução.tex`. A pergunta é como as emissões geradas em **Santa Catarina em 2018** se distribuem entre setores sob atribuição pela produção e pela demanda. O projeto prevê a MIP estadual de 74 atividades. O artigo da disciplina usa o **Brasil em 2015**, com 67 atividades, como aplicação exploratória. A transferência útil é metodológica; resultados nacionais não devem ser transportados para SC.

O plano de ensino, a dissertação e os livros indicados no AGENTS estão no repositório irmão. O push de `Redes` não transfere eventuais alterações não sincronizadas de `Mestrado`. Localizar esses documentos pela estrutura relativa e pelos títulos se a raiz dos repositórios for diferente no outro computador.

## Avaliação de mérito anterior ao aprofundamento (histórico)

**Julgamento:** a aplicação é pertinente à disciplina, tem contribuição descritiva identificável e liga-se de forma consistente à dissertação. A interpretação econômica pode ser fortalecida. A validade ambiental é a principal limitação para sustentar conclusões empíricas sobre o Brasil. Esse julgamento não equivale a uma previsão de nota ou a uma validação dos coeficientes.

A dissertação compara duas distribuições setoriais. O artigo investiga as contrapartes e a concentração das relações que compõem essas distribuições. Essa é uma contribuição complementar: identificar as origens emissoras, os produtos finais associados e a repartição dos volumes entre eles.

### Pontos fortes

- A rede tem interpretação econômica explícita: atividades como nós e atribuições entre origem emissora e produto final como arestas.
- As medidas cumprem funções distintas: forças para volume; número efetivo para concentração; filtro para relações destacadas sob seu modelo nulo; graus e cobertura para avaliar a seleção.
- Os casos tornam os contrastes concretos. Energia e água/resíduos têm volumes externos próximos com concentrações diferentes. Energia e construção ilustram papéis distintos como origem e destino.
- O tratamento de redes ponderadas e da concentração dos perfis fornece ligação substantiva com os conteúdos da disciplina. Acrescentar intermediação, proximidade ou comunidades apenas para ampliar a lista de técnicas não é necessário.
- A interpretação distingue atribuição contábil, causalidade física e responsabilidade normativa, além de reconhecer os limites da base.

### Questões a melhorar

| Questão | Diagnóstico e consequência |
| --- | --- |
| Contribuição analítica | Está diluída entre explicações do procedimento. Destacar o que a identificação das contrapartes acrescenta aos totais e saldos. |
| Resultados esperados pelo desenho | Conservação dos totais, elevada conectividade após requisitos indiretos e redução das ligações pelo filtro são propriedades ou consequências esperadas. Explicá-las sem apresentá-las como a principal descoberta empírica. |
| Interpretação econômica | Os casos demonstram bem as medidas, mas ainda explicam pouco por que os perfis diferem. Relacionar os contrastes observados à composição das atribuições, respeitando a evidência disponível. |
| Coordenação da mitigação | Os resultados indicam relações a investigar conjuntamente. Não demonstram ganhos de coordenação, capacidade de intervenção, custos ou eficácia de instrumentos. |
| Base ambiental | As limitações de cobertura, alocação e preços afetam volumes, comparações setoriais e parte da estrutura ponderada. O caráter exploratório é uma restrição substantiva. |

Uma aplicação exploratória bem delimitada pode ter mérito como trabalho da disciplina. A [auditoria ambiental](../docs/auditoria_coeficientes_emissoes_2015.md) continua relevante para avaliar a força das afirmações empíricas. Sua análise histórica usa também outros objetos e notações; não importar automaticamente seu desenho antigo para a entrega atual. Os balanços internos e a sensibilidade do filtro não validam os volumes físicos.

## O que recuperar da versão antiga

O usuário esclareceu que a versão anteriormente no GitHub era uma tentativa própria, esquecida, de realizar uma revisão semelhante à de hoje. Ela não corresponde a uma nova base empírica: mantém o núcleo dos cálculos e acrescenta uma comparação de fornecedores e alternativas de apresentação.

### Comparação com fornecedores

A versão antiga calcula `q_i = soma de L_ij para j diferente de i`, em que `L` é a inversa de Leontief. O indicador soma os requerimentos de produção da atividade `i` associados à mesma demanda monetária unitária em cada um dos outros produtos finais. Exclui a diagonal inteira e independe das intensidades ambientais e da demanda final observada.

A comparação pode distinguir requerimentos produtivos padronizados de participação nas contas ambientais. Seu alcance precisa ficar claro:

- A soma mede volume de requerimentos padronizados, sem distinguir sua concentração entre destinos. Não conta clientes nem mede insubstituibilidade.
- A comparação com as contas ambientais muda simultaneamente a intensidade ambiental e a ponderação pela demanda observada. Diferenças de posição não isolam o efeito da estrutura produtiva.
- O cálculo de `q` independe dos coeficientes ambientais; isso não valida a coordenada ambiental nem os contrastes conjuntos.
- A designação “presença como fornecedor” exige definição operacional. Não a tratar como centralidade causal ou importância econômica geral.

**Recomendação registrada:** análise complementar interessante, mas ainda insuficientemente integrada à pergunta atual para ocupar o centro do artigo. Reservá-la para material complementar se sustentar um contraste econômico que os resultados atuais não mostrem. A inclusão não foi decidida nem implementada.

### Prioridades recomendadas

1. Recuperar a apresentação da matriz completa `F`, com as contas nas margens, para ligar as distribuições às relações analisadas.
2. Aproveitar a representação das contrapartes com barras e cobertura, facilitando a comparação dos casos.
3. Fortalcer a interpretação dos resultados existentes, separando identidades contábeis, consequências da seleção e achados específicos do cenário.
4. Avaliar a comparação com fornecedores como complemento, sem acrescentá-la automaticamente ao núcleo.

Essas propostas devem ser conciliadas com o escopo anterior, que preservava todas as figuras existentes. A avaliação não autoriza, por si só, eliminar figuras ou substituir a organização atual. O próximo ganho de qualidade depende da clareza da contribuição, não da quantidade de indicadores.

## Estado do artigo antes do aprofundamento e verificação anterior (histórico)

O arquivo principal é `entrega/main.tex`. A introdução, os dados, a derivação das contas, os resultados e os anexos têm arquivos próprios; os métodos de rede, a discussão e a conclusão também incluem texto no arquivo principal. O artigo já contém resumo e palavras-chave.

A revisão anterior do restante do documento preservou os dados, os cálculos e os critérios da rede. Reduziu redundâncias, acrescentou discussão, conclusão e resumo, e deslocou detalhes de rankings e de motivos de retenção para o anexo existente. A introdução permaneceu preservada. Foram mantidas as nove figuras existentes. A compilação LaTeX/Biber e a inspeção do PDF foram feitas naquela revisão; não representam uma nova execução nesta etapa de documentação.

Última contagem informada por TeXcount, excluindo resumo e anexos: **3.026 palavras de texto**, ou **3.284 incluindo títulos e legendas do corpo**. São convenções de contagem diferentes. A redução não é um critério autônomo de sucesso e não há meta atual de palavras no AGENTS.

SHA-256 histórico da introdução de 28/10/2026, anterior à revisão feita pelo usuário em 29/10:

```text
DCF33337277ADD90448A90D7590F1F76BE3B279415401F891CC6E25FEFE8C082
```

O notebook atual é `entrega_final/analise_redes_2015.ipynb`, relativo à raiz do repositório. Seguir o [README](../README.md) para reprodução e compilação. Não executar novamente a análise numérica por rotina para alterações exclusivamente documentais.

## Histórico do Git e acesso à versão antiga no outro computador

O conflito de sincronização foi resolvido conforme a escolha explícita do usuário: **preservar os arquivos deste computador e guardar a versão antiga para revisão posterior**.

| Commit | Papel |
| --- | --- |
| `dd7ec11` | Base anterior às revisões de 28/10 e à tentativa antiga de revisão. |
| `00972ea8d5c3d69e686f0c4ea0968c99d88489af` | Tentativa antiga que estava no GitHub, datada de 21/10. |
| `f1cc714838e0e7e071781c6b6f6b1b467900c33e` | Versão local revisada em 28/10. |
| `d183a680d28f22b294159cd87f92416769b4f574` | Merge que preservou integralmente a árvore local e manteve os dois históricos. Foi enviado a `origin/main`. |

O registro inicial e seu link no README foram incluídos no commit `0ed1045`. O merge acima não incorporou as análises adicionais da versão antiga à árvore atual. As mudanças posteriores à retomada estão descritas no início deste handover.

A cópia integral da versão antiga ficou **fora do repositório**, no computador de origem da passagem inicial:

```text
C:/GitHub/Redes-1_backup_GitHub_00972ea/repositorio/
C:/GitHub/Redes-1_backup_GitHub_00972ea/versao_online.zip
```

Essa pasta não é transferida pelo push. A versão antiga, entretanto, permanece no histórico compartilhado e pode ser [consultada no GitHub](https://github.com/G-Cintra/Redes/tree/00972ea8d5c3d69e686f0c4ea0968c99d88489af). Para extraí-la no outro computador sem substituir os arquivos atuais, executar da raiz do clone, escolhendo um nome de saída ainda inexistente:

```powershell
git archive --format=zip --output=../Redes_versao_antiga_00972ea.zip 00972ea8d5c3d69e686f0c4ea0968c99d88489af
```

Arquivos de interesse nesse commit, todos com caminhos relativos à raiz:

- `entrega_final/analise_redes_2015.ipynb`: inclui as etapas adicionais de comparação e apresentação.
- `entrega_final/comparacao_fornecedor.csv`: resultados da comparação com fornecedores.
- `entrega_final/entrega/figuras/artigo_matriz_F.pdf`: matriz completa e margens.
- `entrega_final/entrega/figuras/emissao_presenca_fornecedor.pdf`: comparação adicional.
- `entrega_final/entrega/figuras/artigo_relacoes_combinada.pdf`: relações focais e barras.
- `entrega_final/entrega/comparacao_figura4.pdf`: alternativas de apresentação dos casos.

Consultar essa versão como material de comparação. Suas instruções históricas não substituem o AGENTS atual nem as decisões posteriores do usuário.

## Escopo da passagem inicial (histórico, anterior à retomada)

Na passagem inicial, foram solicitados o registro da análise, o handover e sua sincronização, sem implementação das recomendações acadêmicas. Naquela etapa, o artigo, a introdução, os cálculos, os dados e as figuras permaneceram inalterados. O aprofundamento e a revisão foram posteriormente autorizados e executados conforme o registro no início deste documento; a introdução continua preservada. Esta seção registra o escopo antigo e não impede as mudanças já solicitadas pelo usuário na retomada.
