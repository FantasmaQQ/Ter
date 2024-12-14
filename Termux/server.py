import socket
import threading
from colorama import Fore, init

# Inicializa o colorama
init(autoreset=True)

# Função para lidar com o cliente
def handle_client(client_socket, addr):
    print(Fore.GREEN + f"Conexão estabelecida com {addr}")
    client_socket.send(Fore.CYAN + b"Bem-vindo ao chat! Você está agora conectado.")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            if message.startswith("FILE:"):
                filename = message.split(":", 1)[1]
                with open(filename, 'wb') as file:
                    while chunk := client_socket.recv(1024):
                        if not chunk:
                            break
                        file.write(chunk)
                print(Fore.YELLOW + f"Arquivo {filename} recebido com sucesso!")
            else:
                print(Fore.YELLOW + f"Mensagem de {addr}: {message}")
        except Exception as e:
            print(Fore.RED + f"Erro: {e}")
            client_socket.close()
            break

# Configuração do servidor
server_ip = "0.0.0.0"  # O servidor escuta em todas as interfaces de rede
server_port = 9999  # Porta do servidor

# Criação do socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

print(Fore.CYAN + f"Servidor rodando em {server_ip}:{server_port}, aguardando conexões...")

while True:
    client_socket, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
