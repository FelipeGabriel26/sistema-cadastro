@echo off
echo ========================================
echo   Sistema de Cadastro - Setup
echo ========================================
echo.

echo [1/5] Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ERRO: Falha ao criar ambiente virtual
    pause
    exit /b 1
)

echo [2/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [3/5] Atualizando pip...
python -m pip install --upgrade pip

echo [4/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo [5/5] Criando arquivo .env...
if not exist .env (
    copy .env.example .env
    echo Arquivo .env criado! Por favor, configure suas credenciais do MySQL.
) else (
    echo Arquivo .env ja existe.
)

echo.
echo ========================================
echo   Setup concluido com sucesso!
echo ========================================
echo.
echo Proximos passos:
echo 1. Configure o arquivo .env com suas credenciais do MySQL
echo 2. Crie o banco de dados: mysql -u root -p ^< setup_database.sql
echo 3. Inicialize as tabelas: flask init-db
echo 4. Popule com dados de exemplo: flask seed-db
echo 5. Execute a aplicacao: python app.py
echo.
pause
