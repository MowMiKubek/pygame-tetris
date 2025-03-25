import random

import pygame

# import constants

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20
BLOCK_SIZE = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Tetromino:
    COLORS = [
        (0, 255, 255),  # I
        (128, 0, 128),  # T
        (255, 165, 0),  # L
        (0, 0, 255),  # J
        (255, 255, 0),  # O
    ]

    tetrominoes = [
        [[1, 1, 1, 1]],          # I
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]],  # J
        [[1, 1], [1, 1]],        # O
        [[0, 1, 1], [1, 1, 0]],  # thunder
    ]

    propabilities = [0.75, 1.0, 1.0, 1.5, 1.0, 2.0]
    shapes_count = [0, 0, 0, 0, 0, 0]

    def __init__(self, forbidden_shape=None):
        Tetromino.normalize_prop()
        random_number = random.uniform(0.0, 1.0)
        prefix_sum = 0
        self.shape = Tetromino.tetrominoes[0]
        for i, prop in enumerate(Tetromino.propabilities):
            if random_number <= prefix_sum + prop:
                self.shape = Tetromino.tetrominoes[i]
                Tetromino.shapes_count[i] += 1
                break
            prefix_sum += prop

        self.color = random.choice(Tetromino.COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    @staticmethod
    def normalize_prop():
        prop_sum = sum(Tetromino.propabilities)
        for i, item in enumerate(Tetromino.propabilities):
            Tetromino.propabilities[i] = item / prop_sum

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    @staticmethod
    def draw_tetromino(surface, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(surface, tetromino.color,
                                     (
                                         (tetromino.x + x) * BLOCK_SIZE,
                                         (tetromino.y + y) * BLOCK_SIZE,
                                         BLOCK_SIZE,
                                         BLOCK_SIZE))
