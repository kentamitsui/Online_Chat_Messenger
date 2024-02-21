import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = "localhost"
server_port = 9001

try:
    username = input("please input your username: ")
    message = input("please input message: ")
    inputcontents = f"username: {username} message: {message}".encode("utf-8")

    client_socket.sendto(inputcontents, (server_address, server_port))

    while True:
        data, server = client_socket.recvfrom(4096)
        print(data.decode("utf-8"))

finally:
    client_socket.close()