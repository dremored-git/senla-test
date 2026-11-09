$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
        py -3 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.11+ and its py launcher first.' }
    }
    if ($env:OS -eq 'Windows_NT') {
        # Pure Python avoids optional SQLAlchemy DLLs blocked by Windows policy.
        $previousCext = $env:DISABLE_SQLALCHEMY_CEXT
        try {
            $env:DISABLE_SQLALCHEMY_CEXT = '1'
            & ./.venv/Scripts/python.exe -m pip install --force-reinstall --no-deps `
                --no-binary=SQLAlchemy --no-cache-dir 'SQLAlchemy>=2,<3'
            if ($LASTEXITCODE -ne 0) { throw 'SQLAlchemy installation failed.' }
        } finally {
            $env:DISABLE_SQLALCHEMY_CEXT = $previousCext
        }
    }
    & ./.venv/Scripts/python.exe -m pip install -e '.[dev,defense]'
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    & ./.venv/Scripts/python.exe -m playwright install chromium
    if ($LASTEXITCODE -ne 0) { throw 'Playwright browser installation failed.' }
    if (-not (Test-Path -LiteralPath '.env')) {
        Copy-Item -LiteralPath '.env.example' -Destination '.env'
    }
    $env:VIRTUAL_ENV = Join-Path $PSScriptRoot '.venv'
    $env:PATH = (Join-Path $env:VIRTUAL_ENV 'Scripts') + ';' + $env:PATH
    Write-Host 'Ready. Fill .env, then run pytest. See docs/running.md for live tests.'
} finally {
    Pop-Location
}
