[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('opencode', 'codex', 'claude')]
    [string]$Target,

    [ValidateSet('global', 'project')]
    [string]$Scope = 'global'
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $packageRoot '.agents\skills'
if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Skill source not found: $sourceRoot"
}

switch ("$Target/$Scope") {
    'opencode/project' { $destination = Join-Path (Get-Location).Path '.agents\skills' }
    'codex/project'    { $destination = Join-Path (Get-Location).Path '.agents\skills' }
    'claude/project'   { $destination = Join-Path (Get-Location).Path '.claude\skills' }
    'opencode/global'  { $destination = Join-Path $HOME '.agents\skills' }
    'codex/global' {
        $codexHome = if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
            Join-Path $HOME '.codex'
        } else {
            $env:CODEX_HOME
        }
        $destination = Join-Path $codexHome 'skills'
    }
    'claude/global'   { $destination = Join-Path $HOME '.claude\skills' }
}

$null = New-Item -ItemType Directory -Path $destination -Force
$copied = 0
$skipped = 0
foreach ($skill in Get-ChildItem -LiteralPath $sourceRoot -Directory) {
    $targetPath = Join-Path $destination $skill.Name
    if (Test-Path -LiteralPath $targetPath) {
        Write-Output "Skipped existing skill: $targetPath"
        $skipped++
        continue
    }
    Copy-Item -LiteralPath $skill.FullName -Destination $targetPath -Recurse
    Write-Output "Installed: $targetPath"
    $copied++
}
Write-Output "Done. Installed $copied skill(s); skipped $skipped existing skill(s)."
