class Bishop:
    @staticmethod
    def get_bishop_moves(board, row, col, piece):
        moves = []
        
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = row, col
            while True:
                new_row += drow
                new_col += dcol
                
                if new_row < 0 or new_row >= board.board_size or new_col < 0 or new_col >= board.board_size:
                    break
                
                target = board.board[new_row][new_col]
                
                if target == 0:
                    moves.append((new_row, new_col))
                elif (piece.isupper() and target.islower()) or (piece.islower() and target.isupper()):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
