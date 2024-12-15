import socket
import pyaudio
import wave

# Função para gravar áudio
def record_audio(filename):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    
    print("Gravando... (pressione Ctrl+C para parar)")
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass
    finally:
        print("Gravação finalizada.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))

# Conecta ao servidor
server_ip = '127.0.0.1'
server_port = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Grava o áudio e envia
filename = "audio.wav"
record_audio(filename)
with open(filename, 'rb') as f:
    client_socket.send(f.read())

# Recebe a resposta do servidor
response = client_socket.recv(1024)
print(response.decode())

client_socket.close()
