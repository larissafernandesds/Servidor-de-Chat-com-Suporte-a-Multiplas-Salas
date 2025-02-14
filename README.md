# Servidor de Chat com Suporte a Multiplas Salas

## Descrição
 Implementação de um servidor de chat onde os clientes podem criar e entrar em diferentes salas de chat. Cada sala deve ter seu próprio conjunto de clientes, e as mensagens enviadas em uma sala devem ser recebidas apenas pelos clientes dessa sala, seguindo requisitos como:
- O servidor deve suportar múltiplas salas de chat simultâneas.
- Os clientes devem poder listar as salas disponíveis e escolher em qual entrar.
- Implementar comandos para criar, entrar e sair de salas.
- As mensagens enviadas por um cliente em uma sala devem ser encaminhadas apenas para outros clientes na mesma sala.


## Tecnologias Utilizadas
 **Linguagem de programação utilizada:** Python

 **Bibliotecas/Frameworks utilizados:**
- socket → Comunicação via sockets
- threading → Manipulação de threads

## Como Executar

### Requisitos
  
    -Versão instalada do Python>=3.6 (uso de f-strings)
  

### Instruções de Execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/larissafernandesds/Servidor-de-Chat-com-Suporte-a-Multiplas-Salas.git

2. Altere o IP no servidor/cliente, se necessário:
   ```bash
   variável -> server_ip
   ```
3. Execute o servidor:
   ```bash
   python server.py
   ```
4. Execute o cliente:
   ```bash
   python client.py
   ```

## Como Testar
 Use os comandos disponíveis:
- /salas - Lista todas as salas disponíveis.

- /criar <nome_da_sala> - Cria uma nova sala.

- /entrar <nome_da_sala> - Entra em uma sala existente.

- /sair - Sai da sala atual.

- /sair_chat - Desconecta do chat (servidor).


## Funcionalidades Implementadas

**No Servidor:**

- Aceita múltiplos clientes simultaneamente.
- Gerencia salas de chat separadas.
- Notifica usuários sobre entradas e saídas das salas.

**No Cliente:**

- Conectar-se ao servidor.
- Enviar um apelido para identificação.
- Criar e entrar em salas de chat.
- Enviar e receber mensagens em tempo real.
- Desconectar-se corretamente.

Para maiores informações, leia o relatório do projeto.

## Possíveis Melhorias Futuras
- Interface Gráfica.
- Histórico de Mensagens.
- Autenticação de Usuários.

