# Create the GitHub repository and push this project to it (Windows PowerShell).
#
#   .\scripts\publish.ps1
#   .\scripts\publish.ps1 -RepoName my-other-repo-name -Visibility private
#
# Requires the GitHub CLI (https://cli.github.com) and `gh auth login` once.
param(
    [string]$RepoName   = "iot-sensor-health-monitor",
    [ValidateSet("public", "private")][string]$Visibility = "public"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is not installed. Install it from https://cli.github.com"
}
gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw "Run 'gh auth login' first." }

$description = "Lecture 1 exercise - rule-based Normal/Abnormal monitoring of IoT motor readings, with a Colab notebook and a VS Code dev container"

gh repo create $RepoName "--$Visibility" --source=. --remote=origin --description $description --push
git push -u origin try 2>$null

Write-Host ""
Write-Host "Done: $(gh repo view $RepoName --json url -q .url)"
