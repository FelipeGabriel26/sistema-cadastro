@echo off
echo Iniciando Sistema de Cadastro...
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Executar aplicacao
python app.py

pause
