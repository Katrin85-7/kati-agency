param(
  [Parameter(Mandatory = $true)]
  [string]$RepoUrl
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".git")) {
  git init
}

git remote remove origin 2>$null
git remote add origin $RepoUrl

git branch -M main
git push -u origin main

Write-Host "Done. Remote: $RepoUrl"
