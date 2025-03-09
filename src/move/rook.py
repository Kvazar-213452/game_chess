class Rook():
    @staticmethod
    def get_rook_moves(self, row, col, piece):
        moves = []

        for dcol in [-1, 1]:
            new_col = col
            while True:
                new_col += dcol
                if new_col < 0 or new_col >= self.board_size:
                    break
                target = self.board[row][new_col]
                if target == 0:
                    moves.append((row, new_col))
                elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    moves.append((row, new_col))
                    break
                else:
                    break

        for drow in [-1, 1]:
            new_row = row
            while True:
                new_row += drow
                if new_row < 0 or new_row >= self.board_size:
                    break
                target = self.board[new_row][col]
                if target == 0:
                    moves.append((new_row, col))
                elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    moves.append((new_row, col))
                    break
                else:
                    break

        return moves