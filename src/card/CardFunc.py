class CardFunc:
    @staticmethod
    def beck_func(board):
        if len(board.history) > 3:
            board.board = board.history.pop()
            board.board = board.history.pop()
            board.board = board.history.pop()

            board.send_board_update1(board.client_socket, board.board)
            print("Оновлено дошку на два кроки назад")
        else:
            print("Немає достатньо попередніх станів для відкату")

    @staticmethod
    def block_func(board):
        print("Функція `block_func` викликана з аргументом:")
