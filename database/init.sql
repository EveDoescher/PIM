-- Script de inicialização do banco de dados
-- Criar usuário da aplicação com permissões adequadas
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON sistema_academico.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- Usar o banco de dados
USE sistema_academico;

-- Configurar charset
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;