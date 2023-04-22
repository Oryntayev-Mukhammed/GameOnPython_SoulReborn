import sys

import pygame

from Game.Button import Button


class MainMenu:
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = screen
        self.start_button = Button(250, 250, 300, 50, 'Start', (0, 255, 0))
        self.exit_button = Button(250, 350, 300, 50, 'Exit', (255, 0, 0))

    def update(self, game_state_machine):
        self.start_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def handle_event(self, event, game_state_machine):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.start_button.clicked(mouse_pos):
                game_state_machine.change_state("GamePlay")

            elif self.exit_button.clicked(mouse_pos):
                pygame.quit()
                sys.exit()