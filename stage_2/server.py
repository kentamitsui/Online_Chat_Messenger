import socket,os,threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001

chat_room = {}

def handle_client(connection, client_address, room_name):
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

def start_server():
    print(f"starting up on {server_address} port: {server_port}")
    server_socket.bind((server_address, server_port))
    server_socket.listen()

    while True:
        connection, client_address = server_socket.accept()
        print(f"connection from: {client_address}")
        threading.Thread(target=client_thread, args=(connection, client_address)).start()

if __name__ == "__main__":
    start_server()