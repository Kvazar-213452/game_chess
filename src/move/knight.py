class Knight:
    @staticmethod
    def get_knight_moves(board, start_x, start_y, piece):
        knight_moves = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        valid_moves = []
        
        for dx, dy in knight_moves:
            end_x = start_x + dx
            end_y = start_y + dy
            
            if 0 <= end_x < board.board_size and 0 <= end_y < board.board_size:
                target_piece = board.board[end_x][end_y]
                
                if target_piece != 0 and board.is_current_player_piece(target_piece):
                    continue

                valid_moves.append((end_x, end_y))
        
        return valid_moves
