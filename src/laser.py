import pygame
from constants import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 8 if direction == "right" else -8  # Velocidad del láser
        self.direction = direction
        self.image = pygame.image.load('./src/assets/Laser/bullet_pink.png')  # Carga la imagen del láser
        self.image = pygame.transform.scale(self.image, (100,100))

    def update(self):
        self.rect.x += self.x_vel

        # Verifica si el láser se ha salido de la pantalla
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def draw(self, win):
        win.blit(self.image, self.rect)
        