import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

# Definindo o IP do servidor diretamente no código
server_ip = "127.0.0.1"  # Substituir com o IP correto, ou manter o padrão "127.0.0.1" para localhost
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 12345))

# Thread para receber mensagens do servidor
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# Solicitar o apelido do usuário
apelido = input("Digite seu apelido: ").strip()
client.send(apelido.encode("utf-8"))

print("Conectado ao servidor. Digite mensagens ou comandos (/salas, /entrar <sala>, /sair, /sair_chat).")

while True:
    msg = input()
    if msg.lower() == "/sair_chat":
        client.send("/sair_chat".encode())
        break
    client.send(msg.encode())

client.close()
print("Desconectado.")

