$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Paper = Join-Path $Root "paper"
$Data = Join-Path $Root "data"
$ValidationPath = Join-Path $Root "results\full_scale\experiment_validation.json"
$OutPdf = "C:\Users\wangz\Downloads\52.pdf"
$LocalPdf = Join-Path $Paper "main.pdf"
$MinPages = 25

function Assert-Equal {
    param(
        [string]$Name,
        $Actual,
        $Expected
    )
    if ($Actual -ne $Expected) {
        throw "$Name expected $Expected but found $Actual"
    }
}

if (-not (Test-Path -LiteralPath $ValidationPath)) {
    throw "Missing full-scale validation file: $ValidationPath"
}

$validation = Get-Content -LiteralPath $ValidationPath -Raw | ConvertFrom-Json
Assert-Equal "status" ([string]$validation.status) "complete"
Assert-Equal "expected_condition_rows" ([int64]$validation.expected_condition_rows) 432000
Assert-Equal "actual_condition_rows" ([int64]$validation.actual_condition_rows) 432000
Assert-Equal "represented_evaluations" ([int64]$validation.represented_evaluations) 99283968000
Assert-Equal "represented_frame_decisions" ([int64]$validation.represented_frame_decisions) 6354173952000

New-Item -ItemType Directory -Force -Path $Data | Out-Null
Remove-Item -LiteralPath $LocalPdf -ErrorAction SilentlyContinue

Push-Location $Paper
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $LocalPdf)) {
    throw "Expected local PDF was not produced: $LocalPdf"
}

$pdfInfo = & pdfinfo $LocalPdf
$pageLine = $pdfInfo | Select-String -Pattern "^Pages:\s+(\d+)"
if (-not $pageLine) {
    throw "Could not read page count from $LocalPdf"
}
$Pages = [int]$pageLine.Matches[0].Groups[1].Value
if ($Pages -lt $MinPages) {
    throw "Final PDF has $Pages pages; required at least $MinPages"
}

Copy-Item -LiteralPath $LocalPdf -Destination $OutPdf -Force
$OutItem = Get-Item -LiteralPath $OutPdf
$Hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $OutPdf).Hash
Remove-Item -LiteralPath $LocalPdf -Force

$status = [ordered]@{
    paper = 52
    status = "final_v4_25_page_gate"
    canonical_pdf = $OutPdf
    canonical_pages = $Pages
    canonical_bytes = $OutItem.Length
    canonical_sha256 = $Hash
    minimum_pages_required = $MinPages
    local_pdf_removed = -not (Test-Path -LiteralPath $LocalPdf)
    compact_rows = [int64]$validation.actual_condition_rows
    represented_evaluations = [int64]$validation.represented_evaluations
    represented_frame_decisions = [int64]$validation.represented_frame_decisions
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}

$status | ConvertTo-Json | Set-Content -Encoding ASCII -LiteralPath (Join-Path $Data "build_status.json")

Write-Host "canonical_pdf=$OutPdf"
Write-Host "canonical_pages=$Pages"
Write-Host "canonical_bytes=$($OutItem.Length)"
Write-Host "canonical_sha256=$Hash"
Write-Host "local_pdf_removed=$(-not (Test-Path -LiteralPath $LocalPdf))"
