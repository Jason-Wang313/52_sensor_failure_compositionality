$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Paper = Join-Path $Root "paper"
$Data = Join-Path $Root "data"
$OutPdf = "C:\Users\wangz\Downloads\52.pdf"

New-Item -ItemType Directory -Force -Path $Data | Out-Null

Push-Location $Paper
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    Copy-Item -Force -Path "main.pdf" -Destination $OutPdf
    Remove-Item -Force -Path "main.pdf"
}
finally {
    Pop-Location
}

$Hash = (Get-FileHash -Algorithm SHA256 -Path $OutPdf).Hash

$status = [ordered]@{
    paper = 52
    status = "final_v3_full_scale"
    canonical_pdf = $OutPdf
    canonical_sha256 = $Hash
    local_pdf_removed = -not (Test-Path (Join-Path $Paper "main.pdf"))
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}

$status | ConvertTo-Json | Set-Content -Encoding UTF8 -Path (Join-Path $Data "build_status.json")
