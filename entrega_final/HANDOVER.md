# Handover da entrega e avaliação de mérito

Registro de 28/10/2026 para continuar o trabalho em outro computador. O usuário solicitou registrar a avaliação acadêmica, preparar este handover e fazer commit e push. A avaliação abaixo não foi implementada no artigo. A versão local revisada em 28/10 permanece a versão de referência.

## Retomada

1. Ler o `AGENTS.md` da raiz e o [AGENTS.md da entrega](entrega/AGENTS.md).
2. Usar como ponto de partida o [artigo atual](entrega/main.tex), o [notebook da entrega](analise_redes_2015.ipynb) e este registro. O [planejamento anterior](02_planejamento_academico.md) contém decisões e questões históricas; conferir seu estado contra a implementação e o texto atuais.
3. Preservar a introdução. O último escopo de revisão do artigo excluía alterações nela. Sua integridade está registrada abaixo.
4. Distinguir as recomendações desta avaliação das mudanças já autorizadas e executadas. Não recuperar automaticamente a versão antiga nem acrescentar indicadores só porque existem no histórico.
5. Na próxima revisão substantiva, priorizar o que a análise das relações permite compreender além da comparação das distribuições pela produção e pela demanda.

## Contexto acadêmico e fontes

O trabalho é para a disciplina **Desigualdade, Diversidade e Redes**, CNM410028, PPGEco/UFSC, professor Dominik Hartmann, 2026.2. O usuário quer relacionar o conteúdo da disciplina ao projeto de dissertação.

O plano preliminar consultado está no repositório irmão `Mestrado`, em `Redes/0 Desigualdade, Diversidade, Redes - Plano de ensino preliminar.pdf`. Neste computador, o caminho é `C:/GitHub/Mestrado/Redes/0 Desigualdade, Diversidade, Redes - Plano de ensino preliminar.pdf`. O plano permite um trabalho empírico próprio no terceiro eixo do projeto aplicado e inclui análise de redes e medidas de diversidade. O projeto e o seminário final correspondem, conjuntamente, a 40% da nota. Não foi encontrada nesse plano uma exigência de centralidades específicas nem um limite de 2.500 palavras. Orientações posteriores do professor podem existir; não transformar a ausência no plano preliminar em confirmação de ausência de requisitos posteriores.

As instruções do professor em `Mestrado/Redes/Critica Construtiva/instruções do professor.txt` destacam tópico e relevância, questão específica, dados e métodos, resultados e implicações políticas; também pedem clareza, figuras bem utilizadas e críticas que indiquem melhorias. O arquivo vizinho `criterios.txt` contém comentários de avaliação de outro trabalho: não tratar suas observações particulares, por exemplo sobre impacto causal, como exigência universal desta entrega.

A introdução atual da dissertação foi conferida em `Mestrado/0-Projeto de Dissertação/secoes/01_introdução.tex`. A pergunta é como as emissões geradas em **Santa Catarina em 2018** se distribuem entre setores sob atribuição pela produção e pela demanda. O projeto prevê a MIP estadual de 74 atividades. O artigo da disciplina usa o **Brasil em 2015**, com 67 atividades, como aplicação exploratória. A transferência útil é metodológica; resultados nacionais não devem ser transportados para SC.

O plano de ensino, a dissertação e os livros indicados no AGENTS estão no repositório irmão. O push de `Redes` não transfere eventuais alterações não sincronizadas de `Mestrado`. Localizar esses documentos pela estrutura relativa e pelos títulos se a raiz dos repositórios for diferente no outro computador.

## Avaliação de mérito da versão atual

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

## Estado do artigo e verificação anterior

O arquivo principal é `entrega/main.tex`. A introdução, os dados, a derivação das contas, os resultados e os anexos têm arquivos próprios; os métodos de rede, a discussão e a conclusão também incluem texto no arquivo principal. O artigo já contém resumo e palavras-chave.

A revisão anterior do restante do documento preservou os dados, os cálculos e os critérios da rede. Reduziu redundâncias, acrescentou discussão, conclusão e resumo, e deslocou detalhes de rankings e de motivos de retenção para o anexo existente. A introdução permaneceu preservada. Foram mantidas as nove figuras existentes. A compilação LaTeX/Biber e a inspeção do PDF foram feitas naquela revisão; não representam uma nova execução nesta etapa de documentação.

Última contagem informada por TeXcount, excluindo resumo e anexos: **3.026 palavras de texto**, ou **3.284 incluindo títulos e legendas do corpo**. São convenções de contagem diferentes. A redução não é um critério autônomo de sucesso e não há meta atual de palavras no AGENTS.

SHA-256 da introdução preservada, conferido em 28/10/2026:

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

Este registro e seu link no README serão acrescentados em um novo commit. O merge acima não incorporou as análises adicionais da versão antiga à árvore atual.

A cópia integral da versão antiga ficou **fora do repositório**, neste computador:

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

## Escopo desta passagem de trabalho

Foram solicitados o registro da análise, o handover e sua sincronização. Não foi solicitada a implementação das recomendações acadêmicas. Nesta passagem, o artigo, a introdução, os cálculos, os dados e as figuras devem permanecer inalterados. A documentação concentra o estado necessário à retomada, sem criar novas instruções ou duplicar as regras do AGENTS.
