# Soul Method bot - deploy 24/7 to Fly.io
# First time: flyctl auth login
# Then: .\DEPLOY-FLY.ps1

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

function Invoke-Fly {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $output = & $script:FlyBin @Args 2>&1
    $code = $LASTEXITCODE
    $ErrorActionPreference = $prev
    if ($code -ne 0) {
        ($output | Out-String) | Write-Host
        throw "flyctl failed ($code): fly $($Args -join ' ')"
    }
    return $output
}

function Get-Flyctl {
    $cmd = Get-Command flyctl -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $cmd = Get-Command fly -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $flyPath = Join-Path $env:USERPROFILE '.fly\bin/flyctl.exe'
    if (Test-Path $flyPath) { return $flyPath }

    Write-Host 'Installing flyctl...' -ForegroundColor Cyan
    $installScript = Join-Path $env:TEMP 'fly-install.ps1'
    Invoke-WebRequest -Uri 'https://fly.io/install.ps1' -OutFile $installScript -UseBasicParsing
    & $installScript
    Remove-Item $installScript -Force -ErrorAction SilentlyContinue

    if (-not (Test-Path $flyPath)) {
        throw 'flyctl not found after install. Restart terminal or add %USERPROFILE%\.fly\bin to PATH.'
    }
    return $flyPath
}

if (-not (Test-Path '.env')) {
    throw 'Missing .env - copy .env.example and set BOT_TOKEN.'
}

$script:FlyBin = Get-Flyctl

Write-Host '1/4 PDF for Docker...' -ForegroundColor Cyan
& (Join-Path $PSScriptRoot 'prepare-deploy.ps1')

Write-Host '2/4 Fly auth...' -ForegroundColor Cyan
try {
    Invoke-Fly auth whoami | Out-Null
} catch {
    Write-Host 'Fly.io login required (browser will open)...' -ForegroundColor Yellow
    Invoke-Fly auth login | Out-Null
}

Write-Host '3/4 Secrets and volume...' -ForegroundColor Cyan
$envLines = Get-Content '.env' | Where-Object { $_ -match '^\s*[^#]' }
$secrets = @{}
foreach ($line in $envLines) {
    if ($line -match '^([^=]+)=(.*)$') {
        $k = $matches[1].Trim()
        $v = $matches[2].Trim()
        if ($k -in @('BOT_TOKEN', 'ACCESS_CODE', 'MAX_CODE_ATTEMPTS')) {
            $secrets[$k] = $v
        }
    }
}
if (-not $secrets['BOT_TOKEN']) { throw 'BOT_TOKEN is empty in .env' }

$appName = 'soul-method-workbook-bot'
$appList = Invoke-Fly apps list | Out-String
if ($appList -notmatch [regex]::Escape($appName)) {
    Write-Host "Creating app $appName ..."
    Invoke-Fly apps create $appName --org personal | Out-Null
}

$volumeList = Invoke-Fly volumes list -a $appName | Out-String
if ($volumeList -notmatch 'bot_data') {
    Write-Host 'Creating volume bot_data (1 GB, ams)...'
    Invoke-Fly volumes create bot_data --size 1 --region ams -a $appName -y | Out-Null
}

foreach ($entry in $secrets.GetEnumerator()) {
    Invoke-Fly secrets set "$($entry.Key)=$($entry.Value)" -a $appName | Out-Null
}

Write-Host '4/4 Deploy...' -ForegroundColor Cyan
Invoke-Fly deploy -a $appName

Write-Host ''
Write-Host 'Done. Bot runs 24/7 on Fly.io.' -ForegroundColor Green
Write-Host "Status: $FlyBin status -a soul-method-workbook-bot"
Write-Host "Logs:   $FlyBin logs -a soul-method-workbook-bot"
Write-Host ''
Write-Host 'Stop local START-WORKBOOK-BOT.bat - only one polling instance allowed.' -ForegroundColor Yellow
