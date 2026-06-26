import pygame
from code.Const import *
from code.scenes.Score import load_scores


class History:
    def __init__(self, window):
        self.window = window

        self.background = pygame.transform.scale(
            pygame.image.load("asset/history.png"),
            (WIN_WIDTH, WIN_HEIGHT)
        )

        self.title_font = pygame.font.Font(None, 70)
        self.text_font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)

    def run(self):
        scores = load_scores()

        while True:
            self.window.blit(self.background, (0, 0))

            y =200


            for score in reversed(scores[-8:]):
                score_text = self.text_font.render(
                    score.strip(),
                    True,
                    WHITE
                )

                self.window.blit(
                    score_text,
                    (
                        WIN_WIDTH // 2 - score_text.get_width() // 2,
                        y
                    )
                )

                y += 55


            back_text = self.small_font.render(
                "ESC - Back",
                True,
                WHITE
            )

            self.window.blit(back_text, (40, WIN_HEIGHT - 40))

            pygame.display.update()

            for event in pygame.event.get():


                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:


                    if event.key == pygame.K_ESCAPE:
                        return