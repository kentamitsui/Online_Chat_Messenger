import socket

server_address = input("type in the server's address to connect to: ")
server_port = 9001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))

try:
    room_name = input(f"enter chat room name to join or create: ")
    client_socket.send(room_name.encode("utf-8"))
finally:
    print("closing socket")
    client_socket.close()

# def protocol_header(filename_length, json_length, data_length):
#     return filename_length.to_bytes(1, "big") + json_length.to_bytes(3, "big") + data_length.to_bytes(4, "big")
# ###############################################################
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = input("type in the server's address to connect to: ")
# server_port = 9001

# print(f"connecting to {server_address} {server_port}".format(server_address, server_port))

# try:
#     filepath = input("type in a file to upload: ")

#     with open(filepath, "rb") as file:
#         file.seek(0, os.SEEK_END)
#         filesize = file.tell()
#         file.seek(0, 0)

#         if filesize > pow(2, 32):
#             raise Exception("file size must be below 2GB.")

#         filename = os.path.basename(file.name)
#         filename_bits = filename.encode("utf-8")
#         header = protocol_header(len(filename_bits), 0, filesize)
#         client_socket.send(header)
#         client_socket.send(filename_bits)
#         data = file.read(4096)

#         while data:
#             print("sending...")
#             client_socket.send(data)
#             data = file.read(4096)
        
# finally:
#     print("closing socket")
#     client_socket.close()