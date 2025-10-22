"""
Configurações do sistema acadêmico
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Classe de configuração do sistema"""
    
    # Configurações do banco de dados MySQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'sistema_academico')
    DB_USER = os.getenv('DB_USER', 'app_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'app_password')
    DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')
    
    # String de conexão SQLAlchemy
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
    
    # Configurações da aplicação
    APP_NAME = "Sistema Acadêmico Colaborativo"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'