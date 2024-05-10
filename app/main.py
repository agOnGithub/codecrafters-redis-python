import socket
import threading

MEMORY = {}

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
                key = parts[4]
                value = parts[5]
                MEMORY[key] = value
                client_socket.sendall(b"+OK\r\n")
            elif command == "GET":
                key = parts[5]
                val = MEMORY.get(key)
                response = f"${len(value)}\r\n{value}\r\n"
                client_socket.sendall(response.encode())
            
    finally:
        client_socket.close()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()