import pygame
import random
from Game.child.Enemy import Enemy


class Slime(Enemy):
    def __init__(self, x, y, SCREEN_WIDTH, SCREEN_HEIGHT, max_health, platform_list, player):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, max_health, platform_list)
        self.platform_list = platform_list
        self.max_health = max_health
        self.current_health = max_health
        self.damage = 5
        self.hud_list = pygame.sprite.Group()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.image.load('assets/enemy/slime/slime.png')
        self.rect.y = y
        self.rect.x = x
        self.player = player
        self.attack_timer = 0
        self.attack_cooldown = 1000
        self.speed = 5
        self.current_time = 1
        self.wait_time = random.randint(20, 500)
        self.start_time = 0

    def update(self):
        # Проверка находится ли он на земле
        if self.change_y != 0:
            self.on_earth = False
        elif self.change_y == 0:
            self.on_earth = True
        # Сложная часть для высчитывания времени ожидания слизьня перед ударом
        if self.change_y != 0 and self.wait:
            self.wait = False
        elif self.change_y == 0 and not self.wait:
            self.stop()
            self.wait = True
            self.start_time = pygame.time.get_ticks()
        elif self.change_y == 0 and self.wait and self.current_time - self.start_time >= self.wait_time:
            self.wait_time = random.randint(1000, 3000)
            self.wait = False
        super(Slime, self).update()
        # движение к игроку
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < 50:
            self.is_attacking = True
        else:
            self.is_attacking = False
            self.current_time = pygame.time.get_ticks()
            if distance > 10:
                if self.player.rect.x < self.rect.x and self.on_earth and not self.wait:
                    self.jump()
                    self.go_left()
                elif self.player.rect.x > self.rect.x and self.on_earth and not self.wait:
                    self.jump()
                    self.go_right()

        # атака игрока
        if self.is_attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_timer > self.attack_cooldown:
                self.attack_timer = now
                self.player.take_damage(self.damage)

    def jump(self):
        super(Slime, self).jump()
        if len(self.platform_list) > 0 or self.rect.bottom >= self.SCREEN_HEIGHT:
            self.change_y = random.randint(-22, -8)