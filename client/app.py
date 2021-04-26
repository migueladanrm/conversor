import socket
import tqdm
import os
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument("-f", "--file", metavar="file", help="The media file.")

args = parser.parse_args()

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000

filename = args.file
filesize = os.path.getsize(filename)

s = socket.socket()

print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")

s.connect((SERVER_HOST, SERVER_PORT))

print("[+] Connected.")

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(
    filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
