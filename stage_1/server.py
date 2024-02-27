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

        length_username = data[0]
        # decode username and message send from client side
        # client =>> server
        username = data[1:length_username + 1].decode("utf-8")
        sentence = data[length_username + 1:].decode("utf-8")
        # send format sentence to client side
        # server ==>> client
        formatted_message = f"\nmessage: {sentence} from: {username}\naddress: {address}".encode("utf-8")

        print(f"\nmessage: {sentence} from: {username}\naddress: {address}")
        for client_address in clients.keys():
            if client_address != address:
                server_socket.sendto(formatted_message, client_address)

        print(clients)
    except Exception as e:
        print(f"error: " + e)