from copy import deepcopy
import pygame
import util.constants as constants
import util.Tetromino as Tetromino

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
game_screen = pygame.Surface((constants.GAME_SCREEN_WIDTH, constants.GAME_SCREEN_HEIGHT))


score_font = pygame.font.SysFont('Arial', 36)

def valid_move(shape, grid, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell != 0:
                if x + off_x < 0 or x + off_x >= constants.GRID_WIDTH or y + off_y >= constants.GRID_HEIGHT:
                    return False
                if grid[y + off_y][x + off_x] != 0:
                    return False
    return True

def draw_grid(surface, grid):
    for y in range(constants.GRID_HEIGHT):
        for x in range(constants.GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(surface, grid[y][x], (x * constants.BLOCK_SIZE, y * constants.BLOCK_SIZE,
                                                       constants.BLOCK_SIZE, constants.BLOCK_SIZE))

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)] # 111101 - keep it; 111111 - discard it
    lines_removed = constants.GRID_HEIGHT - len(new_grid)
    new_grid = [[0 for _ in range(constants.GRID_WIDTH)] for _ in range(lines_removed)] + new_grid
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
                                 ((x_loc + x) * constants.BLOCK_SIZE, (y_loc + y) * constants.BLOCK_SIZE,
                                  constants.BLOCK_SIZE,
                                  constants.BLOCK_SIZE))

def split(text):
    separator_idx = text.find(':')
    return text[:separator_idx], text[separator_idx+1:]


grid = [[0 for _ in range(constants.GRID_WIDTH)] for _ in range(constants.GRID_HEIGHT)]

running = True
current_tetromino = Tetromino.Tetromino()
next_tetromino = Tetromino.Tetromino(current_tetromino.shape)
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

DIFF_LEVELS = {
    "EASY": {
        "speed": [500, 500, 400, 350]
    },
    "MEDIUM": {
        "speed": [500, 400, 300, 200],
        "show_hint": False
    },
    "HARD": {
        "speed": [300, 300, 200, 200],
        "bonus_tetrominos": [
            [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        ]
    }
}

diff_level = "MEDIUM"

# set game speed
diff_settings = DIFF_LEVELS[diff_level]

# set bonus tetrominos
if "bonus_tetrominos" in DIFF_LEVELS[diff_level].keys():
    for tetromino in DIFF_LEVELS[diff_level]["bonus_tetrominos"]:
        Tetromino.Tetromino.tetrominoes.append(tetromino)

# set hint
show_hint = True
if "show_hint" in DIFF_LEVELS[diff_level].keys() and DIFF_LEVELS[diff_level]["show_hint"] == False:
    show_hint = False

game_score = 0

while running:
    game_screen.fill(constants.BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    if game_score < 1000:
        fall_speed = diff_settings["speed"][0]
    elif 1000 <= game_score < 2000:
        fall_speed = diff_settings["speed"][1]
    elif 2000 <= game_score < 3000:
        fall_speed = diff_settings["speed"][2]
    else:
        fall_speed = diff_settings["speed"][3]

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
            next_tetromino = Tetromino.Tetromino(current_tetromino.shape)
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
    Tetromino.Tetromino.draw_tetromino(game_screen, ghost_tetromino)
    Tetromino.Tetromino.draw_tetromino(game_screen, current_tetromino)

    text_score = score_font.render(f"Score: {game_score}", True, (255, 255, 255))
    text_rect = text_score.get_rect(topleft=(0, 0))

    game_screen.blit(text_score, text_rect)

    window.fill((20, 20, 20))
    if show_hint:
        draw_next_tetromino(window, next_tetromino, (20, 5))
    window.blit(game_screen, ((constants.SCREEN_WIDTH - constants.GAME_SCREEN_WIDTH) // 2, 0))

    pygame.display.flip()


lines = []
places = []

player_name = "PLAYER"
SCORE_ENTER = True
while SCORE_ENTER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    window.fill((20, 20, 20))
    window.blit(game_screen, ((constants.SCREEN_WIDTH - constants.GAME_SCREEN_WIDTH) // 2, 0))

    font_game_over = pygame.font.SysFont("Comic Sans MS", 50)
    font_player = pygame.font.SysFont("Comic Sans MS", 30)

    text_game_over = font_game_over.render(f"Game Over", True, (255, 0, 0))
    text_rect = text_game_over.get_rect(center=(constants.GAME_SCREEN_WIDTH // 2, constants.GAME_SCREEN_HEIGHT // 2))
    window.blit(text_game_over, text_rect)

    text_player = font_player.render(f"Your name:", True, (255, 255, 255))
    text_rect = text_game_over.get_rect(center=(constants.GAME_SCREEN_WIDTH // 2, constants.GAME_SCREEN_HEIGHT // 2 + 75))
    window.blit(text_player, text_rect)

    text_player = font_player.render(f"{player_name}", True, (255, 255, 255))
    text_rect = text_game_over.get_rect(center=(constants.GAME_SCREEN_WIDTH // 2, constants.GAME_SCREEN_HEIGHT // 2 + 150))
    window.blit(text_player, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            if event.key == pygame.K_RETURN:
                with open("leaderboard.txt", "a") as file:
                    file.write(f"{player_name}:{game_score}\n")
                with open("leaderboard.txt", "r") as file:
                    lines = file.readlines()
                    lines = [line[:-1] if line.endswith('\n') else line for line in lines]
                    lines = [split(line) for line in lines]
                    lines = sorted(lines, key=lambda data: int(data[1]), reverse=True)
                    places = [1] * len(lines)
                    for i in range(1, len(lines)):
                        if lines[i][1] == lines[i-1][1]:
                            places[i] = places[i-1]
                        else:
                            places[i] = i + 1
                    for i, line in enumerate(lines):
                        print(f"{places[i]}. Player name: {line[0]}, scored {line[1]} points")
                SCORE_ENTER = False
                print("Score enter", SCORE_ENTER)
            if pygame.K_a <= event.key <= pygame.K_z:
                player_name = player_name + chr(event.key).upper()

    clock.tick()
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    window.fill((20, 20, 20))
    window.blit(game_screen, ((constants.SCREEN_WIDTH - constants.GAME_SCREEN_WIDTH) // 2, 0))

    font_game_over = pygame.font.SysFont("Comic Sans MS", 50)
    font_player = pygame.font.SysFont("Comic Sans MS", 30)

    text_game_over = font_game_over.render(f"Leaderboard", True, (255, 0, 0))
    text_rect = text_game_over.get_rect(center=(constants.GAME_SCREEN_WIDTH // 2, constants.GAME_SCREEN_HEIGHT // 2))
    window.blit(text_game_over, text_rect)

    for i in range(3):
        text_player = font_player.render(f"{places[i]}. {lines[i][0]}: {lines[i][1]}", True, (255, 255, 255))
        text_rect = text_game_over.get_rect(center=(
            constants.GAME_SCREEN_WIDTH // 2, constants.GAME_SCREEN_HEIGHT // 2 + 75 + 30 * i))
        window.blit(text_player, text_rect)

    index = 0
    for i, line in enumerate(lines):
        score = int(line[1])
        if game_score == score:
            index = i
            break

    if index >= 3:
        text_player = font_player.render(f"{places[index]}. {lines[index][0]}: {lines[index][1]}", True, (255, 255, 255))
        text_rect = text_game_over.get_rect(center=(constants.GAME_SCREEN_WIDTH // 2, constants.GAME_SCREEN_HEIGHT // 2 + 210))
        window.blit(text_player, text_rect)

    clock.tick()
    pygame.display.flip()
