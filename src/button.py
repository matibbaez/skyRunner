import pygame
from constants import *

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, win):
        pygame.draw.rect(win, self.hover_color if self.hovered else self.color, self.rect, border_radius=5)
        font = pygame.font.SysFont("Poppins", 25)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(text, text_rect)

    def is_hovered(self, pos):
        self.hovered = self.rect.collidepoint(pos)