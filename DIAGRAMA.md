# 📊 Diagrama do Sistema

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     NAVEGADOR WEB                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Admin   │  │Funcionário│  │ Cliente  │                  │
│  └────┬─────┘  └─────┬────┘  └────┬─────┘                  │
└───────┼──────────────┼────────────┼─────────────────────────┘
        │              │            │
        └──────────────┴────────────┘
                       │
        ┌──────────────▼──────────────┐
        │      FLASK APPLICATION       │
        │  ┌────────────────────────┐ │
        │  │   Routes & Controllers │ │
        │  └───────────┬────────────┘ │
        │              │               │
        │  ┌───────────▼────────────┐ │
        │  │   Business Logic       │ │
        │  │  - Autenticação        │ │
        │  │  - Validações          │ │
        │  │  - Cálculos            │ │
        │  └───────────┬────────────┘ │
        │              │               │
        │  ┌───────────▼────────────┐ │
        │  │   SQLAlchemy ORM       │ │
        │  └───────────┬────────────┘ │
        └──────────────┼───────────────┘
                       │
        ┌──────────────▼──────────────┐
        │      MySQL DATABASE          │
        │  ┌────────────────────────┐ │
        │  │  Tabelas:              │ │
        │  │  - usuarios            │ │
        │  │  - reservas            │ │
        │  │  - registros_ponto     │ │
        │  │  - promocoes           │ │
        │  └────────────────────────┘ │
        └─────────────────────────────┘
```

## 🔄 Fluxo de Dados

### Autenticação
```
Cliente → Login Form → Flask → Verificar Senha → MySQL
                                      ↓
                              Criar Sessão
                                      ↓
                              Redirecionar Dashboard
```

### Criação de Reserva (Cliente)
```
Cliente → Seleciona Serviço → Preenche Dados → Submit
                                                   ↓
                                            Flask Valida
                                                   ↓
                                            Salva no MySQL
                                                   ↓
                                            Retorna Confirmação
```

### Registro de Ponto (Funcionário)
```
Funcionário → Clica "Bater Ponto" → Flask
                                       ↓
                              Verifica Último Registro
                                       ↓
                        Entrada ou Saída? → MySQL
                                       ↓
                              Atualiza Interface
```

## 📁 Estrutura de Arquivos Detalhada

```
cadastro/
│
├── 📄 app.py                    # Aplicação principal Flask
│   ├── Rotas de autenticação
│   ├── Dashboards
│   └── APIs REST
│
├── 📄 models.py                 # Modelos do banco de dados
│   ├── Usuario
│   ├── Reserva
│   ├── RegistroPonto
│   └── Promocao
│
├── 📄 config.py                 # Configurações
│   └── Variáveis de ambiente
│
├── 📄 requirements.txt          # Dependências Python
│
├── 📄 .env                      # Variáveis de ambiente (não versionar)
├── 📄 .env.example              # Exemplo de .env
├── 📄 .gitignore                # Arquivos ignorados pelo Git
│
├── 📄 README.md                 # Documentação completa
├── 📄 GUIA_RAPIDO.md            # Guia de início rápido
├── 📄 DIAGRAMA.md               # Este arquivo
│
├── 📄 setup.bat                 # Script de instalação (Windows)
├── 📄 run.bat                   # Script para executar (Windows)
├── 📄 setup_database.sql        # Script SQL inicial
│
├── 📁 static/                   # Arquivos estáticos
│   ├── 📁 css/
│   │   └── 📄 style.css        # Estilos CSS completos
│   └── 📁 js/
│       └── 📄 main.js          # JavaScript principal
│
└── 📁 templates/                # Templates HTML
    ├── 📄 base.html            # Template base
    ├── 📄 login.html           # Página de login
    ├── 📄 registro.html        # Página de registro
    ├── 📄 dashboard_admin.html # Dashboard Admin
    ├── 📄 dashboard_funcionario.html # Dashboard Funcionário
    └── 📄 dashboard_cliente.html     # Dashboard Cliente
```

## 🗄️ Modelo de Dados (ER)

```
┌─────────────────────────────────────────────────┐
│                   USUARIOS                       │
├─────────────────────────────────────────────────┤
│ PK │ id (INT)                                   │
│    │ nome (VARCHAR)                             │
│    │ email (VARCHAR) UNIQUE                     │
│    │ cpf (VARCHAR) UNIQUE                       │
│    │ telefone (VARCHAR)                         │
│    │ senha_hash (VARCHAR)                       │
│    │ tipo_usuario (ENUM: ADM, FUNCIONARIO, CLIENTE) │
│    │ ativo (BOOLEAN)                            │
│    │ data_cadastro (DATETIME)                   │
│    │ ultima_visita (DATETIME)                   │
│    │ total_visitas (INT)                        │
└─────────────────────────────────────────────────┘
         │                    │
         │                    │
         ▼                    ▼
┌──────────────────┐  ┌──────────────────┐
│    RESERVAS      │  │ REGISTROS_PONTO  │
├──────────────────┤  ├──────────────────┤
│ PK │ id          │  │ PK │ id          │
│ FK │ cliente_id  │  │ FK │funcionario_id│
│ FK │funcionario_id│ │    │ data        │
│    │tipo_servico │  │    │hora_entrada │
│    │placa_veiculo│  │    │hora_saida   │
│    │numero_quarto│  │    │total_horas  │
│    │numero_vaga  │  │    │observacoes  │
│    │data_entrada │  └──────────────────┘
│    │data_saida_* │
│    │valor_base   │
│    │desconto_%   │
│    │valor_final  │
│    │status       │
│    │observacoes  │
└──────────────────┘

┌─────────────────────────┐
│      PROMOCOES          │
├─────────────────────────┤
│ PK │ id                 │
│    │ nome               │
│    │ descricao          │
│    │ desconto_percentual│
│    │ tipo_servico       │
│    │ data_inicio        │
│    │ data_fim           │
│    │ ativa              │
│    │ minimo_visitas     │
└─────────────────────────┘
```

## 🎯 Casos de Uso Principais

### 1. Cliente Novo se Cadastra
```
1. Acessa /registro
2. Preenche formulário
3. Sistema valida dados
4. Verifica se CPF/email já existe
5. Cria usuário com tipo CLIENTE
6. Redireciona para login
```

### 2. Cliente Retornante Faz Login
```
1. Acessa /login
2. Insere email e senha
3. Sistema verifica credenciais
4. Incrementa total_visitas
5. Atualiza ultima_visita
6. Mostra mensagem de boas-vindas personalizada
7. Redireciona para dashboard
```

### 3. Funcionário Cria Reserva
```
1. Acessa dashboard funcionário
2. Clica em "Nova Reserva"
3. Insere CPF do cliente
4. Sistema busca cliente
5. Seleciona tipo de serviço
6. Preenche detalhes
7. Aplica promoção (se aplicável)
8. Sistema calcula valor final
9. Confirma reserva
10. Salva no banco de dados
```

### 4. Admin Analisa Clientes Frequentes
```
1. Acessa dashboard admin
2. Clica em "Clientes Frequentes"
3. Seleciona período (3-18 meses)
4. Sistema consulta banco de dados
5. Ordena por total_visitas
6. Exibe top 10 clientes
7. Mostra estatísticas de cada um
```

## 🔐 Níveis de Acesso

```
┌─────────────────────────────────────────────────┐
│                    ADM                           │
│  ✓ Todas as funcionalidades                     │
│  ✓ Ver todos os usuários                        │
│  ✓ Ver todas as reservas                        │
│  ✓ Ver presença de funcionários                 │
│  ✓ Análises e relatórios                        │
│  ✓ Estatísticas completas                       │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌──────────────────┐      ┌──────────────────┐
│   FUNCIONARIO    │      │     CLIENTE      │
│  ✓ Bater ponto   │      │  ✓ Fazer reservas│
│  ✓ Criar reservas│      │  ✓ Ver histórico │
│  ✓ Ver promoções │      │  ✓ Ver promoções │
│  ✓ Aplicar desc. │      │  ✓ Perfil próprio│
│  ✓ Ver histórico │      └──────────────────┘
│    de ponto      │
└──────────────────┘
```

## 🚀 Fluxo de Inicialização

```
1. Instalar Python 3.8+
        ↓
2. Instalar MySQL 8.0+
        ↓
3. Clonar/Baixar projeto
        ↓
4. Executar setup.bat
        ↓
5. Criar ambiente virtual
        ↓
6. Instalar dependências
        ↓
7. Configurar .env
        ↓
8. Criar banco de dados
        ↓
9. Executar flask init-db
        ↓
10. Executar flask seed-db (opcional)
        ↓
11. Executar python app.py
        ↓
12. Acessar http://localhost:5000
```

## 📊 Tecnologias e Versões

```
Backend:
├── Python 3.8+
├── Flask 3.0.0
├── SQLAlchemy 3.1.1
├── Flask-Login 0.6.3
├── PyMySQL 1.1.0
└── Werkzeug 3.0.1

Frontend:
├── HTML5
├── CSS3 (Vanilla)
├── JavaScript ES6+
└── Google Fonts (Inter)

Database:
└── MySQL 8.0+

Design:
├── Dark Theme
├── Gradients
├── Animations
└── Responsive Layout
```

---

**Este diagrama fornece uma visão completa da arquitetura e funcionamento do sistema!** 📊
