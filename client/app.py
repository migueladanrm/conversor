def read_file(path):
    stream = b""

    file = open(path, "rb")
    stream = file.read()

    return stream


if __name__ == "__main__":
    print("Hello, world!")
