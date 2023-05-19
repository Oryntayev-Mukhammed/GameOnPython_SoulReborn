import pygame
import random

from Game.Animation import Animation
from Game.Enemy.Slime import Slime
from Game.child.Enemy import Enemy
from Game.functions.coin_drop import coin_drop


class Apple(Enemy):
    def __init__(self, x, y, SCREEN_WIDTH, SCREEN_HEIGHT, max_health, platform_list, player):
        super().__init__(x, y, SCREEN_WIDTH, SCREEN_HEIGHT, max_health, platform_list)
        self.damage = 5
        self.hud_list = pygame.sprite.Group()
        self.image = pygame.Surface((60, 70))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.player = player
        self.attack_timer = 0
        self.attack_cooldown = 1000
        self.speed = 5
        self.current_time = 1
        self.wait_time = random.randint(20, 500)
        self.start_time = 0
        self.anim = Animation(self.player, self)
        self.anim.addAnim('idle', 'assets/enemy/apple/idle/', 2)
        self.anim.addAnim('target', 'assets/enemy/apple/target/', 28)
        self.anim.addAnim('rolling', 'assets/enemy/apple/rolling/', 11)
        self.anim.addAnim('folding', 'assets/enemy/apple/folding/', 12)
        self.anim.addAnim('dead', 'assets/enemy/apple/dead/', 23)
        self.is_trap = True
        self.cool = False
        self.right = True
        self.is_attacking = False
        self.is_rolling = False
        self.is_folding = False
        self.is_slime_trap = True

    def addition(self):
        self.is_rolling = False

    def update(self):
        if self.is_dead:
            self.set_animation()
            self.anim.update_animation()
            return None
        super().update()
        if self.rect.x >= 739 or self.rect.x <= 1:
            self.is_rolling = False
            self.change_x = 0
        self.set_animation()
        self.anim.update_animation()

        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < 50:
            self.is_attacking = True
        else:
            self.is_attacking = False
            # Если игрок не дальше от нас на 500 пикселей и не выше на 150 пикселей - атаковать

            if self.is_trap and distance < 100:
                self.is_trap = False
                if self.is_slime_trap:
                    for i in range(0, random.randint(0, 3)):
                        item1 = Slime(self.rect.x, self.rect.y, 800, 500, 40, self.platform_list, self.player)
                        item1.change_y = random.randint(-15, -1)
                        item1.change_x = random.randint(0, 5)
                        self.player.level.enemy_list.add(item1)
                        self.player.level.enemy_list.draw(self.player.screen)
                if not self.is_rolling and self.player.rect.x > self.rect.x:
                    self.is_rolling = True
                    self.right = True
                    self.change_x = 12
                elif not self.is_rolling and self.player.rect.x < self.rect.x:
                    self.is_rolling = True
                    self.right = False
                    self.change_x = -12
            elif distance < 500 and self.player.rect.y + 150 > self.rect.y and not self.is_trap:
                self.is_trap = False
                if not self.is_rolling and self.player.rect.x > self.rect.x:
                    self.is_rolling = True
                    self.right = True
                    self.change_x = 12
                elif not self.is_rolling and self.player.rect.x < self.rect.x:
                    self.is_rolling = True
                    self.right = False
                    self.change_x = -12

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

    def drop(self):
        coin_drop(self.rect.x, self.rect.y, self.player, 20)

    def set_animation(self):
        if self.is_dead:
            self.anim.set_animation('dead')
            if self.anim.current_frame == 21:
                self.kill()
        elif self.is_trap:
            self.anim.set_animation_by_side('idle', self.right)
        # cool нужен для дублирования всех картинок анимации
        elif self.is_rolling and self.cool:
            self.anim.current_frame -= 1
            self.anim.set_animation_by_side('rolling', not self.right)
            self.cool = False
        elif self.is_rolling and not self.cool:
            self.anim.set_animation_by_side('rolling', not self.right)
            self.cool = True
        else:
            self.anim.set_animation_by_side('target', self.right)
