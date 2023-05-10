import pygame
import random

from Game.Animation import Animation
from Game.child.Enemy import Enemy
from Game.functions.coin_drop import coin_drop


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
        self.rect.y = y
        self.rect.x = x
        self.player = player
        self.attack_timer = 0
        self.attack_cooldown = 1000
        self.speed = 5
        self.current_time = 1
        self.wait_time = random.randint(20, 500)
        self.start_time = 0
        self.is_jump = False
        self.anim = Animation(self.player, self)
        self.anim.addAnim('idle', 'assets/enemy/slime/idle/Char0', 2)
        self.anim.addAnim('hurt', 'assets/enemy/slime/hurt/Char0', 2)
        self.anim.addAnim('jump', 'assets/enemy/slime/jump/Char0', 14)

    def update(self):
        # Проверка находится ли он на земле
        if self.change_y != 0:
            self.on_earth = False
        elif self.change_y == 0:
            self.on_earth = True
            self.stunned = False
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
        if self.stunned:
            if pygame.time.get_ticks() - self.stun_time > 2000:
                self.stunned = False
        else:
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
                        self.right = False
                        self.jump()
                        self.go_left()
                    elif self.player.rect.x > self.rect.x and self.on_earth and not self.wait:
                        self.right = True
                        self.jump()
                        self.go_right()

        # атака игрока
        if self.is_attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_timer > self.attack_cooldown:
                self.attack_timer = now
                # Откидывание игрока
                if self.player.rect.x > self.rect.x:
                    self.player.take_damage(self.damage, 10, 10)
                else:
                    self.player.take_damage(self.damage, 10, -10)

        self.set_animation()
        self.update_animation()

    def set_animation(self):
        if self.is_jump:
            self.anim.set_animation('jump')
            if self.anim.current_frame == 12:
                self.anim.current_frame -= 1
            if self.on_earth:
                self.anim.current_frame = 13
        elif self.stunned:
            self.anim.set_animation('hurt')
        else:
            self.anim.set_animation('idle')

    def update_animation(self):
        self.anim.update_animation()
        # Получение картинки в соответсвии с направлением удара игрока
        if self.anim.current_animation == self.anim.animations['hurt']:
            if self.player.right:
                self.image = self.anim.current_animation['right'][self.anim.current_frame]
            elif not self.player.right:
                self.image = self.anim.current_animation['left'][self.anim.current_frame]
        else:
            if not self.right:
                self.image = self.anim.current_animation['right'][self.anim.current_frame]
            else:
                self.image = self.anim.current_animation['left'][self.anim.current_frame]

    def get_damage(self, damage):
        super(Slime, self).get_damage(damage)
        self.is_jump = False
        # Откидывание от удара
        if self.player.right:
            self.change_x += 10
        else:
            self.change_x -= 10
        self.change_y -= 7

    def drop(self):
        coin_drop(self.rect.x, self.rect.y, self.player, 'rand')

    def jump(self):
        super(Slime, self).jump()
        if len(self.platform_list) > 0 or self.rect.bottom >= self.SCREEN_HEIGHT:
            self.is_jump = True
            self.change_y = random.randint(-22, -8)