import pygame
from Game.Level import Level
from Game.objects.Ground import Ground
from Game.objects.Underground import GroundUnder
from Game.objects.Platform import Platform
from Game.Enemy.Slime import Slime


# Подключение фото для заднего фона
# Здесь лишь создание переменной, вывод заднего фона ниже в коде

backGround = pygame.image.load('assets/bg.jpg')


# Класс, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_04(Level):
    def __init__(self, player):
        # Вызываем родительский конструктор
        Level.__init__(self, player, backGround)

        # Массив с данными про платформы. Данные в таком формате:
        # ширина, высота, x и y позиция
        ground = [0, 500]
        ground_under = [0, 500]

        block = GroundUnder()
        block.rect.x = ground_under[0]
        block.rect.y = ground_under[1]
        block.player = self.player
        self.platform_list.add(block)

        block = Ground()
        block.rect.x = ground[0]
        block.rect.y = ground[1]
        block.player = self.player
        self.platform_list.add(block)

        block = Platform(200, 30)
        block.rect.x = 25
        block.rect.y = 300
        self.platform_list.add(block)

        block = Platform(200, 30)
        block.rect.x = 600
        block.rect.y = 280
        self.platform_list.add(block)

        block = Platform(200, 30)
        block.rect.x = 550
        block.rect.y = 400
        self.platform_list.add(block)

        block = Platform(200, 30)
        block.rect.x = 550
        block.rect.y = 400
        self.platform_list.add(block)

        # Враг слизень
        slime1 = Slime(0, 300, 800, 500, 40, self.platform_list, self.player)
        slime2 = Slime(120, 300, 800, 500, 40, self.platform_list, self.player)
        slime3 = Slime(340, 300, 800, 500, 40, self.platform_list, self.player)
        slime4 = Slime(560, 300, 800, 500, 40, self.platform_list, self.player)

        self.enemy_list.add(slime1, slime2, slime3, slime4)
