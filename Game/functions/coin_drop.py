from random import randint

from Game.item.Coin_big import Coin_big
from Game.item.Coin_lil import Coin_lil


def coin_drop(x, y, player, count):
    big_coin = randint(0, 3)
    if count == 'rand':
        count = randint(2, 10)
    count -= big_coin
    for i in range(0, count):
        item1 = Coin_lil(x, y, player, player.level.platform_list, 800, 500)
        item1.change_y = randint(-15, -1)
        item1.change_x = randint(0, 5)
        player.level.item_list.add(item1)
        player.level.item_list.draw(player.screen)
    for i in range(0, big_coin):
        item1 = Coin_big(x, y, player, player.level.platform_list, 800, 500)
        item1.change_y = randint(-15, -1)
        item1.change_x = randint(0, 5)
        player.level.item_list.add(item1)
        player.level.item_list.draw(player.screen)