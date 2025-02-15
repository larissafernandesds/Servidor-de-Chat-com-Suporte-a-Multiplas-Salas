import socket
import threading
import time

# Configurações
HOST = "127.0.0.1" # IP servidor
PORT = 6789 
NUM_CONNECTIONS = 500 # Número de clientes simultâneos
TEMPO_DE_ESPERA = 5  # Tempo em segundos antes de todos se desconectarem

# Lock para sincronizar os prints
print_lock = threading.Lock()

# Função para receber dados completos do servidor
def receive_full_response(sock, buffer_size=1024, delimiter="\n"):
    data = ""
    while True:
        part = sock.recv(buffer_size).decode("utf-8")
        data += part
        if delimiter in data:
            break
    return data

# Função para simular conexões
def connect_to_server(user_id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        with print_lock:
            print(f"User-{user_id} conectado ao servidor.")

        # Envia o apelido
        apelido = f"User-{user_id}"
        s.sendall(apelido.encode("utf-8"))
        
        # Aguarda a resposta do servidor após enviar o apelido
        resposta_apelido = receive_full_response(s)
        with print_lock:
            print(f"User-{user_id}: Resposta do servidor (apelido): {resposta_apelido}")

        # Nome da sala compartilhada por todos
        sala_nome = "sala_unica"
        
        # Cria a sala (apenas o primeiro cliente, ou pode ser opcional)
        if user_id == 0:  # Apenas o primeiro cliente cria a sala
            s.sendall(f"/criar {sala_nome}".encode("utf-8"))
            resposta_criar = receive_full_response(s)
            with print_lock:
                print(f"User-{user_id}: Resposta do servidor (criar sala): {resposta_criar}")
        
        # Todos os clientes entram na mesma sala
        s.sendall(f"/entrar {sala_nome}".encode("utf-8"))
        resposta_entrar = receive_full_response(s)
        with print_lock:
            print(f"User-{user_id}: Resposta do servidor (entrar na sala): {resposta_entrar}")
        
        # Envia uma mensagem
        s.sendall("Olá, sala!".encode("utf-8"))
        resposta_mensagem = receive_full_response(s)
        with print_lock:
            print(f"User-{user_id}: Resposta do servidor (mensagem): {resposta_mensagem}")
        
        # Aguarda o tempo de espera antes de desconectar
        time.sleep(TEMPO_DE_ESPERA)
        
        # Envia o comando de desconexão
        s.sendall("/sair_chat".encode("utf-8"))
        resposta_sair = receive_full_response(s)
        with print_lock:
            print(f"User-{user_id}: Resposta do servidor (sair): {resposta_sair}")
        
        # Fecha a conexão
        s.close()
        with print_lock:
            print(f"User-{user_id} desconectado.")
    except Exception as e:
        with print_lock:
            print(f"Erro na conexão do User-{user_id}: {e}")

# Criar múltiplas conexões
threads = []
for i in range(NUM_CONNECTIONS):
    t = threading.Thread(target=connect_to_server, args=(i,))
    threads.append(t)
    t.start()

# Aguardar todas as threads finalizarem
for t in threads:
    t.join()

print("Todas as conexões foram encerradas.")