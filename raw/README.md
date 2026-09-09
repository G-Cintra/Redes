# Dados brutos

Esta pasta contém os arquivos originais da **Matriz de Insumo-Produto 2015** do IBGE, nos níveis de detalhamento 12, 20 e 67.

Fonte declarada: [IBGE — Matriz de Insumo-Produto](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9085-matriz-de-insumo-produto.html).

Os arquivos devem ser tratados como dados de entrada imutáveis. Transformações e produtos de análise devem ser salvos fora desta pasta.

## Integridade

Os hashes SHA-256 de referência estão em [`SHA256SUMS`](SHA256SUMS). Para verificar os arquivos no PowerShell, a partir da raiz do repositório, execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verificar_hashes.ps1
```

O comando retorna erro se um arquivo estiver ausente ou se seu conteúdo tiver mudado. Ao substituir deliberadamente um arquivo por uma nova versão da fonte, gere novamente os hashes e registre a alteração no histórico do projeto.
