import socket
import json
from math import sqrt

def handle_connection(conn):
    data = conn.recv(1024)
    if not data:
        return
    try:
        request = json.loads(data.decode("utf-8"))
        a = float(request["a"])
        b = float(request["b"])
        c = sqrt(a ** 2 + b ** 2)
        response = f"Гипотенуза: {c:.2f}"
    except Exception as e:
        response = f"Ошибка обработки запроса: {e}"
    print(f"Ответ клиенту {conn.getpeername()}: {response}")
    conn.sendall(response.encode("utf-8"))
    conn.close()

def main():
    sock = socket.socket()
    sock.bind(("", 8080))
    sock.listen(5)
    sock.settimeout(5.0)
    print("Сервер запущен на порту 8080...")
    try:
        while True:
            conn, addr = sock.accept()
            print(f"Подключение от {addr}")
            handle_connection(conn)
    except KeyboardInterrupt:
        print("Сервер остановлен.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
