import socket
from threading import Thread

def main():
    print("Logs from your program will appear here!")
    pong = "+PONG\r\n"

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        conn, _ = server_socket.accept() # wait for client
        Thread(target=return_pong, args=(conn, pong)).start()

def return_pong(Client: socket.socket, pong):
    Client.recv(1024)
    Client.sendall(pong.encode())

if __name__ == "__main__":
    main()
