# 🧪 Guia de Testes do Sistema

## 📋 Checklist de Testes

### ✅ Testes de Instalação

- [ ] Python 3.8+ instalado
- [ ] MySQL 8.0+ instalado e rodando
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas sem erros
- [ ] Arquivo .env configurado corretamente
- [ ] Banco de dados criado
- [ ] Tabelas criadas (flask init-db)
- [ ] Dados de exemplo carregados (flask seed-db)
- [ ] Aplicação inicia sem erros

### ✅ Testes de Autenticação

#### Registro de Novo Cliente
1. [ ] Acessar http://localhost:5000
2. [ ] Clicar em "Cadastre-se"
3. [ ] Preencher todos os campos:
   - Nome: Teste Silva
   - CPF: 123.456.789-00
   - Telefone: (11) 98765-4321
   - Email: teste@email.com
   - Senha: teste123
4. [ ] Verificar máscaras automáticas (CPF e telefone)
5. [ ] Submeter formulário
6. [ ] Verificar mensagem de sucesso
7. [ ] Verificar redirecionamento para login

#### Login
1. [ ] Fazer login com usuário criado
2. [ ] Verificar mensagem de boas-vindas
3. [ ] Verificar redirecionamento para dashboard correto
4. [ ] Verificar nome do usuário no navbar
5. [ ] Verificar badge de tipo de usuário

#### Teste de Cliente Retornante
1. [ ] Fazer logout
2. [ ] Fazer login novamente
3. [ ] Verificar mensagem "Bem-vindo de volta!"
4. [ ] Verificar incremento no contador de visitas

### ✅ Testes do Dashboard Cliente

#### Visualização Inicial
1. [ ] Verificar card de boas-vindas
2. [ ] Verificar data de cadastro
3. [ ] Verificar total de visitas
4. [ ] Verificar tabs (Nova Reserva, Minhas Reservas, Promoções)

#### Criar Reserva - Hotel
1. [ ] Clicar em "Nova Reserva"
2. [ ] Selecionar "Hotel"
3. [ ] Preencher número do quarto (opcional): 101
4. [ ] Selecionar data de saída
5. [ ] Verificar valor exibido
6. [ ] Confirmar reserva
7. [ ] Verificar mensagem de sucesso

#### Criar Reserva - Garagem
1. [ ] Clicar em "Nova Reserva"
2. [ ] Selecionar "Garagem"
3. [ ] Preencher placa: ABC-1234
4. [ ] Preencher vaga (opcional): A-15
5. [ ] Selecionar data de saída
6. [ ] Verificar valor exibido
7. [ ] Confirmar reserva
8. [ ] Verificar mensagem de sucesso

#### Visualizar Reservas
1. [ ] Clicar em "Minhas Reservas"
2. [ ] Verificar lista de reservas
3. [ ] Verificar informações corretas
4. [ ] Verificar status (Ativa)
5. [ ] Verificar valores

#### Visualizar Promoções
1. [ ] Clicar em "Promoções"
2. [ ] Verificar promoções disponíveis
3. [ ] Verificar detalhes das promoções
4. [ ] Verificar requisitos

### ✅ Testes do Dashboard Funcionário

#### Login como Funcionário
1. [ ] Fazer logout
2. [ ] Login: joao@sistema.com / func123
3. [ ] Verificar redirecionamento para dashboard funcionário

#### Registro de Ponto
1. [ ] Verificar status inicial (não bateu ponto)
2. [ ] Clicar em "Bater Ponto" (entrada)
3. [ ] Verificar mensagem de sucesso
4. [ ] Verificar status atualizado (trabalhando)
5. [ ] Verificar hora de entrada exibida
6. [ ] Clicar em "Bater Ponto" (saída)
7. [ ] Verificar mensagem de sucesso
8. [ ] Verificar total de horas calculado

#### Criar Reserva para Cliente
1. [ ] Clicar em "Nova Reserva"
2. [ ] Inserir CPF do cliente: 222.222.222-22
3. [ ] Selecionar tipo de serviço: Hotel
4. [ ] Preencher detalhes
5. [ ] Selecionar promoção (se disponível)
6. [ ] Verificar cálculo do valor final
7. [ ] Confirmar reserva
8. [ ] Verificar mensagem de sucesso

#### Visualizar Promoções
1. [ ] Clicar em "Promoções"
2. [ ] Verificar lista de promoções ativas
3. [ ] Verificar detalhes

#### Histórico de Ponto
1. [ ] Clicar em "Meu Histórico"
2. [ ] Verificar registros de ponto
3. [ ] Verificar cálculo de horas
4. [ ] Verificar datas corretas

### ✅ Testes do Dashboard Administrador

#### Login como Admin
1. [ ] Fazer logout
2. [ ] Login: admin@sistema.com / admin123
3. [ ] Verificar redirecionamento para dashboard admin

#### Estatísticas
1. [ ] Verificar card "Clientes" (número correto)
2. [ ] Verificar card "Funcionários" (número correto)
3. [ ] Verificar card "Reservas Ativas"
4. [ ] Verificar card "Receita Total"

#### Gerenciar Usuários
1. [ ] Verificar tab "Usuários" ativa por padrão
2. [ ] Verificar lista de todos os usuários
3. [ ] Testar filtro por tipo:
   - [ ] Todos
   - [ ] Clientes
   - [ ] Funcionários
   - [ ] Administradores
4. [ ] Verificar informações exibidas:
   - [ ] ID
   - [ ] Nome
   - [ ] Email
   - [ ] CPF
   - [ ] Tipo
   - [ ] Visitas
   - [ ] Última visita
   - [ ] Status

#### Presença de Funcionários
1. [ ] Clicar em tab "Presença"
2. [ ] Verificar lista de funcionários
3. [ ] Verificar status (Presente/Ausente)
4. [ ] Verificar horários de entrada/saída

#### Clientes Frequentes
1. [ ] Clicar em tab "Clientes Frequentes"
2. [ ] Testar filtros de período:
   - [ ] 3 meses
   - [ ] 6 meses
   - [ ] 12 meses
   - [ ] 15 meses
   - [ ] 18 meses
3. [ ] Verificar ordenação por visitas
4. [ ] Verificar informações dos clientes

### ✅ Testes de Validação

#### Validação de Formulários
1. [ ] Tentar submeter formulário vazio
2. [ ] Verificar mensagens de erro
3. [ ] Verificar destaque em campos obrigatórios
4. [ ] Testar CPF inválido
5. [ ] Testar email inválido
6. [ ] Testar senha muito curta

#### Validação de Acesso
1. [ ] Tentar acessar dashboard admin como cliente
2. [ ] Verificar redirecionamento/erro
3. [ ] Tentar acessar rotas protegidas sem login
4. [ ] Verificar redirecionamento para login

### ✅ Testes de Interface

#### Responsividade
1. [ ] Redimensionar janela do navegador
2. [ ] Testar em diferentes tamanhos:
   - [ ] Desktop (1920x1080)
   - [ ] Tablet (768x1024)
   - [ ] Mobile (375x667)
3. [ ] Verificar menu responsivo
4. [ ] Verificar cards adaptáveis
5. [ ] Verificar tabelas responsivas

#### Animações
1. [ ] Verificar fade in ao carregar página
2. [ ] Verificar hover effects em cards
3. [ ] Verificar transições suaves
4. [ ] Verificar alertas animados

#### Alertas e Mensagens
1. [ ] Verificar mensagens de sucesso
2. [ ] Verificar mensagens de erro
3. [ ] Verificar auto-fechamento (5 segundos)
4. [ ] Verificar botão de fechar manual

### ✅ Testes de Performance

1. [ ] Tempo de carregamento inicial < 2s
2. [ ] Tempo de resposta de APIs < 500ms
3. [ ] Animações suaves (60fps)
4. [ ] Sem travamentos ao navegar

### ✅ Testes de Segurança

1. [ ] Senhas não visíveis no código-fonte
2. [ ] Sessões expiram após logout
3. [ ] Não é possível acessar dados de outros usuários
4. [ ] SQL injection protegido (testar com ' OR '1'='1)
5. [ ] XSS protegido (testar com <script>alert('xss')</script>)

### ✅ Testes de Banco de Dados

1. [ ] Dados persistem após reiniciar aplicação
2. [ ] Relacionamentos funcionam corretamente
3. [ ] Cálculos automáticos corretos (horas, valores)
4. [ ] Datas armazenadas corretamente
5. [ ] Caracteres especiais salvos corretamente

## 🐛 Problemas Comuns e Soluções

### Erro: "No module named 'flask'"
**Solução**: Ativar ambiente virtual
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "Access denied for user"
**Solução**: Verificar credenciais no .env
```
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/sistema_cadastro
```

### Erro: "Unknown database 'sistema_cadastro'"
**Solução**: Criar banco de dados
```sql
CREATE DATABASE sistema_cadastro;
```

### Erro: "Table doesn't exist"
**Solução**: Inicializar tabelas
```bash
flask init-db
```

### Porta 5000 em uso
**Solução**: Alterar porta em app.py
```python
app.run(debug=True, port=5001)
```

## 📊 Relatório de Testes

Após completar todos os testes, preencha:

- **Data do teste**: _______________
- **Testador**: _______________
- **Versão**: 1.0.0
- **Testes passados**: ___ / ___
- **Testes falhados**: ___
- **Bugs encontrados**: ___
- **Status geral**: [ ] Aprovado [ ] Reprovado

## 🎯 Critérios de Aceitação

Para o sistema ser considerado aprovado:
- [ ] 100% dos testes de instalação passam
- [ ] 100% dos testes de autenticação passam
- [ ] 95%+ dos testes funcionais passam
- [ ] 90%+ dos testes de interface passam
- [ ] 100% dos testes de segurança passam
- [ ] Nenhum bug crítico encontrado

---

**Boa sorte com os testes! 🧪**
