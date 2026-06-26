import pygame
import random
from code.Background import Background
from code.factory.EntityFactory import get_entity
from code.entities.PlayerShot import PlayerShot
from code.entities.BossShot import BossShot
from code.Const import *
from code.scenes.Victory import Victory
from code.scenes.Defeat import Defeat


class Battle:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()

        self.background = Background("asset/fundo.png")

        self.player = get_entity("Player")
        self.boss = get_entity("Boss")

        self.player.hp = PLAYER_MAX_HP
        self.boss.hp = BOSS_MAX_HP

        self.player_shots = []
        self.boss_shots = []

        self.last_shot = 0
        self.last_big_shot = 0
        self.last_player_shot = 0

        self.phase_two = False
        self.phase_transition = False
        self.phase_transition_start = 0

        self.start_time = pygame.time.get_ticks()

        self.laugh_sound = pygame.mixer.Sound("asset/risada_boss.wav")
        self.player_damage_sound = pygame.mixer.Sound("asset/dano_mago.wav")
        self.explosion_sound = pygame.mixer.Sound("asset/explosion.mp3")

        self.font = pygame.font.Font(None, 28)

        pygame.mixer.music.load("asset/batalha.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.image = pygame.transform.scale(
                            pygame.image.load("asset/Mago f1.png"),
                            (180, 180)
                        )

            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE] and not self.phase_transition:
                if current_time - self.last_player_shot > 350:
                    self.player.image = pygame.transform.scale(
                        pygame.image.load("asset/mago_posição2.png"),
                        (180, 180)
                    )

                    shot = PlayerShot(
                        (self.player.rect.centerx, self.player.rect.centery)
                    )

                    self.player_shots.append(shot)
                    self.last_player_shot = current_time


            current_speed = PLAYER_SPEED_PHASE_TWO if self.phase_two else PLAYER_SPEED_PHASE_ONE

            if keys[pygame.K_w] and self.player.rect.y > 50:
                self.player.rect.y -= current_speed
            if keys[pygame.K_s] and self.player.rect.y < 530:
                self.player.rect.y += current_speed
            if keys[pygame.K_a] and self.player.rect.x > 0:
                self.player.rect.x -= current_speed
            if keys[pygame.K_d] and self.player.rect.x < 520:
                self.player.rect.x += current_speed

            if self.boss.hp <= PHASE_TWO_TRIGGER and not self.phase_two and not self.phase_transition:
                self.phase_transition = True
                self.phase_transition_start = current_time

                pygame.mixer.music.stop()
                self.laugh_sound.play()

            if self.phase_transition:
                if current_time - self.phase_transition_start >= 2500:
                    self.phase_transition = False
                    self.phase_two = True

                    pygame.mixer.music.load("asset/batalha_final.wav")
                    pygame.mixer.music.play(-1)

            lateral_positions = [
                (self.boss.rect.x - 23, self.boss.rect.y + 16),
                (self.boss.rect.x + 48, self.boss.rect.y + 83),
                (self.boss.rect.x + 370, self.boss.rect.y + 241),
                (self.boss.rect.x - 41, self.boss.rect.y + 329),
                (self.boss.rect.x + 252, self.boss.rect.y + 448),
                (self.boss.rect.x + 12, self.boss.rect.y + 153)
            ]

            attack_delay = ATTACK_DELAY_PHASE_TWO if self.phase_two else ATTACK_DELAY_NORMAL

            if current_time - self.last_shot > attack_delay and not self.phase_transition:
                random_eye = random.choice(lateral_positions)

                shot = BossShot(
                    "asset/atk_lateral_boss.png",
                    random_eye,
                    3
                )

                self.boss_shots.append(shot)
                self.last_shot = current_time

            if self.phase_two and not self.phase_transition:
                if current_time - self.last_big_shot > BIG_SHOT_DELAY:
                    big_shot = BossShot(
                        "asset/atk_principal_boss.png",
                        (self.boss.rect.x + 180, self.boss.rect.y + 190),
                        4,
                        (80, 80),
                        random.randint(-1, 1)
                    )

                    self.boss_shots.append(big_shot)
                    self.last_big_shot = current_time

            self.boss.hitbox.center = self.boss.rect.center

            for shot in self.player_shots[:]:
                shot.rect.x += PLAYER_SHOT_SPEED

                if shot.rect.left > WIN_WIDTH:
                    self.player_shots.remove(shot)
                    continue

                shot_hitbox = shot.rect.inflate(-20, -20)

                if shot_hitbox.colliderect(self.boss.hitbox):
                    if self.phase_two:
                        self.boss.hp -= PLAYER_DAMAGE_PHASE_TWO
                    else:
                        self.boss.hp -= PLAYER_DAMAGE

                    self.boss.damage_timer = 3
                    self.player_shots.remove(shot)


            for shot in self.boss_shots[:]:
                shot.speed = BOSS_SHOT_PHASE_TWO_SPEED if self.phase_two else BOSS_SHOT_SPEED
                shot.move()

                if shot.rect.right < 0:
                    self.boss_shots.remove(shot)
                    continue

                if shot.rect.colliderect(self.player.rect):
                    self.player_damage_sound.play()

                    if shot.rect.width == 80:
                        self.player.hp -= BOSS_BIG_SHOT_DAMAGE
                    else:
                        self.player.hp -= BOSS_DAMAGE_PHASE_TWO if self.phase_two else BOSS_DAMAGE

                    self.boss_shots.remove(shot)


            if self.player.hp <= 0:
                self.player.hp = 0

                pygame.mixer.music.stop()

                self.player.image = pygame.transform.scale(
                    pygame.image.load("asset/morte_mago.png"),
                    (180, 180)
                )

                self.background.draw(self.window)
                self.player.draw(self.window)
                self.boss.draw(self.window)

                pygame.display.update()
                pygame.time.delay(1200)

                end_time = pygame.time.get_ticks()
                battle_time = (end_time - self.start_time) // 1000

                score = ((BOSS_MAX_HP - self.boss.hp) * 1) + (battle_time//2)

                defeat_screen = Defeat(
                    self.window,
                    score,
                    battle_time
                )

                result = defeat_screen.run()

                if result == "restart":
                    new_battle = Battle(self.window)
                    new_battle.run()
                    return
                if result == "menu":
                    return

                running = False


            if self.boss.hp <= 0:
                pygame.mixer.music.stop()

                self.background.draw(self.window)
                self.player.draw(self.window)

                pygame.display.update()

                self.explosion_sound.play()
                pygame.time.delay(1500)

                end_time = pygame.time.get_ticks()
                battle_time = (end_time - self.start_time) // 1000

                if battle_time <= 30:
                    time_bonus = 200
                elif battle_time <= 60:
                    time_bonus = 120
                elif battle_time <= 90:
                    time_bonus = 70
                else:
                    time_bonus = 30

                score = 500+(self.player.hp * 8) + time_bonus

                victory_screen = Victory(
                    self.window,
                    score,
                    battle_time
                )

                result = victory_screen.run()

                if result == "restart":
                    new_battle = Battle(self.window)
                    new_battle.run()
                    return

                if result == "menu":
                    return

                running = False


            self.background.draw(self.window)
            self.player.draw(self.window)

            if self.boss.damage_timer > 0:
                red_boss = self.boss.image.copy()
                red_boss.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)
                self.window.blit(red_boss, self.boss.rect.topleft)
                self.boss.damage_timer -= 1
            else:
                self.boss.draw(self.window)

            for shot in self.player_shots:
                shot.draw(self.window)

            for shot in self.boss_shots:
                shot.draw(self.window)


            pygame.draw.rect(self.window, RED, (40, 30, 300, 20))
            pygame.draw.rect(
                self.window,
                BLUE,
                (40, 30, int((self.player.hp / PLAYER_MAX_HP) * 300), 20)
            )


            pygame.draw.rect(self.window, RED, (940, 30, 300, 20))
            pygame.draw.rect(
                self.window,
                GREEN,
                (940, 30, int((self.boss.hp / BOSS_MAX_HP) * 300), 20)
            )


            player_hp_text = self.font.render(
                f"{self.player.hp}/{PLAYER_MAX_HP}", True, WHITE
            )
            self.window.blit(player_hp_text, (150, 55))

            boss_hp_text = self.font.render(
                f"{self.boss.hp}/{BOSS_MAX_HP}", True, WHITE
            )
            self.window.blit(boss_hp_text, (1050, 55))

            pygame.display.update()