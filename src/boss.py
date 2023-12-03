import pygame
from enemies import Enemy
from constants import HEIGHT

class Boss(Enemy):
    def __init__(self, x, y, width, height, sprites):
        super().__init__(x, y, width, height, sprites)
        self.lives = 5  # El jefe muere después de 5 golpes
        self.bullets = pygame.sprite.Group()  # Los disparos del jefe
        self.y_vel = 3  # La velocidad vertical del jefe
        self.direction = "left"  # Dirección inicial del jefe
        self.last_shot = pygame.time.get_ticks()  # La última vez que el jefe disparó
        self.bullet_speed = 8 # La velocidad inicial de las balas del jefe
        self.bullet_speed_increased = False
        bullet_image = pygame.image.load('./src/assets/Laser/Projectile.png')  # Carga la imagen del disparo
        self.bullet_image = pygame.transform.scale(bullet_image, (15, 15))  

    def loop(self, objects):
        # Cambia la dirección si llega a los bordes
        if self.rect.y <= 0 or self.rect.y >= 550:
            self.y_vel = -self.y_vel

        self.move(0, self.y_vel)  # Mueve al jefe verticalmente

        # Siempre usa las animaciones "idle"
        sprite_sheet_name = "idle_" + self.direction
        sprites = self.sprites[sprite_sheet_name]

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.animation_count += 1
        sprite = sprites[sprite_index]
        self.image = sprite

        # Hace que el jefe dispare
        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()  # La hora actual
        if now - self.last_shot > 2000:  # Si han pasado más de 2 segundos desde el último disparo
            bullet = BulletBoss(self.rect.centerx, self.rect.centery, -self.bullet_speed, 0, self.bullet_image)  # Crea un nuevo disparo
            self.bullets.add(bullet)  # Añade el disparo al grupo de disparos
            self.last_shot = now  # Actualiza la última vez que el jefe disparó

    def update_bullets(self, player):
        from levels import window, game_over_menu
        self.bullets.update()  # Actualiza los disparos
        for bullet in self.bullets:  # Comprueba si algún disparo ha golpeado al jugador
            if pygame.sprite.collide_rect(player, bullet):
                player.lives -= 1  # Reduce las vidas del jugador
                self.bullets.remove(bullet)  # Elimina el disparo
                if player.lives <= 0:  # Si el jugador no tiene vidas
                    game_over_menu(window)  # Muestra el menú de game over

    def draw(self, win):
        super().draw(win)  # Dibuja al jefe
        for bullet in self.bullets:  # Dibuja los disparos
            bullet.draw(win)

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