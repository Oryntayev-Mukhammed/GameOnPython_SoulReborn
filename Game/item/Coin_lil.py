import pygame

from Game.Animation import Animation
from Game.child.Item import Item


class Coin_lil(Item):
    def __init__(self, x, y, player, platform_list, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__(x, y, player, platform_list, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.image = pygame.Surface((5, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.anim.addAnim('idle', 'assets/entity/lil_coin/Char0', 8)
        self.anim.set_animation('idle')
    
    def update(self):
        self.anim.set_animation('idle')
        self.anim.update_animation()

        if 10 >= int(self.player.rect.x - self.rect.x) >= -50 \
                and int(self.rect.bottom - self.player.rect.bottom) <= 10 and int(self.rect.top - self.player.rect.top) >= 10:
            self.pickup()
        super(Coin_lil, self).update()
    
    def pickup(self):
        self.player.hud.money += 1
        super(Coin_lil, self).pickup()
        