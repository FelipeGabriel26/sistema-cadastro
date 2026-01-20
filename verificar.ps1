# Script de Verificação Simplificado

Write-Host "=== Verificacao de Pre-requisitos ===" -ForegroundColor Cyan
Write-Host ""

$pythonOK = $false

# 1. Verificar Python
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Python encontrado (comando 'py')" -ForegroundColor Green
    $pythonOK = $true
}
elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Python encontrado (comando 'python')" -ForegroundColor Green
    $pythonOK = $true
}
else {
    Write-Host "[ERRO] Python NAO encontrado!" -ForegroundColor Red
}

Write-Host ""

# 2. Verificar MySQL
if (Get-Command "mysql" -ErrorAction SilentlyContinue) {
    Write-Host "[OK] MySQL encontrado no PATH" -ForegroundColor Green
}
else {
    if (Test-Path "C:\xampp\mysql\bin\mysql.exe") {
        Write-Host "[OK] MySQL encontrado no XAMPP" -ForegroundColor Green
    }
    else {
        Write-Host "[AVISO] MySQL nao encontrado no PATH (mas pode estar instalado)" -ForegroundColor Yellow
    }
}

Write-Host ""

# 3. Executar Setup se Python estiver OK
if ($pythonOK) {
    Write-Host "Iniciando Setup..." -ForegroundColor Cyan
    Start-Sleep -Seconds 1
    & .\setup.ps1
}
else {
    Write-Host "Por favor, instale o Python antes de continuar." -ForegroundColor Red
}
