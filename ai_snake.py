from typing import List, Tuple
import random

class AISnake:
    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.body = [(width - 100, height - 100)]
        self.direction = (-cell_size, 0)

    def get_next_move(self, food: Tuple[int, int]) -> Tuple[int, int]:
        head = self.body[0]
        possible_moves = [
            (self.cell_size, 0),
            (-self.cell_size, 0),
            (0, self.cell_size),
            (0, -self.cell_size)
        ]

        # Remove moves that would cause wall collision
        valid_moves = []
        for move in possible_moves:
            new_x = head[0] + move[0]
            new_y = head[1] + move[1]
            if (0 <= new_x < self.width and
                0 <= new_y < self.height and
                (new_x, new_y) not in self.body):
                valid_moves.append(move)

        if not valid_moves:
            return self.direction

        # Choose move that gets closer to food
        best_move = valid_moves[0]
        min_distance = float('inf')
        for move in valid_moves:
            new_x = head[0] + move[0]
            new_y = head[1] + move[1]
            distance = abs(new_x - food[0]) + abs(new_y - food[1])
            if distance < min_distance:
                min_distance = distance
                best_move = move

        return best_move

    def update(self, food: Tuple[int, int]):
        self.direction = self.get_next_move(food)
        new_head = (self.body[0][0] + self.direction[0],
                   self.body[0][1] + self.direction[1])
        
        self.body.insert(0, new_head)
        
        # Grow if food is eaten
        if new_head == food:
            return
        self.body.pop()