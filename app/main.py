import socket
from threading import Thread

def send_reply(conn: socket.socket):
    pong = "+PONG\r\n"
    with conn:
        while True:
            cmd = conn.recv(1024).decode()
            data = str(data.decode("utf-8")).strip()
            parts = data.split("\r\n")
            command = parts[2].lower()

            if "ping" == command:
                conn.sendall(pong)

            elif "echo" == command:
                message = parts[4]  # the command is the 5th part
                response = f"${len(message)}\r\n{message}\r\n"
                conn.sendall(response.encode("utf-8"))

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen()
    
    while True:
        conn, _ = server_socket.accept() # wait for client
        Thread(target=send_reply, args=(conn)).start()

if __name__ == "__main__":
    main()
