# Redes

Análise da Matriz de Insumo-Produto brasileira de 2015 e contabilidade setorial de CO₂ por produção, consumo e renda.

O notebook [analise_matriz_insumo_produto.ipynb](analise_matriz_insumo_produto.ipynb) é o roteiro principal. Ele mostra as entradas, as hipóteses, as transformações da MIP, os cálculos de Leontief e Ghosh, os resultados e a figura final.

## Executar

No Windows:

```powershell
uv venv .venv --python 3.12
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Abra o notebook e execute as células em ordem. As intensidades de CO₂ de 2015 são estimadas por interpolação linear entre 2011 e 2018, com peso de 4/7 para a variação entre os anos, e aplicadas à MIP de 2015. Os resultados atuais são gravados em `outputs/contabilidade_co2_2015.csv` e `outputs/contabilidade_co2_2015.png`; uma nova execução os sobrescreve.

## Estrutura

| Local | Conteúdo |
| --- | --- |
| `redes/dados.py` | Leitura e verificação das entradas canônicas. |
| `redes/mip.py` | Extração das tabelas da MIP do IBGE. |
| `redes/modelo.py` | Matrizes de Leontief e Ghosh. |
| `redes/emissoes.py` | Contabilidade de CO₂. |
| `redes/visualizacoes.py` | Figura final. |
| `raw/` | Entradas canônicas e seu manifesto. |
| `references/` | Artigos e demais fontes bibliográficas. |

## Entradas verificadas

[raw/manifesto.csv](raw/manifesto.csv) é a lista única das entradas que podem alterar os resultados. Cada linha informa o identificador usado no notebook, arquivo, SHA-256, fonte, ano e descrição.

O notebook escolhe explicitamente os coeficientes brasileiros e o cenário exterior por identificador. `dados.py` encontra a linha correspondente, compara o SHA-256 do arquivo e só então chama `pandas`. Para alterar uma entrada intencionalmente, atualize seu arquivo e o hash no manifesto na mesma alteração versionada.

## Verificar

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes verificam as entradas declaradas, a verificação de hash antes da leitura e os interpolação linear e os totais de referência de 2015.
