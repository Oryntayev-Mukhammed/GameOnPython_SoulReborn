import pygame


class Enemy(pygame.sprite.Sprite):
    right = True
    teg_move = True
    is_moving = False

    def __init__(self, x, y, SCREEN_HEIGHT, max_health, platform_list):
        super().__init__()
        self.platform_list = platform_list
        self.image = pygame.Surface((50, 40))  # установим базовое изображение в виде поверхности 50х50 пикселей
        self.rect = self.image.get_rect()  # получим прямоугольник поверхности и сохраним его в self.rect
        self.rect.x = x  # установим начальные координаты
        self.rect.y = y
        self.max_health = max_health
        self.current_health = max_health
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.stunned = False  # Флаг, указывающий на то, оглушен ли игрок
        self.stun_time = 0  # Время оглушения (в кадрах)

        # self.current_frame = 0
        # # Стандартная анимация (заглушка)
        # self.current_animation = self.animations['idle']

        # Задаем вектор скорости игрока
        self.change_x = 0
        self.change_y = 0

    def stun(self, duration):
        # Оглушение игрока на указанное время
        self.stunned = True
        self.stun_time = pygame.time.get_ticks()

    def update(self):
        if not self.stunned:
            # В этой функции мы передвигаем игрока
            # Сперва устанавливаем для него гравитацию
            self.calc_grav()

            # Передвигаем его на право/лево
            # change_x будет меняться позже при нажатии на стрелочки клавиатуры
            self.rect.x += self.change_x

            # Следим ударяем ли мы какой-то другой объект, платформы, например
            block_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
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
            block_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
            for block in block_hit_list:
                # Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                # Останавливаем вертикальное движение
                self.change_y = 0
        else:
            if pygame.time.get_ticks() - self.stun_time > 2000:
                self.stunned = False

    def calc_grav(self):
        # Здесь мы вычисляем как быстро объект будет
        # падать на землю под действием гравитации
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95

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
        platform_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        self.rect.y -= 10

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.SCREEN_HEIGHT:
            self.change_y = -16

    # Передвижение игрока
    def go_left(self):
        # Сами функции будут вызваны позже из основного цикла
        self.change_x = -9  # Двигаем игрока по Х
        if (self.right):  # Проверяем куда он смотрит и если что, то переворачиваем его
            self.flip()
            self.right = False

    def go_right(self):
        # то же самое, но вправо
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
