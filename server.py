import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 12345

statuses = ['white', 'black']
clients = []
curnt = 1

pieces = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

def broadcast_board_update(board_data):
    course = ""
    global curnt

    if curnt == 0:
        course = "white"
        curnt = 1
    else:
        course = "black"
        curnt = 0

    for client, _, _ in clients:
        try:
            client.send(json.dumps(["board_data", json.dumps(board_data), course]).encode())
        except Exception as e:
            print(f"Не вдалося відправити оновлену шахівницю: {e}")

def handle_client(client_socket, client_address, client_status):
    print(f"add claint {client_address} status {client_status}")
    client_socket.send(client_status.encode())

    client_socket.send(json.dumps(pieces).encode())

    if len(clients) == 2:
        print("start game")
        for client, _, status in clients:
            client.send(json.dumps(["game_start"]).encode())

    while True:
        message = client_socket.recv(1024)
        if not message:
            break
        
        message = message.decode()
        message = json.loads(message)

        if message[0] == "board_data":
            try:
                broadcast_board_update(json.loads(message[1]))
            except json.JSONDecodeError:
                print(f"Повідомлення від {client_address}: {message}")

    print(f"disconect {client_address}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print("satrt")

    while len(clients) < 2:
        client_socket, client_address = server_socket.accept()
        client_status = statuses[len(clients)]
        clients.append((client_socket, client_address, client_status))

        threading.Thread(target=handle_client, args=(client_socket, client_address, client_status)).start()

if __name__ == "__main__":
    start_server()
