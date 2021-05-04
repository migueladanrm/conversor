from datetime import datetime
from uuid import uuid4
import _thread
import os
import socket
import subprocess

BUFFER_SIZE = 1024
SEPARATOR = "|"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7000
STORE_PATH = "/tmp"

ACTION_SHOW_TASKS = "show-tasks"
ACTION_UPLOAD_FILE = "upload-file"
ACTION_RETRIEVE_FILE = "retrieve-file"

tasks = []

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


def generate_file_ref(file_name):
    return f"{STORE_PATH}/{str(uuid4())[:8]}_{file_name}"


def convert_file(task_id):
    task = task_get(task_id)
    task["conversion_start"] = datetime.utcnow()

    task_set(task)

    output_file = generate_file_ref(
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
        result = ""
        if len(tasks) < 1:
            result = "There aren't files in the queue."
        else:
            for t in tasks:
                result = f'{result}Id: {t["id"]}\tInput file: {t["file_name"]}\tTarget format: {t["target_format"]}\tStart: {t["conversion_start"]}\tEnd: {t["conversion_end"]}\n'

        connection.sendall(result.encode())
        connection.close()
    elif action == ACTION_UPLOAD_FILE:
        _, file_name, file_size, target_format = raw.split(SEPARATOR)

        task_id = str(uuid4())[:4]

        connection.sendall(task_id.encode())

        file_name = os.path.basename(file_name)
        file_size = int(file_size)
        tmp_file = generate_file_ref(file_name)

        with open(tmp_file, "wb") as f:
            try:
                while True:
                    bytes_read = connection.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break

                    f.write(bytes_read)
            finally:
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
            f'{task_id}{SEPARATOR}{tmp_task["file_name"]}{SEPARATOR}{tmp_task["target_format"]}{SEPARATOR}{tmp_task["conversion_start"]}{SEPARATOR}{datetime.utcnow()}'.encode())

        while True:
            if task_get(task_id)["conversion_end"] != None:
                break

        connection.send(
            f'{datetime.utcnow()}{SEPARATOR}{os.path.getsize(task_get(task_id)["output_file"])}'.encode())

        with open(task_get(task_id)["output_file"], "rb") as f:
            try:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)

                    if not bytes_read:
                        break

                    connection.sendall(bytes_read)
            finally:
                connection.close()


while True:
    connection, client_info = ServerSocket.accept()

    _thread.start_new_thread(handle_request, (connection,))
