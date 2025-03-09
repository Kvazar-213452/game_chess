class Queen:
    @staticmethod
    def get_queen_moves(board, start_x, start_y, piece):
        valid_moves = []

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = start_x, start_y
            while True:
                x += dx
                y += dy
                if not (0 <= x < board.board_size and 0 <= y < board.board_size):
                    break
                target_piece = board.board[x][y]
                if target_piece == 0:
                    valid_moves.append((x, y))
                elif board.is_current_player_piece(target_piece):
                    break
                else:
                    valid_moves.append((x, y))
                    break

        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            x, y = start_x, start_y
            while True:
                x += dx
                y += dy
                if not (0 <= x < board.board_size and 0 <= y < board.board_size):
                    break
                target_piece = board.board[x][y]
                if target_piece == 0:
                    valid_moves.append((x, y))
                elif board.is_current_player_piece(target_piece):
                    break
                else:
                    valid_moves.append((x, y))
                    break

        return valid_moves
