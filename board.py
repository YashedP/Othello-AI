import pygame

CELL_SIZE = 80
BOARD_OFFSET_Y = 40  # leave space for top title bar
BOTTOM_BAR_HEIGHT = 40
DIRECTIONS = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]


def draw_board(screen, board, valid_moves, current_player, time_remaining):
    screen.fill((0, 100, 0))

    # --- Draw Top Bar ---
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 640, BOARD_OFFSET_Y))
    font = pygame.font.Font(None, 36)
    title_text = font.render("Othello", True, (0, 0, 0))
    screen.blit(title_text, (640 // 2 - title_text.get_width() // 2, 5))

    # --- Draw Bottom Bar ---
    pygame.draw.rect(screen, (255, 255, 255), (0, 680, 640, BOTTOM_BAR_HEIGHT))
    info_font = pygame.font.Font(None, 28)
    turn_text = info_font.render(f"Turn: {current_player.capitalize()}", True, (0, 0, 0))
    time_text = info_font.render(f"Timer: {int(time_remaining)}s", True, (0, 0, 0))
    screen.blit(turn_text, (10, 685))
    screen.blit(time_text, (500, 685))

    # --- Draw Grid ---
    for i in range(9):
        pygame.draw.line(screen, (0, 0, 0), (0, BOARD_OFFSET_Y + i * CELL_SIZE), (640, BOARD_OFFSET_Y + i * CELL_SIZE))
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, BOARD_OFFSET_Y), (i * CELL_SIZE, 680))

    # --- Draw Pieces ---
    for r in range(8):
        for c in range(8):
            if board[r][c] == "black":
                pygame.draw.circle(screen, (0, 0, 0),
                                   (c * CELL_SIZE + CELL_SIZE // 2, BOARD_OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2), 30)
            elif board[r][c] == "white":
                pygame.draw.circle(screen, (255, 255, 255),
                                   (c * CELL_SIZE + CELL_SIZE // 2, BOARD_OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2), 30)

    # --- Highlight Valid Moves ---
    for (r, c) in valid_moves:
        pygame.draw.circle(screen, (200, 200, 200),
                           (c * CELL_SIZE + CELL_SIZE // 2, BOARD_OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2), 10)


def get_score(board):
    black_score = 0
    white_score = 0
    for row in board:
        for cell in row:
            if cell == "black":
                black_score += 1
            elif cell == "white":
                white_score += 1
    return black_score, white_score


def get_opponent(player):
    return "white" if player == "black" else "black"


def is_on_board(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def get_valid_moves(board, player):
    valid_moves = []
    opponent = get_opponent(player)

    for r in range(8):
        for c in range(8):
            if board[r][c] is not None:
                continue

            flips = []
            for dr, dc in DIRECTIONS:
                row, col = r + dr, c + dc
                temp_flips = []

                while is_on_board(row, col) and board[row][col] == opponent:
                    temp_flips.append((row, col))
                    row += dr
                    col += dc

                if is_on_board(row, col) and board[row][col] == player and len(temp_flips) > 0:
                    flips.extend(temp_flips)

            if len(flips) > 0:
                valid_moves.append((r, c))

    return valid_moves


def make_move(board, row, col, current_player):
    opponent = get_opponent(current_player)
    board[row][col] = current_player

    for dr, dc in DIRECTIONS:
        flips = []
        r, c = row + dr, col + dc

        while is_on_board(r, c) and board[r][c] == opponent:
            flips.append((r, c))
            r += dr
            c += dc

        if is_on_board(r, c) and board[r][c] == current_player:
            for fr, fc in flips:
                board[fr][fc] = current_player