import argparse
from datetime import datetime
import sys
import socket
import os
from uuid import uuid4
import tqdm
import ffmpeg
import threading
import socketserver
import _thread
import subprocess

import file_manager
import time


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7000
BUFFER_SIZE = 1024
SEPARATOR = "|"
MAX_CONNECTIONS = 10
TEMP_DIR = "/tmp"

ACTION_SHOW_HISTORY = "show-history"
ACTION_CONVERT_FILE = "convert-file"

history = []
entry = {
    "id": "0x4932423",
    "source_file": "video.mp4",
    "source_file_length": 2943474,
    "target_format": "ogg",
    "conversion_started_at": "",
    "conversion_finished_at": ""
}

print("Server is listening...")

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket.bind((SERVER_HOST, SERVER_PORT))
except socket.error as e:
    print(str(e))

ServerSocket.listen(5)


def history_get(id):
    for i in len(history):
        if(history[i]["id"] == id):
            return history[i]


def history_set(data):
    for i in len(history):
        if(history[i]["id"] == data["id"]):
            history.pop(i)
            break

    history.append(data)


def handle_request(connection: socket.socket):
    raw = connection.recv(BUFFER_SIZE).decode()
    action = raw.split(SEPARATOR)[0]

    if action == ACTION_SHOW_HISTORY:
        connection.sendall("No hay archivos pendientes.".encode())
        connection.close()
    elif action == ACTION_CONVERT_FILE:
        _, file_name, file_size, target_format = raw.split(SEPARATOR)

        session_id = str(uuid4())[:4]
        file_name = os.path.basename(file_name)
        file_size = int(file_size)

        # if file_name and file_size and target_format:

        #print(f"Receiving file '{file_name}' ({file_size} bytes)...")

        original_file = file_manager.generate_file_ref(file_name)

        with open(original_file, "wb") as f:
            try:
                while True:
                    #connection.sendall("receiving file...".encode())
                    bytes_read = connection.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break

                    f.write(bytes_read)
            finally:
                #connection.close()
                print("michelle")
                #f.close()
        time.sleep(1)


        connection.sendall("converting".encode())

        history_entry = {
            "id": session_id,
            "input_file": file_name,
            "target_format": target_format,
            "conversion_start": datetime.utcnow(),
            "conversion_end": "",
            "output_file":""
        }
        history_set(history_entry)

        output_file = file_manager.generate_file_ref("out.{target_format}")

        cmd = ["ffmpeg", "-i", original_file, output_file]

        ffmpeg_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
        #ffmpeg_process.wait()

        while ffmpeg_process.returncode == None:
            connection.sendall("converting".encode())

        history_entry["conversion_end"] = datetime.utcnow()
        history_set(history_entry)

        connection.send("done".encode())

        connection.close()


while True:
    connection, client_info = ServerSocket.accept()
    print(f"Connected to {client_info[0]}:{client_info[1]}")

    _thread.start_new_thread(handle_request, (connection,))

# ServerSocket.close()
