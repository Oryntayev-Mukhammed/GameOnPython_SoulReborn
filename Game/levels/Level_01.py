import pygame
from Game.Level import Level
from Game.objects.Platform import Platform


# Подключение фото для заднего фона
# Здесь лишь создание переменной, вывод заднего фона ниже в коде

backGround = pygame.image.load('assets/bg.jpg')


# Класс, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_01(Level):
    def __init__(self, player):
        # Вызываем родительский конструктор
        Level.__init__(self, player, backGround)

        # Массив с данными про платформы. Данные в таком формате:
        # ширина, высота, x и y позиция
        level = [
            [200, 30, 500, 500],
            [200, 30, 200, 400],
            [180, 30, 640, 300],
        ]

        # Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


