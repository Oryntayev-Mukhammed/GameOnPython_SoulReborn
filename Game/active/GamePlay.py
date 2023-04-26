import pygame
from pygame.locals import *

from assets.entity.Sword import Sword


class GamePlay:
    def __init__(self, active_sprite_list, level_list, current_level_no, player, screen, SCREEN_WIDTH):
        self.active_sprite_list = active_sprite_list
        self.current_level_no = current_level_no
        self.current_level = level_list[current_level_no]
        self.level_list = level_list
        self.player = player
        self.screen = screen
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.clock = pygame.time.Clock()
        self.state = False
        self.key_state = pygame.key.get_pressed()
        self.key_press = False

    def update(self, game_state_machine):
        # Обновляем игрока
        self.active_sprite_list.update()
        self.player.entity_sprite_list.update()

        # Проверка умер ли игрок
        self.player.die_check(game_state_machine)

        # Обновляем карту
        self.current_level = self.level_list[self.current_level_no]

        # Какая карта действует на персонажа
        self.player.level = self.current_level

        # Смена типа анимации
        self.player.set_animation()

        self.player.update_animation()

        # Обновляем объекты на сцене
        self.current_level.update()

        # Если игрок приблизится к правой стороне, то дальше его не двигаем или переходим на другой уровень
        if self.player.rect.right > self.SCREEN_WIDTH:
            if self.current_level_no != len(self.level_list) - 1 and self.player.right:
                self.current_level_no += 1
                self.current_level = self.level_list[self.current_level_no]
                self.load(self.current_level_no, 5, self.player.rect.y)
            else:
                self.player.rect.right = self.SCREEN_WIDTH

        # Если игрок приблизится к левой стороне, то дальше его не двигаем
        if self.player.rect.left < 0:
            if self.current_level_no != 0 and not self.player.right:
                self.current_level_no -= 1
                self.current_level = self.level_list[self.current_level_no]
                self.load(self.current_level_no, 795, self.player.rect.y - 1)
            else:
                self.player.rect.left = 0

        if self.player.rect.bottom > 599:
            self.player.take_damage(9)
            # Оглушение (передаваемое число не имеет смысла)
            self.player.stun(20)
            # Возвращение в начало
            self.main_pos()

        # Рисуем объекты на окне ОЧЕНЬ ВАЖНО ПИСАТЬ СЮДА ВСЕ DRAW и ЛЮБЫЕ ОБЬЕКТЫ
        self.current_level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)
        self.player.entity_sprite_list.draw(self.screen)
        # Добавил сюда обновление полоски жизни и он перестал моргать
        self.player.hud.update_hud()
        # Устанавливаем количество фреймов
        self.clock.tick(30)

    def handle_event(self, event, game_state_machine):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # обработка нажатия клавиши ESC
            game_state_machine.change_state("MainMenu")

    # Возвращение в начало
    def main_pos(self):
        self.current_level_no = 0
        self.player.rect.x = 340
        self.player.rect.y = 330

    def load(self, current_level_no, playerX, playerY):
        self.current_level_no = current_level_no
        self.player.rect.x = playerX
        self.player.rect.y = playerY

    def player_control(self, event):
        # Проверка на передвижение
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.player.is_moving = True
        else:
            self.player.is_moving = False
            self.player.moment_move = True

        if keys[pygame.K_SPACE] and self.player.hud.current_plasma > 0 and not self.player.is_fly:
            self.player.fly(0.05)
            self.player.reduce_plasma(0.8)
            if self.player.change_y < 0:
                self.player.change_y = self.player.fly_max_speed
            else:
                self.player.change_y = self.player.change_y / 2
        elif keys[pygame.K_SPACE] and self.player.hud.current_plasma > 0 and self.player.is_fly:
            self.player.fly(0.05)
            self.player.reduce_plasma(0.2)
        elif self.player.is_fly:
            self.player.is_fly = False

        current_key_state = pygame.key.get_pressed()
        # Проверка наличия нажатия клавиши
        if current_key_state[K_a] and not self.key_state[K_SPACE]:
            self.key_press = True
        else:
            self.key_press = False
        if self.key_press:
            self.player.sword.is_attack = True
            self.player.sword.attack()
        # Если нажали на стрелки клавиатуры, то двигаем объект
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.go_left()
            if event.key == pygame.K_RIGHT:
                self.player.go_right()
            if event.key == pygame.K_UP:
                self.player.jump()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.player.change_x < 0:
                self.player.stop()
            if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                self.player.stop()

    def edit(self):
        self.state = not self.state
