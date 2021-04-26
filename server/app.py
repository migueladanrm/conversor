import argparse
import sys
import socket
import os
import tqdm


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7000
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
MAX_CONNECTIONS = 10
TEMP_DIR = "/tmp"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(MAX_CONNECTIONS)

print(
    f"Server is listening on {SERVER_HOST}:{SERVER_PORT} and it's ready to receive connections.")

client_socket, client_address = s.accept()

print(f"[+] {client_address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(
    filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(f"{TEMP_DIR}/{filename}", "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break

        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
s.close()
