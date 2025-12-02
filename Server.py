import socket
import random
import threading

HOST = "127.0.0.1"
PORT = 5000

def gerar_leituras():
    """Simula sensores do data center."""
    return {
        "TEMPERATURE": round(random.uniform(20, 45), 2),
        "HUMIDITY": random.randint(20, 90),
        "POWER": random.randint(210, 250),
        "DOOR": random.choice(["OPEN", "CLOSED"])
    }

def processar_comando(comando):
    sensores = gerar_leituras()

    if comando == "GET_ALL":
        return f"STATUS: 200 OK\nDATA: {sensores}"

    elif comando == "GET_TEMP":
        return f"STATUS: 200 OK\nDATA: TEMPERATURE={sensores['TEMPERATURE']}"

    elif comando == "GET_HUMID":
        return f"STATUS: 200 OK\nDATA: HUMIDITY={sensores['HUMIDITY']}"

    elif comando == "GET_POWER":
        return f"STATUS: 200 OK\nDATA: POWER={sensores['POWER']}"

    elif comando == "GET_DOOR":
        return f"STATUS: 200 OK\nDATA: DOOR={sensores['DOOR']}"

    else:
        return "STATUS: 400 Bad Request\nMESSAGE: Invalid command"

def handle_client(conn, addr):
    print(f"[CLIENT CONNECTED] {addr}")

    while True:
        try:
            data = conn.recv(1024).decode(errors="ignore").strip()

            # Evita desconexão por mensagens vazias no Windows
            if data == "":
                continue

            print(f"[RECEBIDO] {data}")

            resposta = processar_comando(data)
            conn.sendall(resposta.encode())

        except Exception as e:
            print("[ERRO]", e)
            conn.sendall("STATUS: 500 Internal Server Error".encode())
            break

    conn.close()
    print(f"[CLIENT DISCONNECTED] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER ON] Aguardando conexões em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
