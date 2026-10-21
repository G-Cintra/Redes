# Entrega final — leitura e continuidade

Atualizado em 21/10/2026. Este é o ponto de entrada para retomar o trabalho.

## Para o autor ler e revisar

- **[ARTIGO_PARA_REVISAO.pdf](ARTIGO_PARA_REVISAO.pdf)** — cópia de acesso rápido, na raiz do repositório, do PDF vigente.
- [Fonte principal](entrega_final/entrega/main.tex) e [PDF na pasta de compilação](entrega_final/entrega/main.pdf).
- [Registro de aceitação por Nikolov e contagem por seção](entrega_final/revisao_artigo_nikolov.md).
- [Comparação das três versões da Figura 4](entrega_final/entrega/comparacao_figura4.pdf) — histórico de alternativas; a escolha vigente é **C**.

O artigo tem quatro figuras centrais (Figura 1: matriz nacional F com totais marginais; exemplos didáticos apenas no apêndice), resumo, introdução, dados/método, resultados, discussão e conclusão. Detalhes de derivação, filtro, sensibilidade, matrizes, vistas globais, painéis integrais e códigos estão nos apêndices. A contagem editorial é **2.018 palavras de prosa, incluindo o resumo**, com limite de 2.500; títulos, legendas, fórmulas, comandos de citação, referências e apêndices são excluídos. Há margem para diferenças de contagem.

## Decisões do autor que permanecem vigentes

1. Contar a história de que magnitude emissora, presença como fornecedor e papel na atribuição pela demanda são dimensões distintas; as relações ajudam a identificar conjuntos de atividades a investigar para mitigação.
2. Manter a MIP nacional de 2015, 67 atividades e os coeficientes aproximados por interpolação de Sanguinet/Azzoni. Explicar as limitações brevemente, sem transformar a reconstrução do inventário em pré-condição para a entrega da disciplina de redes.
3. Usar Nikolov (2023) como critério de exposição: pergunta e achados antecipados, contribuição delimitada, parágrafos focados, figuras compreensíveis e conclusões proporcionais. Não impor identificação causal a este estudo descritivo.
4. **Figura 4: opção C por ora**, combinando redes focais completas do backbone com barras das saídas de energia e entradas de construção. Os nós centrais foram ampliados de 450 para 1.500 pontos quadrados para os códigos caberem. O afastamento das setas considera o tamanho de cada nó. Isso não altera indicadores ou pesos.
5. O autor retirou o exemplo didático do corpo. A Figura 1 deve ser a matriz F completa de 67 × 67, sem filtro, com diagonal, cores logarítmicas, margens lineares de produção e demanda. Não recolocar o esquema didático entre as quatro figuras centrais.
6. As quatro figuras do corpo devem compartilhar páginas com o texto, em orientação retrato, sem quebras obrigatórias ou páginas exclusivas de figura. Os apêndices mantêm suas páginas detalhadas, inclusive horizontais.
7. Preservar históricos e não incorporar automaticamente árvores máximas, centralidades antigas, similaridades, satélite ou regionalização ao artigo.

## O que está pronto e o que falta

A reescrita e as figuras estão prontas para **leitura e revisão pelo autor**. Não tratar a versão como aprovada para envio ao professor. A opção C já está incorporada; não voltar a perguntar qual alternativa usar sem uma nova indicação do autor. Não há pedido de envio, publicação, commit ou push.

No próximo trabalho, partir dos comentários de leitura do autor. Eventuais ajustes devem preservar a definição das contas e a distinção entre rede completa e backbone. Evitar expandir novamente a exposição para um catálogo de métodos. O corpo pode receber ajustes dentro da margem de palavras; o texto não precisa atingir exatamente 2.500.

## Reprodução e verificação

- Ambiente: `.venv` deste repositório. Notebook: [entrega_final/analise_redes_2015.ipynb](entrega_final/analise_redes_2015.ipynb).
- Seções 1–18: dados, contas, indicadores e backbone. Seções 19–24: explorações/figuras detalhadas. Seção 25: comparação entre presença como fornecedor e contas ambientais. **Seção 26, célula `artigo-figuras`: geração das figuras do artigo**, incluindo tamanho dos nós centrais e alternativas A/B/C. **Seção 27, célula `panorama-F`: matriz F com margens**, exportando também `matriz_F_artigo.csv` e `margens_F_artigo.csv`. Não corrigir só os PDFs: mudar a célula e regenerar.
- O texto da Figura 4 está em `entrega_final/entrega/resultados.tex`; a figura incluída é `figuras/artigo_relacoes_combinada.pdf`. A legenda distingue os dois grafos das duas barras e seus universos.
- Execute o notebook em ordem para reprodução integral. Nesta revisão foram executadas as seções analíticas 1–18 e as células de figuras 26/27 em suas respectivas revisões; não foi alegada nova execução de todas as explorações históricas. As verificações conferem F/W/backbone preservados, quatro perfis fechados e conjuntos exatos de arestas incidentes.
- Compilar em `entrega_final/entrega/`: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. Para o caderno comparativo, compilar `comparacao_figura4.tex`.
- **Após recompilar, atualizar a cópia de leitura na raiz:** `Copy-Item -LiteralPath entrega_final/entrega/main.pdf -Destination ARTIGO_PARA_REVISAO.pdf -Force`. Os dois PDFs devem ser idênticos.
- Contagem da raiz: `python entrega_final/contar_palavras.py` (TeXcount). Exporta [contagem_palavras.json](entrega_final/contagem_palavras.json), com hashes dos fontes e totais.
- A revisão do artigo passou pelos **62 testes** de `python -m unittest discover -s tests`. O ajuste posterior de nó é visual; as verificações de conservação foram reexecutadas. PDFs compilados e conferidos visualmente.

## Cuidados para o próximo agente

O repositório relevante é **`C:/Users/acarm/GitHub/Redes`**, não a pasta `C:/Users/acarm/GitHub/Mestrado/Redes` inicialmente aberta no chat. Leia o `AGENTS.md` da raiz correta. Existem muitas alterações e arquivos novos ainda **sem commit**, pertencentes ao trabalho desta conversa. Não restaurar, apagar ou sobrescrever esse conjunto como se fosse sujeira de execução.

O resumo entregue anteriormente está em `relatorio/Gabriel_Cintra_-_Resumo_v2.pdf`. Ele é um marco histórico, não a versão atual. O planejamento em `entrega_final/02_planejamento_academico.md` também contém propostas históricas; priorizar o texto atual, este handover e as instruções mais recentes do autor.
