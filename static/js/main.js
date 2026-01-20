// ==================== UTILITY FUNCTIONS ====================

/**
 * Exibe uma mensagem de alerta
 */
function showAlert(message, type = 'info') {
    const container = document.querySelector('.flash-messages') || createFlashContainer();

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button class="alert-close" onclick="this.parentElement.remove()">×</button>
    `;

    container.appendChild(alert);

    // Auto-remover após 5 segundos
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

/**
 * Cria o container de mensagens flash se não existir
 */
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

/**
 * Formata um valor monetário
 */
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

/**
 * Formata uma data no padrão brasileiro
 */
function formatarData(isoString) {
    if (!isoString) return '-';
    const data = new Date(isoString);
    return data.toLocaleDateString('pt-BR');
}

/**
 * Formata uma data e hora no padrão brasileiro
 */
function formatarDataHora(isoString) {
    if (!isoString) return '-';
    const data = new Date(isoString);
    return data.toLocaleDateString('pt-BR') + ' às ' +
        data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

/**
 * Formata apenas a hora
 */
function formatarHora(isoString) {
    if (!isoString) return '-';
    const data = new Date(isoString);
    return data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

/**
 * Valida CPF
 */
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');

    if (cpf.length !== 11) return false;

    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cpf)) return false;

    // Valida primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = 11 - (soma % 11);
    let digitoVerificador1 = resto === 10 || resto === 11 ? 0 : resto;

    if (digitoVerificador1 !== parseInt(cpf.charAt(9))) return false;

    // Valida segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = 11 - (soma % 11);
    let digitoVerificador2 = resto === 10 || resto === 11 ? 0 : resto;

    return digitoVerificador2 === parseInt(cpf.charAt(10));
}

/**
 * Valida email
 */
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Aplica máscara de CPF
 */
function mascaraCPF(valor) {
    valor = valor.replace(/\D/g, '');
    if (valor.length <= 11) {
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
        valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    return valor;
}

/**
 * Aplica máscara de telefone
 */
function mascaraTelefone(valor) {
    valor = valor.replace(/\D/g, '');
    if (valor.length <= 11) {
        valor = valor.replace(/(\d{2})(\d)/, '($1) $2');
        valor = valor.replace(/(\d{5})(\d)/, '$1-$2');
    }
    return valor;
}

/**
 * Aplica máscara de placa de veículo
 */
function mascaraPlaca(valor) {
    valor = valor.toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (valor.length <= 7) {
        valor = valor.replace(/(\w{3})(\w)/, '$1-$2');
    }
    return valor;
}

/**
 * Debounce para otimizar chamadas de funções
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Faz uma requisição fetch com tratamento de erros
 */
async function fetchWithErrorHandling(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || errorData.error || 'Erro na requisição');
        }

        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

/**
 * Cria um elemento de loading
 */
function createLoadingElement() {
    const loading = document.createElement('div');
    loading.className = 'spinner';
    return loading;
}

/**
 * Mostra loading em um elemento
 */
function showLoading(element) {
    const loading = createLoadingElement();
    element.innerHTML = '';
    element.appendChild(loading);
}

/**
 * Confirma uma ação com o usuário
 */
function confirmar(mensagem) {
    return confirm(mensagem);
}

/**
 * Copia texto para a área de transferência
 */
async function copiarParaClipboard(texto) {
    try {
        await navigator.clipboard.writeText(texto);
        showAlert('Copiado para a área de transferência!', 'success');
    } catch (error) {
        showAlert('Erro ao copiar', 'error');
    }
}

/**
 * Calcula a diferença em dias entre duas datas
 */
function diferencaEmDias(data1, data2) {
    const umDia = 24 * 60 * 60 * 1000;
    const primeiraData = new Date(data1);
    const segundaData = new Date(data2);

    return Math.round(Math.abs((primeiraData - segundaData) / umDia));
}

/**
 * Calcula a diferença em horas entre duas datas
 */
function diferencaEmHoras(data1, data2) {
    const umaHora = 60 * 60 * 1000;
    const primeiraData = new Date(data1);
    const segundaData = new Date(data2);

    return Math.round(Math.abs((primeiraData - segundaData) / umaHora));
}

/**
 * Gera um ID único
 */
function gerarId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * Scroll suave para um elemento
 */
function scrollParaElemento(elemento, offset = 0) {
    const elementoAlvo = typeof elemento === 'string'
        ? document.querySelector(elemento)
        : elemento;

    if (elementoAlvo) {
        const posicao = elementoAlvo.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({
            top: posicao,
            behavior: 'smooth'
        });
    }
}

/**
 * Verifica se um elemento está visível na viewport
 */
function estaVisivel(elemento) {
    const rect = elemento.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Adiciona animação de entrada aos elementos
 */
function animarEntrada(elementos, delay = 100) {
    const elementosArray = Array.isArray(elementos) ? elementos : [elementos];

    elementosArray.forEach((elemento, index) => {
        setTimeout(() => {
            elemento.style.opacity = '0';
            elemento.style.transform = 'translateY(20px)';
            elemento.style.transition = 'all 0.5s ease-out';

            setTimeout(() => {
                elemento.style.opacity = '1';
                elemento.style.transform = 'translateY(0)';
            }, 50);
        }, index * delay);
    });
}

/**
 * Salva dados no localStorage
 */
function salvarLocal(chave, valor) {
    try {
        localStorage.setItem(chave, JSON.stringify(valor));
        return true;
    } catch (error) {
        console.error('Erro ao salvar no localStorage:', error);
        return false;
    }
}

/**
 * Recupera dados do localStorage
 */
function recuperarLocal(chave) {
    try {
        const valor = localStorage.getItem(chave);
        return valor ? JSON.parse(valor) : null;
    } catch (error) {
        console.error('Erro ao recuperar do localStorage:', error);
        return null;
    }
}

/**
 * Remove dados do localStorage
 */
function removerLocal(chave) {
    try {
        localStorage.removeItem(chave);
        return true;
    } catch (error) {
        console.error('Erro ao remover do localStorage:', error);
        return false;
    }
}

// ==================== EVENT LISTENERS GLOBAIS ====================

// Fechar alertas ao clicar no X
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('alert-close')) {
        e.target.parentElement.remove();
    }
});

// Prevenir submit de formulários vazios
document.addEventListener('submit', (e) => {
    const form = e.target;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    let valido = true;
    inputs.forEach(input => {
        if (!input.value.trim()) {
            valido = false;
            input.style.borderColor = 'var(--error)';
        } else {
            input.style.borderColor = '';
        }
    });

    if (!valido) {
        e.preventDefault();
        showAlert('Por favor, preencha todos os campos obrigatórios', 'error');
    }
});

// Remover destaque de erro ao digitar
document.addEventListener('input', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
        e.target.style.borderColor = '';
    }
});

// ==================== INICIALIZAÇÃO ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Sistema de Cadastro inicializado');

    // Animar elementos na primeira carga
    const cards = document.querySelectorAll('.stat-card, .servico-card, .promocao-card');
    if (cards.length > 0) {
        animarEntrada(Array.from(cards), 100);
    }
});

// ==================== EXPORTS (se necessário) ====================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showAlert,
        formatarMoeda,
        formatarData,
        formatarDataHora,
        formatarHora,
        validarCPF,
        validarEmail,
        mascaraCPF,
        mascaraTelefone,
        mascaraPlaca,
        debounce,
        fetchWithErrorHandling,
        confirmar,
        copiarParaClipboard,
        diferencaEmDias,
        diferencaEmHoras,
        gerarId,
        scrollParaElemento,
        estaVisivel,
        animarEntrada,
        salvarLocal,
        recuperarLocal,
        removerLocal
    };
}
