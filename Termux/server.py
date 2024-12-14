import socket
import threading

# Função para lidar com cada cliente (receber e enviar mensagens)
def handle_client(client_socket, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    while True:
        try:
            # Recebe mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            print(f"[{addr}] {message}")
            # Envia a mensagem para todos os outros clientes
            broadcast(message, client_socket)
        except:
            # Se o cliente desconectar, remove ele da lista
            print(f"[DESCONECTADO] {addr}")
            clients.remove(client_socket)
            client_socket.close()
            break

# Função para enviar mensagens a todos os clientes conectados
def broadcast(message, client_socket):
    for client in clients:
        # Não envia para o próprio cliente
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Remove o cliente caso haja erro
                clients.remove(client)

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))  # Porta do servidor (9999)
server.listen(5)
print("[SERVIDOR INICIADO] Aguardando conexões...")

# Lista para armazenar clientes conectados
clients = []

# Loop principal para aceitar conexões
while True:
    client_socket, addr = server.accept()  # Aceita a conexão
    clients.append(client_socket)  # Adiciona o cliente à lista
    print(f"[CONEXÃO ESTABELECIDA] {addr}")
    # Inicia uma nova thread para lidar com o cliente (isso permite múltiplos clientes)
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
