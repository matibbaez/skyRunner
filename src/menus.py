import pygame
import sys
from button import Button
from levels import game_over_menu, pause_menu, quit_game, Level
from block import Block
from enemies import Enemy
from obstacle import Obstacle
from constants import *
from boss import Boss
import json

block_size = 96
floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]

def main_menu(window):
    button_width = 200
    button_height = 50
    padding = 20  # Espacio entre los botones

    # Calcula las coordenadas x para cada botón
    total_width = 4 * button_width + 3 * padding  # Aumenta el total_width para incluir el nuevo botón
    start_x = (WIDTH - total_width) / 2
    play_button_x = start_x
    instructions_button_x = start_x + button_width + padding
    score_button_x = start_x + 2 * button_width + 2 * padding  # Añade un nuevo botón aquí
    quit_button_x = start_x + 3 * button_width + 3 * padding  # Actualiza la posición del botón de salir

    # Las coordenadas y son las mismas para todos los botones
    button_y = HEIGHT - button_height - padding

    play_button = Button("Jugar", play_button_x, button_y, button_width, button_height, WHITE, SKY, action=level_menu)
    instructions_button = Button("Instrucciones", instructions_button_x, button_y, button_width, button_height, WHITE, SKY, action=instructions_menu)
    score_button = Button("Puntuaciones", score_button_x, button_y, button_width, button_height, WHITE, SKY, action=score_menu)  
    quit_button = Button("Salir", quit_button_x, button_y, button_width, button_height, (255, 0, 0), (128, 0, 0), action=quit_game)

    buttons = [play_button, instructions_button, score_button, quit_button]
    background_menu = pygame.transform.scale(pygame.image.load("./src/assets/Background/skyrunner.jpg"), (WIDTH, HEIGHT))

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
        
def get_player_name(window):
    w, h = 200, 50  # Define el ancho y la altura de la caja de entrada
    x = (WIDTH - w) / 2
    y = (HEIGHT - h) / 2
    input_box = pygame.Rect(x, y, w, h) # Define la posición y el tamaño de la caja de entrada
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.SysFont("Minecraft", 32)
    label = font.render('Ingrese su nombre', True, (255, 255, 255))  # Nuevo: crea la etiqueta de texto
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return text
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        window.fill((30, 30, 30))
        window.blit(label, (x, y - 40))  # Nuevo: dibuja la etiqueta de texto en la ventana
        txt_surface = font.render(text, True, color)
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(window, color, input_box, 2)
        pygame.display.flip()
        
def start_level1(window):
    player_name = get_player_name(window)
    enemies_level_1 = pygame.sprite.Group(
        Enemy(800, 225, 50, 50, ("Characters", "Enemy", 48, 48, True)),
        Enemy(320, 417, 50, 50, ("Characters", "Enemy", 48, 48, True)),
        Enemy(750, 610, 50, 50, ("Characters", "Enemy", 48, 48, True)),
        Enemy(150, 610, 50, 50, ("Characters", "Enemy", 48, 48, True))
    )
    objects_level_1 = [*floor, 
                   Block(block_size * 2, HEIGHT - block_size * 3, block_size), 
                   Block(block_size * 3, HEIGHT - block_size * 3, block_size), 
                   Block(block_size * 4, HEIGHT - block_size * 3, block_size), 
                   Block(block_size * 5, HEIGHT - block_size * 3, block_size),
                   
                   Block(block_size * 6.4, HEIGHT - block_size * 5, block_size),
                   Block(block_size * 7.4, HEIGHT - block_size * 5, block_size),
                   Block(block_size * 8.4, HEIGHT - block_size * 5, block_size),
                   Block(block_size * 9.4, HEIGHT - block_size * 5, block_size),
                    
                   Block(block_size * 0, HEIGHT - block_size * 6.5, block_size), 
                   Block(block_size, HEIGHT - block_size * 6.5, block_size), 
                   Block(block_size * 2, HEIGHT - block_size * 6.5, block_size), 
                   Block(block_size * 3, HEIGHT - block_size * 6.5, block_size),]

    # Crear el nivel con los corazones
    level_1_final = Level(window, pause_menu, game_over_menu, enemies_level_1, objects_level_1, floor, "Citysky.png", max_score=4, level_number=1, player_name=player_name)
    level_1_final.run()
    
    if not enemies_level_1:
        # Si todos los enemigos han sido eliminados, iniciar el siguiente nivel
        start_level2(window)
    
def start_level2(window):
    player_name = get_player_name(window)
    enemies_level_2 = pygame.sprite.Group(
    Enemy(670, 33, 50, 50, ("Characters", "Enemy2", 48, 48, True)),
    Enemy(500, 417, 50, 50, ("Characters", "Enemy2", 48, 48, True)),
    Enemy(290, 225, 50, 50, ("Characters", "Enemy", 48, 48, True)),
    Enemy(750, 610, 50, 50, ("Characters", "Enemy", 48, 48, True)),
    Enemy(300, 610, 50, 50, ("Characters", "Enemy2", 48, 48, True))
    )
    
    objects_level_2 = [*floor, 
               Block(block_size * 4, HEIGHT - block_size * 3, block_size), 
               Block(block_size * 5, HEIGHT - block_size * 3, block_size), 
               Block(block_size * 6, HEIGHT - block_size * 3, block_size), 
               Block(block_size * 7, HEIGHT - block_size * 3, block_size),
               
               Block(block_size * 5.4, HEIGHT - block_size * 7, block_size),
               Block(block_size * 6.4, HEIGHT - block_size * 7, block_size),
               Block(block_size * 7.4, HEIGHT - block_size * 7, block_size),
               Block(block_size * 8.4, HEIGHT - block_size * 7, block_size),
                
               Block(block_size * 4.5, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 1.5, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 3.5, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 2.5, HEIGHT - block_size * 5, block_size),]
    
    level_2_final = Level(window, pause_menu, game_over_menu, enemies_level_2, objects_level_2, floor, "Citypink.png", max_score=5, level_number=2, player_name=player_name)
    
    level_2_final.run()
    
def start_level3(window):
    player_name = get_player_name(window)
    boss = Boss(800, 225, 50, 50, ("Characters", "Boss", 100, 100, True))
    
    enemies_level_3 = pygame.sprite.Group(boss,
    Enemy(350, 417, 50, 50, ("Characters", "Enemy2", 48, 48, True)),
    Enemy(600, 610, 50, 50, ("Characters", "Enemy2", 48, 48, True)),
    Enemy(160, 610, 50, 50, ("Characters", "Enemy", 48, 48, True)),
    Enemy(90, 417, 50, 50, ("Characters", "Enemy2", 48, 48, True)),
    Enemy(160, 225, 50, 50, ("Characters", "Enemy", 48, 48, True)),
    Enemy(200, 417, 50, 50, ("Characters", "Enemy", 48, 48, True))
    )
    
    objects_level_3 = [*floor, 
               Block(block_size * 0, HEIGHT - block_size * 3, block_size), 
               Block(block_size * 1, HEIGHT - block_size * 3, block_size), 
               Block(block_size * 2, HEIGHT - block_size * 3, block_size), 
               Block(block_size * 3, HEIGHT - block_size * 3, block_size),
               Block(block_size * 4, HEIGHT - block_size * 3, block_size),
               Block(block_size * 5, HEIGHT - block_size * 3, block_size),
               
               Block(block_size * 0, HEIGHT - block_size * 7, block_size),
               Block(block_size * 1, HEIGHT - block_size * 7, block_size),
               Block(block_size * 2, HEIGHT - block_size * 7, block_size),
               Block(block_size * 3, HEIGHT - block_size * 7, block_size),
                
               Block(block_size * 0, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 1, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 2, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 3, HEIGHT - block_size * 5, block_size),
               Block(block_size * 4, HEIGHT - block_size * 5, block_size),]
    
    level_3_final = Level(window, pause_menu, game_over_menu, enemies_level_3, objects_level_3, floor, "Cityorange.png", max_score=11, level_number=3, player_name=player_name)
    
    level_3_final.run()
        
def level_menu(window):
    button_width = 200
    button_height = 50
    padding = 20  # Espacio entre los botones

    # Calcula las coordenadas x para cada botón
    total_width = 4 * button_width + 3 * padding
    start_x = (WIDTH - total_width) / 2
    level1_button_x = start_x
    level2_button_x = start_x + button_width + padding
    level3_button_x = start_x + 2 * button_width + 2 * padding
    back_button_x = start_x + 3 * button_width + 3 * padding

    # Las coordenadas y son las mismas para todos los botones
    button_y = HEIGHT - button_height - padding

    level1_button = Button("Nivel 1", level1_button_x, button_y, button_width, button_height, WHITE, SKY, action=start_level1)
    level2_button = Button("Nivel 2", level2_button_x, button_y, button_width, button_height, WHITE, SKY, action=start_level2)
    level3_button = Button("Nivel 3", level3_button_x, button_y, button_width, button_height, WHITE, SKY, action=start_level3)
    back_button = Button("Atras", back_button_x, button_y, button_width, button_height, (255, 0, 0), (128, 0, 0), action=main_menu)

    buttons = [level1_button, level2_button, level3_button, back_button]
    background_menu = pygame.transform.scale(pygame.image.load("./src/assets/Background/skyrunner_levels.jpg"), (WIDTH, HEIGHT))

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

def instructions_menu(window):
    back_button = Button("Atras", 400, 725, 200, 50, (255, 0, 0), (128, 0, 0), action=main_menu)
    buttons = [back_button]
    background_instructions = pygame.transform.scale(pygame.image.load("./src/assets/Background/instrucciones.jpg"), size_screen)

    running = True
    while running:
        window.fill((255, 255, 255))
        window.blit(background_instructions, origin)

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
        
def make_action(level):
    return lambda window: show_scores(window, level)
        
def score_menu(window):
    button_width = 200
    button_height = 50
    padding = 20  # Espacio entre los botones
    total_width = 4 * button_width + 3 * padding
    start_x = (WIDTH - total_width) / 2
    back_button_x = start_x + 3 * button_width + 3 * padding
    button_y = HEIGHT - button_height - padding
    
    # Leer las puntuaciones del archivo JSON
    with open('scores.json', 'r') as f:
        scores = json.load(f)

    # Agrupar las puntuaciones por nivel
    scores_by_level = {}
    for score in scores:
        level = score['level']
        if level not in scores_by_level:
            scores_by_level[level] = []
        scores_by_level[level].append(score)

    # Crear un botón para cada nivel
    buttons = []
    sorted_levels = sorted(scores_by_level.keys(), key=int)

    for i, level in enumerate(sorted_levels):
        button_x = start_x + i * (button_width + padding)
        button_y = HEIGHT - button_height - padding
        button = Button(f"Nivel {level}", button_x, button_y, button_width, button_height, WHITE, SKY, action=make_action(level))
        buttons.append(button)
        
    back_button = Button("Atras", back_button_x, button_y, button_width, button_height, (255, 0, 0), (128, 0, 0), action=main_menu)
    
    buttons.append(back_button)
        
    background_menu = pygame.transform.scale(pygame.image.load("./src/assets/Background/scoresbackground.jpg"), (WIDTH, HEIGHT))

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

def show_scores(window, level):
    # Leer las puntuaciones del archivo JSON
    with open('scores.json', 'r') as f:
        scores = json.load(f)

    # Filtrar las puntuaciones para el nivel seleccionado
    scores = [score for score in scores if score['level'] == level]

    button_width = 200
    button_height = 50
    padding = 20  # Espacio entre los botones
    total_width = 4 * button_width + 3 * padding
    start_x = (WIDTH - total_width) / 2
    back_button_x = start_x + 3 * button_width + 3 * padding
    button_y = HEIGHT - button_height - padding
    back_button = Button("Atras", back_button_x, button_y, button_width, button_height, (255, 0, 0), (128, 0, 0), action=lambda: score_menu(window))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    back_button.action()
                    return

        # Mostrar las puntuaciones
        font = pygame.font.SysFont("Minecraft", 25)  # Elige la fuente que prefieras
        for i, score in enumerate(scores):
            score_text = f"Player = {score['player']}, Puntuacion = {score['score']}, Tiempo = {score['time']}"
            label = font.render(score_text, True, (255, 255, 255), BLACK)  # Crea una etiqueta de texto
            text_width, text_height = font.size(score_text)  # Obtiene el ancho y alto del texto
            text_x = (WIDTH - text_width) / 2  # Calcula la posición x del texto para centrarlo
            window.blit(label, (text_x, 70 + i*30))  # Dibuja la etiqueta en la ventana

        back_button.draw(window)  # Dibuja el botón "Atrás"

        pygame.display.update()

