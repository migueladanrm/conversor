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

ACTION_SHOW_TASKS = "show-tasks"
ACTION_UPLOAD_FILE = "upload-file"
ACTION_RETRIEVE_FILE = "retrieve-file"

tasks = []
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


def task_get(id):
    for i in range(len(tasks)):
        if(tasks[i]["id"] == id):
            return tasks[i]


def task_set(t):
    for i in range(len(tasks)):
        if(tasks[i]["id"] == t["id"]):
            tasks.pop(i)
            break

    tasks.append(t)


def convert_file(task_id):
    task = task_get(task_id)
    task["conversion_start"] = datetime.utcnow()

    task_set(task)

    output_file = file_manager.generate_file_ref(
        f'output.{task["target_format"]}')

    cmd = ["ffmpeg", "-i", task["input_file"], output_file]

    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
    p.wait()

    task["conversion_end"] = datetime.utcnow()
    task["output_file"] = output_file

    task_set(task)


def handle_request(connection: socket.socket):
    raw = connection.recv(BUFFER_SIZE).decode()
    action = raw.split(SEPARATOR)[0]

    if action == ACTION_SHOW_TASKS:
        connection.sendall("No hay archivos pendientes.".encode())
        connection.close()
    elif action == ACTION_UPLOAD_FILE:
        _, file_name, file_size, target_format = raw.split(SEPARATOR)

        task_id = str(uuid4())[:4]

        connection.sendall(task_id.encode())

        file_name = os.path.basename(file_name)
        file_size = int(file_size)
        tmp_file = file_manager.generate_file_ref(file_name)

        with open(tmp_file, "wb") as f:
            try:
                while True:
                    bytes_read = connection.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break

                    f.write(bytes_read)
            finally:
                print("michelle")
                connection.close()

        task_set({
            "id": task_id,
            "file_name": file_name,
            "input_file": tmp_file,
            "target_format": target_format,
            "conversion_start": None,
            "conversion_end": None,
            "output_file": None
        })

        _thread.start_new_thread(convert_file, (task_id, ))
    elif action == ACTION_RETRIEVE_FILE:
        _, task_id = raw.split(SEPARATOR)

        tmp_task = task_get(task_id)
        connection.send(
            f'{task_id}{SEPARATOR}{tmp_task["file_name"]}{SEPARATOR}{tmp_task["target_format"]}{SEPARATOR}{tmp_task["conversion_start"]}'.encode())

        while True:
            if task_get(task_id)["conversion_end"] != None:
                break
            else:
                print("not yet!")

        with open(task_get(task_id)["output_file"], "rb") as f:
            try:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)

                    if not bytes_read:
                        break

                    connection.sendall(bytes_read)
            finally:
                print("Michelle")
                connection.close()

while True:
    connection, client_info = ServerSocket.accept()
    print(f"Connected to {client_info[0]}:{client_info[1]}")

    print(tasks)

    _thread.start_new_thread(handle_request, (connection,))

# ServerSocket.close()
