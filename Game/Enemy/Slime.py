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
        self.rect.y = y
        self.rect.x = x
        self.player = player
        self.attack_timer = 0
        self.attack_cooldown = 1000
        self.speed = 5
        self.current_time = 1
        self.wait_time = random.randint(20, 500)
        self.start_time = 0

        # Тут хранятся анимации
        self.animations = {'idle': {'left': [], 'right': []},
                           'hurt': {'left': [], 'right': []},
                           }

        for i in range(1, 2):
            image = pygame.image.load(f'assets/enemy/slime/hurt/Char0{i}.png').convert_alpha()
            self.animations['hurt']['left'].append(image)
            self.animations['hurt']['right'].append(pygame.transform.flip(image, True, False))

        for i in range(1, 2):
            image = pygame.image.load(f'assets/enemy/slime/idle/Char0{i}.png').convert_alpha()
            self.animations['idle']['right'].append(image)
            self.animations['idle']['left'].append(pygame.transform.flip(image, True, False))

        self.current_frame = 0
        self.current_animation = self.animations['idle']

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
                self.player.take_damage(self.damage)

        self.set_animation()
        self.update_animation()

    def set_animation(self):
        if self.stunned:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['hurt']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['hurt']
            # Получение картинки в соответсвии с направлением игрока
            if self.player.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
            if self.current_frame == 9:
                self.is_attack = False
        else:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['idle']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['idle']
            # Получение картинки в соответсвии с направлением слизня
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]

    def update_animation(self):
        # Получение следующего кадра анимации
        self.current_frame += 1
        # Если кадра не существует начинаем заново
        if self.current_frame >= len(self.current_animation['right']):
            self.current_frame = 0
        # Получение картинки в соответсвии с направлением удара игрока
        if self.current_animation == ['hurt']:
            if self.player.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
        else:
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]

    def get_damage(self, damage):
        super(Slime, self).get_damage(damage)
        # Откидывание от удара
        if self.player.right:
            self.change_x += 10
        else:
            self.change_x -= 10
        self.change_y -= 7
        self.stun(2000)


    def jump(self):
        super(Slime, self).jump()
        if len(self.platform_list) > 0 or self.rect.bottom >= self.SCREEN_HEIGHT:
            self.change_y = random.randint(-22, -8)