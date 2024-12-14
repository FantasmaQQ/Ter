import socket
import threading
import os
from colorama import Fore, init

# Inicializa o colorama
init(autoreset=True)

# Função para receber mensagens do servidor
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print(Fore.RED + "Conexão perdida...")
            client.close()
            break

# Função para enviar arquivos
def send_file(filename):
    try:
        client.send(f"FILE:{filename}".encode('utf-8'))
        
        with open(filename, 'rb') as file:
            while chunk := file.read(1024):
                client.send(chunk)
        
        print(Fore.GREEN + "Arquivo enviado com sucesso!")
    except Exception as e:
        print(Fore.RED + f"Erro ao enviar arquivo: {e}")

# Solicitar nome de usuário
username = input(Fore.YELLOW + "Digite seu nome de usuário: ")

# Mensagem de boas-vindas
print(Fore.CYAN + f"Bem-vindo, {username}! Você está no chat agora.")

# Substitua pelo IP e a porta gerados pelo ngrok no PC
server_ip = "0.tcp.sa.ngrok.io"  # IP do ngrok
server_port = 11811  # Porta do ngrok

# Conectar ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Iniciar a thread para receber mensagens
threading.Thread(target=receive_messages).start()

print(Fore.GREEN + "Conectado ao chat! Digite suas mensagens ou envie um arquivo:")

while True:
    message = input(Fore.YELLOW + f"{username}: ")

    # Enviar arquivo se o comando for 'enviar arquivo'
    if message.startswith("enviar arquivo"):
        filename = message.split(" ", 1)[1]
        if os.path.isfile(filename):
            send_file(filename)
        else:
            print(Fore.RED + "Arquivo não encontrado.")
    else:
        client.send(f"{username}: {message}".encode('utf-8'))
