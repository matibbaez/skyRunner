import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, window):
        window.blit(self.image, self.rect)