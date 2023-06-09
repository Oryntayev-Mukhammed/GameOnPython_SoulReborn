import pygame

from Game.Enemy.Apple import Apple
from Game.Level import Level
from Game.child.Item import Item
from Game.item.Coin_lil import Coin_lil
from Game.item.Apple import Apple_big
from Game.objects.Ground import Ground
from Game.objects.Underground import GroundUnder
from Game.objects.Platform import Platform


# Подключение фото для заднего фона
# Здесь лишь создание переменной, вывод заднего фона ниже в коде

backGround = pygame.image.load('assets/bg.jpg')


# Класс, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_03(Level):
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

        item1 = Coin_lil(310, 300, self.player, self.platform_list, 800, 500)
        item2 = Coin_lil(340, 310, self.player, self.platform_list, 800, 500)
        item3 = Coin_lil(360, 320, self.player, self.platform_list, 800, 500)
        item4 = Coin_lil(320, 330, self.player, self.platform_list, 800, 500)
        item5 = Coin_lil(330, 340, self.player, self.platform_list, 800, 500)
        item6 = Coin_lil(350, 305, self.player, self.platform_list, 800, 500)
        self.item_list.add(item1, item2, item3, item4, item5, item6)

        apple1 = Apple(2, 300, 800, 500, 40, self.platform_list, self.player)
        self.enemy_list.add(apple1)

        block = Platform(200, 30)
        block.rect.x = 550
        block.rect.y = 450
        self.platform_list.add(block)

        block = Platform(200, 30)
        block.rect.x = 550
        block.rect.y = 260
        self.platform_list.add(block)

        apple_item = Apple_big(600, 220, self.player, self.platform_list, 800, 500)
        self.item_list.add(apple_item)


