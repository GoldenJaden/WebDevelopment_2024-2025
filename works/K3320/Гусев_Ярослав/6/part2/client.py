import socket
import json

def main():
    a = input("Введите катет a: ")
    b = input("Введите катет b: ")
    request = {"a": a, "b": b}

    with socket.socket() as conn:
        conn.connect(("127.0.0.1", 8080))
        conn.sendall(json.dumps(request).encode("utf-8"))
        response = conn.recv(1024).decode("utf-8")
        print("Ответ от сервера:", response)

if __name__ == "__main__":
    main()
