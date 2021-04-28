
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
'''
if len(sys.argv) == 2:
    texto = sys.argv[1]
    print(texto)
'''


