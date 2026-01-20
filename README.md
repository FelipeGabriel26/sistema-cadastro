# Sistema de Cadastro e Reservas (Ambiente de Testes)

Sistema profissional de gestão de reservas e controle de cadastro, focado em facilidade de uso e design moderno. Desenvolvido com Python (Flask) e MySQL como um projeto didático e de testes.

## 🚀 Funcionalidades

- **Gestão de Reservas:** Fluxo completo para Hotelaria e Estacionamentos.
- **Controle de Acesso:** Sistema de login com níveis de permissão (Admin, Funcionário e Cliente).
- **Painéis (Dashboards):** Interfaces específicas para cada tipo de usuário.
- **Checkout Formal:** Processo de finalização de reserva limpo e profissional.
- **Didática:** Código totalmente comentado em português para facilitar o aprendizado de desenvolvedores juniores.

## 🛠️ Tecnologias

- **Backend:** Python 3.13+, Flask, SQLAlchemy.
- **Banco de Dados:** MySQL (compatível com XAMPP).
- **Frontend:** HTML5, CSS3 Moderno (Baseado em variáveis e Grid), Font Awesome para ícones.

## 📦 Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/sistema-cadastro.git
   cd sistema-cadastro
   ```

2. **Crie o ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o Banco de Dados:**
   - Crie o banco de dados no seu MySQL (ex: `sistema_cadastro`).
   - Configure o arquivo `.env` com sua conexão:
     ```env
     DATABASE_URL=mysql+pymysql://root:@localhost/sistema_cadastro
     SECRET_KEY=sua_chave_secreta
     ```

5. **Inicialize o Sistema:**
   Use os comandos exclusivos em português:
   ```bash
   flask iniciar-banco   # Cria as tabelas necessárias
   flask popular-banco   # (Opcional) Cria usuários de teste: Admin, Func e Cliente
   ```

## ▶️ Como Executar

```bash
python app.py
```
Acesse em: `http://localhost:8080`

## 👥 Contas de Teste (Padrão)
Se você usou o comando `popular-banco`, pode entrar com:
- **Admin:** admin@sistema.com / senha: `admin123`
- **Funcionário:** joao@sistema.com / senha: `func123`
- **Cliente:** maria@email.com / senha: `cliente123`

---
Desenvolvido para fins de estudo e testes de sistemas.
