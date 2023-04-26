import pygame
from Game.child.Hud import Hud


# Класс, описывающий поведение главного игрока
from assets.entity.Sword import Sword


class Player(pygame.sprite.Sprite):
    # Изначально игрок смотрит вправо, поэтому эта переменная True
    right = True
    # Момент переходя в движение
    moment_move = True
    # Движется ли
    is_moving = False
    # Момент начало прыжка
    jump_moment = False

    # Методы
    def __init__(self, SCREEN_HEIGHT, screen):
        self.get_hurt = False
        self.is_fly = False
        self.max_health = 40
        self.current_health = 40
        self.health_bar_length = 100
        self.max_plasma = 20
        self.current_plasma = 20
        self.plasma_bar_length = 80
        self.hud_list = pygame.sprite.Group()
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = screen
        self.hud = Hud(screen,
                       self.max_health, self.current_health, self.health_bar_length,
                       self.max_plasma, self.current_plasma, self.plasma_bar_length)
        self.stunned = False  # Флаг, указывающий на то, оглушен ли игрок
        self.stun_time = 0  # Время оглушения (в кадрах)
        self.fly_speed = 0.1
        self.fly_max_speed = 0.1
        self.sword = Sword(player=self, screen=self.screen)
        self.entity_sprite_list = pygame.sprite.Group(self.sword)

        # Стандартный конструктор класса
        # Нужно ещё вызывать конструктор родительского класса
        super().__init__()

        # Тут хранятся анимации
        self.animations = {'idle': {'left': [], 'right': []},
                           'moving_moment': {'left': [], 'right': []},
                           'moving': {'left': [], 'right': []},
                           'hurt': {'left': [], 'right': []},
                           'fly': {'left': [], 'right': []},
                           'jump': {'left': [], 'right': []}
                           }
        # Ложим в словарь картинки для анимации в папках
        for i in range(1, 17):
            image = pygame.image.load(f'assets/jump/Char0{i}.png').convert_alpha()
            self.animations['jump']['right'].append(image)
            self.animations['jump']['left'].append(pygame.transform.flip(image, True, False))

        for i in range(1, 13):
            image = pygame.image.load(f'assets/fly/Char0{i}.png').convert_alpha()
            self.animations['fly']['right'].append(image)
            self.animations['fly']['left'].append(pygame.transform.flip(image, True, False))

        for i in range(1, 7):
            image = pygame.image.load(f'assets/moving_moment/Char0{i}.png').convert_alpha()
            self.animations['moving_moment']['right'].append(image)
            self.animations['moving_moment']['left'].append(pygame.transform.flip(image, True, False))

        for i in range(1, 19):
            image = pygame.image.load(f'assets/moving/Char0{i}.png').convert_alpha()
            self.animations['moving']['right'].append(image)
            self.animations['moving']['left'].append(pygame.transform.flip(image, True, False))
        # Ложим в словарь картинки для анимации в папках
        for i in range(1, 33):
            image = pygame.image.load(f'assets/idle/idle_{i}.png').convert_alpha()
            self.animations['idle']['right'].append(image)
            self.animations['idle']['left'].append(pygame.transform.flip(image, True, False))
        # Ложим в словарь картинки для анимации в папках
        for i in range(1, 2):
            image = pygame.image.load(f'assets/get_hurt/hurt0{i}.png').convert_alpha()
            self.animations['hurt']['right'].append(image)
            self.animations['hurt']['left'].append(pygame.transform.flip(image, True, False))

        self.current_frame = 0
        # Стандартная анимация (заглушка)
        self.current_animation = self.animations['idle']

        # Создаем изображение для игрока
        # Изображение находится в этой же папке проекта
        self.image = pygame.Surface((50, 70))

        # Установите ссылку на изображение прямоугольника
        self.rect = self.image.get_rect()
        self.rect.width -= 10

        # Задаем вектор скорости игрока
        self.change_x = 0
        self.change_y = 0

    def set_animation(self):
        if self.stunned or self.get_hurt:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['hurt']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['hurt']
            # Получение картинки в соответсвии с направлением игрока
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
            self.get_hurt = False
        elif self.is_fly:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['fly']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['fly']
            # Получение картинки в соответсвии с направлением игрока
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
            self.moment_move = False
        elif self.moment_move and self.is_moving:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['moving_moment']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['moving_moment']
            # Получение картинки в соответсвии с направлением игрока
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
            self.moment_move = False
        # Тут анимация не должно зациклиться поэтому перестаем увеличивать кадры
        elif self.jump_moment:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['jump']:
                self.current_frame = 0
            if self.current_frame >= len(self.animations['jump']['right'])-1:
                self.current_frame -= 1
            # Назначение текущей анимаций
            self.current_animation = self.animations['jump']
            # Получение картинки в соответсвии с направлением игрока
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
        elif self.is_moving:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['moving']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['moving']
            # Получение картинки в соответсвии с направлением игрока
            if self.right:
                self.image = self.current_animation['right'][self.current_frame]
            else:
                self.image = self.current_animation['left'][self.current_frame]
        else:
            # Если текущая анимация изменилась тогда кадр анимации 0
            if self.current_animation != self.animations['idle']:
                self.current_frame = 0
            # Назначение текущей анимаций
            self.current_animation = self.animations['idle']
            # Получение картинки в соответсвии с направлением игрока
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
        # Получение картинки в соответсвии с направлением игрока
        if self.right:
            self.image = self.current_animation['right'][self.current_frame]
        else:
            self.image = self.current_animation['left'][self.current_frame]

    def stun(self, duration):
        # Оглушение игрока на указанное время
        self.stunned = True
        self.stun_time = pygame.time.get_ticks()
        # Анимация аглушения
        self.set_animation()
        self.update_animation()

    def update(self):
        if not self.stunned:
            # В этой функции мы передвигаем игрока
            # Сперва устанавливаем для него гравитацию
            self.calc_grav()

            # Передвигаем его на право/лево
            # change_x будет меняться позже при нажатии на стрелочки клавиатуры
            self.rect.x += self.change_x

            # Следим ударяем ли мы какой-то другой объект, платформы, например
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            # Перебираем все возможные объекты, с которыми могли бы столкнуться
            for block in block_hit_list:
                # Если мы идем направо,
                # устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # В противном случае, если мы движемся влево, то делаем наоборот
                    self.rect.left = block.rect.right

            # Передвигаемся вверх/вниз
            self.rect.y += self.change_y

            # То же самое, вот только уже для вверх/вниз
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
                # Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                # Когда на земле восстанавливает плазму
                self.get_plasma(0.5)
                self.jump_moment = False
                # Останавливаем вертикальное движение
                self.change_y = 0
        else:
            if pygame.time.get_ticks() - self.stun_time > 2000:
                self.stunned = False

    def calc_grav(self):
        # Здесь мы вычисляем как быстро объект будет
        # падать на землю под действием гравитации
        if self.is_fly:
            if self.change_y < -4:
                self.change_y = -4
            else:
                self.change_y -= self.fly_speed
        elif self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.95

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.y >= self.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # Обработка прыжка
        # Нам нужно проверять здесь, контактируем ли мы с чем-либо
        # или другими словами, не находимся ли мы в полете.
        # Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.SCREEN_HEIGHT:
            self.change_y = -16
            self.jump_moment = True

    def fly(self, fly_speed):
        # Обработка прыжка
        # Нам нужно проверять здесь, контактируем ли мы с чем-либо
        # или другими словами, не находимся ли мы в полете.
        # Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
        self.is_fly = True
        self.fly_speed = fly_speed

    def take_damage(self, damage):
        # Уменьшение здаровья
        self.hud.current_health -= damage
        # Обновление полоски жизни
        self.hud.update_health_bar()
        self.get_hurt = True

    def die_check(self, game_state_machine):
        # Проверка на смерть
        if self.hud.current_health <= 0:
            # Запуск экрана поражение
            game_state_machine.change_state("GameOver")
            # Восстановление здаровья
            self.reset_all()
            # Обновление полоски жизни
            self.hud.update_health_bar()

    def reduce_plasma(self, plasma):
        # Уменьшение здаровья
        self.hud.current_plasma -= plasma
        # Обновление полоски жизни
        self.hud.update_plasma_bar()

    def get_plasma(self, plasma):
        if self.hud.max_plasma != self.hud.current_plasma:
            self.hud.current_plasma += plasma
        if self.hud.current_plasma > self.hud.max_plasma:
            self.hud.current_plasma = self.hud.max_plasma
        # Обновление полоски жизни
        self.hud.update_plasma_bar()

    # Восстановление здаровья
    def reset_all(self):
        self.hud.current_health = self.hud.max_health
        self.hud.current_plasma = self.hud.max_plasma

    # Передвижение игрока
    def go_left(self):
        # Сами функции будут вызваны позже из основного цикла
        if self.is_fly:
            self.change_x = -5
        else:
            self.change_x = -9  # Двигаем игрока по Х
        if (self.right):  # Проверяем куда он смотрит и если что, то переворачиваем его
            self.flip()
            self.right = False

    def go_right(self):
        # то же самое, но вправо
        if self.is_fly:
            self.change_x = 5
        else:
            self.change_x = 9
        if (not self.right):
            self.flip()
            self.right = True

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.change_x = 0

    def flip(self):
        # переворот игрока (зеркальное отражение)
        self.image = pygame.transform.flip(self.image, True, False)
