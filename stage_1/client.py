import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address_port = ("localhost", 9001)
client_socket.connect(server_address_port)
username = input("please input your username: ")


while True:
    try:
        bytes_username = username.encode("utf-8")

        length_username = len(bytes_username)
        if length_username > 255:
            raise ValueError("username is too long. please less than inputed before it.")

        message = input("please input message: ")
        bytes_message = message.encode("utf-8")

        header = bytes([length_username])
        inputcontents = header + bytes_username + bytes_message

        if len(inputcontents) < 4096:
            client_socket.sendto(inputcontents, server_address_port)

            data, server = client_socket.recvfrom(4096)
            print(data.decode("utf-8"))
            
    except Exception as e:
        print(f"error: " + e)
