import sys

import pygame

from Game.GameStateMachine import GameStateMachine
from Game.Player import Player
from Game.active.GameOver import GameOver
from Game.active.GamePlay import GamePlay
from Game.active.MainMenu import MainMenu
from Game.levels.Level_01 import Level_01
from Game.levels.Level_02 import Level_02
from Game.levels.Level_03 import Level_03

# Переменные для установки ширины и высоты окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Основная функция прогарммы
def main():
    # Инициализация
    pygame.init()

    # Установка высоты и ширины
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # Название игры
    pygame.display.set_caption("Платформер")

    # Создаем игрока
    player = Player(SCREEN_HEIGHT, screen)

    # Создание уровня
    level_01 = Level_01(player)
    level_02 = Level_02(player)
    level_03 = Level_03(player)

    # Создаем все уровни
    level_list = [
        level_01,
        level_02,
        level_03
    ]

    # Устанавливаем текущий уровень
    current_level_no = 2
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()

    player.level = current_level

    # Настройка появления игрока
    player.rect.x = 340
    playerX = 340
    player.rect.y = SCREEN_HEIGHT / 2
    playerY = SCREEN_HEIGHT / 2
    active_sprite_list.add(player)

    # Реализуем активные окна
    main_menu = MainMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    game_play = GamePlay(active_sprite_list, level_list, current_level_no, player, screen,
                         SCREEN_WIDTH)
    game_over = GameOver(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_state_machine = GameStateMachine(
        {"MainMenu": main_menu, "GamePlay": game_play, "GameOver": game_over},
        main_menu
    )

    # Цикл будет до тех пор, пока пользователь не нажмет кнопку закрытия
    done = False

    # Основной цикл программы
    while not done:
        # Отслеживание действий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если закрыл программу, то останавливаем цикл
                done = True

            # Сменя состояния между active
            game_state_machine.handle_event(event, game_state_machine)

            # Game over
            if game_play.state:
                game_play.load(0, playerX, playerY)
                game_play.edit()

        # Обновление состояния
        game_state_machine.update(game_state_machine)

        pygame.display.update()

        game_play.player_control(event)

    # Корректное закртытие программы
    pygame.quit()


main()
