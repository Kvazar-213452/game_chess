class Pawn():
    @staticmethod
    def get_pawn_moves(self, row, col, piece):
        moves = []
        direction = -1 if piece == "P" else 1
        start_row = 6 if piece == "P" else 1

        if 0 <= row + direction < self.board_size and self.board[row + direction][col] == 0:
            moves.append((row + direction, col))

        if row == start_row and 0 <= row + 2 * direction < self.board_size and self.board[row + direction][col] == 0 and self.board[row + 2 * direction][col] == 0:
            moves.append((row + 2 * direction, col))

        for dcol in [-1, 1]:
            new_col = col + dcol
            if 0 <= new_col < self.board_size and 0 <= row + direction < self.board_size:
                target = self.board[row + direction][new_col]
                if target != 0 and ((piece == "P" and target.lower() == target) or
                                    (piece == "p" and target.upper() == target)):
                    moves.append((row + direction, new_col))

        return moves