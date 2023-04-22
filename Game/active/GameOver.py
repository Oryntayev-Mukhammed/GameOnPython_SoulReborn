import pygame

from Game.Button import Button


class GameOver:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_button = Button(250, 350, 300, 50, 'Start', (0, 255, 0))

    def update(self, game_state_machine):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (0, 0, 0))
        self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, self.SCREEN_HEIGHT // 2 - text.get_height() // 2))
        self.start_button.draw(self.screen)

    def handle_event(self, event, game_state_machine):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.start_button.clicked(mouse_pos):
                game_state_machine.change_state("GamePlay")
                game_state_machine.edit()


