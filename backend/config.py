# Importações necessárias para configuração
import os  # Para acessar variáveis de ambiente do sistema
from dotenv import load_dotenv  # Para carregar variáveis do arquivo .env

# Carrega as variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

class Config:
    """Classe de configuração centralizada do sistema acadêmico"""
    
    # Configurações de conexão com o banco de dados MySQL
    # Utiliza variáveis de ambiente com valores padrão como fallback
    DB_HOST = os.getenv('DB_HOST', 'localhost')  # Endereço do servidor MySQL
    DB_PORT = int(os.getenv('DB_PORT', 3306))  # Porta do MySQL (padrão 3306)
    DB_NAME = os.getenv('DB_NAME', 'sistema_academico')  # Nome do banco de dados
    DB_USER = os.getenv('DB_USER', 'app_user')  # Usuário para conexão
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'app_password')  # Senha do usuário
    DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')  # Codificação de caracteres
    
    # String de conexão completa para SQLAlchemy com MySQL
    # Formato: mysql+pymysql://usuario:senha@host:porta/banco?charset=codificacao
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
    
    # Configurações gerais da aplicação
    APP_NAME = "Sistema Acadêmico Colaborativo"  # Nome oficial da aplicação
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # Modo debug (padrão False)