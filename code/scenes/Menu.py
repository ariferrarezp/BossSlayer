import pygame
from code.Const import *


class Menu:
    def __init__(self, window):
        self.window = window

        self.background = pygame.transform.scale(
            pygame.image.load("asset/tela_menu.png"),
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.title_font = pygame.font.Font(None, 120)
        self.menu_font = pygame.font.Font(None, 70)
        self.info_font = pygame.font.Font(None, 40)

        self.options = ["Start Game", "View Score"]
        self.selected = 0

        pygame.mixer.music.load("asset/menu.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            self.window.blit(self.background, (0, 0))


            title = self.title_font.render("BOSS SLAYER", True, (255, 215, 0))
            self.window.blit(
                title,
                (WIN_WIDTH // 2 - title.get_width() // 2, 60)
            )


            for i, option in enumerate(self.options):

                if i == self.selected:
                    text = "> " + option
                    color = RED
                else:
                    text = option
                    color = WHITE

                option_text = self.menu_font.render(text, True, color)

                self.window.blit(
                    option_text,
                    (
                        WIN_WIDTH // 2 - option_text.get_width() // 2,
                        350 + i * 100
                    )
                )


            controls1 = self.info_font.render(
                "Move: W A S D",
                True,
                WHITE
            )

            controls2 = self.info_font.render(
                "Shoot: SPACE",
                True,
                WHITE
            )

            self.window.blit(controls1, (40, WIN_HEIGHT - 120))
            self.window.blit(controls2, (40, WIN_HEIGHT - 80))

            exit_text = self.info_font.render(
                "ESC - Exit",
                True,
                WHITE
            )

            self.window.blit(exit_text, (WIN_WIDTH - 170, WIN_HEIGHT - 50))

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.selected -= 1
                        if self.selected < 0:
                            self.selected = len(self.options) - 1

                    if event.key == pygame.K_DOWN:
                        self.selected += 1
                        if self.selected >= len(self.options):
                            self.selected = 0

                    if event.key == pygame.K_RETURN:

                        if self.selected == 0:
                            pygame.mixer.music.stop()
                            return "start"

                        if self.selected == 1:
                            return "history"

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()