# Script de Verificacao de Codigo (Build Check)

Write-Host "=== VERIFICACAO DE CODIGO ===" -ForegroundColor Cyan
Write-Host ""

# 1. Encontrar Python
$pyCmd = "python"
if (Get-Command "py" -ErrorAction SilentlyContinue) { $pyCmd = "py" }
Write-Host "[OK] Usando: $pyCmd" -ForegroundColor Green

# 2. Verificar Sintaxe
Write-Host "Verificando sintaxe..." -ForegroundColor Yellow

$arquivos = "app.py", "models.py", "config.py"
$temErro = $false

foreach ($arq in $arquivos) {
    if (Test-Path $arq) {
        # Compila para checar erro
        & $pyCmd -c "import py_compile; py_compile.compile('$arq', doraise=True)" 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] $arq" -ForegroundColor Green
        }
        else {
            Write-Host "  [ERRO] $arq (Erro de sintaxe)" -ForegroundColor Red
            $temErro = $true
        }
    }
}

if ($temErro) {
    Write-Host "FALHA NA COMPILACAO. Corrija os erros." -ForegroundColor Red
    exit 1
}

# 3. Executar Testes
Write-Host "Rodando testes..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\python.exe") {
    & .\venv\Scripts\python.exe test_app.py
}
else {
    & $pyCmd test_app.py
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== SUCESSO! CODIGO APROVADO ===" -ForegroundColor Green
    Write-Host "Pode rodar o sistema com .\run.ps1"
}
else {
    Write-Host "FALHA NOS TESTES." -ForegroundColor Red
}
