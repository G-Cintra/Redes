# Redes

Análises da Matriz de Insumo-Produto (MIP) brasileira de 2015, divulgada pelo IBGE.

## Preparação do ambiente

O ambiente virtual local está em `.venv` e inclui `pandas`, `seaborn` e `xlrd` (necessário para ler os arquivos legados `.xls`). Para recriá-lo em Windows:

```powershell
uv venv .venv --python 3.12
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Ative-o, se desejar trabalhar no terminal:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Dados

Os arquivos originais ficam em [`raw/`](raw/README.md). A pasta documenta a origem no IBGE e mantém hashes SHA-256 para detectar qualquer alteração nos arquivos. As funções de leitura e validação ficam em [`scr/arquivos.py`](scr/arquivos.py).

O CSV de coeficientes de Sanguinet e Azzoni também tem seu SHA-256 verificado antes da leitura, usando o [manifesto da referência](references/sanguinet_azzoni_2024/SHA256SUMS). O hash registra a versão atual da transcrição; alterações exigem revisão do conteúdo e atualização explícita do manifesto. O `.gitattributes` preserva os bytes desse CSV para evitar conversão de quebras de linha pelo Git.

## Organização do código

O notebook apresenta a sequência da análise, suas hipóteses e as comparações com o IBGE. As funções reutilizáveis estão divididas por responsabilidade:

| Módulo | Responsabilidade |
| --- | --- |
| [`scr/arquivos.py`](scr/arquivos.py) | Caminhos, checksums e leitura de XLS e CSV, incluindo parâmetros do exterior. |
| [`scr/mip.py`](scr/mip.py) | Extração das tabelas da MIP de 67 atividades e conversão da demanda final de produtos para atividades. |
| [`scr/modelos.py`](scr/modelos.py) | Construção de A, Z, x, Am e dos sistemas de Leontief e Ghosh. |
| [`scr/emissoes.py`](scr/emissoes.py) | Contabilidade de CO₂ por produção, consumo com importações e renda. |
| [`scr/visualizacoes.py`](scr/visualizacoes.py) | Gráficos dos resultados. |
| [`scr/proveniencia.py`](scr/proveniencia.py) | Registro das entradas, versão do código e exportação rastreável. |

Use `from scr import arquivos, mip, modelos, emissoes` e chamadas explícitas como `modelos.calcular_inversa_leontief(A)`. A extração da MIP depende da leitura; os modelos dependem da extração; a contabilidade de emissões recebe matrizes e vetores, sem acessar arquivos. O notebook coordena essas partes.

A separação preserva fórmulas, ordem das operações, unidades, alinhamento setorial e validações. As intensidades de 2011 e 2018 continuam sendo aplicadas à estrutura econômica de 2015; o exterior representativo continua sendo um parâmetro de cenário.

## Proveniência dos outputs

Salve o notebook, reinicie o kernel e execute todas as células na ordem. A seção 1 cria uma `Execucao`; a seção 2 registra em `execucao.entradas` o caminho, a descrição e o SHA-256 de cada uma das quatro entradas, depois de sua leitura e validação. Os parâmetros externos também são verificados contra `parameters/exterior_representativo/SHA256SUMS`.

A exportação salva a tabela setorial de 2018 em CSV, seu gráfico em PNG e um arquivo `contabilidade_co2_2018.proveniencia.json` em `outputs/<execucao_id>/`. Cada execução usa um identificador próprio e não sobrescreve as anteriores. O JSON inclui:

- entradas e hashes; hashes do CSV e do PNG, permitindo conferir o par correto;
- commit Git e estado das alterações locais no início da execução (incluindo arquivos não rastreados);
- conteúdo e hash dos módulos, scripts, requisitos, manifestos de entrada, documentação do cenário e células salvas do notebook;
- data/hora UTC, Python, plataforma e versões das bibliotecas de cálculo e visualização.

O hash do notebook considera o conteúdo das células e ignora outputs e contadores de execução. Assim, alterações nos cálculos ou textos mudam a identificação, mas salvar uma nova saída não a muda. As cópias de código no JSON permitem inspecionar o código local mesmo quando há alterações não commitadas. Os hashes identificam as entradas; os arquivos de dados em si devem continuar preservados no repositório ou no arquivo da pesquisa.

O PNG contém o campo de metadados `Proveniencia`, com fontes, versão e identificador da execução. O CSV mantém seu formato tabular usual: compartilhe-o junto ao JSON. Editores de imagem podem remover metadados; preserve também o JSON ao compartilhar o PNG.

O registro usa os arquivos salvos em disco, não o estado interno do editor. Não captura edições não salvas, módulos antigos no kernel nem alterações manuais de variáveis: por isso, gere resultados finais em um kernel novo. A exportação rejeita mudanças nas entradas ou nas fontes salvas detectadas entre o início e o fim da execução. Quando Git não está disponível, o commit fica `null`, mas os hashes e cópias das fontes continuam registrados.

## Verificação

Execute a partir da raiz do projeto:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes executam as células de cálculo do notebook com os dados reais, verificam as referências do IBGE, os fechamentos econômicos, as contas de emissões e a rejeição de setores desalinhados e arquivos adulterados. O gráfico é gerado em diretório temporário. Os testes não regravam o notebook nem os parâmetros de cenário.

## Referências

Os arquivos de apoio estão organizados por obra em [`references/`](references/README.md).

As referências metodológicas complementares ficam em [`references/fontes_secundarias/`](references/fontes_secundarias/README.md).

- [Miller, Ronald E.; Blair, Peter D. (2009). *Input–Output Analysis: Foundations and Extensions* (2ª ed.)](references/miller_blair_2009/input_output_analysis_foundations_extensions_2ed.pdf). Cambridge University Press. Referência teórica para a construção e análise da matriz de insumo-produto.
- [Montoya, Marco Antonio; Bertussi, Luís Antônio Sleimann; Allegretti, Gabriela; Talamini, Edson (2026). “Brazilian energy and carbon footprints: structural changes and sectoral contributions to climate change”](references/montoya_et_al_2026/brazilian_energy_carbon_footprints.pdf). *Environment, Development and Sustainability*, 28, 6725–6755. https://doi.org/10.1007/s10668-024-05251-8. Referência para a análise de consumo energético e pegada de carbono no Brasil.
- [Sanguinet, Eduardo Rodrigues; Azzoni, Carlos Roberto (2024). “Carbon emissions drivers in Brazilian regional production chains: Value-added and consumption-based approaches”](references/sanguinet_azzoni_2024/carbon_emissions_drivers_brazilian_regional_production_chains.pdf). *Regional Science Policy & Practice*, 16, 100015. https://doi.org/10.1016/j.rspp.2024.100015. Referência para emissões de CO₂, cadeias produtivas regionais e abordagens baseadas em valor adicionado e consumo no Brasil. A [Tabela 2 transcrita em CSV](references/sanguinet_azzoni_2024/coeficientes_co2_2011_2018.csv) contém os coeficientes de intensidade direta de CO₂ de 2011 e 2018, em Gg de CO₂ por R$ milhão de produção bruta. A [tese de doutorado de Sanguinet](references/sanguinet_azzoni_2024/tese_integracion_cadenas_globales_valor_2021.pdf) é incluída como referência metodológica relacionada.
- [Marques, Alexandra; Rodrigues, João; Lenzen, Manfred; Domingos, Tiago (2012). “Income-based environmental responsibility”](references/marques_et_al_2012/income_based_environmental_responsibility.pdf). *Ecological Economics*, 84, 57–65. https://doi.org/10.1016/j.ecolecon.2012.09.010. Referência primária para a responsabilidade ambiental baseada em renda e a perspectiva *downstream*.

## Primeiro notebook

Abra [`analise_matriz_insumo_produto.ipynb`](analise_matriz_insumo_produto.ipynb). Ele valida o checksum e então carrega todas as 15 abas da matriz de nível 67 como DataFrames `pandas`, preservando a estrutura original de cada planilha.
