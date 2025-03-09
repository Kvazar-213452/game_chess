import socket
import pygame
import sys
import json
import threading
from src.config import config
from src.board import Board
from src.card.CardRender import Card

HOST = '127.0.0.1'
PORT = 12345

pygame.init()

screen = pygame.display.set_mode((config["window_width"], config["window_height"]), pygame.RESIZABLE)
pygame.display.set_caption("Python Chess")

font = pygame.font.SysFont("Arial", 16)

panel_width = 200
panel_color = (240, 240, 240)
panel_z_index = 1000000000000

let_card_course = 0

def handle_button_click(event, card, board):
    if board.player_color == board.current_turn:
        for button in card.buttons:
            if button["rect"].collidepoint(event.pos):
                print(f"Натиснуто на кнопку: {button['label']}")
                button["function"]()
                card.remove_card(button['label'])

def display_status(status):
    text = font.render(f"Статус: {status}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def receive_updates(client_socket, board, card):
    global let_card_course

    while True:
        try:
            data = client_socket.recv(1024).decode()
            data1 = json.loads(data)

            if not data1:
                break

            if data1[0] == "board_data":
                let_card_course += 1

                board.history.append(board.board.copy())

                board.board = json.loads(data1[1])
                board.current_turn = data1[2]
                print("updata")

                if let_card_course == 2:
                    card.get_card()
                    card.card_render()
                    let_card_course = 0

        except Exception as e:
            print("error", e)
            break

def start_chess_game(status, board_data, client_socket):
    board = Board(screen, status, board_data, client_socket, "white")
    board.load_textures()
    board.load_board()
    board.update_board_size()

    card = Card(board)

    card.get_card()
    card.card_render()

    receive_thread = threading.Thread(target=receive_updates, args=(client_socket, board, card), daemon=True)
    receive_thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                board.update_board_size()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(event, card, board)
                board.mouse_pressed(event.pos)

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, panel_color, pygame.Rect(0, 0, panel_width, config["window_height"]), border_radius=10)

        for button in card.buttons:
            pygame.draw.rect(screen, (0, 128, 255), button["rect"])
            screen.blit(button["text"], (button["rect"].x + (button["rect"].width - button["text"].get_width()) // 2,
                                         button["rect"].y + (button["rect"].height - button["text"].get_height()) // 2))

        board.draw_board()
        board.draw_pieces()
        board.draw_highlights()

        display_status(f"Ваш статус: {status}")

        pygame.display.flip()

    pygame.quit()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    status = client_socket.recv(1024).decode()
    board_data = json.loads(client_socket.recv(1024).decode())

    while True:
        message = client_socket.recv(1024).decode()
        message = json.loads(message)
        
        if message[0] == "game_start":
            print("satrt game")
            start_chess_game(status, board_data, client_socket)
            break

    client_socket.close()
    sys.exit()

if __name__ == "__main__":
    start_client()
