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
    if cmd.split(" ")[0] == "ping":
        conn.send(ping.encode())
    else:
        conn.send(cmd.encode())

if __name__ == "__main__":
    main()
