import socket
import os

HOST = ""
PORT = 8080
HTML_FILE = "index.html"

def load_html():
    if not os.path.exists(HTML_FILE):
        return "<h1>404 Not Found</h1>", 404

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read(), 200

def build_http_response(body, status_code=200):
    status_line = {
        200: "HTTP/1.1 200 OK",
        404: "HTTP/1.1 404 Not Found"
    }.get(status_code, "HTTP/1.1 500 Internal Server Error")

    headers = [
        status_line,
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body.encode('utf-8'))}",
        "Connection: close",
        "",
        ""
    ]
    response = "\r\n".join(headers) + body
    return response.encode("utf-8")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Сервер запущен на http://localhost:{PORT}")
        while True:
            client_conn, client_addr = server.accept()
            with client_conn:
                print(f"Подключение от {client_addr}")
                request = client_conn.recv(1024).decode("utf-8")
                print("Запрос клиента:")
                print(request.splitlines()[0])

                html, status = load_html()
                response = build_http_response(html, status)
                client_conn.sendall(response)

if __name__ == "__main__":
    main()