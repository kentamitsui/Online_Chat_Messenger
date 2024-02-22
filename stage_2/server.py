import socket,os
from pathlib import Path

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001

file_receive = "temp"
if not os.path.exists(file_receive):
    os.makedirs(file_receive)

print(f"starting up on {server_address} port: {server_port}")
server_socket.bind((server_address, server_port))
server_socket.listen(1)

while True:
    connection, client_address = server_socket.accept()
    
    try:
        print(f"connection from: ", client_address)
        header = connection.recv(8)

        filename_length = int.from_bytes(header[:1], "big")
        json_length = int.from_bytes(header[1:3], "big")
        data_length = int.from_bytes(header[4:8], "big")
        stream_rate = 4096

        print(f"received header from client.\nbyte length: title length: {filename_length}, JSON length: {json_length}, data length: {data_length}".format(filename_length, json_length, data_length))

        filename = connection.recv(filename_length).decode("utf-8")
        print(f"filename: {filename}".format(filename))

        if json_length != 0:
            raise Exception("JSON data is not currently supported.")
        if data_length == 0:
            raise Exception("no data to read from client.")
        
        with open(os.path.join(file_receive, filename), "wb+") as file:
            while data_length > 0:
                data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                file.write(data)
                print(f"received {data} bytes".format(len(data)))
                data_length -= len(data)
                print(data_length)
            print("finished downloading the file from client.")
                
    except Exception as e:
        print(f"error: " + str(e))

    finally:
        print("closing current connection")
        connection.close()