import socket
import threading

# Função para lidar com cada cliente
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
            # Remove o cliente caso ele desconecte
            print(f"[DESCONECTADO] {addr}")
            clients.remove(client_socket)
            client_socket.close()
            break

# Função para enviar mensagens a todos os clientes conectados
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Remove o cliente caso haja erro ao enviar a mensagem
                clients.remove(client)

# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))  # Porta do servidor (altere se necessário)
server.listen(5)
print("[SERVIDOR INICIADO] Aguardando conexões...")

# Lista para armazenar clientes conectados
clients = []

# Loop principal para aceitar conexões
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"[CONEXÃO ESTABELECIDA] {addr}")
    # Inicia uma nova thread para lidar com o cliente
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
