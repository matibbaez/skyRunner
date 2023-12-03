import pygame
from os import listdir
from os.path import isfile, join
from constants import *

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def get_background(name):
    image = pygame.image.load(join("src", "assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
            
    return tiles, image

def handle_move(player, objects, enemies, coins):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)
    
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_f] and len(player.lasers) < 1:  # Limite de disparos simultáneos
        player.shoot()
        
    player.update_lasers(enemies, coins)
        
    handle_vertical_collision(player, objects, player.y_vel)

    # Verificar la colisión con los enemigos
    player_rect = player.rect
    
    for enemy in enemies:
        enemy_rect = enemy.rect
        if player_rect.colliderect(enemy_rect):
            player.make_hit()  # Activa el estado de golpe del jugador

def draw(window, background, bg_image, player, objects, enemies, coins, elapsed_time, score):
    for tile in background:
        window.blit(bg_image, tile)
        
    for obj in objects:
        obj.draw(window)
         
    # Dibuja cada enemigo
    for enemy in enemies:
        enemy.draw(window)
        
    for coin in coins:
        window.blit(coin.image, coin.rect) 
    
    player.draw(window)
    player.draw_lasers(window)
    
    # Dibuja el tiempo en la pantalla
    font = pygame.font.SysFont("Minecraft", 25)
    minutes = int(elapsed_time) // 60
    seconds = int(elapsed_time) % 60
    text = font.render("{:02d}:{:02d}".format(minutes, seconds), True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH / 2, 20))  # Obtiene un rectángulo con el centro en (WIDTH / 2, 10)
    window.blit(text, text_rect)

    # Dibuja la puntuación en la pantalla
    score_text = font.render("Puntos: " + str(score), True, (0, 0, 0))
    score_rect = score_text.get_rect(top=10, right=WIDTH - 10)  # Obtiene un rectángulo con el centro en (WIDTH / 2, 50)
    window.blit(score_text, score_rect)
    
    lives_text = font.render("Vidas: " + str(player.lives), True, (0, 0, 0))
    lives_rect = lives_text.get_rect(top=10, left=10)  # Obtiene un rectángulo con la parte superior a 10 y alineado a la izquierda
    window.blit(lives_text, lives_rect)

    pygame.display.update()