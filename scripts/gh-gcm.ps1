param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $GhArgs
)

Set-StrictMode -Version 2.0

if (-not $GhArgs -or $GhArgs.Count -eq 0) {
  Write-Error "Usage: powershell -File scripts/gh-gcm.ps1 <gh arguments>"
  exit 2
}

$oldGhToken = $env:GH_TOKEN
$exitCode = 0

try {
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI 'gh' was not found in PATH."
  }

  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git was not found in PATH."
  }

  if ([string]::IsNullOrWhiteSpace($env:GH_TOKEN)) {
    $query = "protocol=https`nhost=github.com`n`n"
    $credential = $query | git credential fill
    if ($LASTEXITCODE -ne 0) {
      throw "git credential fill failed."
    }

    $passwordLine = $credential | Where-Object { $_ -like 'password=*' } | Select-Object -First 1
    if (-not $passwordLine) {
      throw "No GitHub token was returned by Git Credential Manager."
    }

    $env:GH_TOKEN = $passwordLine.Substring("password=".Length)
  }

  & gh @GhArgs
  $exitCode = $LASTEXITCODE
} catch {
  Write-Error $_.Exception.Message
  $exitCode = 1
} finally {
  if ([string]::IsNullOrEmpty($oldGhToken)) {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
  } else {
    $env:GH_TOKEN = $oldGhToken
  }
}

exit $exitCode
