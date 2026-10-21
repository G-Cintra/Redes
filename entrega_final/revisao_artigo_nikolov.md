# Revisão do artigo e aceitação editorial

Revisão de 21/10/2026. O artigo ativo é `entrega/main.tex`; o PDF inclui corpo, referências e apêndices. A versão anterior foi condensada sem alterar entradas, coeficientes, F, W ou backbone. A derivação foi deslocada para `entrega/metodologia_detalhada.tex`; matrizes, sensibilidade, vistas globais, painéis integrais e códigos permanecem nos apêndices.

## História e montagem

Magnitude emissora, presença como fornecedor e papel na atribuição pela demanda são dimensões distintas. A exposição parte dessa diferença, examina volume e concentração, identifica contrapartes de energia e construção e discute conjuntos de atividades a investigar para mitigação.

As quatro figuras do corpo mostram: (1) panorama nacional da matriz F completa e suas margens por produção e demanda; (2) presença como fornecedor versus as contas de produção e demanda; (3) volume, número efetivo e cobertura; (4) redes focais e barras dos sentidos predominantes de energia e construção. O exemplo didático de quatro atividades permanece apenas no apêndice metodológico. O esquema simplificado de três atividades foi retirado do corpo; seu arquivo e sua geração são preservados como histórico. A matriz nacional da Figura 1 usa 4.489 células, incluindo diagonal, com zeros em cinza e cores logarítmicas para pesos positivos. As barras marginais têm escala linear de mesma amplitude e foram conferidas com as duas contas.

A Figura 4 usa **a opção C, redes focais e barras**, escolhida pelo autor por ora. Os nós centrais foram ampliados para acomodar os códigos sem alterar pesos ou métricas. O caderno `entrega/comparacao_figura4.pdf` apresenta, em três páginas A4 horizontais comparáveis, barras, redes focais e combinação. A escolha vigente é C; as outras opções permanecem para referência. As três opções usam os mesmos pesos e backbone. Os grafos preservam todas as relações incidentes; as barras fecham os perfis representados. A opção C apresenta os dois grafos e as barras dos sentidos predominantes: saídas de energia e entradas de construção.

## Contagem reproduzível

Comando da raiz: `python entrega_final/contar_palavras.py` (requer TeXcount). O script exporta `contagem_palavras.json`, com contagem por fonte e SHA-256.

| Parte | Palavras de prosa |
| --- | ---: |
| Resumo | 112 |
| Introdução | 272 |
| Dados e método | 374 |
| Resultados | 762 |
| Discussão | 374 |
| Conclusão | 124 |
| **Total, incluindo resumo** | **2.018** |

Usa-se o campo `Words in text` do TeXcount. Excluem-se títulos, blocos completos de figuras/legendas/notas marcados com `%TC:ignore`, fórmulas, comandos de citação, referências e apêndices. Fórmulas inline são registradas pelo TeXcount separadamente e não contam como palavras de prosa. O limite de 2.500 deixa 482 palavras de margem para diferenças editoriais de tokenização e contagem das citações. Os orçamentos do plano eram tetos de orientação, não metas a preencher com texto adicional.

## Aceitação baseada em Nikolov

Referência editorial: Plamen Nikolov (2023), *Writing Tips for Crafting Effective Economics Research Papers*, IZA DP 16276, especialmente seções I, IV–VIII e X–XIII. Texto local consultado: `C:/Users/acarm/GitHub/Mestrado/outputs/Nikolov (2023)_extraido.txt`. A tabela operacionaliza as recomendações para este estudo; não constitui certificação científica nem uma rubrica numérica do autor. As recomendações de identificação causal não são impostas ao desenho descritivo.

| Critério | Evidência verificável na versão entregue | Pendência |
| --- | --- | --- |
| Pergunta antecipada | Primeiro parágrafo da introdução identifica recorte, duas contas e organização relacional. | Nenhuma editorial. |
| Contribuição delimitada | Terceiro parágrafo situa Miller/Blair, Sanguinet/Azzoni e Huang; contribuição como leitura conjunta, sem nova centralidade. | Nenhuma editorial. |
| Resultados antecipados | Resumo informa densidade qualitativa, casos e cobertura; segundo parágrafo da introdução antecipa os perfis. | Nenhuma editorial. |
| Parágrafos focados | Aberturas enunciam um resultado ou argumento; demais frases definem, sustentam ou limitam essa ideia. | Nenhuma identificada na revisão. |
| Concisão | 2.018 palavras de prosa; remoção de promessas e catálogo de procedimentos; detalhes auditáveis nos apêndices. | Nenhuma editorial. |
| Precisão | F, c/u, W, q, forças, D₂ e cobertura definidos antes dos resultados; conservação declarada como identidade. | Incerteza ambiental permanece explicitamente documentada. |
| Evidência visual | Cada figura é chamada pelo argumento correspondente e recebe interpretação econômica. | Opção C escolhida pelo autor; revisão de leitura permanece aberta. |
| Autonomia visual | Legendas informam universo, direção, unidades, diagonal, seleção e cobertura; grafos têm códigos e escala de pesos, com chave setorial no apêndice. | Nenhuma para a montagem com a opção C. |
| Conclusões proporcionais | Discussão distingue diagnóstico de avaliação de políticas, insubstituibilidade e incerteza dos coeficientes. | Validação ambiental adicional exigida apenas para extrapolações físicas definitivas. |
| Fechamento | Conclusão responde à pergunta com resultados já apresentados e delimita o aproveitamento do procedimento. | Nenhuma editorial. |

## Verificação computacional e visual

- Executadas as células analíticas das seções 1–18 e as seções gráficas 26/27 em suas respectivas revisões para produzir e conferir os gráficos. A seção 27 gera a matriz nacional e as margens, executadas após as seções 1–5. As demais células históricas e seus outputs foram preservados; não se alega uma nova execução integral de todas as explorações.
- Matriz da Figura 1 conferida célula a célula: 4.489 valores, 132 zeros, diagonal preservada; margens iguais às contas de produção e demanda, com total conservado.
- Conservação exata de F, W e backbone durante a exportação; 4.290 arestas na rede externa e 575 no backbone de referência.
- Mesmo conjunto de 12 atividades do quadro anterior, sem nova seleção analítica.
- Em cada um dos quatro perfis, soma das seis maiores relações mais 60 restantes igual ao volume completo e ao retido, com checagem numérica. Zeros são mantidos no grupo restante.
- Cada grafo focal contém exatamente todas as arestas incidentes do backbone. Arestas compartilhadas aparecem nos dois recortes, sem soma para gerar totais globais.
- As versões combinadas reutilizam as mesmas tabelas e grafos; as espessuras usam escala comum e legendas em Gg de CO₂.
- Os 62 testes de `python -m unittest discover -s tests` passaram. As verificações são computacionais, não validam um inventário físico.
- PDFs compilados com LaTeX/Biber e conferidos visualmente, com as quatro figuras centrais intercaladas ao texto em páginas retrato (páginas 3–6), conforme a preferência mais recente do autor. As páginas horizontais são mantidas apenas nos apêndices. Sem referências indefinidas ou caixas excedendo margens nos logs finais.

A data do cabeçalho corresponde à revisão de 21/10/2026. Não é uma confirmação de prazo oficial da disciplina.
