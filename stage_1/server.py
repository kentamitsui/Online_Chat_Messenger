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
        timestamp = int.from_bytes(data[1:5], byteorder="big")
        # decode username and message send from client side
        # client =>> server
        username = data[5:length_username + 5].decode("utf-8")
        message = data[length_username + 5:].decode("utf-8")
        
        current_time = int(time.time())
        clients[address] = {"last_active time": current_time, "errors": 0, "active": True}
        # send format sentence to client side
        # server ==>> client
        formatted_message = f"\nmessage: {message} from: {username}\naddress: {address}".encode("utf-8")
        print(formatted_message.decode("utf-8"))

        for client_address, info in list(clients.items()):
            if (current_time - info["last_active time"] > 60) or (info["errors"] >= 5):
                message_disconnect = f"\n{username} is disconnected room".encode("utf-8")
                server_socket.sendto(message_disconnect, client_address)
                server_socket.sendto("you were disconnected".encode("utf-8"), address)
                print(f"removing client: {username}")
                clients[client_address]["active"] = False
                continue
            
            # if clients[client_address]["active"]:
            if info["active"]:
                try:
                    if client_address != address:
                        server_socket.sendto(formatted_message, client_address)
                except Exception as error:
                    clients[client_address]["errors"] += 1
                    print(f"error sending to {client_address}: {error}")                

    except Exception as e:
        print(f"error: {e}")