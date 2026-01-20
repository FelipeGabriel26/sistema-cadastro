# ⚡ INÍCIO RÁPIDO - PowerShell

## 🚀 3 Passos para Rodar o Sistema

### 1️⃣ Setup (Primeira vez apenas)
```powershell
.\setup.ps1
```

### 2️⃣ Configurar .env
Edite o arquivo `.env` e coloque sua senha do MySQL:
```
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost/sistema_cadastro
```

### 3️⃣ Inicializar e Executar
```powershell
# Criar banco e tabelas
.\init-db.ps1

# Executar aplicação
.\run.ps1
```

## 🌐 Acessar
Abra: **http://localhost:5000**

## 🔑 Login
- **Admin**: admin@sistema.com / admin123
- **Funcionário**: joao@sistema.com / func123
- **Cliente**: maria@email.com / cliente123

---

## ❓ Problemas?

### Script não executa?
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro no MySQL?
1. Verifique se o MySQL está rodando
2. Crie o banco manualmente:
```sql
CREATE DATABASE sistema_cadastro;
```

### Mais ajuda?
Leia: `INSTALACAO_POWERSHELL.md`

---

**Pronto! Sistema funcionando! 🎉**
