import json

class CardFunc:
    @staticmethod
    def back_func(board, card):
        if len(board.history) > 3:
            if card.let_card_back == 0:
                board.board = board.history.pop()
                board.board = board.history.pop()
                board.board = board.history.pop()

                board.client_socket.send(json.dumps(["card_back", 1]).encode())
                board.send_board_update1(board.client_socket, board.board)
                print("Оновлено дошку на два кроки назад")
            else:
                print("pass")
        else:
            print("Немає достатньо попередніх станів для відкату")

    @staticmethod
    def block_func(board, card):
        print("Функція `block_func` викликана з аргументом:")
