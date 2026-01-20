import unittest
import os

# 1. Configura ambiente de TESTE antes de importar o app
# Isso força o sistema a usar um banco na memória (SQLite) em vez do MySQL real
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['FLASK_ENV'] = 'testing'

try:
    from app import app, db
    from models import Usuario
except ImportError as e:
    print(f"\n[ERRO CRITICO] Falha ao importar a aplicacao: {e}")
    exit(1)

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        # Configura o app para modo de teste
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.app = app.test_client()
        
        # Cria contexto e banco
        self.context = app.app_context()
        self.context.push()
        
        # Cria tabelas no banco de memoria
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_01_app_starts(self):
        """Teste 1: Verifica se o app inicia corretamente"""
        print("\n[Teste] Verificando se o servidor responde...")
        try:
            response = self.app.get('/login')
            self.assertEqual(response.status_code, 200)
            print("  [OK] Pagina de login carregada com sucesso.")
        except Exception as e:
            self.fail(f"O app falhou ao iniciar: {e}")

    def test_02_database_models(self):
        """Teste 2: Verifica modelos e banco de dados"""
        print("[Teste] Verificando criacao de usuarios...")
        u = Usuario(nome="Teste", email="teste@teste.com", cpf="000", telefone="000")
        u.set_senha("123")
        
        db.session.add(u)
        db.session.commit()
        
        user_db = Usuario.query.filter_by(email="teste@teste.com").first()
        self.assertIsNotNone(user_db)
        self.assertEqual(user_db.nome, "Teste")
        print("  [OK] Modelos e Banco de Dados funcionando (em memoria).")

if __name__ == "__main__":
    unittest.main()
