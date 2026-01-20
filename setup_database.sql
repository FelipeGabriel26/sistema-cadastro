-- Script de criação do banco de dados para o Sistema de Cadastro
-- Execute este script no MySQL antes de inicializar a aplicação

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sistema_cadastro 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar o banco de dados
USE sistema_cadastro;

-- Mensagem de sucesso
SELECT 'Banco de dados criado com sucesso!' AS Mensagem;
SELECT 'Execute: flask init-db para criar as tabelas' AS ProximoPasso;
SELECT 'Execute: flask seed-db para popular com dados de exemplo' AS Opcional;
