param(
  [string]$Name = "practice-automation-tests",
  [string]$Desc = "Selenium + Pytest + Allure UI autotests for practice-automation.com",
  [string]$Token = $env:GH_TOKEN,
  [switch]$Public
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (-not $Token) {
  Write-Host ""
  Write-Host "NET TOKENA."
  Write-Host "Zadayte ego tak:"
  Write-Host "   `$env:GH_TOKEN = 'ghp_...'"
  Write-Host "   .\publish.ps1"
  Write-Host ""
  Write-Host "Token dolzhen umet sozdavat repozytorii (scope repo u klassicheskogo PAT"
  Write-Host "libo prava 'Administration: write' u fine-grained token)."
  Write-Host "Alternativa: sozdat privatny repozitoriy vruchnuyu na github.com i vypolnite:"
  Write-Host "   git remote add origin https://github.com/<LV_LOGIN>/$Name.git"
  Write-Host "   git push -u origin main"
  exit 1
}

$h = @{
  "Authorization" = "Bearer $Token"
  "User-Agent"    = "opencode"
  "Accept"        = "application/vnd.github+json"
}

$me = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $h -Method Get -TimeoutSec 30
Write-Host "Avtorizovan pod: $($me.login)"

$body = @{
  name        = $Name
  description = $Desc
  private     = (-not $Public)
  auto_init   = $false
  has_issues  = $true
  has_wiki    = $false
} | ConvertTo-Json

$repo = $null
try {
  $repo = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $h -Method Post `
    -Body ([Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json" -TimeoutSec 60
  Write-Host "Sozdan repozitoriy: $($repo.full_name) (private=$($repo.private))"
} catch {
  $msg = $_.ErrorDetails.Message
  if ($msg -match '"name"\s*:\s*"([^"]+)"') {
    Write-Host "Repozitoriy uzhe est, beru ego: $msg"
    $repo = Invoke-RestMethod -Uri "https://api.github.com/repos/$($me.login)/$Name" -Headers $h -Method Get -TimeoutSec 30
  } else {
    Write-Host "Ne udalos sozdat repozitoriy: $msg"
    exit 1
  }
}

$url = $repo.clone_url
Write-Host "Push v: $url"

$old = git remote
if ($old -contains "origin") {
  git remote set-url origin $url
} else {
  git remote add origin $url
}

git push -u origin main
if ($LASTEXITCODE -ne 0) {
  Write-Host "Push ne proshol. Proverte prava na repozitorii."
  exit 1
}

Write-Host ""
Write-Host "Gotovo. Adres dlya Tasky: $($repo.html_url)"
Write-Host "Vidimost: $(if ($repo.private) { 'PRIVATE' } else { 'PUBLIC' })"
