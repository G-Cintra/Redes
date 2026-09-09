[CmdletBinding()]
param()

$raiz = Split-Path -Parent $PSScriptRoot
$manifesto = Join-Path $raiz 'raw/SHA256SUMS'
$falhas = [System.Collections.Generic.List[string]]::new()

Get-Content -LiteralPath $manifesto | Where-Object { $_.Trim() } | ForEach-Object {
    if ($_ -notmatch '^(?<hash>[A-Fa-f0-9]{64}) \*(?<arquivo>.+)$') {
        $falhas.Add("Linha inválida no manifesto: $_")
        return
    }

    $caminho = Join-Path $raiz (Join-Path 'raw' $Matches.arquivo)
    if (-not (Test-Path -LiteralPath $caminho -PathType Leaf)) {
        $falhas.Add("Arquivo ausente: raw/$($Matches.arquivo)")
        return
    }

    $atual = (Get-FileHash -LiteralPath $caminho -Algorithm SHA256).Hash
    if ($atual -ne $Matches.hash.ToUpperInvariant()) {
        $falhas.Add("Hash divergente: raw/$($Matches.arquivo)")
    }
}

if ($falhas.Count) {
    $falhas | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host 'Todos os hashes SHA-256 conferem.'

