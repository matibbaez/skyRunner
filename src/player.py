import pygame
from coins import Coin
from laser import Laser
from os import listdir
from os.path import isfile, join
from constants import *

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 4
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.sprites = self.load_sprite_sheets("Characters", "Punk", 48, 48, True)
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_time = 0
        self.hit = False
        self.hit_count = 0
        self.lasers = pygame.sprite.Group()
        
    def load_sprite_sheets(self, dir1, dir2, width, height, direction = False):
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
    
    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    def shoot(self):
        laser = Laser(self.rect.centerx, self.rect.centery - 40, 10, 5, self.direction)
        self.lasers.add(laser)

    def update_lasers(self, enemies, coins):
        self.lasers.update()
        collisions = pygame.sprite.groupcollide(self.lasers, enemies, True, True)

        for laser, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                coin = Coin(enemy.rect.centerx, enemy.rect.centery)
                coins.add(coin)

    def draw_lasers(self, win):
        self.lasers.draw(win)
        
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
    
    def move(self, dx, dy):
        if 0 <= self.rect.x + dx <= WIDTH - self.rect.width:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= HEIGHT - self.rect.height:
            self.rect.y += dy
        
    def make_hit(self):
        self.hit = True
        self.hit_count = 0
        
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
            
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
            
        if self.hit and pygame.time.get_ticks() - self.invulnerable_time > 2000:  # 2 segundos de invulnerabilidad
            self.hit = False
            self.invulnerable = False
            
        self.fall_count += 1
        self.update_sprite()
        
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    def draw(self, win,):
        win.blit(self.sprite, (self.rect.x, self.rect.y))
        