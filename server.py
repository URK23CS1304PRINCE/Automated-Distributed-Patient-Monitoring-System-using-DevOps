import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 9999

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            data_dict = json.loads(data)

            print("\n📊 PATIENT DATA")
            print("-" * 30)
            print(data_dict)
            print("-" * 30)

            # 🚨 Alert system
            if data_dict["state"] == "CRITICAL":
                print(f"🚨 ALERT! Patient {data_dict['patient_id']} is CRITICAL!")

        except:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("🟢 Server Started...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()