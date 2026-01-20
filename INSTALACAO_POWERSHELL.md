# 🚀 Guia de Instalação - PowerShell

## ⚡ Instalação Rápida com PowerShell

### Pré-requisitos

1. **Python 3.8+** instalado
   - Download: https://www.python.org/downloads/
   - ✅ Marque "Add Python to PATH" durante instalação

2. **MySQL 8.0+** instalado e rodando
   - Download: https://dev.mysql.com/downloads/mysql/
   - ✅ Lembre-se da senha do root

3. **PowerShell** (já vem com Windows)

### 📋 Passo a Passo

#### 1. Abrir PowerShell no diretório do projeto

```powershell
# Navegue até a pasta do projeto
cd C:\Users\acer\Desktop\cadastro
```

#### 2. Permitir execução de scripts (se necessário)

```powershell
# Execute como Administrador (apenas uma vez)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Executar o setup automático

```powershell
# Execute o script de setup
.\setup.ps1
```

**O que o script faz:**
- ✅ Verifica Python e MySQL
- ✅ Cria ambiente virtual
- ✅ Instala dependências
- ✅ Cria arquivo .env

#### 4. Configurar o arquivo .env

Abra o arquivo `.env` e configure suas credenciais do MySQL:

```env
DATABASE_URL=mysql+pymysql://root:SUA_SENHA_AQUI@localhost/sistema_cadastro
SECRET_KEY=sua_chave_secreta_super_segura_aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

**Substitua:**
- `SUA_SENHA_AQUI` pela senha do seu MySQL
- `sua_chave_secreta_super_segura_aqui` por uma chave aleatória

#### 5. Criar o banco de dados

**Opção A - Via MySQL Command Line:**
```powershell
mysql -u root -p < setup_database.sql
```

**Opção B - Manualmente no MySQL:**
```sql
CREATE DATABASE sistema_cadastro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 6. Inicializar o banco de dados

```powershell
# Execute o script de inicialização
.\init-db.ps1
```

**O script irá:**
- ✅ Criar todas as tabelas
- ✅ Perguntar se deseja dados de exemplo
- ✅ Criar usuários de teste (se escolher sim)

#### 7. Executar a aplicação

```powershell
# Execute o script de execução
.\run.ps1
```

**OU manualmente:**
```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar aplicação
python app.py
```

#### 8. Acessar o sistema

Abra seu navegador em: **http://localhost:5000**

### 👥 Usuários de Teste

Se você escolheu popular com dados de exemplo:

| Tipo | Email | Senha |
|------|-------|-------|
| 👨‍💼 Admin | admin@sistema.com | admin123 |
| 👔 Funcionário | joao@sistema.com | func123 |
| 👤 Cliente | maria@email.com | cliente123 |

## 🔧 Scripts PowerShell Disponíveis

### setup.ps1
**Instalação inicial do sistema**
```powershell
.\setup.ps1
```
- Cria ambiente virtual
- Instala dependências
- Configura .env

### init-db.ps1
**Inicializa o banco de dados**
```powershell
.\init-db.ps1
```
- Cria tabelas
- Popula dados de exemplo (opcional)

### run.ps1
**Executa a aplicação**
```powershell
.\run.ps1
```
- Ativa ambiente virtual
- Inicia servidor Flask

## ❌ Solução de Problemas

### Erro: "Não é possível executar scripts"

**Problema:** PowerShell bloqueando execução de scripts

**Solução:**
```powershell
# Execute como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Python não encontrado"

**Problema:** Python não está no PATH

**Solução:**
1. Reinstale Python marcando "Add Python to PATH"
2. OU adicione manualmente ao PATH:
   - Painel de Controle → Sistema → Variáveis de Ambiente
   - Adicione: `C:\Python3X` e `C:\Python3X\Scripts`

### Erro: "MySQL não encontrado"

**Problema:** MySQL não está no PATH ou não está rodando

**Solução:**
1. Verifique se o MySQL está rodando:
   - Serviços do Windows → MySQL → Iniciar
2. Adicione MySQL ao PATH se necessário

### Erro: "Access denied for user"

**Problema:** Credenciais incorretas no .env

**Solução:**
1. Abra `.env`
2. Verifique usuário e senha do MySQL
3. Teste a conexão no MySQL Workbench

### Erro: "Unknown database"

**Problema:** Banco de dados não foi criado

**Solução:**
```powershell
# Criar banco manualmente
mysql -u root -p
```
```sql
CREATE DATABASE sistema_cadastro;
exit;
```

### Erro: "Port 5000 already in use"

**Problema:** Porta 5000 já está em uso

**Solução:**
Edite `app.py` na última linha:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🎯 Comandos Úteis

### Ativar ambiente virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### Desativar ambiente virtual
```powershell
deactivate
```

### Instalar nova dependência
```powershell
.\venv\Scripts\Activate.ps1
pip install nome-do-pacote
pip freeze > requirements.txt
```

### Resetar banco de dados
```powershell
.\venv\Scripts\Activate.ps1
flask init-db
flask seed-db
```

### Ver logs do MySQL
```powershell
# No MySQL
mysql -u root -p
SHOW DATABASES;
USE sistema_cadastro;
SHOW TABLES;
```

## 📊 Verificação da Instalação

Execute estes comandos para verificar se tudo está OK:

```powershell
# 1. Verificar Python
python --version
# Deve mostrar: Python 3.8.x ou superior

# 2. Verificar pip
pip --version
# Deve mostrar a versão do pip

# 3. Verificar MySQL
mysql --version
# Deve mostrar a versão do MySQL

# 4. Verificar ambiente virtual
.\venv\Scripts\Activate.ps1
python -c "import flask; print(flask.__version__)"
# Deve mostrar: 3.0.0 ou similar

# 5. Verificar banco de dados
mysql -u root -p -e "SHOW DATABASES LIKE 'sistema_cadastro';"
# Deve mostrar: sistema_cadastro
```

## 🔄 Atualização do Sistema

Para atualizar o sistema após mudanças no código:

```powershell
# 1. Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# 2. Atualizar dependências (se necessário)
pip install -r requirements.txt

# 3. Atualizar banco de dados (se necessário)
flask init-db

# 4. Reiniciar aplicação
python app.py
```

## 🎓 Próximos Passos

Após a instalação bem-sucedida:

1. ✅ Teste o login com usuários de exemplo
2. ✅ Explore cada dashboard (Admin, Funcionário, Cliente)
3. ✅ Crie uma reserva de teste
4. ✅ Leia a documentação completa em `README.md`
5. ✅ Execute os testes em `TESTES.md`

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs no terminal
2. Consulte `TESTES.md` - Seção "Problemas Comuns"
3. Revise `GUIA_RAPIDO.md`
4. Verifique se todos os pré-requisitos estão instalados

## ✨ Dicas

- **Use sempre o ambiente virtual** para evitar conflitos
- **Faça backup** do banco de dados antes de mudanças
- **Mantenha o MySQL rodando** enquanto usa o sistema
- **Leia os logs** para entender erros
- **Teste com dados de exemplo** antes de usar dados reais

---

**Instalação via PowerShell concluída! 🎉**

**Execute `.\run.ps1` para iniciar o sistema!**
