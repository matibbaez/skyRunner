import pygame 

pygame.mixer.init()

background_music = pygame.mixer.music.load('./src/assets/sounds/musica_cyber.mp3')
laser_sound = pygame.mixer.Sound('./src/assets/sounds/laser.mp3')
coin_sound = pygame.mixer.Sound('./src/assets/sounds/coin.mp3')
game_over_sound = pygame.mixer.Sound('./src/assets/sounds/game_over_final.mp3')

        