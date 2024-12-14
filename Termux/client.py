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

# Defina diretamente o IP do servidor e a porta
server_ip = "0.tcp.sa.ngrok.io"  # IP gerado pelo ngrok
server_port = 15437  # Porta gerada pelo ngrok

# Conectar ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

threading.Thread(target=receive_messages).start()

print("Conectado ao chat! Digite suas mensagens:")
while True:
    message = input()
    client.send(message.encode('utf-8'))
