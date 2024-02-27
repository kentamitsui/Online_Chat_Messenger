import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = "0.0.0.0"
server_port = 9001
server_socket.bind((server_address, server_port))
clients = {}

print(f"starting up on {server_address} port: {server_port}")

while True:
    try:
        data, address = server_socket.recvfrom(4096)

        if address not in clients:
            clients[address] = True
            print(f"New client connected: {address}")

        for client_address in clients.keys():
            if client_address != address:
                server_socket.sendto(data, client_address)

        print(clients)
    except Exception as e:
        print(f"error: " + e)