'''
import socket
import sys

port = 7000
ip = "35.222.58.153"
#client.connect(ip)
#client.emit('my message', {'foo': 'bar'})

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (ip, port)
    sock.connect(address)
    message = "Envía la retrasada"
    sock.sendto(message.encode('utf-8'),(ip, port))
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        print("Miguel")
        data = sock.recv(16)
        amount_received += len(data)

client()

if len(sys.argv) == 2:
    texto = sys.argv[1]
    print(texto)

'''

import socket
import tqdm
import os
from argparse import ArgumentParser
import sys

def printFormats():
    file = open('formats.txt', 'r')
    text = file.read()
    print(text)
    file.close()

printFormats()
parser = ArgumentParser()
parser.add_argument("-f", "--file", metavar="file", help="The media file.")
parser.add_argument("-ft", "--format", metavar="file", help="The media file.")


args = parser.parse_args()

SEPARATOR = "|"
BUFFER_SIZE = 1024
SERVER_HOST = "35.222.58.153"
SERVER_PORT = 7000

filename = args.file
filesize = os.path.getsize(filename)

s = socket.socket()

print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")

s.connect((SERVER_HOST, SERVER_PORT))

print("[+] Connected.")

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}MIGUEL".encode())

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
