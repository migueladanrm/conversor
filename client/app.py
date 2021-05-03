import socket
import tqdm
import os
from argparse import ArgumentParser
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
            progress.close()
            s.close()

        print("File uploaded! Waiting for conversion...")

        time.sleep(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    s.send(f"{ACTION_RETRIEVE_FILE}{SEPARATOR}{task_id}".encode())

    t_id, t_source, t_format, t_start, server_time = s.recv(
        BUFFER_SIZE).decode().split(SEPARATOR)

    print(f"Connected to {SERVER_HOST}:{SERVER_PORT} | Server time: {server_time}\nConversion task running -- {task_id}\tStart: {t_start}\nInput: {t_source}\tTarget format: {t_format}")

    t_finish, output_length = s.recv(BUFFER_SIZE).decode().split(SEPARATOR)

    print(f"Conversion finished at {t_finish}")

    progress = tqdm.tqdm(range(
        int(output_length)), f"Receiving converted file...", unit="B", unit_scale=True, unit_divisor=1024)

    with open(output_file, "wb") as f:
        try:
            while True:
                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:
                    break

                f.write(bytes_read)

                progress.update(len(bytes_read))
        finally:
            progress.close()
            s.close()

    print(f"Converted file has been saved as {output_file}")
