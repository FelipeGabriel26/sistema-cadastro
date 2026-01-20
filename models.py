from datetime import datetime
from decimal import Decimal, InvalidOperation
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializamos o SQLAlchemy que cuidará de salvar tudo no banco de dados automaticamente
db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    """
    Representa qualquer pessoa que usa o sistema: 
    Pode ser o Administrador (Donos), Funcionários ou Clientes.
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    telefone = db.Column(db.String(20), nullable=False)
    # A senha não é salva pura, mas sim uma "hash" (código embaralhado) por segurança
    senha_hash = db.Column(db.String(255), nullable=False)
    # Define se é ADM, FUNCIONARIO ou CLIENTE
    tipo_usuario = db.Column(db.Enum('ADM', 'FUNCIONARIO', 'CLIENTE'), nullable=False, default='CLIENTE')
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_visita = db.Column(db.DateTime, default=datetime.utcnow)
    total_visitas = db.Column(db.Integer, default=1)
    
    # Listas automáticas (Relacionamentos)
    reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic', foreign_keys='Reserva.cliente_id')
    pontos = db.relationship('RegistroPonto', backref='funcionario', lazy='dynamic')
    
    def set_senha(self, senha):
        """
        Transforma a senha digitada em um código secreto embaralhado (Hash).
        """
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        """
        Verifica se a senha que o usuário digitou confere com o código secreto do banco.
        """
        return check_password_hash(self.senha_hash, senha)
    
    def registrar_visita(self):
        """
        Atualiza a data da última vez que o usuário entrou e aumenta o contador de visitas.
        """
        self.ultima_visita = datetime.utcnow()
        self.total_visitas += 1
        db.session.commit()
    
    # Funções de ajuda para saber o tipo do usuário rapidamente
    def is_admin(self):
        return self.tipo_usuario == 'ADM'
    
    def is_funcionario(self):
        return self.tipo_usuario == 'FUNCIONARIO'
    
    def is_cliente(self):
        return self.tipo_usuario == 'CLIENTE'
    
    def to_dict(self):
        """Transforma os dados do usuário em um dicionário (útil para APIs)"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'tipo_usuario': self.tipo_usuario,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'ultima_visita': self.ultima_visita.isoformat() if self.ultima_visita else None,
            'total_visitas': self.total_visitas
        }
    
    def __repr__(self):
        return f'<Usuario {self.nome} ({self.tipo_usuario})>'


class Reserva(db.Model):
    """
    Representa uma vaga de garagem ou um quarto de hotel reservado.
    """
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    tipo_servico = db.Column(db.Enum('HOTEL', 'GARAGEM'), nullable=False)
    
    # Detalhes dependendo do serviço
    placa_veiculo = db.Column(db.String(10), nullable=True)  # Se for Garagem
    numero_quarto = db.Column(db.String(10), nullable=True)  # Se for Hotel
    numero_vaga = db.Column(db.String(10), nullable=True)    # Se for Garagem
    
    # Datas importantes
    data_entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_saida_prevista = db.Column(db.DateTime, nullable=True)
    data_saida_real = db.Column(db.DateTime, nullable=True)
    
    # Dinheiro
    valor_base = db.Column(db.Numeric(10, 2), nullable=False)
    desconto_percentual = db.Column(db.Numeric(5, 2), default=0.0)
    valor_final = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Controle de status
    status = db.Column(db.Enum('ATIVA', 'FINALIZADA', 'CANCELADA'), default='ATIVA')
    observacoes = db.Column(db.Text, nullable=True)
    
    # Ligação com o funcionário que atendeu
    funcionario = db.relationship('Usuario', foreign_keys=[funcionario_id])
    
    def calcular_valor_final(self):
        """
        Faz a conta: Valor Base menos a porcentagem de desconto.
        """
        try:
            base = Decimal(str(self.valor_base))
            desconto_pct = Decimal(str(self.desconto_percentual)) / Decimal('100')
            desconto = (base * desconto_pct).quantize(Decimal('0.01'))
            self.valor_final = (base - desconto).quantize(Decimal('0.01'))
        except (InvalidOperation, TypeError):
            self.valor_final = Decimal('0.00')
    
    def to_dict(self):
        """Transforma a reserva em um formato legível por computadores (JSON)"""
        return {
            'id': self.id,
            'cliente': self.cliente.nome if self.cliente else None,
            'funcionario': self.funcionario.nome if self.funcionario else None,
            'tipo_servico': self.tipo_servico,
            'placa_veiculo': self.placa_veiculo,
            'numero_quarto': self.numero_quarto,
            'numero_vaga': self.numero_vaga,
            'data_entrada': self.data_entrada.isoformat() if self.data_entrada else None,
            'data_saida_prevista': self.data_saida_prevista.isoformat() if self.data_saida_prevista else None,
            'data_saida_real': self.data_saida_real.isoformat() if self.data_saida_real else None,
            'valor_base': float(self.valor_base),
            'desconto_percentual': float(self.desconto_percentual),
            'valor_final': float(self.valor_final),
            'status': self.status,
            'observacoes': self.observacoes
        }
    
    def __repr__(self):
        return f'<Reserva {self.id} - {self.tipo_servico} - {self.status}>'


class RegistroPonto(db.Model):
    """
    Cofre de registros de entrada e saída dos funcionários para o RH.
    """
    __tablename__ = 'registros_ponto'
    
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    hora_entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hora_saida = db.Column(db.DateTime, nullable=True)
    total_horas = db.Column(db.Numeric(5, 2), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    def calcular_horas(self):
        """
        Sabe quanto tempo o funcionário trabalhou subtraindo entrada da saída.
        """
        if self.hora_saida:
            delta = self.hora_saida - self.hora_entrada
            try:
                horas = Decimal(str(delta.total_seconds())) / Decimal('3600')
                self.total_horas = horas.quantize(Decimal('0.01'))
            except (InvalidOperation, TypeError):
                self.total_horas = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'funcionario': self.funcionario.nome,
            'data': self.data.isoformat() if self.data else None,
            'hora_entrada': self.hora_entrada.isoformat() if self.hora_entrada else None,
            'hora_saida': self.hora_saida.isoformat() if self.hora_saida else None,
            'total_horas': float(self.total_horas) if self.total_horas else None,
            'observacoes': self.observacoes
        }
    
    def __repr__(self):
        return f'<RegistroPonto {self.funcionario.nome} - {self.data}>'


class Promocao(db.Model):
    """
    Configurações de descontos especiais (ex: Natal, Cliente Fiel).
    """
    __tablename__ = 'promocoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    desconto_percentual = db.Column(db.Numeric(5, 2), nullable=False)
    tipo_servico = db.Column(db.Enum('HOTEL', 'GARAGEM', 'AMBOS'), default='AMBOS')
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    ativa = db.Column(db.Boolean, default=True)
    minimo_visitas = db.Column(db.Integer, default=0) # Só vale se o cliente já veio X vezes
    
    def is_valida(self):
        """
        Confere se a promoção ainda está no prazo e se não foi desligada.
        """
        agora = datetime.utcnow()
        return self.ativa and self.data_inicio <= agora <= self.data_fim
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'desconto_percentual': float(self.desconto_percentual),
            'tipo_servico': self.tipo_servico,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'ativa': self.ativa,
            'minimo_visitas': self.minimo_visitas
        }
    
    def __repr__(self):
        return f'<Promocao {self.nome} - {self.desconto_percentual}%>'
