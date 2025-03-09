import socket
import threading
import json
from board_update import Board

HOST = '127.0.0.1'
PORT = 12345

class ChessServer:
    def __init__(self):
        self.statuses = ['white', 'black']
        self.clients = []
        self.current_turn = 1
        self.let_card_back = 0
        self.unix = 0
        self.unixP = 0
        self.pieces = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

    def handle_client(self, client_socket, client_address, client_status):
        print(f"add client {client_address} status {client_status}")
        client_socket.send(client_status.encode())

        client_socket.send(json.dumps(self.pieces).encode())

        if len(self.clients) == 2:
            print("start game")
            for client, _, status in self.clients:
                client.send(json.dumps(["game_start"]).encode())

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            
            message = message.decode()
            message = json.loads(message)

            if message[0] == "board_data":

                if self.let_card_back == 1:
                    print("1")
                    self.unixP = 1
                    if self.unix == 2:
                        print("2")
                        self.let_card_back = 0
                    else:
                        print(self.unix)
                        self.unix += 1
                else:
                    self.unixP = 0

                try:
                    Board.broadcast_board_update(self, json.loads(message[1]))
                except json.JSONDecodeError:
                    print(f"Повідомлення від {client_address}: {message}")
            elif message[0] == "card_back":
                self.let_card_back = 1

        print(f"disconnect {client_address}")
        client_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        print("start")

        while len(self.clients) < 2:
            client_socket, client_address = server_socket.accept()
            client_status = self.statuses[len(self.clients)]
            self.clients.append((client_socket, client_address, client_status))

            threading.Thread(target=self.handle_client, args=(client_socket, client_address, client_status)).start()

if __name__ == "__main__":
    server = ChessServer()
    server.start_server()
