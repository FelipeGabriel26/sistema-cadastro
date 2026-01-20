# Script para adicionar Python e MySQL ao PATH do usuário
# NÃO precisa executar como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Adicionando ao PATH" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Caminhos encontrados
$pythonPath = "C:\Users\acer\AppData\Local\Programs\Python\Python313"
$pythonScripts = "C:\Users\acer\AppData\Local\Programs\Python\Python313\Scripts"
$mysqlPath = "C:\xampp\mysql\bin"

# Obter PATH atual do usuário
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Verificar e adicionar Python
if ($currentPath -notlike "*$pythonPath*") {
    Write-Host "Adicionando Python ao PATH..." -ForegroundColor Yellow
    $newPath = $currentPath + ";" + $pythonPath + ";" + $pythonScripts
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✓ Python adicionado!" -ForegroundColor Green
}
else {
    Write-Host "✓ Python já está no PATH" -ForegroundColor Green
}

# Verificar e adicionar MySQL
if ($currentPath -notlike "*$mysqlPath*") {
    Write-Host "Adicionando MySQL ao PATH..." -ForegroundColor Yellow
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $newPath = $currentPath + ";" + $mysqlPath
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✓ MySQL adicionado!" -ForegroundColor Green
}
else {
    Write-Host "✓ MySQL já está no PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ PATH configurado com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "1. FECHE este PowerShell" -ForegroundColor White
Write-Host "2. Abra um NOVO PowerShell" -ForegroundColor White
Write-Host "3. Execute: .\verificar.ps1" -ForegroundColor Cyan
Write-Host ""
pause
