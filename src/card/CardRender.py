import random
import pygame
from functools import partial
from src.card.CardFunc import CardFunc

class Card:
    def __init__(self, board):
        self.card_list = [
            ["beck", partial(CardFunc.beck_func, board)],
            ["block", partial(CardFunc.block_func, board)]
        ]
        
        self.card_user = []
        self.buttons = []
        self.button_y_position = 50
        self.font = pygame.font.SysFont("Arial", 16)
        self.button_vertical_spacing = 10
        self.board = board 

    def create_button(self, text, y, width, height, function):
        button_rect = pygame.Rect(10, y, width, height)
        button_text = self.font.render(text, True, (255, 255, 255))
        self.buttons.append({"rect": button_rect, "text": button_text, "function": function, "label": text})
        self.button_y_position = button_rect.bottom + self.button_vertical_spacing

    def get_card(self):
        random_index = random.randint(0, len(self.card_list) - 1)
        selected_card = self.card_list[random_index]
        self.card_user.append(selected_card)
        return selected_card

    def card_render(self):
        self.clear_cards()
        for card in self.card_user:
            self.create_button(card[0], self.button_y_position, 180, 40, card[1])

    def remove_card(self, beck):
        i = 0

        while i < len(self.card_user):
            if self.card_user[i][0] == beck:
                del self.card_user[i]
                i += 1
                break
            i += 1
        self.card_render()

    def clear_cards(self):
        self.buttons.clear()
        self.button_y_position = 50
