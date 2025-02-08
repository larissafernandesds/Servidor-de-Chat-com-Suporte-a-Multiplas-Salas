import socket # biblioteca para comunicação via rede
import threading # biblioteca para trabalhar com threads (execução paralela)


def receive_messages(sock):
    """
    Função responsável por receber mensagens do servidor e exibi-las na tela.

    Parâmetros:
    - sock: objeto socket do cliente, usado para receber dados do servidor.

    Retorno:
    - Não retorna nada explicitamente, mas imprime mensagens recebidas.
    """
    
    while True: # loop infinito para continuar recebendo mensagens
        try:
            msg = sock.recv(1024).decode() # recebe até 1024 bytes e decodifica de bytes para string
            if not msg: # se a mensagem estiver vazia, significa que a conexão foi encerrada
                break
            print(msg) # exibe a mensagem recebida no terminal do cliente
        except:
            break # em caso de erro, encerra a função


server_ip = "127.0.0.1"  # IP (padrão "127.0.0.1" para localhost)
server_port = 6789 # porta do servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criação do socket do cliente para comunicação via TCP/IP
client.connect((server_ip, server_port)) # conecta ao servidor na porta


# criação de uma thread para receber mensagens do servidor de forma assíncrona
threading.Thread(target=receive_messages, args=(client,), daemon=True).start() 


# solicitação do apelido do usuário e envia para o servidor
apelido = input("Digite seu apelido: ").strip() # remove espaços extras
client.send(apelido.encode("utf-8"))  # envia o apelido convertido para bytes


# loop principal para enviar mensagens ao servidor
while True:
    msg = input() # captura a mensagem do usuário
    if msg.lower() == "/sair_chat":  # se o usuário deseja sair
        client.send("/sair_chat".encode())  # envia o comando de saída para o servidor
        break # encerra o loop
    client.send(msg.encode())  # envia a mensagem para o servidor


# finalização da conexão
client.close() # fecha o socket do cliente
print("\n__Desconectado__\n")

# Função do Cliente
# Conectar-se ao servidor.
# Enviar um apelido para identificação.
# Capturar mensagens digitadas e enviá-las ao servidor.
# Receber mensagens do servidor e exibi-las ao usuário.
# Desconectar corretamente quando o usuário quiser sair.