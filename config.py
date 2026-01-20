import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações da aplicação"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-desenvolvimento-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/sistema_cadastro'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log de queries SQL
    
    # Configurações de sessão
    SESSION_COOKIE_SECURE = False  # True em produção com HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configurações de upload (se necessário)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = 'uploads'
