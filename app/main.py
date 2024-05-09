import socket
from threading import Thread

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while True:
        conn, _ = server_socket.accept() # wait for client
        Thread(target=send_reply, args=(conn)).start()

def send_reply(conn: socket.socket):
    pong = "+PONG\r\n"
    cmd = conn.recv(1024).decode()
    while True:
        if "ping" in str(cmd.decode("utf-8")).lower():
            conn.send(pong.encode())
        else:
            conn.send(cmd.encode())

if __name__ == "__main__":
    main()
