import pygame
from os import listdir
from os.path import isfile, join

class Enemy(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 4
    MOVE_SPEED = 3  # Velocidad de movimiento

    def __init__(self, x, y, width, height, sprites):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = self.MOVE_SPEED  # Inicia moviéndose a la derecha
        self.mask = None
        self.direction = "right"  # Dirección inicial
        self.animation_count = 0
        self.sprites = self.load_enemy_sprites(*sprites)  # Asegúrate de que 'sprites' es una tupla con los argumentos correctos para 'load_enemy_sprites'
        self.left_limit = x - 100  # Límite izquierdo
        self.right_limit = x + 100  # Límite derecho

    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    def load_enemy_sprites(self, dir1, dir2, width, height, direction=False):
        path = join("src", "assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            sprites = []
            for i in range(sprite_sheet.get_width() // width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = self.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def loop(self, objects):
        # Cambia la dirección si llega a los bordes
        if self.rect.x <= self.left_limit or self.rect.x >= self.right_limit:
            self.x_vel = -self.x_vel
            if self.direction == "right":
                self.direction = "left"
            else:
                self.direction = "right"

        self.move(self.x_vel, 0)

        # Actualiza la animación según la dirección y la velocidad
        if self.x_vel != 0:
            try:
                sprite_sheet_name = "walk_" + self.direction
                sprites = self.sprites[sprite_sheet_name]
            except KeyError:  # Si no hay animaciones de caminar, usa las animaciones "idle"
                sprite_sheet_name = "idle_" + self.direction
                sprites = self.sprites[sprite_sheet_name]
        else:
            sprite_sheet_name = "idle_" + self.direction
            sprites = self.sprites[sprite_sheet_name]

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.animation_count += 1
        sprite = sprites[sprite_index]
        self.image = sprite

    def draw(self, win):
        sprite_sheet_name = "walk_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        sprite = sprites[sprite_index]
        win.blit(sprite, (self.rect.x, self.rect.y))