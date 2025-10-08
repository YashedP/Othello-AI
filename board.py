import pygame
import copy

CELL_SIZE = 80
DIRECTIONS = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]


def draw_board(screen, board, valid_moves):
    screen.fill((0, 100, 0))  # Green board color

    # Draw grid
    for i in range(9):
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (640, i * CELL_SIZE))
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, 640))

    # Draw pieces
    for r in range(8):
        for c in range(8):
            if board[r][c] == "black":
                pygame.draw.circle(screen, (0, 0, 0),
                                   (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), 30)
            elif board[r][c] == "white":
                pygame.draw.circle(screen, (255, 255, 255),
                                   (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), 30)

    # Highlight valid moves
    for (r, c) in valid_moves:
        pygame.draw.circle(screen, (200, 200, 200),  # Yellow highlight
                           (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), 10)


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


def make_move(board, row, col, player):
    opponent = get_opponent(player)
    board[row][col] = player

    for dr, dc in DIRECTIONS:
        flips = []
        r, c = row + dr, col + dc

        while is_on_board(r, c) and board[r][c] == opponent:
            flips.append((r, c))
            r += dr
            c += dc

        if is_on_board(r, c) and board[r][c] == player:
            for fr, fc in flips:
                board[fr][fc] = player