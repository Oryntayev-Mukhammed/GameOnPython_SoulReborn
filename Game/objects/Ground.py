import pygame


# Класс для описания платформы
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        # Конструктор платформ
        super().__init__()
        # Также указываем фото платформы
        self.image = pygame.image.load('assets/ground.png')

        # Делаем плотформе высоту и ширину картинки
        self.rect = self.image.get_rect()
