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

import time


def printFormats():
    file = open('formats.txt', 'r')
    text = file.read()
    print(text)
    file.close()


# printFormats()
parser = ArgumentParser()
parser.add_argument("-f", "--file", metavar="file", help="The media file.")
parser.add_argument("-ft", "--format", metavar="file", help="The media file.")


args = parser.parse_args()

SEPARATOR = "|"
BUFFER_SIZE = 1024
#SERVER_HOST = "35.222.58.153"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000

ACTION_SHOW_HISTORY = "show-history"
ACTION_CONVERT_FILE = "convert-file"

filename = args.file
filesize = os.path.getsize(filename)

action = ACTION_CONVERT_FILE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}")

s.connect((SERVER_HOST, SERVER_PORT))

print("Connected.\n")

#s.setblocking(False)

if action == ACTION_SHOW_HISTORY:
    s.send(f"{action}{SEPARATOR}".encode())

    data = s.recv(BUFFER_SIZE*8)

    print(data.decode())

    s.close()

if action == ACTION_CONVERT_FILE:
    s.send(
        f"{action}{SEPARATOR}{filename}{SEPARATOR}{filesize}{SEPARATOR}avi".encode())

    progress = tqdm.tqdm(range(
        filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as f:
        try:
            while True:
                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                s.sendall(bytes_read)

                #tmp = s.recv(BUFFER_SIZE)
                #print(tmp.decode())

                progress.update(len(bytes_read))
        finally:
            #tmp = s.recv(BUFFER_SIZE).decode()
            #print(tmp)
            #s.close()
            print("Michelle")
            f.close()

        # time.sleep(1)
        print("File uploaded! Waiting for conversion...")

        # s.close()

        while True:
            tmp = s.recv(BUFFER_SIZE)

            if tmp:
                print(tmp.decode())
                break
        
        print("hola")

        

    # print(s.recv(BUFFER_SIZE).decode())
    # s.close()
    #tmp = s.recv(BUFFER_SIZE).decode()

    # print(tmp)
    # while True:
    #     if tmp == "converting":
    #         #print("Converting file...", sep=' ', end='', flush=True)
    #         print("Converting file...");
    #     else:
    #         break

    # done = s.recv(BUFFER_SIZE)
    # if done == "done":
    #     s.close()

    # wait for conversion...
    # close the socket
    # s.close()
