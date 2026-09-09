# Cenário: exterior representativo

Esta pasta contém os parâmetros usados na conta de consumo com importações. Eles representam um único exterior agregado com 67 atividades, na mesma ordem da MIP brasileira de nível 67.

- `intensidades_co2_exterior_representativo.csv`: intensidade direta de CO2 por atividade, em Gg de CO2 por R$ milhão de produção bruta, para 2011 e 2018.
- `inversa_leontief_exterior_representativo.csv`: inversa de Leontief do exterior, com atividades nas linhas e nas colunas.

## Hipótese inicial

Os CSVs foram gerados por `scripts/gerar_parametros_exterior_representativo.py` como cenário de referência, não como dados observados internacionais:

```text
gamma_exterior = gamma_Brasil
L_exterior = L_Brasil (MIP brasileira de 2015)
```

Assim, o exterior representativo inicialmente possui a mesma intensidade direta de CO2 e a mesma tecnologia de produção do Brasil. Essa hipótese permite calcular emissões incorporadas em importações sem uma MRIO global, mas não representa parceiros comerciais reais.

Para usar outro cenário, substitua os CSVs mantendo os 67 códigos de atividade, sua ordem e unidades. Documente neste arquivo a fonte, o ano, a concordância setorial e qualquer transformação aplicada.
