# Script para executar o Sistema de Cadastro
# PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando Sistema de Cadastro" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "venv")) {
    Write-Host "✗ Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "  Execute primeiro: .\setup.ps1" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Iniciando aplicação Flask..." -ForegroundColor Green
Write-Host "Acesse: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""

# Tenta rodar com python (do venv) ou py se falhar
try {
    python app.py
}
catch {
    py app.py
}
