import pygame
import random
from typing import List, Tuple
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.block_size = 20
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game with AI Adversary')
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
        # Initialize game state
        self.reset_game()
        
    def reset_game(self):
        """Reset the game state to initial conditions."""
        self.player_snake = [(self.width//4, self.height//2)]
        self.player_direction = Direction.RIGHT
        
        self.ai_snake = [(3*self.width//4, self.height//2)]
        self.ai_direction = Direction.LEFT
        
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        
    def spawn_food(self) -> Tuple[int, int]:
        """Spawn food at random location."""
        while True:
            x = random.randrange(0, self.width, self.block_size)
            y = random.randrange(0, self.height, self.block_size)
            if (x, y) not in self.player_snake and (x, y) not in self.ai_snake:
                return (x, y)
    
    def move_ai_snake(self):
        """Move AI snake using simple pathfinding."""
        head = self.ai_snake[0]
        food = self.food
        
        # Simple AI: Move towards food
        dx = food[0] - head[0]
        dy = food[1] - head[1]
        
        if abs(dx) > abs(dy):
            if dx > 0 and self.ai_direction != Direction.LEFT:
                self.ai_direction = Direction.RIGHT
            elif dx < 0 and self.ai_direction != Direction.RIGHT:
                self.ai_direction = Direction.LEFT
        else:
            if dy > 0 and self.ai_direction != Direction.UP:
                self.ai_direction = Direction.DOWN
            elif dy < 0 and self.ai_direction != Direction.DOWN:
                self.ai_direction = Direction.UP
                
        # Move AI snake
        new_head = self.get_new_head(self.ai_snake[0], self.ai_direction)
        self.ai_snake.insert(0, new_head)
        self.ai_snake.pop()
    
    def get_new_head(self, head: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
        """Calculate new head position based on direction."""
        x, y = head
        if direction == Direction.UP:
            return (x, y - self.block_size)
        elif direction == Direction.DOWN:
            return (x, y + self.block_size)
        elif direction == Direction.LEFT:
            return (x - self.block_size, y)
        else:  # Direction.RIGHT
            return (x + self.block_size, y)
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_input(event.key)
            
            # Move snakes
            new_head = self.get_new_head(self.player_snake[0], self.player_direction)
            self.player_snake.insert(0, new_head)
            
            # Check collisions
            if self.check_collision():
                self.game_over = True
                break
            
            # Check if food eaten
            if new_head == self.food:
                self.score += 1
                self.food = self.spawn_food()
            else:
                self.player_snake.pop()
            
            # Move AI snake
            self.move_ai_snake()
            
            # Draw everything
            self.draw()
            
            clock.tick(10)
        
        self.show_game_over()
    
    def handle_input(self, key):
        """Handle keyboard input."""
        if key == pygame.K_UP and self.player_direction != Direction.DOWN:
            self.player_direction = Direction.UP
        elif key == pygame.K_DOWN and self.player_direction != Direction.UP:
            self.player_direction = Direction.DOWN
        elif key == pygame.K_LEFT and self.player_direction != Direction.RIGHT:
            self.player_direction = Direction.LEFT
        elif key == pygame.K_RIGHT and self.player_direction != Direction.LEFT:
            self.player_direction = Direction.RIGHT
    
    def check_collision(self) -> bool:
        """Check for collisions with walls and snake bodies."""
        head = self.player_snake[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= self.width or
            head[1] < 0 or head[1] >= self.height):
            return True
        
        # Self collision
        if head in self.player_snake[1:]:
            return True
        
        # AI snake collision
        if head in self.ai_snake:
            return True
        
        return False
    
    def draw(self):
        """Draw game state to screen."""
        self.screen.fill(self.BLACK)
        
        # Draw player snake
        for segment in self.player_snake:
            pygame.draw.rect(self.screen, self.GREEN,
                           [segment[0], segment[1], self.block_size, self.block_size])
        
        # Draw AI snake
        for segment in self.ai_snake:
            pygame.draw.rect(self.screen, self.BLUE,
                           [segment[0], segment[1], self.block_size, self.block_size])
        
        # Draw food
        pygame.draw.rect(self.screen, self.RED,
                        [self.food[0], self.food[1], self.block_size, self.block_size])
        
        pygame.display.update()
    
    def show_game_over(self):
        """Display game over screen."""
        font = pygame.font.Font(None, 50)
        text = font.render(f'Game Over! Score: {self.score}', True, self.WHITE)
        self.screen.blit(text, (self.width//4, self.height//2))
        pygame.display.update()
        pygame.time.wait(2000)

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
    pygame.quit()
