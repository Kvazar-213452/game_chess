class King:
    @staticmethod
    def get_king_moves(board, row, col, piece):
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (1, 1), (-1, 1), (1, -1)
        ]
        
        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.board[new_row][new_col] == 0 or \
                   (board.is_current_player_piece(board.board[new_row][new_col]) != board.is_current_player_piece(piece)):
                    moves.append((new_row, new_col))
        
        return moves
