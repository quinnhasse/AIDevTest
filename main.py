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
        self.ai_snake = AISnake(self.width, self.height, self.cell_size)
        self.food = self.spawn_food()
        
        # Game state
        self.game_over = False
        self.game_started = False

        # Load fonts
        self.font = pygame.font.Font(None, 36)

    def spawn_food(self) -> Tuple[int, int]:
        x = random.randrange(0, self.width, self.cell_size)
        y = random.randrange(0, self.height, self.cell_size)
        return (x, y)

    def draw_snake_face(self, head: Tuple[int, int], is_player: bool):
        color = self.BLACK
        # Eyes
        pygame.draw.circle(self.screen, color,
                          (head[0] + 5, head[1] + 5), 2)
        pygame.draw.circle(self.screen, color,
                          (head[0] + 15, head[1] + 5), 2)
        # Smile
        pygame.draw.arc(self.screen, color,
                       (head[0] + 5, head[1] + 5, 10, 10),
                       0, 3.14, 2)

    def draw(self):
        self.screen.fill(self.GRASS_COLOR)

        # Draw food
        pygame.draw.rect(self.screen, self.FOOD_COLOR,
                        (self.food[0], self.food[1],
                         self.cell_size, self.cell_size))

        # Draw player snake
        for segment in self.player_snake:
            pygame.draw.rect(self.screen, self.GREEN,
                           (segment[0], segment[1],
                            self.cell_size, self.cell_size))
        self.draw_snake_face(self.player_snake[0], True)

        # Draw AI snake
        for segment in self.ai_snake.body:
            pygame.draw.rect(self.screen, self.RED,
                           (segment[0], segment[1],
                            self.cell_size, self.cell_size))
        self.draw_snake_face(self.ai_snake.body[0], False)

        if not self.game_started:
            start_text = self.font.render('Press SPACE to Start',
                                         True, self.BLACK)
            self.screen.blit(start_text,
                            (self.width//2 - 100, self.height//2))

        if self.game_over:
            over_text = self.font.render('Game Over! Press R to Restart',
                                        True, self.BLACK)
            self.screen.blit(over_text,
                            (self.width//2 - 150, self.height//2))

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                if not self.game_over and self.game_started:
                    if event.key == pygame.K_UP:
                        self.player_direction = (0, -self.cell_size)
                    elif event.key == pygame.K_DOWN:
                        self.player_direction = (0, self.cell_size)
                    elif event.key == pygame.K_LEFT:
                        self.player_direction = (-self.cell_size, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player_direction = (self.cell_size, 0)
        return True

    def reset_game(self):
        self.player_snake = [(100, 100)]
        self.player_direction = (self.cell_size, 0)
        self.ai_snake = AISnake(self.width, self.height, self.cell_size)
        self.food = self.spawn_food()
        self.game_over = False
        self.game_started = False

    def update(self):
        if not self.game_started or self.game_over:
            return

        # Move player snake
        new_head = (self.player_snake[0][0] + self.player_direction[0],
                   self.player_snake[0][1] + self.player_direction[1])

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return

        self.player_snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.food = self.spawn_food()
        else:
            self.player_snake.pop()

        # Update AI snake
        self.ai_snake.update(self.food)

        # Check collision with AI snake
        if (new_head in self.ai_snake.body or
            new_head in self.player_snake[1:]):
            self.game_over = True

    def run(self):
        clock = pygame.time.Clock()
        while True:
            if not self.handle_input():
                break
            self.update()
            self.draw()
            clock.tick(10)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()