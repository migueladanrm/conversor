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
parser.add_argument("-i", "--input", metavar="input", help="The media file.")
parser.add_argument("-f", "--format", metavar="format", help="The media file.")
parser.add_argument("-o", "--output", metavar="output", help="The output file")


args = parser.parse_args()

# print(args)

SEPARATOR = "|"
BUFFER_SIZE = 1024
#SERVER_HOST = "35.222.58.153"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000

ACTION_SHOW_TASKS = "show-tasks"
ACTION_UPLOAD_FILE = "upload-file"
ACTION_RETRIEVE_FILE = "retrieve-file"

input_file = args.input
target_format = args.format
output_file = args.output

filesize = os.path.getsize(input_file)

action = ACTION_UPLOAD_FILE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}")

s.connect((SERVER_HOST, SERVER_PORT))

print("Connected.\n")

# s.setblocking(False)


task_id = ""

if action == ACTION_SHOW_TASKS:
    s.send(f"{action}{SEPARATOR}".encode())

    data = s.recv(BUFFER_SIZE*8)

    print(data.decode())

    s.close()

if action == ACTION_UPLOAD_FILE:
    s.send(
        f"{action}{SEPARATOR}{input_file}{SEPARATOR}{filesize}{SEPARATOR}{target_format}".encode())

    task_id = s.recv(BUFFER_SIZE).decode()

    progress = tqdm.tqdm(range(
        filesize), f"Sending {input_file}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(input_file, "rb") as f:
        try:
            while True:
                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                s.sendall(bytes_read)

                progress.update(len(bytes_read))
        finally:
            print("Michelle")
            progress.close()
            s.close()

        print("File uploaded! Waiting for conversion...")

        time.sleep(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    s.send(f"{ACTION_RETRIEVE_FILE}{SEPARATOR}{task_id}".encode())

    task_info = s.recv(BUFFER_SIZE)

    print(task_info.decode())

    with open(output_file, "wb") as f:
        try:
            while True:
                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:
                    break

                f.write(bytes_read)
        finally:
            print("michelle")
            s.close()

    print("HECHO!!!")
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
