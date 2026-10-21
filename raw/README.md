# Entradas canônicas

Esta pasta contém os arquivos que alimentam a análise. [manifesto.csv](manifesto.csv) identifica cada entrada usada pelo notebook, sua fonte, seu ano e o SHA-256 esperado.

Os arquivos não devem ser alterados silenciosamente. Uma alteração intencional exige atualizar o hash correspondente no manifesto e versionar ambos no Git.

A análise principal usa a MIP de nível 67. A MIP de nível 12 também alimenta o [diagrama completo de 12 setores](../diagrama_mip12.ipynb); as de níveis 20 e 67 alimentam os [Sankeys completos](../sankeys_mip20_67.ipynb).

As MIPs usadas pelo manifesto têm o sufixo `.xls.original` para evitar edições acidentais. O conteúdo permanece no formato XLS e é lido com `xlrd`, sem renomear os arquivos. O sufixo não bloqueia alterações; a verificação SHA-256 detecta mudanças nos arquivos.
