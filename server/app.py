import argparse
import sys
import socket
import os
import tqdm


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7000
BUFFER_SIZE = 1024
SEPARATOR = "|"
MAX_CONNECTIONS = 10
TEMP_DIR = "/tmp"


def handle_request(client_socket, client_address):
    print(f"[+] {client_address} is connected.")

    file_name, file_size, target_format = client_socket.recv(
        BUFFER_SIZE).decode().split(SEPARATOR)

    print(file_name)

    if file_name and file_size and target_format:
        print(f"Receiving file '{file_name}' ({file_size} bytes)...")
        file_name = os.path.basename(file_name)
        file_size = int(file_size)

        progress = tqdm.tqdm(range(
            file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(f"{TEMP_DIR}/{file_name}", "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break

                f.write(bytes_read)
                progress.update(len(bytes_read))

        client_socket.close()
    else:
        client_socket.close()
    print("Connection finished successfuly!")
    # s.close()


if __name__ == "__main__":
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(MAX_CONNECTIONS)

    print(
        f"Server is listening on {SERVER_HOST}:{SERVER_PORT} and it's ready to receive connections.")

    while True:
        client_socket, client_address = s.accept()
        handle_request(client_socket, client_address)
