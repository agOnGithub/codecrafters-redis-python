import socket
from threading import Thread

def send_reply(conn: socket.socket):
    pong = "+PONG\r\n"
    while True:
        cmd = conn.recv(1024).decode()
        data = str(data.decode("utf-8")).strip()
        parts = data.split("\r\n")
        command = parts[2].lower()

        if "ping" == command:
             conn.sendall(pong.encode("utf-8"))

        elif "echo" == command:
            raw_message_length = len(parts)
            message = ""

            for i in range(4, raw_message_length, 2):
                message += parts[i]
                if i < raw_message_length - 1:
                    message += " "
                    
            message_send = f"${len(message)}\r\n{message}\r\n"
            conn.sendall(message_send.encode("utf-8"))

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while True:
        conn, _ = server_socket.accept() # wait for client
        Thread(target=send_reply, args=(conn)).start()

if __name__ == "__main__":
    main()
