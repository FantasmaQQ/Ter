import socket
import pyaudio
import wave
import speech_recognition as sr

# Função para gravar áudio
def record_audio():
    # Configurações de gravação de áudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    print("Gravando...")

    frames = []
    for i in range(0, int(44100 / 1024 * 5)):  # Grava por 5 segundos
        data = stream.read(1024)
        frames.append(data)

    print("Gravação finalizada.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Salva o áudio em um arquivo WAV
    wf = wave.open("audio.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

# Função para transcrever o áudio para texto
def recognize_audio():
    r = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)  # Lê o áudio gravado

    try:
        # Usa o Google Web Speech API para transcrever o áudio
        text = r.recognize_google(audio, language="pt-BR")
        print(f"Texto reconhecido: {text}")
        return text
    except sr.UnknownValueError:
        print("Não consegui entender o áudio")
        return None
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de voz: {e}")
        return None

# Endereço e porta do servidor (ngrok)
server_ip = '0.tcp.sa.ngrok.io'  # Endereço fornecido pelo ngrok
server_port = 16483  # Porta fornecida pelo ngrok

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

print("Conectado ao servidor!")

# Envia uma mensagem inicial
client_socket.send("Olá, estou no chat!\n".encode('utf-8'))

while True:
    # Pergunta ao usuário se ele quer enviar áudio ou texto
    option = input("Deseja enviar áudio (a) ou texto (t)? ").strip().lower()

    if option == 'a':
        record_audio()  # Grava o áudio
        text = recognize_audio()  # Converte o áudio em texto
        if text:
            client_socket.send(text.encode('utf-8'))  # Envia o texto transcrito
    elif option == 't':
        message = input("Digite sua mensagem: ")
        client_socket.send(message.encode('utf-8'))
    
    # Recebe a resposta do servidor
    response = client_socket.recv(1024)
    print(f"Servidor respondeu: {response.decode('utf-8')}")
    
    if message.lower() == 'sair':
        break

client_socket.close()
