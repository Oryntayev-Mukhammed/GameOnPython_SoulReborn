import pygame


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

    def update(self, game_state_machine):
        # Обновляем игрока
        self.active_sprite_list.update()

        # Обновляем карту
        self.current_level = self.level_list[self.current_level_no]

        # Какая карта действует на персонажа
        self.player.level = self.current_level

        # Обновление полоски жизни
        self.player.hud.update_health_bar()

        # Смена типа анимации
        self.player.set_animation()

        self.player.update_animation()
        # Обновляем объекты на сцене
        # self.current_level.update()


        # Если игрок приблизится к правой стороне, то дальше его не двигаем или переходим на другой уровень
        if self.player.rect.right > self.SCREEN_WIDTH:
            if self.current_level_no != len(self.level_list)-1 and self.player.right:
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
                self.load(self.current_level_no, 795, self.player.rect.y-1)
            else:
                self.player.rect.left = 0

        if self.player.rect.bottom > 599:
            self.player.take_damage(10, game_state_machine)
            # Оглушение (передаваемое число не имеет смысла)
            self.player.stun(20)
            # Возвращение в начало
            self.pos()

        # Рисуем объекты на окне
        self.current_level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)
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

