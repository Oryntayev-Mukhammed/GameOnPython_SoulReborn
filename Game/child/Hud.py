#
# import pygame
#
#
# # Класс для расстановки платформ на сцене
# class Hud(object):
#     def __init__(self, player):
#         # Создаем группу спрайтов (поместим платформы различные сюда)
#         self.hud_list = pygame.sprite.Group()
#         # Ссылка на основного игрока
#         self.player = player
#
#     # Чтобы все рисовалось, то нужно обновлять экран
#     # При вызове этого метода обновление будет происходить
#     def update(self):
#         self.hud_list.update()
#
#     # Метод для рисования объектов на сцене
#     def draw(self, screen, lenght):
#         # Рисуем задний фон
#         screen.blit(pygame.Surface((lenght, 10)), (0, 0))
#
#         # Рисуем все платформы из группы спрайтов
#         self.hud_list.draw(screen)
#

import pygame


class Hud:
    def __init__(self, screen, max_health, current_health, health_bar_lenght, max_plasma, current_plasma, plasma_bar_lenght):
        self.max_health = max_health
        self.current_health = current_health
        self.max_plasma = max_plasma
        self.current_plasma = current_plasma
        self.health_bar_lenght = health_bar_lenght
        self.plasma_bar_lenght = plasma_bar_lenght
        # Рассчитываем пропорцию для изменения длины полоски жизни
        self.health_ratio = self.max_health / self.health_bar_lenght
        self.plasma_ratio = self.max_plasma / self.plasma_bar_lenght

        self.screen = screen

    def update_health_bar(self):
        # Рисуем полоску жизни на экране
        if self.current_health * 4 < self.max_health:
            pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, self.current_health / self.health_ratio, 25))
        elif self.current_health * 2 < self.max_health:
            pygame.draw.rect(self.screen, (255, 140, 0), (10, 10, self.current_health / self.health_ratio, 25))
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, self.current_health / self.health_ratio, 25))
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.current_health) + ' / ' + str(self.max_health), True, (0, 0, 0))
        self.screen.blit(text, (40, 17))
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, self.health_bar_lenght, 25), 4)

    def update_plasma_bar(self):
        pygame.draw.rect(self.screen, (187, 209, 254), (10, 40, self.current_plasma / self.plasma_ratio, 25))
        font = pygame.font.Font(None, 20)
        text = font.render(str(int(self.current_plasma)) + ' / ' + str(self.max_plasma), True, (0, 0, 0))
        self.screen.blit(text, (30, 47))
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 40, self.plasma_bar_lenght, 25), 4)

    def update_hud(self):
        self.update_health_bar()
        self.update_plasma_bar()
        pygame.display.flip()
