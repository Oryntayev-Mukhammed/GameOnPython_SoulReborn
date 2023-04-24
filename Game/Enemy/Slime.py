import pygame
from Game.child.Enemy import Enemy


class Slime(Enemy):
    def __init__(self, x, y, SCREEN_HEIGHT, max_health, platform_list, player):
        super().__init__(x, y, SCREEN_HEIGHT, max_health, platform_list)
        self.platform_list = platform_list
        self.max_health = max_health
        self.current_health = max_health
        self.hud_list = pygame.sprite.Group()
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.image.load('assets/enemy/slime/slime.png')
        self.rect.y = y
        self.rect.x = x
        self.player = player
        self.attack_timer = 0
        self.attack_cooldown = 1000
        self.speed = 5

    def update(self):
        super(Slime, self).update()
        # движение к игроку
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < 50:
            self.is_attacking = True
        else:
            self.is_attacking = False
            if distance > 10:
                self.rect.x += self.speed * dx / distance
                self.rect.y += self.speed * dy / distance

        # атака игрока
        if self.is_attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_timer > self.attack_cooldown:
                self.attack_timer = now
                self.player.take_damage(10)