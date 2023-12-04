import pygame

class BulletBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, image):
        super().__init__()
        self.image = image  # Usa la imagen pasada como argumento
        self.rect = self.image.get_rect()  # Obtiene el rectángulo del disparo a partir de la imagen
        self.rect.topleft = (x, y)  # Posiciona el disparo
        self.dx = dx  # La velocidad horizontal del disparo
        self.dy = dy  # La velocidad vertical del disparo

    def update(self):
        self.rect.x += self.dx  # Mueve el disparo horizontalmente
        self.rect.y += self.dy  # Mueve el disparo verticalmente

    def draw(self, win):
        win.blit(self.image, self.rect)  # Dibuja el disparo usando la imagen