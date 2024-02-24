import socket,sys

def encode_tcp_request(server_address, server_port, room_name, operation, state, username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    room_name_encoded = room_name.encode("utf-8")
    room_name_size = len(room_name_encoded)
    operation_payload = username.encode("utf-8")
    operation_payload_size = len(operation_payload)
    header = bytearray([room_name_size, int(operation), int(state)]) + operation_payload_size.to_bytes(29, byteorder="big")

    client_socket.send(header + room_name_encoded + operation_payload)
    client_socket.close()
    pass

server_address = "localhost"
server_port = 9001

room_name = input("input room name: ")
operation = input("input operation code\n1: create new chat room 2: join chat room: ")
state = input("input state code\n0: initialize of server 1: request of server 2: complete of request: ")
username = input("input any username: ")
                        
encode_tcp_request(server_address, server_port, room_name, operation, state, username)

def connect_udp():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = "localhost"
    server_port = 9001

    try:
        message = input("please input message: ")
        inputcontents = f"message: {message}".encode("utf-8")

        client_socket.sendto(inputcontents, (server_address, server_port))

        while True:
            data, server = client_socket.recvfrom(4096)
            print(data.decode("utf-8"))

    finally:
        client_socket.close()
        pass
    
connect_udp()