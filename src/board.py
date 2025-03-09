import pygame
import json
from src.config import config
from src.load import load_textures, draw_board
from src.screen import update_board_size
from src.move.pawn import Pawn
from src.move.rook import Rook
from src.move.bishop import Bishop
from src.move.knight import Knight
from src.move.queen import Queen
from src.move.king import King

class Board:
    def __init__(self, screen, player_color, board_data, client_socket, current_turn):
        self.screen = screen
        self.board_size = config["board_size"]
        self.cell_size = config["cell_size"]
        self.textures = {}
        self.board = []
        self.offset_x, self.offset_y = 0, 0
        self.highlighted_moves = []
        self.selected_piece = None
        self.player_color = player_color
        self.board_data = board_data
        self.client_socket = client_socket
        self.current_turn = current_turn
        self.history = []

    def load_textures(self):
        self.textures = load_textures()

    def draw_board(self):
        draw_board(self.screen, self.board_size, self.cell_size, self.offset_x, self.offset_y)

    def load_board(self):
        for row in range(8):
            self.board.append(self.board_data[row])

    def update_board_size(self):
        self.cell_size, self.offset_x, self.offset_y = update_board_size(self.screen, self.board_size, self.cell_size)

    def draw_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if piece != 0 and piece in self.textures:
                    img = self.textures[piece]
                    img_width, img_height = img.get_size()
                    scale_x = self.cell_size / img_width * config["piece_scale"]
                    scale_y = self.cell_size / img_height * config["piece_scale"]
                    x = self.offset_x + (col * self.cell_size) + (self.cell_size - img_width * scale_x) / 2
                    y = self.offset_y + (row * self.cell_size) + (self.cell_size - img_height * scale_y) / 2
                    self.screen.blit(pygame.transform.scale(img, (int(img_width * scale_x), int(img_height * scale_y))), (x, y))

    def draw_highlights(self):
        for move in self.highlighted_moves:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (self.offset_x + move[1] * self.cell_size,
                              self.offset_y + move[0] * self.cell_size, self.cell_size, self.cell_size),
                             width=0)

    def send_board_update(self, client_socket, board_data):
        try:
            board_data_json = json.dumps(board_data)
            client_socket.send(json.dumps(["board_data", board_data_json]).encode())
            print("server board")
        except Exception as e:
            print(f"Помилка при відправці шахівниці: {e}")

    @staticmethod
    def send_board_update1(client_socket, board_data):
        try:
            board_data_json = json.dumps(board_data)
            client_socket.send(json.dumps(["board_data", board_data_json]).encode())
            print("server board")
        except Exception as e:
            print(f"Помилка при відправці шахівниці: {e}")

    def mouse_pressed(self, pos):
        col = int((pos[0] - self.offset_x) / self.cell_size)
        row = int((pos[1] - self.offset_y) / self.cell_size)

        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            piece = self.board[row][col]

            if piece != 0:
                is_current_player_piece = self.is_current_player_piece(piece)
                if is_current_player_piece:
                    if self.selected_piece:
                        if self.is_move_valid(self.selected_piece, self.selected_x, self.selected_y, row, col):
                            if self.player_color == self.current_turn:
                                self.board[row][col] = self.selected_piece
                                self.board[self.selected_x][self.selected_y] = 0
                                self.selected_piece = None
                                self.highlighted_moves = []

                                self.send_board_update(self.client_socket, self.board)
                        else:
                            self.selected_piece = self.board[row][col]
                            self.selected_x, self.selected_y = row, col
                            if self.selected_piece.lower() == 'r':
                                self.highlighted_moves = Rook.get_rook_moves(self, row, col, piece)
                            elif self.selected_piece.lower() == 'b':
                                self.highlighted_moves = Bishop.get_bishop_moves(self, row, col, self.selected_piece)
                            elif self.selected_piece.lower() == 'n':
                                self.highlighted_moves = Knight.get_knight_moves(self, row, col, piece)
                            elif self.selected_piece.lower() == 'q':
                                self.highlighted_moves = Queen.get_queen_moves(self, row, col, piece)
                            elif self.selected_piece.lower() == 'k':
                                self.highlighted_moves = King.get_king_moves(self, row, col, piece)
                            else:
                                self.highlighted_moves = Pawn.get_pawn_moves(self, row, col, piece)
                    else:
                        self.selected_piece = self.board[row][col]
                        self.selected_x, self.selected_y = row, col
                        if self.selected_piece.lower() == 'r':
                            self.highlighted_moves = Rook.get_rook_moves(self, row, col, piece)
                        elif self.selected_piece.lower() == 'b':
                            self.highlighted_moves = Bishop.get_bishop_moves(self, row, col, self.selected_piece)
                        elif self.selected_piece.lower() == 'n':
                            self.highlighted_moves = Knight.get_knight_moves(self, row, col, piece)
                        elif self.selected_piece.lower() == 'q':
                            self.highlighted_moves = Queen.get_queen_moves(self, row, col, piece)
                        elif self.selected_piece.lower() == 'k':
                            self.highlighted_moves = King.get_king_moves(self, row, col, piece)
                        else:
                            self.highlighted_moves = Pawn.get_pawn_moves(self, row, col, piece)
                else:
                    if self.selected_piece:
                        if self.is_move_valid(self.selected_piece, self.selected_x, self.selected_y, row, col):
                            if self.player_color == self.current_turn:
                                self.board[row][col] = self.selected_piece
                                self.board[self.selected_x][self.selected_y] = 0
                                self.selected_piece = None
                                self.highlighted_moves = []

                                self.send_board_update(self.client_socket, self.board)
            else:
                if self.selected_piece:
                    if self.is_move_valid(self.selected_piece, self.selected_x, self.selected_y, row, col):
                        if self.player_color == self.current_turn:
                            self.board[row][col] = self.selected_piece
                            self.board[self.selected_x][self.selected_y] = 0
                            self.selected_piece = None
                            self.highlighted_moves = []

                            self.send_board_update(self.client_socket, self.board)

    def is_move_valid(self, piece, start_x, start_y, end_x, end_y):
        for move in self.highlighted_moves:
            if move[0] == end_x and move[1] == end_y:
                return True
        return False

    def is_current_player_piece(self, piece):
        if (self.player_color == "white" and piece.isupper()) or (self.player_color == "black" and piece.islower()):
            return True
        return False
