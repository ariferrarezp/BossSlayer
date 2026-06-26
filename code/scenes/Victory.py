import pygame
from code.Const import *
from code.scenes.Score import save_score

class Victory:
    def __init__(self, window, score, battle_time):
        self.window = window
        self.score = score
        self.battle_time = battle_time

        self.background = pygame.transform.scale(
            pygame.image.load("asset/vitoria.png"),
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.big_font = pygame.font.Font(None, 110)
        self.menu_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 28)

        self.options = ["Play Again","Back to Menu"]
        self.selected = 0

        pygame.mixer.music.load("asset/victory_music.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            self.window.blit(self.background, (0, 0))


            victory_text = self.big_font.render(
                "VICTORY",
                True,
                WHITE
            )

            self.window.blit(
                victory_text,
                (
                    WIN_WIDTH // 2 - victory_text.get_width() // 2,
                    90
                )
            )


            score_text = self.menu_font.render(
                f"Score: {self.score}",
                True,
                WHITE
            )

            time_text = self.small_font.render(
                f"Time: {self.battle_time}s",
                True,
                WHITE
            )

            self.window.blit(
                score_text,
                (
                    WIN_WIDTH // 2 - score_text.get_width() // 2,
                    260
                )
            )

            self.window.blit(
                time_text,
                (
                    WIN_WIDTH // 2 - time_text.get_width() // 2,
                    310
                )
            )


            for i, option in enumerate(self.options):
                if i == self.selected:
                    text = "> " + option
                    color = RED
                else:
                    text = option
                    color = WHITE

                option_text = self.menu_font.render(
                    text,
                    True,
                    color
                )

                self.window.blit(
                    option_text,
                    (
                        WIN_WIDTH // 2 - option_text.get_width() // 2,
                        390 + i * 80
                    )
                )


            exit_text = self.small_font.render(
                "ESC - Exit",
                True,
                WHITE
            )

            self.window.blit(
                exit_text,
                (20, WIN_HEIGHT - 30)
            )

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
                            save_score("Victory", self.score, self.battle_time)
                            return "restart"

                        if self.selected == 1:
                            pygame.mixer.music.stop()
                            save_score("Victory", self.score, self.battle_time)
                            return "menu"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()

                            exit()