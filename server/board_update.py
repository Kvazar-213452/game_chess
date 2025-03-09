import json

class Board:
    @staticmethod
    def broadcast_board_update(chessServer, board_data):
        course = "white" if chessServer.current_turn == 0 else "black"
        chessServer.current_turn = 1 - chessServer.current_turn

        for client, _, _ in chessServer.clients:
            try:
                client.send(json.dumps(["board_data", json.dumps(board_data), course, chessServer.unixP]).encode())
            except Exception as e:
                print(f"Не вдалося відправити оновлену шахівницю: {e}")