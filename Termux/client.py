import socket
import threading

# Função para receber mensagens do servidor
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Conexão perdida...")
            client.close()
            break

# Substitua pelo IP e a porta gerados pelo ngrok no PC
server_ip = "0.tcp.sa.ngrok.io"  # IP do ngrok
server_port = 11811  # Porta do ngrok

# Conectar ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Iniciar a thread para receber mensagens
threading.Thread(target=receive_messages).start()

print("Conectado ao chat! Digite suas mensagens:")
while True:
    message = input()
    client.send(message.encode('utf-8'))
