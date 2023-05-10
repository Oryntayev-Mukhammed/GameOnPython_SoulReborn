import pygame

from Game.Animation import Animation


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, player, platform_list, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.platform_list = platform_list
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.anim = Animation(self.player, self)

        self.change_x = 0
        self.change_y = 0

    def update(self):
        # В этой функции мы передвигаем игрока
        # Сперва устанавливаем для него гравитацию
        self.calc_grav()

        # Передвигаем его на право/лево
        # change_x будет меняться позже при нажатии на стрелочки клавиатуры
        self.rect.x += self.change_x

        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
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

    def calc_grav(self):
        # Здесь мы вычисляем как быстро объект будет
        # падать на землю под действием гравитации
        if self.change_y == 0:
            self.change_y = 1
            self.change_x = 0
        else:
            self.change_y += .95

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.y >= self.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.SCREEN_HEIGHT - self.rect.height

    def pickup(self):
        self.kill()