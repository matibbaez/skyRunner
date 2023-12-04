import pygame
from objects import Object
from os import listdir
from os.path import isfile, join

class Block(Object):
    def __init__(self, x, y, size, terrain):
        super().__init__(x, y, size, size)
        block = self.get_block(size, terrain)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        
    def get_block(self, size, terrain):
        path = join("src", "assets", "Terrain", "Terrain.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)

        if terrain == "terrain1":
            rect = pygame.Rect(0, 0, size, size)
        elif terrain == "terrain2":
            rect = pygame.Rect(0, 128, size, size)
        elif terrain == "terrain3":
            rect = pygame.Rect(0, 64, size, size)

        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)