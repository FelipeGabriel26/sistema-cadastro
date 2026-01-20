import socket
import pymysql
import os

print("\n" + "="*40)
print(" DIAGNÓSTICO DE BANCO DE DADOS (MySQL)")
print("="*40)

# 1. Verificar Portas Ativas
print("\n[1/2] Verificando portas do MySQL...")
ports_to_check = [3306, 3307, 3308, 8889]
active_port = None

for port in ports_to_check:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        print(f"  [OK] Encontrado serviço rodando na porta {port}!")
        active_port = port
        sock.close()
        break
    else:
        print(f"  [..] Nada na porta {port}")
    sock.close()

if not active_port:
    print("\n[ERRO CRÍTICO] O MySQL NÃO foi encontrado em nenhuma porta comum.")
    print("SOLUÇÃO: Abra o XAMPP e clique em 'Start' no MySQL.")
    print("         Verifique se a luz fica VERDE.")
    exit(1)

# 2. Tentar Conexão
print(f"\n[2/2] Tentando conectar na porta {active_port} com usuário 'root'...")
try:
    # Tenta sem senha (padrão XAMPP)
    conn = pymysql.connect(host='127.0.0.1', user='root', password='', port=active_port)
    print(f"  [SUCESSO] Conexão bem sucedida com senha vazia!")
    conn.close()
    
    if active_port != 3306:
        print(f"\n[ATENÇÃO] Seu MySQL está na porta {active_port}, mas o padrão é 3306.")
        print(f"PRECISAMOS AJUSTAR A CONFIGURAÇÃO.")
    else:
        print(f"\n[CONCLUSÃO] O banco está OK e acessível na porta {active_port}.")
        
except Exception as e:
    print(f"  [FALHA] Senha vazia não funcionou. Erro: {e}")
    print("  Tentando senha 'root'...")
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', port=active_port)
        print(f"  [SUCESSO] Conexão bem sucedida com senha 'root'!")
        conn.close()
    except Exception as e2:
        print(f"  [ERRO FINAL] Não foi possível conectar. Verifique sua senha.")

print("\n" + "="*40)
