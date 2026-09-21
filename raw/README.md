# Entradas canônicas

Esta pasta contém os arquivos que alimentam a análise. [manifesto.csv](manifesto.csv) identifica cada entrada usada pelo notebook, sua fonte, seu ano e o SHA-256 esperado.

Os arquivos não devem ser alterados silenciosamente. Uma alteração intencional exige atualizar o hash correspondente no manifesto e versionar ambos no Git.

As MIPs de níveis 12 e 20 são mantidas como material de consulta; a análise usa a MIP de nível 67.

As MIPs usadas pelo manifesto têm o sufixo `.xls.original` para evitar edições acidentais. O conteúdo permanece no formato XLS e é lido com `xlrd`, sem renomear os arquivos. O sufixo não bloqueia alterações; a verificação SHA-256 detecta mudanças nos arquivos.
