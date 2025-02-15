import socket  # biblioteca para comunicação via rede
import threading # biblioteca para trabalhar com threads (execução paralela)

# dicionário que armazena as salas e seus respectivos clientes
salas = {}

def handle_client(client_socket, addr):
    """
    Função para gerenciar a comunicação com um cliente.
    
    Parâmetros:
    - client_socket: socket do cliente
    - addr: endereço IP e porta do cliente
    
    Retorno:
    - Sem retorno, a função gerencia a interação do cliente até que ele saia
    """
    
    # variável para armazenar a sala atual do cliente
    sala_atual = None
    nome = None  # nome será o apelido do cliente

    print(f"Nova conexão de {addr} (aguardando apelido...)")

    # solicita ao cliente seu apelido
    #client_socket.send("Digite seu apelido: ".encode("utf-8"))
    nome = client_socket.recv(1024).decode().strip()

    # caso o cliente não forneça um apelido, atribui um nome padrão
    if not nome:
        nome = f"Usuário-{addr[1]}"  

    print(f"Cliente conectado: {nome} ({addr})")
    client_socket.send("\n__Conectado ao servidor__\n".encode())
 

    # envia instruções para o cliente
    client_socket.send(f"\nBem-vindo(a) ao chat, {nome}! Use os comandos:\n"
                       "/salas - listar salas disponíveis\n"
                       "/criar <sala> - criar uma nova sala\n"
                       "/entrar <sala> - entrar em uma sala existente\n"
                       "/sair - sair da sala atual\n"
                       "/sair_chat - desconectar\n".encode("utf-8"))

    while True:
        try:
            # recebe a mensagem do cliente
            msg = client_socket.recv(1024).decode().strip()
            if not msg: # se a mensagem estiver vazia, encerra a conexão
                break
            
            # comando para listar salas disponíveis
            if msg.startswith("/salas"):
                salas_disponiveis = ", ".join(salas.keys()) if salas else "Nenhuma sala disponível."
                client_socket.send(f"Salas disponíveis: {salas_disponiveis}\n".encode("utf-8"))
    
            # comando para criar uma nova sala
            elif msg.startswith("/criar "):
                _, nome_sala = msg.split(maxsplit=1)
                if nome_sala in salas:
                    client_socket.send("⚠️ Essa sala já existe! Tente outro nome.\n".encode("utf-8"))
                else:
                    salas[nome_sala] = {"clientes": []}
                    client_socket.send(f"✅ Sala '{nome_sala}' criada com sucesso!\n".encode("utf-8"))

            # comando para entrar em uma sala existente
            elif msg.startswith("/entrar "):
                _, nome_sala = msg.split(maxsplit=1)
                if nome_sala not in salas:
                    client_socket.send("❌ Sala não encontrada. Use /salas para ver as disponíveis ou /criar para criar uma nova.\n".encode("utf-8"))
                else:
                    # remove o cliente da sala atual, se ele já estiver em uma
                    if sala_atual:
                        salas[sala_atual]["clientes"].remove(client_socket)
                        for cliente in salas[sala_atual]["clientes"]:
                            cliente.send(f"📝 {nome} saiu da sala '{sala_atual}'.\n".encode("utf-8"))

                    # adiciona o cliente à nova sala
                    salas[nome_sala]["clientes"].append(client_socket)
                    sala_atual = nome_sala

                    # avisa os outros membros da sala sobre a entrada do novo cliente
                    for cliente in salas[nome_sala]["clientes"]:
                        if cliente != client_socket:
                            cliente.send(f"📝 {nome} entrou na sala '{nome_sala}'.\n".encode("utf-8"))
                    client_socket.send(f"✅ Você entrou na sala '{nome_sala}'.\n".encode("utf-8"))

            # comando para sair da sala atual
            elif msg.startswith("/sair"):
                if sala_atual:
                    salas[sala_atual]["clientes"].remove(client_socket)
                    for cliente in salas.get(sala_atual, {}).get("clientes", []):
                        cliente.send(f"📝 {nome} saiu da sala '{sala_atual}'.\n".encode("utf-8"))
                    sala_atual = None
                    client_socket.send("🔹 Você saiu da sala.\n".encode("utf-8"))
                else:
                    client_socket.send("⚠️ Você não está em nenhuma sala.\n".encode("utf-8"))

            # comando para desconectar do chat
            elif msg.startswith("/sair_chat"):
                if sala_atual:
                    for cliente in salas[sala_atual]["clientes"]:
                        if cliente != client_socket:
                            cliente.send(f"👋 {nome} saiu do chat da sala '{sala_atual}'.\n".encode("utf-8"))
                client_socket.send("👋 Você saiu do chat.\n".encode("utf-8"))
                break
            
            # envio de mensagens normais dentro da sala
            else:
                if sala_atual:
                    mensagem = f"[{nome}] {msg}\n"
                    for cliente in salas[sala_atual]["clientes"]:
                        if cliente != client_socket:
                            cliente.send(mensagem.encode("utf-8"))
                else:
                    client_socket.send("⚠️ Você não está em nenhuma sala. Use /entrar <sala> para participar.\n".encode("utf-8"))
        # se houver erro na comunicação, encerra a conexão
        except:
            break
        
    # remove o cliente da sala e fecha a conexão ao sair
    if sala_atual and client_socket in salas.get(sala_atual, {}).get("clientes", []):
        salas[sala_atual]["clientes"].remove(client_socket)
        sala_atual = None  
   

    print(f"{nome} {addr} desconectou do chat.")
    client_socket.close()


def start_server():
    """
    Função responsável por iniciar o servidor e aceitar conexões de clientes.
    
    Retorno:
    - Sem retorno explícito, o servidor fica rodando...
    """
    server_ip = "127.0.0.1" #IP SERVIDOR!!
    server_port = 6789 # porta do servidor

    # criação do socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port)) # vincula o socket ao endereço e porta
    server.listen(30) # ele especifica o número de conexões não aceitas que o sistema permitirá antes de recusar novas conexões. 
    print(f"Servidor rodando em {server_ip}:{server_port}")

    # loop principal para aceitar conexões
    while True:
        client_socket, addr = server.accept() # aceita um novo cliente
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__": # se importar esse arquivo em outro, não executa automáticamente
    start_server()