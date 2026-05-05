<#
.SYNOPSIS
    Builds a loth.cls document in all variants declared in the .tex file.
.DESCRIPTION
    Reads \documentclass lines from the source file using a commenting convention:
      \documentclass[...]{loth}    -- active (built)
      %\documentclass[...]{loth}   -- single comment: also built
      %%\documentclass[...]{loth}  -- double comment: ignored

    The variant name (handout / choir / lectionary / pamphlet) is derived from
    the options on each line. Flags are taken exactly as written in the file.
.PARAMETER TexFile
    Path to the source .tex file (absolute or relative to the current directory).
.PARAMETER OutputDir
    Directory for the output PDFs. Defaults to the directory containing the .tex file.
.EXAMPLE
    .\chant-build-all.ps1 5-TP-A-VII.tex
    .\chant-build-all.ps1 GNM\TP\GNM-TP-4.tex -OutputDir GNM\TP
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$TexFile,

    [string]$OutputDir = ''
)

$AuxExtensions = @('.aux', '.log', '.gaux', '.synctex.gz', '.fls', '.fdb_latexmk', '.out')

# Resolve paths
$TexPath = [IO.Path]::GetFullPath((Join-Path (Get-Location) $TexFile))
if (-not (Test-Path $TexPath)) {
    Write-Error "File not found: $TexPath"
    exit 1
}
$TexDir  = Split-Path $TexPath
$TexBase = [IO.Path]::GetFileNameWithoutExtension($TexPath)

if ($OutputDir -eq '') {
    $OutputDir = $TexDir
} else {
    $OutputDir = [IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputDir))
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# Parse variant lines from the .tex file.
# Convention:
#   \documentclass[...]{loth}   -- no comment  -> build
#   %\documentclass[...]{loth}  -- single %    -> build
#   %%\documentclass[...]{loth} -- double %%   -> skip
#
# Variant name is derived from the options: lectionary > choir > pamphlet > handout.
# If two lines resolve to the same name the last one wins.
$variants = [ordered]@{}  # name -> full '\documentclass[...]{loth}' line

foreach ($line in (Get-Content $TexPath)) {
    $t = $line.TrimStart()
    if ($t -match '^%%') { continue }                          # double comment: skip
    if ($t -match '^%?\\documentclass\[([^\]]+)\]\{loth\}') { # active or single comment
        $opts = $Matches[1]
        $name = if     ($opts -match '\blectionary\b') { 'lectionary' }
                elseif ($opts -match '\bchoir\b')       { 'choir' }
                elseif ($opts -match '\bpamphlet\b')    { 'pamphlet' }
                else                                    { 'handout' }
        $variants[$name] = '\documentclass[' + $opts + ']{loth}'
    }
}

if ($variants.Count -eq 0) {
    Write-Error "No \documentclass[...]{loth} lines found in $TexFile"
    exit 1
}

Write-Host "Variants to build: $($variants.Keys -join ', ')"

# Active-line pattern: the uncommented \documentclass that will be replaced in each pass
$activePattern = '(?m)^\\documentclass\[.*?\]\{loth\}'

$totalStart = Get-Date

foreach ($name in $variants.Keys) {
    $start    = Get-Date
    $tempBase = "${TexBase}__${name}"
    $tempTex  = Join-Path $TexDir "${tempBase}.tex"

    Write-Host ""
    Write-Host "---  $name  ---" -ForegroundColor Cyan
    Write-Host "    $($variants[$name])"

    $original = [IO.File]::ReadAllText($TexPath)

    if ($original -notmatch $activePattern) {
        Write-Warning "No active (uncommented) \documentclass line found -- skipping $name"
        continue
    }

    $patched = $original -replace $activePattern, $variants[$name]
    [IO.File]::WriteAllText($tempTex, $patched, [Text.UTF8Encoding]::new($false))

    Push-Location $TexDir
    try {
        $luaArgs = @('--interaction=nonstopmode', '--shell-escape', "${tempBase}.tex")

        Write-Host "  Compiling..." -NoNewline
        $out = & lualatex @luaArgs 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Warning " lualatex exited with code $LASTEXITCODE"
            $out | Select-String 'rror|Emergency' | ForEach-Object {
                Write-Host "    $_" -ForegroundColor Red
            }
        } else {
            Write-Host " done"
        }
    } finally {
        Pop-Location
    }

    $builtPdf = Join-Path $TexDir "${tempBase}.pdf"
    $finalPdf = Join-Path $OutputDir "${TexBase}-${name}.pdf"

    if (Test-Path $builtPdf) {
        Move-Item $builtPdf $finalPdf -Force
        $elapsed = [math]::Round(((Get-Date) - $start).TotalSeconds, 1)
        Write-Host "  -> $(Split-Path $finalPdf -Leaf)  ($elapsed s)" -ForegroundColor Green
    } else {
        Write-Warning "  No PDF produced for $name"
    }

    Remove-Item $tempTex -Force -ErrorAction SilentlyContinue
    foreach ($ext in $AuxExtensions) {
        $aux = Join-Path $TexDir "${tempBase}${ext}"
        if (Test-Path $aux) { Remove-Item $aux -Force }
    }
}

$total = [math]::Round(((Get-Date) - $totalStart).TotalSeconds, 1)
Write-Host ""
Write-Host "Done -- $($variants.Count) variant(s) in $total s." -ForegroundColor Cyan
