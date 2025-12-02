import socket
import time

HOST = "127.0.0.1"
PORT = 5000

# ➤ LIMITES PRÉ-CONFIGURADOS (CONSTANTES)
TEMP_LIMIT = 35
HUMID_LIMIT = 80
POWER_LIMIT = 240

def analisar_resposta(resposta):
    """Lê a resposta do servidor e verifica alarmes."""
    print("\n--- RESPOSTA DO SERVIDOR ---")
    print(resposta)

    # Extrai a parte de dados
    if "DATA:" not in resposta:
        print("[ERRO] Resposta inválida do servidor.")
        return

    dados_str = resposta.split("DATA:")[1].strip()

    # Tenta converter em dict
    try:
        if dados_str.startswith("{"):  
            # Caso GET_ALL (vem como dict completo)
            dados = eval(dados_str)
        else:
            # Caso formatos simples: VAR=VAL;VAR=VAL
            dados = dict([item.split("=") for item in dados_str.split(";")])
    except Exception as e:
        print("[ERRO] Não foi possível interpretar os dados:", e)
        return

    # --- Alarmes ---
    if "TEMPERATURE" in dados:
        temp = float(dados["TEMPERATURE"])
        if temp > TEMP_LIMIT:
            print(f"[ALERTA] Temperatura CRÍTICA: {temp}°C")

    if "HUMIDITY" in dados:
        hum = int(dados["HUMIDITY"])
        if hum > HUMID_LIMIT:
            print(f"[ALERTA] Umidade elevada: {hum}%")

    if "POWER" in dados:
        powe = int(dados["POWER"])
        if powe > POWER_LIMIT:
            print(f"[ALERTA] Tensão elétrica acima do normal: {powe}V")

def cliente():
    """Envia comandos ao servidor a cada 2 segundos."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("[CLIENTE] Conectando ao servidor...")

        try:
            s.connect((HOST, PORT))
        except Exception as e:
            print("[ERRO] Não foi possível conectar ao servidor:", e)
            return

        print("[CLIENTE CONECTADO]")

        while True:
            try:
                # Envia comando ao servidor
                s.sendall("GET_ALL".encode())

                # Recebe resposta
                resp = s.recv(2048).decode()

                if not resp:
                    print("[ERRO] Servidor fechou a conexão.")
                    break

                # Analisar conteúdo recebido
                analisar_resposta(resp)

            except Exception as e:
                print("[ERRO] Falha durante comunicação:", e)
                break

            time.sleep(2)  # intervalo entre requisições

if __name__ == "__main__":
    cliente()
    
