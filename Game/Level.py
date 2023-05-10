import pygame


# Класс для расстановки платформ на сцене
class Level(object):
    def __init__(self, player, backGround):
        self.backGround = backGround
        # Создаем группу спрайтов (поместим платформы различные сюда)
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        # Ссылка на основного игрока
        self.player = player

    # Чтобы все рисовалось, то нужно обновлять экран
    # При вызове этого метода обновление будет происходить
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.item_list.update()

    # Метод для рисования объектов на сцене
    def draw(self, screen):
        # Рисуем задний фон
        screen.blit(self.backGround, (0, 0))

        # Рисуем все из группы спрайтов
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)

