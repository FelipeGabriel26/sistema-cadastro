# 🚀 Guia Rápido de Início

## ⚡ Instalação Rápida (Windows)

### Opção 1: Automática (Recomendado)
```bash
# Execute o script de setup
setup.bat
```

### Opção 2: Manual

1. **Criar ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Instalar dependências**
```bash
pip install -r requirements.txt
```

3. **Configurar MySQL**
```bash
# No MySQL, execute:
mysql -u root -p < setup_database.sql

# OU manualmente:
CREATE DATABASE sistema_cadastro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. **Configurar .env**
```
Edite o arquivo .env com suas credenciais do MySQL
```

5. **Inicializar banco de dados**
```bash
flask init-db
flask seed-db
```

6. **Executar aplicação**
```bash
python app.py
# OU
run.bat
```

## 🔑 Acessar o Sistema

Abra seu navegador em: **http://localhost:5000**

### Usuários de Teste

| Tipo | Email | Senha |
|------|-------|-------|
| 👨‍💼 Admin | admin@sistema.com | admin123 |
| 👔 Funcionário | joao@sistema.com | func123 |
| 👤 Cliente | maria@email.com | cliente123 |

## 📱 Funcionalidades por Usuário

### 👨‍💼 Administrador
- ✅ Ver todas as estatísticas do sistema
- ✅ Gerenciar usuários (clientes, funcionários, admins)
- ✅ Verificar presença de funcionários
- ✅ Analisar clientes frequentes (3-18 meses)
- ✅ Visualizar receita total

### 👔 Funcionário
- ✅ Bater ponto (entrada/saída)
- ✅ Criar reservas para clientes
- ✅ Aplicar promoções
- ✅ Ver histórico de ponto
- ✅ Auxiliar clientes

### 👤 Cliente
- ✅ Fazer reservas (hotel ou garagem)
- ✅ Ver histórico de reservas
- ✅ Acessar promoções exclusivas
- ✅ Mensagem de boas-vindas personalizada

## 🎯 Fluxo de Uso Típico

### Para Clientes Novos:
1. Acesse http://localhost:5000
2. Clique em "Cadastre-se"
3. Preencha seus dados (nome, CPF, email, telefone, senha)
4. Faça login
5. Escolha entre Hotel ou Garagem
6. Preencha os detalhes da reserva
7. Confirme!

### Para Funcionários:
1. Faça login
2. Bata o ponto (entrada)
3. Crie reservas para clientes usando o CPF deles
4. Aplique promoções quando aplicável
5. Ao final do dia, bata o ponto (saída)

### Para Administradores:
1. Faça login
2. Visualize estatísticas em tempo real
3. Gerencie usuários na aba "Usuários"
4. Verifique presença na aba "Presença"
5. Analise clientes frequentes na aba "Clientes Frequentes"

## 🔧 Solução Rápida de Problemas

### ❌ Erro: "No module named 'flask'"
```bash
# Certifique-se de ativar o ambiente virtual
venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ Erro de conexão MySQL
```bash
# Verifique se o MySQL está rodando
# Verifique as credenciais no arquivo .env
# Certifique-se de que o banco foi criado
```

### ❌ Porta 5000 em uso
```python
# Em app.py, linha final, altere:
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📊 Estrutura de Dados

### Tipos de Serviço:
- **HOTEL**: Requer número do quarto (opcional)
- **GARAGEM**: Requer placa do veículo e vaga (opcional)

### Status de Reserva:
- **ATIVA**: Reserva em andamento
- **FINALIZADA**: Reserva concluída
- **CANCELADA**: Reserva cancelada

### Tipos de Usuário:
- **ADM**: Acesso total ao sistema
- **FUNCIONARIO**: Acesso a criação de reservas e ponto
- **CLIENTE**: Acesso a suas próprias reservas

## 🎨 Personalização

### Alterar cores do tema:
Edite `static/css/style.css` nas variáveis CSS (`:root`)

### Adicionar novos campos:
1. Adicione no modelo em `models.py`
2. Execute `flask init-db` novamente
3. Atualize os formulários nos templates

### Criar novos tipos de usuário:
Modifique o enum em `models.py` no campo `tipo_usuario`

## 📞 Comandos Úteis

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco
flask init-db

# Popular com dados de teste
flask seed-db

# Executar aplicação
python app.py

# Desativar ambiente virtual
deactivate
```

## 🌟 Dicas

1. **Sempre ative o ambiente virtual** antes de executar comandos
2. **Use dados reais** apenas em produção
3. **Faça backup** do banco de dados regularmente
4. **Mude a SECRET_KEY** em produção
5. **Use HTTPS** em produção

## 📈 Próximos Passos

Após dominar o básico:
- Explore as APIs REST disponíveis
- Personalize o design
- Adicione novos relatórios
- Implemente notificações
- Adicione exportação de dados (PDF, Excel)

---

**Pronto para começar? Execute `setup.bat` ou siga o guia manual acima!** 🚀
