import socket
import threading

def handle_client(client_socket, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message, client_socket)
        except:
            print(f"[DESCONECTADO] {addr}")
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))  # Altere "9999" para outra porta se necessário
server.listen(5)
clients = []

print("[SERVIDOR INICIADO] Aguardando conexões...")
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
