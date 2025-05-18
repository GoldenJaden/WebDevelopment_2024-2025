import socket
import traceback
from logging import getLogger, basicConfig, INFO

# Configure logger
basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = getLogger()

def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
    addr = conn.getpeername()
    logger.info(f"[{addr[0]}:{addr[1]}] Answering with: \"{data}\"")
    data = data.encode("utf-8")
    try:
        conn.sendall(data)
        logger.info(f"[{addr[0]}:{addr[1]}] Successfully sent response.")
    except BrokenPipeError:
        logger.error(f"[{addr[0]}:{addr[1]}] Connection closed before response could be sent.")

def parse(conn):
    addr = conn.getpeername()
    conn.settimeout(1.0)
    data = b""
    try:
        tmp = conn.recv(1024)
        while tmp and "\r\n\r\n" not in str(tmp):
            data += tmp
            tmp = conn.recv(1024)
    except socket.timeout:
        logger.warning(f"[{addr[0]}:{addr[1]}] Timed out waiting for data.")

    if not data:
        return

    udata = data.decode("utf-8")
    # logger.info(udata)

    logger.info(f"[{addr[0]}:{addr[1]}] sent message: \"{udata}\"")

    answer = "Hello, client"
    send_answer(conn, data=answer)

sock = socket.socket()
sock.bind(("", 8080))
sock.listen(5)
sock.settimeout(1.0)

logger.info("Server started on port 8080. Press Ctrl+C to stop.")

try:
    while True:
        try:
            conn, addr = sock.accept()
            conn.setblocking(0)
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error("Unexpected error during accept: %s", e)
            logger.error(traceback.format_exc())
            continue

        try:
            logger.info("New connection from %s:%s", addr[0], addr[1])
            parse(conn)
        except Exception as e:
            logger.error("Exception occurred while handling request: %s", e)
            logger.error(traceback.format_exc())
            try:
                send_answer(conn, "500 Internal Server Error", data="Ошибка")
            except:
                pass
        finally:
            try:
                conn.close()
            except:
                pass

except KeyboardInterrupt:
    logger.info("Server stopped by user.")
finally:
    sock.close()
    logger.info("Socket closed.")