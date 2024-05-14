import socket
import threading
import time

MEMORY = {}
EXPIRE = {}

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            decoded_data = data.decode("utf-8").strip()
            parts = decoded_data.split("\r\n") # redis is case-insensitive
            command = parts[2].upper()

            if command == "ECHO":
                message = parts[4]  # the command is the 5th part
                response = f"${len(message)}\r\n{message}\r\n"
                client_socket.sendall(response.encode())  # response.encode() --> binary format data
            elif command == "PING":
                client_socket.sendall(b"+PONG\r\n")
            elif command == "SET":
                if len(parts) < 8:
                    key = parts[4]
                    value = parts[6]
                    MEMORY[key] = value
                    client_socket.sendall(b"+OK\r\n")
                elif len(parts) > 7 and parts[8].upper() == "PX":
                    key = parts[4]
                    value = parts[6]
                    expire = parts[10]
                    MEMORY[key] = value
                    EXPIRE[key] = time.time() * 1000 + int(expire)
                    client_socket.sendall(b"+OK\r\n")
            elif command == "GET":
                key = parts[4]
                value = MEMORY.get(key)
                if key in EXPIRE:
                    if time.time() * 1000 < EXPIRE[key]:
                        response = f"${len(value)}\r\n{value}\r\n"
                        client_socket.sendall(response.encode())
                    else:
                        del MEMORY[key]
                        del EXPIRE[key]
                        client_socket.sendall(b"$-1\r\n")
                else:
                    response = f"${len(value)}\r\n{value}\r\n"
                    client_socket.sendall(response.encode())
            elif command == "TYPE":
                key = parts[4]
                if key in MEMORY:
                    client_socket.sendall(b"+string\r\n")
                else:
                    client_socket.sendall(b"+none\r\n")
            
    finally:
        client_socket.close()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()