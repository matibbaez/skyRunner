import pygame
import sys
import json
from enemies import Enemy
from player import Player
from constants import *
from block import Block
from functions import *
from button import Button, ToggleButton
from boss import Boss
from sounds import *
import os

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Level:
    def __init__(self, window, pause_menu, game_over_menu, enemies, objects, floor, background_image, max_score, level_number, player_name):
        self.window = window
        self.player_name = player_name
        self.max_score = max_score
        self.level_number = level_number
        self.pause_menu = pause_menu
        self.game_over_menu = game_over_menu
        self.enemies = enemies
        self.objects = objects
        self.floor = floor
        self.background_image = background_image
        self.clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        self.pause_start = 0
        self.total_pause_time = 0
        self.score = 0
        self.background, self.bg_image = get_background(self.background_image)
        self.block_size = 96
        self.player = Player(30, 100, 50, 50)
        self.coins = pygame.sprite.Group()
        self.running = True

    def run(self):
        pygame.mixer.music.play(-1)
        
        enemies_added = False
        
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.jump_count < 2:
                        self.player.jump()
                    if event.key == pygame.K_p:
                        self.pause_start = pygame.time.get_ticks()
                        self.pause_menu(self.window)
                        self.total_pause_time += pygame.time.get_ticks() - self.pause_start
                    if event.key == pygame.K_m:
                        if pygame.mixer.music.get_busy():  # Si la música está sonando
                            pygame.mixer.music.stop()  # Detén la música
                        else:
                            pygame.mixer.music.play(-1)
                    
            elapsed_time = (pygame.time.get_ticks() - self.start_ticks - self.total_pause_time) / 1000
                    
            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if enemy_hits and not self.player.invulnerable:
                self.player.lives -= 1
                self.player.hit = True
                self.player.invulnerable = True
                self.player.invulnerable_time = pygame.time.get_ticks()
                if self.player.lives <= 0:
                    pygame.mixer.music.stop()  # Detén la música de fondo
                    game_over_sound.play()  # Reproduce el sonido de "game over"
                    self.game_over_menu(self.window)
                    
            for enemy in self.enemies:
                enemy.loop(self.objects)
                if isinstance(enemy, Boss):  # Si el enemigo es un jefe
                    enemy.update_bullets(self.player)  # Actualiza los disparos del jefe
                    if self.score == 2 and not enemy.bullet_speed_increased:  # Si el jugador ha alcanzado 2 puntos y la velocidad de las balas no ha sido incrementada
                        enemy.bullet_speed += 15  # Aumenta la velocidad de las balas del jefe
                        enemy.bullet_speed_increased = True  # Indica que la velocidad de las balas ha sido incrementada
                
            for coin in self.coins:
                coin.update(self.objects)

            self.player.loop(FPS)
            handle_move(self.player, self.objects, self.enemies, self.coins)
            
            self.player.update_lasers(self.enemies, self.coins)
            
            coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
            self.score += len(coin_hits)

            if self.score == 6 and not enemies_added:
                # Añade nuevos enemigos al grupo self.enemies
                new_enemy1 = Enemy(350, 417, 50, 50, ("Characters", "Enemy", 48, 48, True))
                new_enemy2 = Enemy(600, 610, 50, 50, ("Characters", "Enemy2", 48, 48, True))
                new_enemy3 = Enemy(160, 610, 50, 50, ("Characters", "Enemy", 48, 48, True))
                new_enemy4 = Enemy(90, 417, 50, 50, ("Characters", "Enemy2", 48, 48, True))
                self.enemies.add(new_enemy1, new_enemy2, new_enemy3, new_enemy4)
                enemies_added = True  
                
            if self.score >= self.max_score:  # Si se ha alcanzado la puntuación máxima
                from menus import level_menu
                # Guardar el nombre del jugador, el nivel, la puntuación y el tiempo en un archivo JSON
                scores = []
                if os.path.exists('scores.json'):
                    with open('scores.json', 'r') as f:
                        scores = json.load(f)
                with open('scores.json', 'w') as f:
                    scores.append({'player': self.player_name, 'level': self.level_number, 'score': self.score, 'time': elapsed_time})
                    json.dump(scores, f)
                # Volver al menú de niveles
                level_menu(self.window)
                
            font = pygame.font.SysFont("Minecraft", 25)
            lives_text = font.render("Vidas: " + str(self.player.lives), True, (0, 0, 0))
            self.window.blit(lives_text, (10, 40))
            draw(self.window, self.background, self.bg_image, self.player, self.objects, self.enemies, self.coins, elapsed_time, self.score)

def resume_game(window=None):
    pass

def quit_game(window = None):
    sys.exit()

def pause_menu(window):
    from menus import main_menu
    
    def mute_music():
        pygame.mixer.music.stop()

    def unmute_music():
        pygame.mixer.music.play(-1)

    mute_button = Button("Musica OFF", 400, 300, 200, 50, WHITE, SKY, mute_music)
    unmute_button = Button("Musica ON", 400, 400, 200, 50, WHITE, SKY, unmute_music)
    continue_button = Button("Continuar", 400, 500, 200, 50, WHITE, SKY, action=resume_game)
    menu_button = Button("Menu", 400, 600, 200, 50, WHITE, SKY, action=main_menu)
    quit_button = Button("Salir", 400, 700, 200, 50, (255, 0, 0), (128, 0, 0), action=quit_game)

    buttons = [continue_button, menu_button, quit_button, mute_button, unmute_button]
    background_pause = pygame.transform.scale(pygame.image.load("./src/assets/Background/background2.jpg"), size_screen)

    running = True
    while running:
        window.fill((255, 255, 255))
        window.blit(background_pause, origin)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.action:
                            button.action()
                            if button in [continue_button, menu_button, quit_button]:
                                running = False

        for button in buttons:
            button.is_hovered(pygame.mouse.get_pos())
            button.draw(window)

        pygame.display.update()

def game_over_menu(window):
    from menus import main_menu
    
    button_width = 200
    button_height = 50
    padding = 20  # Espacio entre los botones

    # Calcula las coordenadas x para cada botón
    total_width = 3 * button_width + 2 * padding
    start_x = (WIDTH - total_width) / 2
    restart_button_x = start_x
    back_button_x = start_x + button_width + padding
    quit_button_x = start_x + 2 * button_width + 2 * padding

    # Las coordenadas y son las mismas para todos los botones
    button_y = HEIGHT - button_height - padding

    back_button = Button("Atras", back_button_x, button_y, button_width, button_height, WHITE, SKY, action=main_menu)
    quit_button = Button("Salir", quit_button_x, button_y, button_width, button_height, (255, 0, 0), (128, 0, 0), action=quit_game)

    buttons = [back_button, quit_button]
    background_menu = pygame.transform.scale(pygame.image.load("./src/assets/Background/lostback.jpg"), (WIDTH, HEIGHT))

    running = True
    while running:
        window.fill((255, 255, 255))
        window.blit(background_menu, origin)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.action:
                            button.action(window)
                            running = False

        for button in buttons:
            button.is_hovered(pygame.mouse.get_pos())
            button.draw(window)

        pygame.display.update()
            