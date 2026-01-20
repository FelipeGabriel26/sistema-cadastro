# Importação das bibliotecas necessárias para o funcionamento do sistema
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import func, extract, and_, or_
from config import Config
from models import db, Usuario, Reserva, RegistroPonto, Promocao
import os

# Criação da nossa aplicação Flask
app = Flask(__name__)
# Carregamos as configurações (Banco de Dados, Chave Secreta, etc) do arquivo config.py
app.config.from_object(Config)

# Inicializamos as extensões do banco de dados e CORS (permite acesso de diferentes domínios)
db.init_app(app)
CORS(app)

# Configuração do Sistema de Login (Flask-Login)
login_manager = LoginManager()
login_manager.init_app(app)
# Define para qual página o usuário deve ir se não estiver logado
login_manager.login_view = 'login'
# Mensagem que aparece quando o usuário tenta acessar algo proibido
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def carregar_usuario(id_usuario):
    """
    Função necessária para o Flask-Login saber como recuperar 
    o usuário do banco de dados usando o ID salvo na sessão.
    """
    return Usuario.query.get(int(id_usuario))


# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/')
def pagina_inicial():
    """
    Rota da Página Inicial.
    Mostra os serviços disponíveis e as promoções ativas.
    """
    # Buscamos as promoções ativas no banco de dados para mostrar na vitrine
    promocoes = Promocao.query.filter_by(ativa=True).all()
    return render_template('index.html', promocoes=promocoes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota de Entrada (Login).
    Gerencia o acesso dos usuários ao sistema.
    """
    # Se o usuário já estiver logado, não precisa logar de novo
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Se o usuário enviou o formulário (POST)
    if request.method == 'POST':
        # Pegamos o e-mail e a senha que foram digitados
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Procuramos o usuário no banco de dados
        usuario = Usuario.query.filter_by(email=email).first()
        
        # Passo 1: O e-mail existe?
        if not usuario:
            flash('Este email não possui conta. Por favor, cadastre-se.', 'info')
            return redirect(url_for('registro'))
            
        # Passo 2: A senha está correta? (A função verificar_senha faz a mágica)
        if usuario.verificar_senha(senha) and usuario.ativo:
            # Tudo certo! Iniciamos a sessão do usuário
            login_user(usuario, remember=True)
            # Registramos que ele entrou hoje (para fins de fidelidade)
            usuario.registrar_visita()
            
            # Avisamos que deu certo e mandamos para o Painel
            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
            return redirect(url_for('dashboard'))
        
        # Se a senha estiver errada
        flash('Senha incorreta. Tente novamente.', 'error')
    
    # Se for apenas um acesso comum (GET), mostramos o formulário
    return render_template('login.html')


@app.route('/logout')
@login_required
def sair():
    """
    Rota de Saída (Logout).
    Encerra a sessão do usuário com segurança.
    """
    logout_user() # Função do Flask-Login que apaga a sessão
    flash('Você saiu do sistema com sucesso.', 'info')
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Rota de Cadastro de novos usuários (Clientes).
    """
    # Se o formulário foi enviado
    if request.method == 'POST':
        # Pegamos todos os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')
        
        # Verificamos se já existe alguém com esse e-mail ou CPF
        usuario_existente = Usuario.query.filter(
            or_(Usuario.email == email, Usuario.cpf == cpf)
        ).first()
        
        if usuario_existente:
            flash('Já existe um cadastro com este E-mail ou CPF. Tente fazer login.', 'warning')
            return redirect(url_for('login'))
        
        # Criamos o novo objeto de Usuário (por padrão é do tipo CLIENTE)
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            cpf=cpf,
            telefone=telefone,
            tipo_usuario='CLIENTE'
        )
        # Transformamos a senha em um código embaralhado (HASH) por segurança
        novo_usuario.set_senha(senha)
        
        try:
            # Tentamos salvar no banco de dados
            db.session.add(novo_usuario)
            db.session.commit()
            
            flash('Sua conta foi criada com sucesso! Você já pode entrar.', 'success')
            return redirect(url_for('login'))
        except Exception as erro:
            # Caso aconteça algum erro imprevisto (ex: banco fora do ar)
            db.session.rollback()
            print(f"Erro no banco: {erro}")
            flash('Infelizmente ocorreu um erro ao salvar seus dados. Tente novamente.', 'error')
    
    # Mostra a tela de cadastro
    return render_template('registro.html')


# ==================== DASHBOARD ====================

# ==================== PAINÉIS DE CONTROLE (DASHBOARDS) ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard Principal.
    Identifica quem está logado e manda para o painel correto.
    """
    if current_user.is_admin():
        return redirect(url_for('painel_admin'))
    elif current_user.is_funcionario():
        return redirect(url_for('painel_funcionario'))
    else:
        # Usuário comum (Cliente)
        return redirect(url_for('painel_cliente'))


@app.route('/dashboard/admin')
@login_required
def painel_admin():
    """Painel Exclusivo do Administrador"""
    if not current_user.is_admin():
        flash('Você não tem permissão para acessar esta área.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard_admin.html')


@app.route('/dashboard/funcionario')
@login_required
def painel_funcionario():
    """Painel do Funcionário (Recepcionista/Garagem)"""
    if not current_user.is_funcionario():
        flash('Área restrita a funcionários.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard_funcionario.html')


@app.route('/dashboard/cliente')
@login_required
def painel_cliente():
    """Painel do Cliente - Histórico de Reservas"""
    if not current_user.is_cliente():
        flash('Acesso negado.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard_cliente.html')


# ==================== API - ESTATÍSTICAS PARA O ADMINISTRADOR ====================

@app.route('/api/admin/estatisticas')
@login_required
def api_admin_estatisticas():
    """
    Retorna números gerais do sistema para o painel do Admin.
    """
    if not current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    # Contagem de usuários registrados por tipo
    total_clientes = Usuario.query.filter_by(tipo_usuario='CLIENTE').count()
    total_funcionarios = Usuario.query.filter_by(tipo_usuario='FUNCIONARIO').count()
    total_admins = Usuario.query.filter_by(tipo_usuario='ADM').count()
    
    # Quantas reservas estão "ATIVAS" no momento
    reservas_ativas = Reserva.query.filter_by(status='ATIVA').count()
    
    # Soma de todo o dinheiro ganho com reservas FINALIZADAS
    receita_total = db.session.query(func.sum(Reserva.valor_final)).filter_by(status='FINALIZADA').scalar() or 0
    
    # Quantos funcionários bateram entrada e ainda não bateram saída hoje
    hoje = datetime.utcnow().date()
    funcionarios_presentes = RegistroPonto.query.filter(
        RegistroPonto.data == hoje,
        RegistroPonto.hora_saida.is_(None)
    ).count()
    
    return jsonify({
        'usuarios': {
            'clientes': total_clientes,
            'funcionarios': total_funcionarios,
            'admins': total_admins
        },
        'reservas_ativas': reservas_ativas,
        'receita_total': float(receita_total),
        'funcionarios_presentes': funcionarios_presentes
    })


@app.route('/api/admin/clientes-frequentes')
@login_required
def api_admin_clientes_frequentes():
    """Mostra quem são os clientes que mais visitam o estabelecimento"""
    if not current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    # Pegamos os últimos 12 meses por padrão
    meses_atras = request.args.get('meses', 12, type=int)
    data_limite = datetime.utcnow() - timedelta(days=30 * meses_atras)
    
    # Busca clientes e ordena pelos que têm mais visitas
    clientes = Usuario.query.filter(
        Usuario.tipo_usuario == 'CLIENTE',
        Usuario.ultima_visita >= data_limite
    ).order_by(Usuario.total_visitas.desc()).limit(10).all()
    
    return jsonify({
        'clientes': [
            {
                'id': c.id,
                'nome': c.nome,
                'email': c.email,
                'total_visitas': c.total_visitas,
                'ultima_visita': c.ultima_visita.isoformat() if c.ultima_visita else None
            }
            for c in clientes
        ]
    })


@app.route('/api/admin/usuarios')
@login_required
def api_admin_usuarios():
    """Lista todos os cadastros (pode filtrar por tipo via URL)"""
    if not current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    tipo_filtro = request.args.get('tipo', None)
    consulta = Usuario.query
    
    if tipo_filtro:
        consulta = consulta.filter_by(tipo_usuario=tipo_filtro)
    
    usuarios = consulta.all()
    return jsonify({'usuarios': [u.to_dict() for u in usuarios]})


@app.route('/api/admin/funcionarios-presenca')
@login_required
def api_admin_funcionarios_presenca():
    """Verifica quem dos funcionários está trabalhando agora"""
    if not current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    hoje = datetime.utcnow().date()
    
    # Pega todos os funcionários ativos
    lista_funcionarios = Usuario.query.filter_by(tipo_usuario='FUNCIONARIO', ativo=True).all()
    
    relatorio = []
    for func in lista_funcionarios:
        # Tenta achar o ponto de hoje desse funcionário
        ponto = RegistroPonto.query.filter_by(
            funcionario_id=func.id,
            data=hoje
        ).first()
        
        relatorio.append({
            'id': func.id,
            'nome': func.nome,
            'presente': ponto is not None and ponto.hora_saida is None,
            'hora_entrada': ponto.hora_entrada.isoformat() if ponto else None,
            'hora_saida': ponto.hora_saida.isoformat() if ponto and ponto.hora_saida else None
        })
    
    return jsonify({'funcionarios': relatorio})


# ==================== API - FUNCIONÁRIO ====================

@app.route('/api/funcionario/bater-ponto', methods=['POST'])
@login_required
def api_funcionario_bater_ponto():
    """Registra entrada ou saída do funcionário"""
    if not current_user.is_funcionario():
        return jsonify({'error': 'Acesso negado'}), 403
    
    hoje = datetime.utcnow().date()
    agora = datetime.utcnow()
    
    # Verificar se já bateu ponto hoje
    ponto_hoje = RegistroPonto.query.filter_by(
        funcionario_id=current_user.id,
        data=hoje
    ).first()
    
    if not ponto_hoje:
        # Registrar entrada
        ponto = RegistroPonto(
            funcionario_id=current_user.id,
            data=hoje,
            hora_entrada=agora
        )
        db.session.add(ponto)
        db.session.commit()
        return jsonify({
            'success': True,
            'tipo': 'entrada',
            'message': 'Entrada registrada com sucesso!',
            'hora': agora.isoformat()
        })
    elif not ponto_hoje.hora_saida:
        # Registrar saída
        ponto_hoje.hora_saida = agora
        ponto_hoje.calcular_horas()
        db.session.commit()
        return jsonify({
            'success': True,
            'tipo': 'saida',
            'message': 'Saída registrada com sucesso!',
            'hora': agora.isoformat(),
            'total_horas': float(ponto_hoje.total_horas)
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Você já completou o ponto de hoje'
        }), 400


@app.route('/api/funcionario/meu-ponto')
@login_required
def api_funcionario_meu_ponto():
    """Histórico de pontos do funcionário"""
    if not current_user.is_funcionario():
        return jsonify({'error': 'Acesso negado'}), 403
    
    pontos = RegistroPonto.query.filter_by(
        funcionario_id=current_user.id
    ).order_by(RegistroPonto.data.desc()).limit(30).all()
    
    return jsonify({'pontos': [p.to_dict() for p in pontos]})


@app.route('/api/funcionario/promocoes')
@login_required
def api_funcionario_promocoes():
    """Lista promoções ativas"""
    if not current_user.is_funcionario():
        return jsonify({'error': 'Acesso negado'}), 403
    
    agora = datetime.utcnow()
    promocoes = Promocao.query.filter(
        Promocao.ativa == True,
        Promocao.data_inicio <= agora,
        Promocao.data_fim >= agora
    ).all()
    
    return jsonify({'promocoes': [p.to_dict() for p in promocoes]})


@app.route('/api/funcionario/criar-reserva', methods=['POST'])
@login_required
def api_funcionario_criar_reserva():
    """Cria uma nova reserva para um cliente"""
    if not current_user.is_funcionario():
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    # Buscar cliente
    cliente = Usuario.query.filter_by(cpf=data.get('cpf_cliente')).first()
    if not cliente:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    # Criar reserva
    reserva = Reserva(
        cliente_id=cliente.id,
        funcionario_id=current_user.id,
        tipo_servico=data.get('tipo_servico'),
        placa_veiculo=data.get('placa_veiculo'),
        numero_quarto=data.get('numero_quarto'),
        numero_vaga=data.get('numero_vaga'),
        data_saida_prevista=datetime.fromisoformat(data.get('data_saida_prevista')) if data.get('data_saida_prevista') else None,
        valor_base=data.get('valor_base'),
        desconto_percentual=data.get('desconto_percentual', 0)
    )
    reserva.calcular_valor_final()
    
    db.session.add(reserva)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Reserva criada com sucesso!',
        'reserva': reserva.to_dict()
    })


# ==================== API - CLIENTE ====================

@app.route('/api/cliente/minhas-reservas')
@login_required
def api_cliente_minhas_reservas():
    """Lista reservas do cliente"""
    if not current_user.is_cliente():
        return jsonify({'error': 'Acesso negado'}), 403
    
    reservas = Reserva.query.filter_by(
        cliente_id=current_user.id
    ).order_by(Reserva.data_entrada.desc()).all()
    
    return jsonify({'reservas': [r.to_dict() for r in reservas]})


@app.route('/api/cliente/nova-reserva', methods=['POST'])
@login_required
def api_cliente_nova_reserva():
    """Cliente cria uma nova reserva"""
    if not current_user.is_cliente():
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    reserva = Reserva(
        cliente_id=current_user.id,
        tipo_servico=data.get('tipo_servico'),
        placa_veiculo=data.get('placa_veiculo'),
        numero_quarto=data.get('numero_quarto'),
        numero_vaga=data.get('numero_vaga'),
        data_saida_prevista=datetime.fromisoformat(data.get('data_saida_prevista')) if data.get('data_saida_prevista') else None,
        valor_base=data.get('valor_base'),
        desconto_percentual=0
    )
    reserva.calcular_valor_final()
    
    db.session.add(reserva)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Reserva criada com sucesso!',
        'reserva': reserva.to_dict()
    })


@app.route('/api/cliente/promocoes-disponiveis')
@login_required
def api_cliente_promocoes_disponiveis():
    """Promoções disponíveis para o cliente"""
    if not current_user.is_cliente():
        return jsonify({'error': 'Acesso negado'}), 403
    
    agora = datetime.utcnow()
    promocoes = Promocao.query.filter(
        Promocao.ativa == True,
        Promocao.data_inicio <= agora,
        Promocao.data_fim >= agora,
        Promocao.minimo_visitas <= current_user.total_visitas
    ).all()
    
    return jsonify({'promocoes': [p.to_dict() for p in promocoes]})


# ==================== CHECKOUT & LOJA ====================

# ==================== CHECKOUT E FINALIZAÇÃO DE RESERVA ====================

@app.route('/checkout')
def checkout():
    """Página onde o cliente finaliza a reserva (Checkout)"""
    tipo = request.args.get('tipo', 'HOTEL')
    # Definimos valores padrão para demonstração
    valor = 250 if tipo == 'HOTEL' else 35
    return render_template('checkout.html', tipo_servico=tipo, valor=valor)


@app.route('/checkout/processar', methods=['POST'])
def processar_checkout():
    """
    Recebe os dados do Checkout e cria a reserva no banco de dados.
    Suporta tanto clientes logados quanto 'convidados' (Guest).
    """
    dados = request.form
    usuario_atual = current_user
    
    # Se o usuário não estiver logado (Modo Convidado)
    if not usuario_atual.is_authenticated:
        if dados.get('guest_mode') == 'true':
            email = dados.get('email')
            cpf = dados.get('cpf')
            
            # Verificamos se esse e-mail ou CPF já tem conta real
            ja_existe = Usuario.query.filter(
                or_(Usuario.email == email, Usuario.cpf == cpf)
            ).first()
            
            if ja_existe:
                flash('Você já tem conta! Por favor, faça login para continuar.', 'warning')
                return redirect(url_for('login'))
            
            # Criamos uma conta automática para o convidado
            try:
                import secrets
                # Geramos uma senha aleatória que ele não sabe (depois ele pode resetar)
                senha_temporaria = secrets.token_urlsafe(8)
                
                novo_guest = Usuario(
                    nome=dados.get('nome'),
                    email=email,
                    cpf=cpf,
                    telefone=dados.get('telefone'),
                    tipo_usuario='CLIENTE'
                )
                novo_guest.set_senha(senha_temporaria)
                db.session.add(novo_guest)
                db.session.commit()
                
                # Logamos ele automaticamente para poder fazer a reserva
                login_user(novo_guest)
                usuario_atual = novo_guest
                
            except Exception as erro:
                db.session.rollback()
                flash(f'Erro ao criar sua conta de convidado: {erro}', 'error')
                return redirect(url_for('checkout', tipo=dados.get('tipo_servico')))
    
    # Agora que temos um usuário (seja logado ou convidado), criamos a Reserva
    try:
        tipo_servico = dados.get('tipo_servico')
        valor_base = dados.get('valor_base')
        
        # Criamos o objeto da Reserva com os dados que vieram do site
        nova_reserva = Reserva(
            cliente_id=usuario_atual.id,
            tipo_servico=tipo_servico,
            valor_base=valor_base,
            numero_quarto=dados.get('numero_quarto'),
            placa_veiculo=dados.get('placa_veiculo'),
            status='ATIVA'
        )
        
        # Chama a função do modelo que calcula descontos se houver
        nova_reserva.calcular_valor_final()
        
        # Salva tudo no banco de dados
        db.session.add(nova_reserva)
        db.session.commit()
        
        flash('Parabéns! Sua reserva foi realizada com sucesso.', 'success')
        return redirect(url_for('painel_cliente'))
        
    except Exception as erro:
        db.session.rollback()
        flash(f'Erro ao processar sua reserva: {erro}', 'error')
        return redirect(url_for('checkout', tipo=dados.get('tipo_servico')))


# ==================== COMANDOS DE TERMINAL (CLI) ====================

@app.cli.command()
def iniciar_banco():
    """Comando para criar as tabelas do banco de dados: flask iniciar-banco"""
    db.create_all()
    print('Sucesso! O banco de dados foi inicializado e as tabelas criadas.')


@app.cli.command()
def popular_banco():
    """Comando para colocar dados de teste no sistema: flask popular-banco"""
    
    # Criamos um Administrador para teste
    admin = Usuario(
        nome='Administrador do Sistema',
        email='admin@sistema.com',
        cpf='000.000.000-00',
        telefone='(00) 00000-0000',
        tipo_usuario='ADM'
    )
    admin.set_senha('admin123')
    
    # Criamos um Funcionário para teste
    funcionario = Usuario(
        nome='João Silva (Recepcionista)',
        email='joao@sistema.com',
        cpf='111.111.111-11',
        telefone='(11) 11111-1111',
        tipo_usuario='FUNCIONARIO'
    )
    funcionario.set_senha('func123')
    
    # Criamos um Cliente para teste
    cliente = Usuario(
        nome='Maria Santos (Cliente)',
        email='maria@email.com',
        cpf='222.222.222-22',
        telefone='(22) 22222-2222',
        tipo_usuario='CLIENTE'
    )
    cliente.set_senha('cliente123')
    
    # Criamos uma Promoção exemplo
    promocao = Promocao(
        nome='Desconto de Boas-Vindas',
        descricao='10% de desconto para todos os serviços este mês!',
        desconto_percentual=10,
        tipo_servico='AMBOS',
        data_inicio=datetime.utcnow(),
        data_fim=datetime.utcnow() + timedelta(days=30),
        minimo_visitas=0
    )
    
    # Adicionamos todos na lista para salvar
    db.session.add_all([admin, funcionario, cliente, promocao])
    db.session.commit()
    
    print('-----------------------------------------')
    print('DADOS DE TESTE CRIADOS COM SUCESSO!')
    print('Acesse com os dados abaixo:')
    print('Admin: admin@sistema.com / admin123')
    print('Funcionário: joao@sistema.com / func123')
    print('Cliente: maria@email.com / cliente123')
    print('-----------------------------------------')


# Início da aplicação
if __name__ == '__main__':
    # Rodamos o servidor na porta 8080 (padrão do sistema)
    app.run(debug=True, host='0.0.0.0', port=8080)
