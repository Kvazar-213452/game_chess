import pygame
from src.config import config

def load_textures():
    textures = {
        "P": pygame.image.load("assets/white_pawn.png"),
        "R": pygame.image.load("assets/white_rook.png"),
        "N": pygame.image.load("assets/white_knight.png"),
        "B": pygame.image.load("assets/white_bishop.png"),
        "Q": pygame.image.load("assets/white_queen.png"),
        "K": pygame.image.load("assets/white_king.png"),
        "p": pygame.image.load("assets/black_pawn.png"),
        "r": pygame.image.load("assets/black_rook.png"),
        "n": pygame.image.load("assets/black_knight.png"),
        "b": pygame.image.load("assets/black_bishop.png"),
        "q": pygame.image.load("assets/black_queen.png"),
        "k": pygame.image.load("assets/black_king.png"),
    }
    return textures

def draw_board(screen, board_size, cell_size, offset_x, offset_y):
    for row in range(board_size):
        for col in range(board_size):
            if (row + col) % 2 == 0:
                color = config["board_color_light"]
            else:
                color = config["board_color_dark"]
            
            pygame.draw.rect(screen, color, 
                             (offset_x + col * cell_size, offset_y + row * cell_size,
                              cell_size, cell_size))
