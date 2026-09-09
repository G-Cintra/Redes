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

Os arquivos originais ficam em [`raw/`](raw/README.md). A pasta documenta a origem no IBGE e mantém hashes SHA-256 para detectar qualquer alteração nos arquivos. As funções de leitura e validação ficam em [`scr/dados.py`](scr/dados.py).

## Referências

Os arquivos de apoio estão organizados por obra em [`references/`](references/README.md).

As referências metodológicas complementares ficam em [`references/fontes_secundarias/`](references/fontes_secundarias/README.md).

- [Miller, Ronald E.; Blair, Peter D. (2009). *Input–Output Analysis: Foundations and Extensions* (2ª ed.)](references/miller_blair_2009/input_output_analysis_foundations_extensions_2ed.pdf). Cambridge University Press. Referência teórica para a construção e análise da matriz de insumo-produto.
- [Montoya, Marco Antonio; Bertussi, Luís Antônio Sleimann; Allegretti, Gabriela; Talamini, Edson (2026). “Brazilian energy and carbon footprints: structural changes and sectoral contributions to climate change”](references/montoya_et_al_2026/brazilian_energy_carbon_footprints.pdf). *Environment, Development and Sustainability*, 28, 6725–6755. https://doi.org/10.1007/s10668-024-05251-8. Referência para a análise de consumo energético e pegada de carbono no Brasil.
- [Sanguinet, Eduardo Rodrigues; Azzoni, Carlos Roberto (2024). “Carbon emissions drivers in Brazilian regional production chains: Value-added and consumption-based approaches”](references/sanguinet_azzoni_2024/carbon_emissions_drivers_brazilian_regional_production_chains.pdf). *Regional Science Policy & Practice*, 16, 100015. https://doi.org/10.1016/j.rspp.2024.100015. Referência para emissões de CO₂, cadeias produtivas regionais e abordagens baseadas em valor adicionado e consumo no Brasil. A [Tabela 2 transcrita em CSV](references/sanguinet_azzoni_2024/coeficientes_co2_2011_2018.csv) contém os coeficientes de intensidade direta de CO₂ de 2011 e 2018, em Gg de CO₂ por R$ milhão de produção bruta. A [tese de doutorado de Sanguinet](references/sanguinet_azzoni_2024/tese_integracion_cadenas_globales_valor_2021.pdf) é incluída como referência metodológica relacionada.
- [Marques, Alexandra; Rodrigues, João; Lenzen, Manfred; Domingos, Tiago (2012). “Income-based environmental responsibility”](references/marques_et_al_2012/income_based_environmental_responsibility.pdf). *Ecological Economics*, 84, 57–65. https://doi.org/10.1016/j.ecolecon.2012.09.010. Referência primária para a responsabilidade ambiental baseada em renda e a perspectiva *downstream*.

## Primeiro notebook

Abra [`analise_matriz_insumo_produto.ipynb`](analise_matriz_insumo_produto.ipynb). Ele valida o checksum e então carrega todas as 15 abas da matriz de nível 67 como DataFrames `pandas`, preservando a estrutura original de cada planilha.
