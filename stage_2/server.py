# the threading method uses multiple thread to can execute parallel processing.
import socket,threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001

chat_room = {}

def handle_client(connection, client_address, operation, room_name):
    while True:
        header = connection.recv(32)
        if not header:
            break

        RoomNameSize = int.from_bytes(header[0], "big")
        operation = int.from_bytes(header[1], "big")
        State = int.from_bytes(header[2], "big")
        OperationPayloadSize = int.from_bytes(header[3:32], "big")

        RoomNames = connection.recv(RoomNameSize).decode("utf-8")
        operation_payload = connection.recv(OperationPayloadSize)

        print(f"room name: {RoomNames}".format(RoomNames))
                                                
            
    try:
        while True:
            message = connection.recv(1024)
            if message:
                print(f"message from {client_address}: {message.decode('utf-8')}")
            else:
                break
    finally:
        connection.close()

def client_thread(connection, client_address):
    try:
        room_name = connection.recv(1024).decode("utf-8")
        if room_name not in chat_room:
            chat_room[room_name] = []
        chat_room[room_name].append((connection, client_address))
        print(f"{client_address} joined room: {room_name}")

        handle_client(connection, client_address, room_name)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def start_tcp_server():
    print(f"starting up on {server_address} port: {server_port}")
    server_socket.bind((server_address, server_port))
    server_socket.listen()

    while True:
        client_address = server_socket.accept()
        print(f"connection from: {client_address}")
        pass

def start_udp_server():
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
                    
        except Exception as e:
            print(f"error: " + e)
        pass

if __name__ == "__main__":
    # use the threading module to send message to all other clients
    threading.Thread(target=start_tcp_server).start()
    threading.Thread(target=start_udp_server).start()
