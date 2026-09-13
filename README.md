# Rede intersetorial de emissões da produção brasileira

> Como se organiza a rede intersetorial de emissões atribuídas à produção brasileira, quais setores ocupam posições mais centrais e de maior alcance, e em que medida os fluxos de emissões se concentram em determinados setores?

Este trabalho parte dessa pergunta para estudar as relações entre 67 setores da economia brasileira, com dados de 2015. A entrega tem como objetivo validar o problema de pesquisa para a disciplina de redes. A preparação das matrizes pela análise insumo-produto está concluída para o recorte adotado. A análise de redes ainda está em estágio exploratório: os indicadores e suas interpretações estão sendo avaliados.

[Explorar os resultados](https://g-cintra.github.io/Redes/)

## Organização do trabalho

- [**Matriz insumo-produto**](analise_matriz_insumo_produto.ipynb): organiza os dados do IBGE e calcula as matrizes de emissões. As hipóteses e as contas ficam explícitas no notebook.
- [**Análise de redes**](analise_redes_emissoes.ipynb): utiliza a matriz de emissões atribuídas à produção brasileira para explorar concentração, centralidade, alcance e dependência entre setores.

As conexões atribuem emissões de um setor produtor à demanda final por bens de outro setor, incluindo efeitos diretos e indiretos e a produção destinada à exportação. Não representam transações diretas entre empresas. O interesse é distinguir quem emite mais, quem distribui suas emissões por mais destinos relevantes e quais destinos dependem fortemente de determinados emissores.

## Exploração inicial

**1. Estrutura da rede.** Cada nó representa um setor. O tamanho indica suas emissões totais; a cor, o número efetivo de destinos; e a espessura das ligações, o peso da atribuição de emissões. A figura mostra as 75 maiores ligações para facilitar a leitura; os indicadores utilizam todas as ligações positivas entre setores. A posição dos nós não tem significado econômico.

[![Rede intersetorial com disposição por forças.](docs/imagens/rede_forcas.png)](docs/imagens/rede_forcas.png)

**2. Concentração dos emissores.** As curvas acumulam a participação dos setores, do maior para o menor emissor. Comparam as emissões totais, incluindo atribuições ao próprio setor, com a parcela atribuída a outros setores.

[![Participação acumulada dos maiores emissores no total e no componente intersetorial.](docs/imagens/concentracao_emissores.png)](docs/imagens/concentracao_emissores.png)

**3. Volume e alcance.** Cada ponto é um setor. O número efetivo de destinos considera como suas atribuições intersetoriais se distribuem: cresce quando os pesos estão menos concentrados em poucos destinos. A cor indica a maior participação desse emissor nas emissões intersetoriais recebidas por um destino. As duas dimensões permitem examinar diferenças que um ranking de emissões, sozinho, não mostra.

[![Emissões totais por setor e número efetivo de destinos.](docs/imagens/volume_alcance.png)](docs/imagens/volume_alcance.png)

As imagens abrem em tamanho completo. A exploração interativa permite identificar os setores e consultar os valores. Estes resultados são preliminares e não demonstram, por si só, o efeito de uma intervenção econômica.

## Referências principais

1. **Miller, R. E.; Blair, P. D. (2009).** [*Input–Output Analysis: Foundations and Extensions*, 2ª ed.](references/miller_blair_2009/input_output_analysis_foundations_extensions_2ed.pdf). Fundamenta a construção e a interpretação das matrizes insumo-produto.
2. **Sanguinet, E. R.; Azzoni, C. R. (2024).** [*Carbon emissions drivers in Brazilian regional production chains: Value-added and consumption-based approaches*.](references/sanguinet_azzoni_2024/carbon_emissions_drivers_brazilian_regional_production_chains.pdf) Fornece os coeficientes de emissão usados no trabalho e discute formas de atribuição de emissões nas cadeias produtivas brasileiras. [DOI](https://doi.org/10.1016/j.rspp.2024.100015).
3. **Montoya, M. A.; Bertussi, L. A. S.; Allegretti, G.; Talamini, E. (2026).** [*Brazilian energy and carbon footprints: structural changes and sectoral contributions to climate change*.](references/montoya_et_al_2026/brazilian_energy_carbon_footprints.pdf) Oferece uma aplicação da análise insumo-produto às pegadas energética e de carbono no Brasil. [DOI](https://doi.org/10.1007/s10668-024-05251-8).
4. **Marques, A.; Rodrigues, J.; Lenzen, M.; Domingos, T. (2012).** [*Income-based environmental responsibility*.](references/marques_et_al_2012/income_based_environmental_responsibility.pdf) Contribui para a discussão das formas de atribuição da responsabilidade ambiental. A abordagem por renda não é aplicada no recorte atual. [DOI](https://doi.org/10.1016/j.ecolecon.2012.09.010).

<details>
<summary>Reproduzir a análise</summary>

No Windows, com Python 3.12, execute na pasta do repositório:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install ipykernel
.venv\Scripts\python.exe -m ipykernel install --user --name redes-1 --display-name "Python (Redes-1 .venv)"
```

Selecione esse kernel e execute primeiro o notebook da MIP, depois o de redes. A segunda etapa lê apenas a matriz de produção e o catálogo de setores exportados pela primeira. Os arquivos de entrada são verificados por SHA-256 conforme o [manifesto](raw/manifesto.csv). A execução do notebook de redes gera os CSVs em `outputs/redes/` e a página interativa em `docs/index.html`.

</details>
