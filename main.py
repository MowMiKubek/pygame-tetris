import random

import pygame

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20
BLOCK_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# grid = [
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, (125,65,9), 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 1, 1, 0],
#     [0, 1, 0, 0],
#     [0, 1, 0, 0],
# ]

"""
    ####    - I
    
    ###
     #      - T
     
    ###
    #       - L
    
    ###
      #     - J 
    
    ##      - O
    ##
"""

tetrominoes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
]

COLORS = [
    (0, 255, 255),  # I
    (128, 0, 128),  # T
    (255, 165, 0),  # L
    (0, 0, 255),  # J
    (255, 255, 0),  # O
]


class Tetromino:
    def __init__(self):
        self.shape = random.choice(tetrominoes)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_tetromino(surface, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(surface, tetromino.color,
                                 ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE))


grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

running = True
current_tetromino = Tetromino()

fall_speed = 500
fall_time = 0

while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time >= fall_speed:
        fall_time = 0
        if current_tetromino.y + len(current_tetromino.shape) + 1 > GRID_HEIGHT:
            for y, row in enumerate(current_tetromino.shape):
                for x, cell in enumerate(row):
                    if cell != 0:
                        grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color
            current_tetromino = Tetromino()
        else:
            current_tetromino.y += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                current_tetromino.y += 1
            if event.key == pygame.K_LEFT:
                current_tetromino.x -= 1
            if event.key == pygame.K_RIGHT:
                current_tetromino.x += 1
            if event.key == pygame.K_UP:
                current_tetromino.rotate()

    draw_grid(screen, grid)
    draw_tetromino(screen, current_tetromino)
    pygame.display.flip()
