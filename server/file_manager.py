from uuid import uuid4

STORE_PATH = "/tmp"


def generate_file_ref(file_name):
    return f"{STORE_PATH}/{str(uuid4())[:8]}{file_name}"


def clear_store():
    print("Cleaning temporary storage directory...")
