# Script para verificar e corrigir banco de dados
from app import app, db
from models import Usuario, Reserva, RegistroPonto, Promocao
from sqlalchemy import inspect

def fix_db():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelas existentes: {tables}")
        
        if 'promocoes' not in tables:
            print("Criando tabela 'promocoes'...")
            try:
                # Tenta criar apenas as tabelas que faltam
                db.create_all()
                print("db.create_all() executado.")
            except Exception as e:
                print(f"Erro ao criar tabelas: {e}")
        else:
            print("Tabela 'promocoes' já existe.")

        # Verificar se está vazia
        try:
            count = Promocao.query.count()
            print(f"Número de promoções: {count}")
            
            if count == 0 and 'promocoes' in inspector.get_table_names():
                print("Criando promoções de exemplo...")
                from datetime import datetime, timedelta
                p1 = Promocao(
                    nome='Fim de Semana Relax',
                    descricao='20% de desconto para estadias de sexta a domingo',
                    desconto_percentual=20,
                    tipo_servico='HOTEL',
                    data_inicio=datetime.utcnow(),
                    data_fim=datetime.utcnow() + timedelta(days=30),
                    minimo_visitas=0
                )
                p2 = Promocao(
                    nome='Estacionamento Mensal',
                    descricao='Desconto especial para mensalistas',
                    desconto_percentual=15,
                    tipo_servico='GARAGEM',
                    data_inicio=datetime.utcnow(),
                    data_fim=datetime.utcnow() + timedelta(days=90),
                    minimo_visitas=0
                )
                db.session.add_all([p1, p2])
                db.session.commit()
                print("Promoções criadas!")
        except Exception as e:
            print(f"Erro ao acessar/criar promoções: {e}")

if __name__ == "__main__":
    fix_db()
