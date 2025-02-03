from typing import List, Tuple

class AISnake:
    def __init__(self, x: int, y: int, cell_size: int):
        self.body = [(x, y)]
        self.direction = (-cell_size, 0)
        self.cell_size = cell_size

    def move(self, food: Tuple[int, int], width: int, height: int):
        head = self.body[0]
        food_dir_x = 1 if food[0] > head[0] else -1 if food[0] < head[0] else 0
        food_dir_y = 1 if food[1] > head[1] else -1 if food[1] < head[1] else 0

        # Decide direction based on food position and boundaries
        if abs(food[0] - head[0]) > abs(food[1] - head[1]):
            new_x = head[0] + (self.cell_size * food_dir_x)
            new_y = head[1]
            if new_x < 0 or new_x >= width:
                new_x = head[0]
                new_y = head[1] + (self.cell_size * food_dir_y)
        else:
            new_x = head[0]
            new_y = head[1] + (self.cell_size * food_dir_y)
            if new_y < 0 or new_y >= height:
                new_y = head[1]
                new_x = head[0] + (self.cell_size * food_dir_x)

        # Update snake position
        self.body.insert(0, (new_x, new_y))
        self.body.pop()

        # Avoid self collision
        if self.body[0] in self.body[1:]:
            self.body.insert(0, (head[0] - self.cell_size, head[1]))
            self.body.pop()