import pygame
import sys
import random
from typing import Tuple, List
from ai_snake import AISnake

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.cell_size = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game with AI')

        # Colors
        self.GREEN = (34, 139, 34)
        self.RED = (220, 20, 60)
        self.FOOD_COLOR = (255, 215, 0)
        self.GRASS_COLOR = (154, 205, 50)
        self.BLACK = (0, 0, 0)

        # Game objects
        self.player_snake = [(100, 100)]
        self.player_direction = (self.cell_size, 0)
        self.ai_snake = AISnake(600, 400, self.cell_size)
        self.food = self.spawn_food()
        
        # Game state
        self.game_over = False
        self.game_started = False

        # Load fonts
        self.font = pygame.font.Font(None, 36)

    def spawn_food(self) -> Tuple[int, int]:
        x = random.randrange(0, self.width - self.cell_size, self.cell_size)
        y = random.randrange(0, self.height - self.cell_size, self.cell_size)
        return (x, y)

    def draw_snake_face(self, pos: Tuple[int, int], color: Tuple[int, int, int]):
        x, y = pos
        # Eyes
        pygame.draw.circle(self.screen, (255, 255, 255), (x + 5, y + 5), 3)
        pygame.draw.circle(self.screen, (255, 255, 255), (x + 15, y + 5), 3)
        # Pupils
        pygame.draw.circle(self.screen, (0, 0, 0), (x + 5, y + 5), 1)
        pygame.draw.circle(self.screen, (0, 0, 0), (x + 15, y + 5), 1)

    def draw(self):
        self.screen.fill(self.GRASS_COLOR)

        # Draw food
        pygame.draw.rect(self.screen, self.FOOD_COLOR,
                        (*self.food, self.cell_size, self.cell_size))

        # Draw player snake
        for segment in self.player_snake:
            pygame.draw.rect(self.screen, self.GREEN,
                            (*segment, self.cell_size, self.cell_size))
        self.draw_snake_face(self.player_snake[0], self.GREEN)

        # Draw AI snake
        for segment in self.ai_snake.body:
            pygame.draw.rect(self.screen, self.RED,
                            (*segment, self.cell_size, self.cell_size))
        self.draw_snake_face(self.ai_snake.body[0], self.RED)

        if not self.game_started:
            start_text = self.font.render('Press SPACE to Start', True, self.BLACK)
            self.screen.blit(start_text, (self.width//2 - 100, self.height//2))

        if self.game_over:
            over_text = self.font.render('Game Over! Press R to Restart', True, self.BLACK)
            self.screen.blit(over_text, (self.width//2 - 150, self.height//2))

        pygame.display.flip()

    def check_collision(self) -> bool:
        head = self.player_snake[0]
        # Wall collision
        if (head[0] < 0 or head[0] >= self.width or
            head[1] < 0 or head[1] >= self.height):
            return True
        # Self collision
        if head in self.player_snake[1:]:
            return True
        # AI snake collision
        if head in self.ai_snake.body:
            return True
        return False

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_started:
                        self.game_started = True
                    if event.key == pygame.K_r and self.game_over:
                        self.__init__()
                    if not self.game_over and self.game_started:
                        if event.key == pygame.K_UP and self.player_direction != (0, self.cell_size):
                            self.player_direction = (0, -self.cell_size)
                        if event.key == pygame.K_DOWN and self.player_direction != (0, -self.cell_size):
                            self.player_direction = (0, self.cell_size)
                        if event.key == pygame.K_LEFT and self.player_direction != (self.cell_size, 0):
                            self.player_direction = (-self.cell_size, 0)
                        if event.key == pygame.K_RIGHT and self.player_direction != (-self.cell_size, 0):
                            self.player_direction = (self.cell_size, 0)

            if not self.game_over and self.game_started:
                # Move player snake
                new_head = (self.player_snake[0][0] + self.player_direction[0],
                           self.player_snake[0][1] + self.player_direction[1])
                self.player_snake.insert(0, new_head)

                # Check food collision
                if new_head == self.food:
                    self.food = self.spawn_food()
                else:
                    self.player_snake.pop()

                # Move AI snake
                self.ai_snake.move(self.food, self.width, self.height)

                # Check collision
                if self.check_collision():
                    self.game_over = True

            self.draw()
            clock.tick(10)

if __name__ == '__main__':
    game = SnakeGame()
    game.run()