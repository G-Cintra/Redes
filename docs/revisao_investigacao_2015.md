# Revisão independente: emissões e rede produtiva brasileira, 2015

Este roteiro permite avaliar a investigação pelo repositório público, sem acesso ao ambiente local de quem a produziu. A revisão deve testar criticamente os resultados, sem procurar confirmar a hipótese inicial.

**Fechamento posterior:** a [especificação acadêmica final](especificacao_final_pesquisa_2015.md) fixa o argumento para a redação, sem alterar os cálculos anteriores. Mantém S como principal e L como robustez; A contrasta vínculos diretos. HEM absoluta e por unidade de produção passam a complemento com estimandos distintos, preservando a divergência observada. A revisão do texto final deve usar essa delimitação, sem perder o registro das etapas abaixo.

## Material principal

1. [Notebook executado](../investigacao_redes_emissoes_2015.ipynb): construção das matrizes, definições, cálculos e verificações.
2. [Relatório acadêmico autocontido](../outputs/investigacao_redes_2015/relatorio.html): 15 seções, literatura, resultados, limitações e perguntas candidatas. O GitHub exibe o código HTML; use **Download raw file** e abra o arquivo em um navegador para ler a apresentação completa. Figuras e tabelas estão incorporadas, sem dependência de internet.
3. [Resultados em CSV e figuras](../outputs/investigacao_redes_2015/): material inspecionável sem executar o notebook.
4. [Manifesto das entradas](../raw/manifesto.csv), [proveniência da execução](../outputs/investigacao_redes_2015/reproducibilidade.json) e [auditoria numérica](../outputs/investigacao_redes_2015/auditoria.csv).
5. [Testes dos cálculos exploratórios](../tests/test_investigacao_2015.py) e [testes de consistência da contabilidade](../tests/test_consistencia.py).

As saídas publicadas são um registro da execução, não dados independentes que confirmam o modelo. Para citar ou revisar uma versão estável, registre o SHA do commit consultado.

## Pergunta e notação

Pergunta inicial: as emissões se concentram em poucos setores dos quais o restante da economia depende direta ou indiretamente?

O notebook distingue emissão própria, tamanho econômico, posição de fornecedor, composição ambiental da cadeia e dispersão dos destinos. Há uma ambiguidade histórica de `C/c` entre notebooks anteriores; use estas definições na revisão:

- `Z[i,j]`: fornecimento intermediário nacional do setor i ao comprador j, em R$ milhões.
- `A = Z diag(x)^(-1)` e `L = (I-A)^(-1)`.
- `gamma`: intensidade direta, em Gg CO₂/R$ milhão; `e = gamma * x`: emissão própria.
- `H = diag(gamma) L`: intensidade incorporada por origem emissora e destino final.
- `P = H diag(y)`: atribuição em volume, incluindo a produção doméstica destinada às exportações; `P 1 = e`.
- `S[i,j] = L[i,j] / sum_k L[k,j]`: participação nos requerimentos monetários brutos da cadeia, não no valor adicionado ou preço final.
- `R[i,j] = H[i,j] / sum_k H[k,j]`: participação ambiental, não essencialidade econômica.

## Pontos que merecem contestação

1. **Validade dos dados ambientais:** coeficientes arredondados de 2011/2018 são interpolados para 2015. A base monetária da fonte e a MIP não foram harmonizadas definitivamente. Avalie a correspondência setorial e a plausibilidade dos coeficientes, especialmente água/resíduos e serviços. O objeto é CO₂, não todos os GEE, nem um inventário observado de 2015.
2. **Concentração:** confira top-k, Lorenz, Gini, HHI e comparação com produção. A afirmação de menor concentração não é universal: o HHI pode inverter no cenário com intensidades de 2018.
3. **Interpretação das redes:** confira direção, denominadores, tratamento da diagonal, demanda final e fronteira doméstica. P já incorpora encadeamentos; não representa transações adjacentes nem fluxos físicos conservados de carbono.
4. **Escolha do resultado principal:** avalie se a média de S é defensável como posição de fornecedor e se as comparações com L, A e mediana realmente sustentam essa escolha. Os destinos têm igual peso por convenção; a agregação a 67 atividades importa.
5. **Dependência matemática:** a intensidade cancela na distribuição dos destinos por linha; Katz com demanda final reproduz x; PageRank reverso de A e Z coincide. Correlação entre e e R compartilha a intensidade. Não contar essas identidades como validações independentes.
6. **Escala e associação:** confira Pearson, Spearman e correlação parcial de postos. Controle de tamanho não identifica causalidade. Os setores não formam uma amostra IID.
7. **Importância sistêmica:** as extrações de demanda e alocação são contrafactuais diferentes, não previsões de ruptura real. Distâncias geodésicas, passeios aleatórios e teletransporte exigem hipóteses adicionais.
8. **Robustez e seleção:** avalie cenários de coeficientes, arredondamento, exclusão de observações, normalizações e resultados fracos. Perturbações uniformes não são intervalos de confiança. Identifique qualquer seleção favorável de métricas, literatura ou setores.

## Reprodução

Clone o repositório, prepare Python com as dependências de [requirements.txt](../requirements.txt) e execute todas as células de `investigacao_redes_emissoes_2015.ipynb` a partir da raiz. As versões efetivamente usadas estão no JSON de proveniência; diferenças em relação às versões declaradas devem ser consideradas na revisão.

As entradas brutas estão em `raw/`. A matriz P e o catálogo setorial canônicos em `outputs/` também estão versionados, pois o notebook compara sua reconstrução com esses arquivos por hash. Não é necessário executar os notebooks antigos para obter essas duas entradas nesta versão pública.

Verificações específicas:

```shell
python -m unittest discover -s tests -p test_investigacao_2015.py -v
python -m unittest discover -s tests -p test_consistencia.py -v
python -m unittest discover -s tests -p test_concentracao_dependencia.py -v
```

A execução do notebook regrava sua pasta de resultados. Compare os números com os CSVs publicados; diferenças gráficas ou de serialização entre versões de bibliotecas não equivalem necessariamente a diferenças analíticas.

## Pedido ao revisor

Produza um parecer independente com:

- erros de dados, implementação ou interpretação, classificados por gravidade;
- resultados reproduzidos e resultados não reproduzidos, com evidência e localização no código;
- conclusões robustas, frágeis e não sustentadas;
- avaliação da literatura e de alternativas metodológicas que poderiam mudar a conclusão;
- julgamento da pergunta recomendada e eventual formulação melhor;
- correções indispensáveis antes de usar o estudo em dissertação ou artigo.

Separe claramente erro demonstrado, dúvida metodológica e sugestão de ampliação. Não aceite a narrativa do relatório como evidência de sua própria validade.

## Validação focal posterior

O [notebook de validação adversarial](../validacao_emissao_centralidade_2015.ipynb) testa especificamente a interpretação emissão própria × presença como fornecedor, usando S, A, L e uma definição de HEM. O [novo relatório](../outputs/validacao_emissao_centralidade_2015/relatorio.html) contém duas figuras e uma tabela principais, com os demais diagnósticos no suplemento.

Essa etapa qualifica a narrativa anterior: Energia e Comércio se destacam em A/L/S, mas sua posição não é invariável à normalização da extração. Na revisão, examine especialmente a diferença entre HEM externa absoluta e por unidade de output, sem tratar uma como substituta silenciosa da outra. Os [testes específicos](../tests/test_validacao_centralidade.py) verificam direção da extração, efeito próprio, normalização, Pareto e correlação parcial. O exercício continua sendo validação interna da mesma base, não confirmação independente.
