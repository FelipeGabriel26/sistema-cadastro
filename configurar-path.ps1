# Script para adicionar Python e MySQL ao PATH
# Execute como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configurando PATH do Sistema" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Procurar Python
Write-Host "Procurando Python..." -ForegroundColor Yellow
$pythonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python312",
    "$env:LOCALAPPDATA\Programs\Python\Python311",
    "$env:LOCALAPPDATA\Programs\Python\Python310",
    "C:\Python312",
    "C:\Python311",
    "C:\Python310"
)

$pythonFound = $false
foreach ($path in $pythonPaths) {
    if (Test-Path "$path\python.exe") {
        Write-Host "✓ Python encontrado em: $path" -ForegroundColor Green
        Write-Host ""
        Write-Host "Adicione ao PATH manualmente:" -ForegroundColor Yellow
        Write-Host "1. Pressione Win + Pause" -ForegroundColor White
        Write-Host "2. Configurações Avançadas do Sistema" -ForegroundColor White
        Write-Host "3. Variáveis de Ambiente" -ForegroundColor White
        Write-Host "4. Em 'Path' do sistema, adicione:" -ForegroundColor White
        Write-Host "   $path" -ForegroundColor Cyan
        Write-Host "   $path\Scripts" -ForegroundColor Cyan
        $pythonFound = $true
        break
    }
}

if (-not $pythonFound) {
    Write-Host "✗ Python não encontrado nas pastas comuns" -ForegroundColor Red
    Write-Host "  Reinstale o Python marcando 'Add to PATH'" -ForegroundColor Yellow
}

Write-Host ""

# Procurar MySQL/XAMPP
Write-Host "Procurando MySQL..." -ForegroundColor Yellow
$mysqlPaths = @(
    "C:\xampp\mysql\bin",
    "C:\Program Files\MySQL\MySQL Server 8.0\bin",
    "C:\Program Files\MySQL\MySQL Server 8.4\bin"
)

$mysqlFound = $false
foreach ($path in $mysqlPaths) {
    if (Test-Path "$path\mysql.exe") {
        Write-Host "✓ MySQL encontrado em: $path" -ForegroundColor Green
        Write-Host ""
        Write-Host "Adicione ao PATH manualmente:" -ForegroundColor Yellow
        Write-Host "   $path" -ForegroundColor Cyan
        $mysqlFound = $true
        break
    }
}

if (-not $mysqlFound) {
    Write-Host "✗ MySQL não encontrado nas pastas comuns" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "IMPORTANTE: Após adicionar ao PATH:" -ForegroundColor Yellow
Write-Host "1. REINICIE o PowerShell" -ForegroundColor White
Write-Host "2. Execute: .\verificar.ps1" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
pause
