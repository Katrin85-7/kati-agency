# Copy 9 PDFs into pdfs/ before Docker build
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$src = Resolve-Path (Join-Path $PSScriptRoot '..\..\design\delivery')
$dst = Join-Path $PSScriptRoot 'pdfs'
New-Item -ItemType Directory -Force -Path $dst | Out-Null

$missing = @()
1..9 | ForEach-Object {
    $name = "Soul-Method-Workbook-CHS$_-tripwire-15eur.pdf"
    $from = Join-Path $src $name
    $to = Join-Path $dst $name
    if (-not (Test-Path $from)) {
        $missing += $name
        return
    }
    Copy-Item -Path $from -Destination $to -Force
    $kb = [math]::Round((Get-Item $to).Length / 1KB)
    Write-Host "OK $name ($kb KB)"
}

if ($missing.Count -gt 0) {
    Write-Host ''
    Write-Host 'Missing PDF files:' -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  $_" }
    exit 1
}

Write-Host ''
Write-Host "Ready: $dst" -ForegroundColor Green
