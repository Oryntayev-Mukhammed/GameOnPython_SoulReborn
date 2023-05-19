import pygame

from Game.Animation import Animation
from Game.child.Item import Item


class Apple_big(Item):
    def __init__(self, x, y, player, platform_list, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__(x, y, player, platform_list, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.image = pygame.Surface((75, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.anim.addAnim('idle', 'assets/entity/apple_big/', 2)
        self.right = True

    def update(self):
        self.anim.set_animation_by_side('idle', self.right)
        self.anim.update_animation()

        if 75 >= int(self.player.rect.x - self.rect.x) >= -50 \
                and int(self.rect.bottom - self.player.rect.bottom) <= 10 and 0 < int(self.rect.top - self.player.rect.top) <= 65:
            self.pickup()
        super(Apple_big, self).update()

    def pickup(self):
        self.player.hud.current_health = self.player.hud.max_health
        super(Apple_big, self).pickup()
