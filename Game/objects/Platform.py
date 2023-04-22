import pygame


# Класс для описания платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        # Конструктор платформ
        super().__init__()
        # Также указываем фото платформы
        self.image = pygame.image.load('assets/Plot01.png')

        # Делаем плотформе высоту и ширину картинки
        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(self.image, (width, height))

        # Меняем высоту и ширину
        self.rect.h = height
        self.rect.w = width
