import pygame
from Game.Animation import Animation


class Sword(pygame.sprite.Sprite):
    def __init__(self, player, screen):
        super().__init__()
        self.player = player
        self.image = pygame.Surface((30, 40))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.screen = screen
        self.sword_bottom = False
        self.is_attack = False
        self.current_time = 1
        self.start_time = 0
        self.attack_timer = 0
        self.attack_cooldown = 1500 # Задержка удара 1.5 сек
        # Создаем анимацию
        self.anim = Animation(self.player, self)
        self.anim.addAnim('idle', 'assets/entity/sword/idle/Char0', 2)
        self.anim.addAnim('attack', 'assets/entity/sword/attack/Char0', 11)

    def update(self):
        if self.player.right and self.is_attack:
            self.rect.x = self.player.rect.x + 16
            self.rect.y = self.player.rect.y - 20
        elif not self.player.right and self.is_attack:
            self.rect.x = self.player.rect.x - 65
            self.rect.y = self.player.rect.y - 20
        elif self.player.right:
            self.rect.x = self.player.rect.x - 30
            self.rect.y = self.player.rect.y - 3
        elif not self.player.right:
            self.rect.x = self.player.rect.x + 25
            self.rect.y = self.player.rect.y - 3

        self.set_animation()
        self.update_animation()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def attack(self):
        # Следим ударяем ли мы какой-то другой объект, слизня, например
        now = pygame.time.get_ticks()
        if now - self.start_time > self.attack_cooldown:
            self.player.sword.is_attack = True
            for enemy in self.player.level.enemy_list:
                if self.player.right:
                    dx = self.rect.x + 70 - enemy.rect.x
                else:
                    dx = self.rect.x - 70 - enemy.rect.x
                dy = self.rect.y - enemy.rect.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < 70:
                    enemy.get_damage(20)
                    enemy.stun(2000)
            self.start_time = pygame.time.get_ticks()

    def set_animation(self):
        if self.is_attack:
            self.anim.set_animation('attack')
            if self.anim.current_frame == 9:
                self.is_attack = False
        else:
            self.anim.set_animation('idle')

    def update_animation(self):
        self.anim.update_animation()
        if not self.player.right:
            self.anim.item.image = self.anim.current_animation['right'][self.anim.current_frame]
        else:
            self.anim.item.image = self.anim.current_animation['left'][self.anim.current_frame]
