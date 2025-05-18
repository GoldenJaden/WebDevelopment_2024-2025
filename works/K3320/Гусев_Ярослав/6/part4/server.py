import socket
import threading

HOST = "0.0.0.0"
PORT = 8080

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[{addr}] подключился.")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"[{addr}] ".encode("utf-8") + data
            broadcast(message, conn)
    except:
        pass
    finally:
        print(f"[{addr}] отключился.")
        conn.close()
        clients.remove(conn)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("Сервер остановлен.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
