import socket

HOST = "127.0.0.1"
PORT = 8080

def main():
    request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(request.encode("utf-8"))

        response = b""
        while True:
            data = client.recv(1024)
            if not data:
                break
            response += data

    print("Ответ от сервера:")
    print(response.decode("utf-8"))

if __name__ == "__main__":
    main()