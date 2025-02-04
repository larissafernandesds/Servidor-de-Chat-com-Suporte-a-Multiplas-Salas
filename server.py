import socket
import threading

# Estrutura para armazenar salas e clientes
salas = {}

def handle_client(client_socket, addr):
    sala_atual = None
    nome = None  # Nome será o apelido do usuário

    print(f"Nova conexão de {addr} (aguardando apelido...)")

    # Solicitar ao cliente o apelido
    client_socket.send("Digite seu apelido: ".encode("utf-8"))
    nome = client_socket.recv(1024).decode().strip()

    if not nome:
        nome = f"Usuário-{addr[1]}"  # Atribui um nome padrão se não for fornecido

    print(f"Cliente conectado: {nome} ({addr})")

    client_socket.send(f"Bem-vindo ao chat, {nome}! Use os comandos:\n"
                       "/salas - listar salas disponíveis\n"
                       "/criar <sala> - criar uma nova sala\n"
                       "/entrar <sala> - entrar em uma sala existente\n"
                       "/sair - sair da sala atual\n"
                       "/sair_chat - desconectar\n".encode("utf-8"))

    while True:
        try:
            msg = client_socket.recv(1024).decode().strip()
            if not msg:
                break

            if msg.startswith("/salas"):
                salas_disponiveis = ", ".join(salas.keys()) if salas else "Nenhuma sala disponível."
                client_socket.send(f"Salas disponíveis: {salas_disponiveis}\n".encode("utf-8"))

            elif msg.startswith("/criar "):
                _, nome_sala = msg.split(maxsplit=1)
                if nome_sala in salas:
                    client_socket.send("⚠️ Essa sala já existe! Tente outro nome.\n".encode("utf-8"))
                else:
                    salas[nome_sala] = {"clientes": []}
                    client_socket.send(f"✅ Sala '{nome_sala}' criada com sucesso!\n".encode("utf-8"))

            elif msg.startswith("/entrar "):
                _, nome_sala = msg.split(maxsplit=1)
                if nome_sala not in salas:
                    client_socket.send("❌ Sala não encontrada. Use /salas para ver as disponíveis ou /criar para criar uma nova.\n".encode("utf-8"))
                else:
                    if sala_atual:
                        salas[sala_atual]["clientes"].remove(client_socket)
                        for cliente in salas[sala_atual]["clientes"]:
                            cliente.send(f"📝 {nome} saiu da sala '{sala_atual}'.\n".encode("utf-8"))

                    salas[nome_sala]["clientes"].append(client_socket)
                    sala_atual = nome_sala

                    for cliente in salas[nome_sala]["clientes"]:
                        if cliente != client_socket:
                            cliente.send(f"📝 {nome} entrou na sala '{nome_sala}'.\n".encode("utf-8"))
                    client_socket.send(f"✅ Você entrou na sala '{nome_sala}'.\n".encode("utf-8"))

            elif msg.startswith("/sair"):
                if sala_atual:
                    salas[sala_atual]["clientes"].remove(client_socket)
                    for cliente in salas.get(sala_atual, {}).get("clientes", []):
                        cliente.send(f"📝 {nome} saiu da sala '{sala_atual}'.\n".encode("utf-8"))
                    sala_atual = None
                    client_socket.send("🔹 Você saiu da sala.\n".encode("utf-8"))
                else:
                    client_socket.send("⚠️ Você não está em nenhuma sala.\n".encode("utf-8"))

            elif msg.startswith("/sair_chat"):
                if sala_atual:
                    for cliente in salas[sala_atual]["clientes"]:
                        if cliente != client_socket:
                            cliente.send(f"👋 {nome} saiu do chat da sala '{sala_atual}'.\n".encode("utf-8"))
                client_socket.send("👋 Você saiu do chat.\n".encode("utf-8"))
                break

            else:
                if sala_atual:
                    mensagem = f"[{nome}] {msg}\n"
                    for cliente in salas[sala_atual]["clientes"]:
                        if cliente != client_socket:
                            cliente.send(mensagem.encode("utf-8"))
                else:
                    client_socket.send("⚠️ Você não está em nenhuma sala. Use /entrar <sala> para participar.\n".encode("utf-8"))

        except:
            break

    if sala_atual and client_socket in salas.get(sala_atual, {}).get("clientes", []):
        salas[sala_atual]["clientes"].remove(client_socket)
        if not salas[sala_atual]["clientes"]:
            del salas[sala_atual]

    print(f"{nome} {addr} desconectou do chat.")
    client_socket.close()


def start_server():
    server_ip = "0.0.0.0"
    server_port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(30)
    print(f"Servidor rodando em {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()


