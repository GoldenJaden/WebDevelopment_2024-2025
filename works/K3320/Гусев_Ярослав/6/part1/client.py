import socket
import time

conn = socket.socket()

conn.connect( ("127.0.0.1", 8080) )
conn.setblocking(0)

def recv_data(conn):
    data = b""
    time.sleep(2)
    try:
        tmp = conn.recv(1024)
        while tmp:
            data += tmp
            tmp = conn.recv(1024)
    except BlockingIOError:
        pass
    return data


def main():
    data = b"Hello server!\r\n\r\n"


    print(f"Sending message: {data}")
    conn.send(data)
    data = recv_data(conn)
    print(f"Получен ответ: {data.decode("utf-8")}")
    conn.close()


if __name__ == "__main__":
    main()