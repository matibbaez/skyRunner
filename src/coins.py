import pygame

class Coin(pygame.sprite.Sprite):
    GRAVITY = 1  # Define la gravedad

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./src/assets/Consumible/coin_points.png")
        self.image = pygame.transform.scale(self.image, (20, 20))  # Escala la imagen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0  # Velocidad inicial en el eje y

    def update(self, platforms):
        self.y_vel += self.GRAVITY  # Aplica la gravedad
        self.rect.y += self.y_vel  # Mueve la moneda

        # Verifica si la moneda ha colisionado con una plataforma
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                self.rect.bottom = platform.rect.top  # Coloca la moneda en la plataforma
                self.y_vel = 0  # Detiene la caída