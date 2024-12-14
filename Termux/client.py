import socket
import threading

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Conexão perdida...")
            client.close()
            break

server_ip = input("Digite o IP do servidor: ")  # IP do servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 9999))  # Porta deve ser a mesma do servidor

threading.Thread(target=receive_messages).start()

print("Conectado ao chat! Digite suas mensagens:")
while True:
    message = input()
    client.send(message.encode('utf-8'))
