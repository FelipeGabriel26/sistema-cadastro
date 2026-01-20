# Setup Simplificado

Write-Host "=== Iniciando Setup ===" -ForegroundColor Cyan
Write-Host ""

# 1. Encontrar comando Python (py ou python)
$pyCmd = "python"
if (Get-Command "py" -ErrorAction SilentlyContinue) { 
    $pyCmd = "py" 
}
Write-Host "[OK] Usando comando: $pyCmd" -ForegroundColor Green

# 2. Criar ambiente virtual
Write-Host "[...] Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "[OK] venv ja existe." -ForegroundColor Green
}
else {
    & $pyCmd -m venv venv
    Write-Host "[OK] venv criado." -ForegroundColor Green
}

# 3. Criar .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Arquivo .env criado." -ForegroundColor Green
}

# 4. Instalar dependencias
Write-Host "[...] Instalando dependencias (isso pode demorar)..." -ForegroundColor Yellow

# Tenta usar o pip do ambiente virtual
if (Test-Path "venv\Scripts\pip.exe") {
    & .\venv\Scripts\pip.exe install -r requirements.txt --quiet
}
else {
    # Fallback
    & $pyCmd -m pip install -r requirements.txt --quiet
}

Write-Host "[OK] Dependencias instaladas." -ForegroundColor Green
Write-Host ""
Write-Host "=== Setup Concluido! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "1. Edite o arquivo .env"
Write-Host "2. Execute: .\init-db.ps1"
Write-Host "3. Execute: .\run.ps1"
