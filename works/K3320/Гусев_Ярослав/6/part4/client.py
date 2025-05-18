import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 8080

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("Соединение с сервером закрыто.")
                break
            print("\r" + data.decode("utf-8") + "\n> ", end="")
        except ConnectionResetError:
            print("Сервер отключился.")
            break
        except Exception as e:
            print(f"Ошибка приема: {e}")
            break

def main():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        print("Подключено к чату. Напиши сообщение и нажми Enter. Введите /exit для выхода.")
    except Exception as e:
        print(f"Не удалось подключиться к серверу: {e}")
        return

    receiver_thread = threading.Thread(target=receive_messages, args=(conn,))
    receiver_thread.start()

    try:
        while True:
            msg = input("> ")
            if msg.strip().lower() == "/exit":
                break
            conn.sendall(msg.encode("utf-8"))
    except KeyboardInterrupt:
        print("\nВыход...")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
