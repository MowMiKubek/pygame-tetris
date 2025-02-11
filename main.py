import random
from copy import deepcopy
import pygame

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20
BLOCK_SIZE = 30

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_screen = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

score_font = pygame.font.SysFont('Arial', 36)

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
    [[0, 1, 1], [1, 1, 0]],
    # [[0, 1, 0],[1, 1, 1],[0, 1, 0]]
]

COLORS = [
    (0, 255, 255),  # I
    (128, 0, 128),  # T
    (255, 165, 0),  # L
    (0, 0, 255),  # J
    (255, 255, 0),  # O
]


class Tetromino:
    def __init__(self, forbidden_shape=None):
        self.shape = random.choice(list(filter(lambda elem: elem != forbidden_shape, tetrominoes)))
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def valid_move(shape, grid, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell != 0:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                    return False
                if grid[y + off_y][x + off_x] != 0:
                    return False
    return True

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            # pygame.draw.rect(surface, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_tetromino(surface, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(surface, tetromino.color,
                                 ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE))

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)] # 111101 - keep it; 111111 - discard it
    lines_removed = GRID_HEIGHT - len(new_grid)
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(lines_removed)] + new_grid
    return new_grid, lines_removed

def check_if_game_over(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if grid[y][x + tetromino.x] != 0 and tetromino.shape[y][x] != 0:
                return False
    return True


def place_ghost(grid, tetromino):
    while valid_move(tetromino.shape, grid, (tetromino.x, tetromino.y + 1)):
        tetromino.y += 1
    tetromino.color = (40, 40, 40)
    return tetromino

def draw_next_tetromino(surface, tetromino, location):
    x_loc, y_loc = location
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell != 0:
                pygame.draw.rect(surface, tetromino.color,
                                 ((x_loc + x) * BLOCK_SIZE, (y_loc + y) * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE))


grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

running = True
current_tetromino = Tetromino()
next_tetromino = Tetromino(current_tetromino.shape)
ghost_tetromino = deepcopy(current_tetromino)
ghost_tetromino.color = (20, 20, 20)
ghost_tetromino = place_ghost(grid, ghost_tetromino)

fall_speed = 500
fall_time = 0

"""
    1 line - 40p
    2 line - 100p
    3 line - 300p
    4 line - 1200p
"""

game_score = 0

while running:
    game_screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    if game_score < 1000:
        fall_speed = 500
    elif 1000 <= game_score < 2000:
        fall_speed = 400
    elif 2000 <= game_score < 3000:
        fall_speed = 300
    else:
        fall_speed = 200

    if fall_time >= fall_speed:
        fall_time = 0
        if valid_move(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y + 1)):
            current_tetromino.y += 1
        else:
            for y, row in enumerate(current_tetromino.shape):
                for x, cell in enumerate(row):
                    if cell != 0:
                        grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color
            grid, lines = clear_lines(grid)
            print(lines)
            if lines == 1:
                game_score += 40
            elif lines == 2:
                game_score += 100
            elif lines == 3:
                game_score += 300
            elif lines == 4:
                game_score += 1200
            current_tetromino = next_tetromino
            next_tetromino = Tetromino(current_tetromino.shape)
            if not check_if_game_over(grid, current_tetromino):
                running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and valid_move(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y + 1)):
                current_tetromino.y += 1
            if event.key == pygame.K_SPACE:
                while valid_move(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y + 1)):
                    current_tetromino.y += 1
            if event.key == pygame.K_LEFT and valid_move(current_tetromino.shape, grid, (current_tetromino.x - 1, current_tetromino.y)):
                current_tetromino.x -= 1
            if event.key == pygame.K_RIGHT and valid_move(current_tetromino.shape, grid, (current_tetromino.x + 1, current_tetromino.y)):
                current_tetromino.x += 1
            if event.key == pygame.K_UP:
                backup_tetromino = deepcopy(current_tetromino)
                current_tetromino.rotate()
                if not valid_move(current_tetromino.shape, grid, (current_tetromino.x, current_tetromino.y)):
                    current_tetromino = backup_tetromino

    ghost_tetromino = deepcopy(current_tetromino)
    ghost_tetromino = place_ghost(grid, ghost_tetromino)

    draw_grid(game_screen, grid)
    draw_tetromino(game_screen, ghost_tetromino)
    draw_tetromino(game_screen, current_tetromino)


    text_score = score_font.render(f"Score: {game_score}", True, (255, 255, 255))
    text_rect = text_score.get_rect(topleft=(0, 0))

    game_screen.blit(text_score, text_rect)

    window.fill((20, 20, 20))
    draw_next_tetromino(window, next_tetromino, (20, 5))
    window.blit(game_screen, ((SCREEN_WIDTH - GAME_SCREEN_WIDTH) // 2, 0))


    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    font_game_over = pygame.font.SysFont("Comic Sans MS", 50)
    text_game_over = font_game_over.render(f"Game Over", True, (255, 0, 0))
    text_rect = text_game_over.get_rect(center=(GAME_SCREEN_WIDTH // 2, GAME_SCREEN_HEIGHT // 2))
    game_screen.blit(text_game_over, text_rect)

    clock.tick()
    pygame.display.flip()
