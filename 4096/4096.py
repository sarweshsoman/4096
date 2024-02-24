import pygame
import random

# Constants
BOARD_SIZE = 4
FPS = 60

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("4096 Game")  # Updated game name
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (139, 125, 107),
    8192: (160, 82, 45)
}

# Game variables
board_values = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
spawn_new = True
init_count = 0
direction = ''
game_over = False

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            pygame.draw.rect(screen, TILE_COLORS[board_values[row][col]], (col * 100, row * 100, 100, 100), border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), (col * 100, row * 100, 100, 100), 2, border_radius=15)  # Bold black lines

def draw_pieces(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = board[row][col]
            if value != 0:
                font = pygame.font.Font(None, 36)
                color = (0, 0, 0) if value <= 4 else (255, 255, 255)  # Adjust text color for visibility
                text = font.render(str(value), True, color)
                text_rect = text.get_rect(center=(col * 100 + 50, row * 100 + 50))
                screen.blit(text, text_rect)

def new_piece(board):
    empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        value = 2 if random.random() < 0.9 else 4  # 90% chance for 2, 10% chance for 4
        board[row][col] = value

def merge_tiles(board, row, col, new_row, new_col, merged):
    # Merge tiles by summing their values, only if not already merged in this move
    if not merged[new_row][new_col]:
        board[new_row][new_col] += board[row][col]
        board[row][col] = 0
        merged[new_row][new_col] = True

def slide_tiles(board, direction):
    # Implement tile sliding and merging similar to 2048
    changed = False  # Flag to check if the board has changed

    if direction == 'UP':
        for col in range(BOARD_SIZE):
            merged = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            for row in range(1, BOARD_SIZE):
                if board[row][col] != 0:
                    for i in range(row, 0, -1):
                        if board[i - 1][col] == 0:
                            board[i - 1][col], board[i][col] = board[i][col], 0
                            changed = True
                        elif board[i - 1][col] == board[i][col]:
                            merge_tiles(board, i, col, i - 1, col, merged)
                            changed = True
                            break
                        else:
                            break

    elif direction == 'DOWN':
        for col in range(BOARD_SIZE):
            merged = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            for row in range(BOARD_SIZE - 2, -1, -1):
                if board[row][col] != 0:
                    for i in range(row, BOARD_SIZE - 1):
                        if board[i + 1][col] == 0:
                            board[i + 1][col], board[i][col] = board[i][col], 0
                            changed = True
                        elif board[i + 1][col] == board[i][col]:
                            merge_tiles(board, i, col, i + 1, col, merged)
                            changed = True
                            break
                        else:
                            break

    elif direction == 'LEFT':
        for row in range(BOARD_SIZE):
            merged = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            for col in range(1, BOARD_SIZE):
                if board[row][col] != 0:
                    for i in range(col, 0, -1):
                        if board[row][i - 1] == 0:
                            board[row][i - 1], board[row][i] = board[row][i], 0
                            changed = True
                        elif board[row][i - 1] == board[row][i]:
                            merge_tiles(board, row, i, row, i - 1, merged)
                            changed = True
                            break
                        else:
                            break

    elif direction == 'RIGHT':
        for row in range(BOARD_SIZE):
            merged = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            for col in range(BOARD_SIZE - 2, -1, -1):
                if board[row][col] != 0:
                    for i in range(col, BOARD_SIZE - 1):
                        if board[row][i + 1] == 0:
                            board[row][i + 1], board[row][i] = board[row][i], 0
                            changed = True
                        elif board[row][i + 1] == board[row][i]:
                            merge_tiles(board, row, i, row, i + 1, merged)
                            changed = True
                            break
                        else:
                            break

    return changed

def is_game_over(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return False  # Game is not over, there is an empty cell

            if col < BOARD_SIZE - 1 and board[row][col] == board[row][col + 1]:
                return False  # Game is not over, there is a merge possibility horizontally

            if row < BOARD_SIZE - 1 and board[row][col] == board[row + 1][col]:
                return False  # Game is not over, there is a merge possibility vertically

            if board[row][col] == 4096:  # Winning condition is 4096
                return True

    return True  # If no empty cells and no merge possibilities, the game is over

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(GRAY)
    draw_board()
    draw_pieces(board_values)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_n:
                # New game functionality
                board_values = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                spawn_new = True
                init_count = 0
                direction = ''
                game_over = False

    if spawn_new or init_count < 2:
        new_piece(board_values)
        spawn_new = False
        init_count += 1

    if direction != '':
        changed = slide_tiles(board_values, direction)
        direction = ''
        spawn_new = changed  # Only spawn new tiles if the board has changed

    if is_game_over(board_values):
        # Game over logic
        game_over = True
        # Additional game over actions can be added here

    if game_over:
        # Display game over screen
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Press Enter to restart.", True, WHITE)
        text_rect = text.get_rect(center=(200, 250))
        screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Restart the game
            board_values = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            spawn_new = True
            init_count = 0
            direction = ''
            game_over = False

    pygame.display.flip()

pygame.quit()
