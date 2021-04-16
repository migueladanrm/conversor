import argparse
import sys
import socket


host = "0.0.0.0"
data_payload = 2048
backlog = 5


def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = (host, port)

    print("Starting up echo server on port {}:{}...".format(host, port))

    sock.bind(server_address)

    sock.listen(backlog)

    while True:
        print("Waiting for connections...")
        client, address = sock.accept()

        if data:
            client.send(data)
            print("Send info to {}, {}...".format(data, address))

        client.close()


def server(host, port):
    # socket.AF_INET se refiere al socket ipv4.SOCK_STREAM usando el protocolo tcp
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                    1)  # Establecer el puerto
    sock.bind((host, port))       # Puerto de enlace
    sock.listen(3)                    # Puerto de escucha
    while True:
        # Cuando hay una solicitud para el puerto especificado, accpte () devolverá un nuevo socket y el host (ip, port)
        sc, sc_name = sock.accept()
        print('Recibió {} solicitud'.format(sc_name))
        # Primero reciba un dato, este dato contiene la longitud del archivo y el nombre del archivo, separados por |, las reglas específicas se pueden especificar en el cliente
        infor = sc.recv(1024)
        length, file_name = infor.decode().split('|')
        if length and file_name:
            # El nombre de archivo analizado desde el cliente se puede usar aquí
            newfile = open('image/'+str(random.randint(1, 10000))+'.jpg', 'wb')
            print('length {},filename {}'.format(length, file_name))
            # Indica la longitud del archivo recibido y el nombre del archivo
            sc.send(b'ok')
            file = b''
            total = int(length)
            get = 0
            while get < total:  # Recibir archivos
                data = sc.recv(1024)
                file += data
                get = get + len(data)
            print('Debería recibir {}, en realidad recibir {}'.format(
                length, len(file)))
            if file:
                print('acturally length:{}'.format(len(file)))
                newfile.write(file[:])
                newfile.close()
                sc.send(b'copy')  # Diga el archivo completo recibido
        sc.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket Server Example")
    parser.add_argument("--port", action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port

    echo_server(port)
