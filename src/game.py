import pygame
import logging
from src.constants import *
from src.snake import Snake
from src.food import Food
from src.utils import draw_text

class Game:
    def __init__(self, screen, fps=15, difficulty="Medium"):
        self.screen = screen
        self.fps = fps
        self.difficulty = difficulty
        self.snake = Snake()
        self.food = Food()
        self.lives = 3
        self.score = 0
        self.paused = False
        self.font_hud = pygame.font.SysFont("arial", FONT_SIZE_HUD)
        self.font_title = pygame.font.SysFont("arial", FONT_SIZE_TITLE, bold=True)

    def run(self):
        logging.info("Game.run() started")
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.info("Game: QUIT event received")
                    return "quit_app"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        logging.info("Game: ESCAPE key pressed")
                        return "menu"
                    elif event.key == pygame.K_p or event.key == pygame.K_TAB:
                        self.paused = not self.paused
                    elif not self.paused:
                        if event.key == pygame.K_UP:
                            self.snake.turn((0, -1))
                        elif event.key == pygame.K_DOWN:
                            self.snake.turn((0, 1))
                        elif event.key == pygame.K_LEFT:
                            self.snake.turn((-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.snake.turn((1, 0))

            if self.paused:
                self.draw_pause()
                pygame.display.flip()
                clock.tick(self.fps)
                continue

            # Game Logic
            if self.snake.direction != (0, 0):
                alive = self.snake.move()
                if not alive:
                    self.lives -= 1
                    if self.lives <= 0:
                        return "game_over"
                    else:
                        self.snake.reset_position()

                if self.snake.get_head_position() == self.food.position:
                    self.snake.grow()
                    self.score += 10
                    self.food.randomize_position(self.snake.positions)

            # Drawing
            self.draw()
            pygame.display.flip()
            clock.tick(self.fps)

        return "menu"

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # HUD
        score_text = f"Score: {self.score}"
        lives_text = f"Lives: {self.lives}"
        draw_text(self.screen, score_text, self.font_hud, WHITE, (70, 20))
        draw_text(self.screen, lives_text, self.font_hud, WHITE, (SCREEN_WIDTH - 70, 20))

    def draw_pause(self):
        draw_text(self.screen, "PAUSED", self.font_title, YELLOW, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
