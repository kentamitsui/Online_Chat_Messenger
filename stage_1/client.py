import socket, threading

def send_message(client_socket, server_address_port, username):
    while True:
        message = input("\nplease input message: ")
        bytes_message = message.encode("utf-8")
        bytes_username = username.encode("utf-8")
        header = bytes([len(bytes_username)])
        inputcontents = header + bytes_username + bytes_message
        
        if len(inputcontents) <= 4096:
            client_socket.sendto(inputcontents, server_address_port)

def receive_message(client_socket):
    while True:
        data, address = client_socket.recvfrom(4096)


        # message = address[0:1 + address:].decode("utf-8")
        print(data.decode("utf-8"))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address_port = ("localhost", 9001)

username = input("please input your username: ")
if len(username.encode("utf-8")) > 255:
    raise ValueError("username is too long. please inputed less than before it.")

threading.Thread(target=send_message, args=(client_socket, server_address_port, username), daemon=True).start()
threading.Thread(target=receive_message, args=(client_socket,), daemon=True).start()

try:
    while True: pass
    
except KeyboardInterrupt:
    print(f"connected closed")
    client_socket.close()