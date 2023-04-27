import pygame


class Sword(pygame.sprite.Sprite):
    def __init__(self, player, screen):
        super().__init__()
        self.player = player
        self.image = pygame.Surface((30, 40))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.screen = screen
        self.sword_bottom = False
        self.is_attack = False
        self.current_time = 1
        self.start_time = 0
        self.attack_timer = 0
        self.attack_cooldown = 1500 # Задержка удара 1.5 сек

        # Тут хранятся анимации
        self.animations = {'idle': {'left': [], 'right': []},
                           'attack': {'left': [], 'right': []},
                           }

        for i in range(1, 2):
            image = pygame.image.load(f'assets/sword/idle/Char0{i}.png').convert_alpha()
            self.animations['idle']['right'].append(image)
            self.animations['idle']['left'].append(pygame.transform.flip(image, True, False))

        for i in range(1, 11):
            image = pygame.image.load(f'assets/sword/attack/Char0{i}.png').convert_alpha()
            self.animations['attack']['right'].append(image)
            self.animations['attack']['left'].append(pygame.transform.flip(image, True, False))

        self.current_frame = 0
        self.current_animation = self.animations['idle']

    def update(self):
        if self.player.right and self.is_attack:
            self.rect.x = self.player.rect.x + 16
            self.rect.y = self.player.rect.y - 20
        elif not self.player.right and self.is_attack:
            self.rect.x = self.player.rect.x - 65
            self.rect.y = self.player.rect.y - 20
        elif self.player.right:
            self.rect.x = self.player.rect.x - 30
            self.rect.y = self.player.rect.y - 3
        elif not self.player.right:
            self.rect.x = self.player.rect.x + 25
            self.rect.y = self.player.rect.y - 3

        self.set_animation()
        self.update_animation()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def attack(self):
        # Следим ударяем ли мы какой-то другой объект, слизня, например
        now = pygame.time.get_ticks()
        if now - self.start_time > self.attack_cooldown:
            self.player.sword.is_attack = True
            for enemy in self.player.level.enemy_list:
                if self.player.right:
                    dx = self.rect.x + 70 - enemy.rect.x
                else:
                    dx = self.rect.x - 70 - enemy.rect.x
                dy = self.rect.y - enemy.rect.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < 70:
                    enemy.get_damage(20)
            self.start_time = pygame.time.get_ticks()

    def set_animation(self):
        if self.is_attack:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['attack']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['attack']
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
            # Получение картинки в соответсвии с направлением игрока
            if self.player.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]

    def update_animation(self):
        # Получение следующего кадра анимации
        self.current_frame += 1
        # Если кадра не существует начинаем заново
        if self.current_frame >= len(self.current_animation['right']):
            self.current_frame = 0
        # Получение картинки в соответсвии с направлением игрока
        if self.player.right:
            self.image = self.current_animation['right'][self.current_frame]
        else:
            self.image = self.current_animation['left'][self.current_frame]
