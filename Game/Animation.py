import pygame

class Animation:
    def __init__(self, player, item):
        self.animations = {'idle': {'left': [], 'right': []}}
        self.current_frame = 0
        self.current_animation = self.animations['idle']
        self.player = player
        self.item = item

    def addAnim(self, name, url, count):
        self.animations[name] = {'left': [], 'right': []}
        for i in range(1, count):
            image = pygame.image.load(url + f'{i}.png').convert_alpha()
            self.animations[name]['left'].append(image)
            self.animations[name]['right'].append(pygame.transform.flip(image, True, False))

    def set_animation(self, name):
        if self.current_animation != self.animations[name]:
            self.current_frame = 0
        # Назначение текущей анимаций
        self.current_animation = self.animations[name]
        # Получение картинки в соответсвии с направлением игрока
        if self.player.right:
            self.item.image = self.current_animation['left'][self.current_frame]
        else:
            self.item.image = self.current_animation['right'][self.current_frame]

    def update_animation(self):
        # Получение следующего кадра анимации
        self.current_frame += 1
        # Если кадра не существует начинаем заново
        if self.current_frame >= len(self.current_animation['right']):
            self.current_frame = 0

