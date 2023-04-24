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

        block1 = GroundUnder()
        block1.rect.x = ground_under[0]
        block1.rect.y = ground_under[1]
        block1.player = self.player
        self.platform_list.add(block1)

        block2 = Ground()
        block2.rect.x = ground[0]
        block2.rect.y = ground[1]
        block2.player = self.player
        self.platform_list.add(block2)

        # Враг слизень
        slime1 = Slime(300, 300, 800, 40, self.platform_list, self.player)

        self.enemy_list.add(slime1)
