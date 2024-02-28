import socket, time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = "0.0.0.0"
server_port = 9001
server_socket.bind((server_address, server_port))
clients = {}

print(f"starting up on {server_address} port: {server_port}")

while True:
    try:
        data, address = server_socket.recvfrom(4096)

        length_username = data[0]
        # decode username and message send from client side
        # client =>> server
        
        # username = data[1:length_username + 1].decode("utf-8")
        # sentence = data[length_username + 1:].decode("utf-8")
        
        # send format sentence to client side
        # server ==>> client
        # formatted_message = f"\nmessage: {sentence} from: {username}\naddress: {address}".encode("utf-8")

        timestamp = int.from_bytes(data[1:5], byteorder="big")
        current_time = int(time.time())
        clients[address] = {"last_active time: ": current_time, "errors: ": 0}

        # print(f"\nmessage: {sentence} from: {username}\naddress: {address}")
        # print(data[1:].decode("utf-8"))
        
        for client_address in clients.keys():
            try:
                if client_address != address:
                    server_socket.sendto(formatted_message, client_address)
            except Exception as error:
                clients[client_address]["errors"] += 1
                print(f"error sending to {client_address}: {error}")                

        for client_address, info in list(clients.items()):
            if (current_time - info["last_active time: "] > 60) or (info["errors: "] >= 5):
                print(f"removing client {client_address}")
                del clients[client_address]
        
        if client_address not in clients:
            clients[client_address] = True
            print(f"New client connected: {client_address}")

    except Exception as e:
        print(f"error: {e}")