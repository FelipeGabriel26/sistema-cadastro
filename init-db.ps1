# Script de inicialização do banco de dados (Atualizado)

Write-Host "=== Inicializando Banco de Dados ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "venv")) {
    Write-Host "[ERRO] Ambiente virtual não encontrado." -ForegroundColor Red
    exit 1
}

Write-Host "[...] Criando tabelas e dados..." -ForegroundColor Yellow

# Script Python temporário para inicialização
$initScript = @"
from app import app, db
from models import Usuario, Promocao
from werkzeug.security import generate_password_hash
import sys
from datetime import datetime, timedelta

try:
    with app.app_context():
        db.create_all()
        print('Tabelas verificadas/criadas.')
        
        # Verificar Admin
        if not Usuario.query.filter_by(email='admin@sistema.com').first():
            print('Criando usuario admin...')
            admin = Usuario(
                nome='Administrador',
                email='admin@sistema.com',
                cpf='000.000.000-00',
                telefone='(00) 00000-0000',
                tipo_usuario='ADM'
            )
            admin.set_senha('admin123')
            db.session.add(admin)
        
        # Verificar Promoções
        if Promocao.query.count() == 0:
            print('Criando promoções iniciais...')
            p1 = Promocao(
                nome='Bem-vindo',
                descricao='10% off na primeira compra',
                desconto_percentual=10,
                tipo_servico='AMBOS',
                data_inicio=datetime.utcnow(),
                data_fim=datetime.utcnow() + timedelta(days=365),
                minimo_visitas=0
            )
            db.session.add(p1)
            
        db.session.commit()
        print('Dados iniciais verificados.')
            
except Exception as e:
    print(f'ERRO: {e}')
    sys.exit(1)
"@

$initScript | Out-File "temp_init_db.py" -Encoding UTF8

if (Test-Path "venv\Scripts\python.exe") {
    & .\venv\Scripts\python.exe temp_init_db.py
}

Remove-Item "temp_init_db.py" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=== Concluido! ===" -ForegroundColor Cyan
