import pygame
from board import draw_board, get_valid_moves, make_move

BOARD_SIZE = 8
CELL_SIZE = 80  # 640x640 window


def start_game(screen):
    # Initialize 8x8 board
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Starting Othello position
    board[3][3] = "white"
    board[3][4] = "black"
    board[4][3] = "black"
    board[4][4] = "white"

    running = True
    current_player = "black"

    while running:
        valid_moves = get_valid_moves(board, current_player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE

                # Only allow legal moves
                if (row, col) in valid_moves:
                    make_move(board, row, col, current_player)
                    # Switch player
                    current_player = "white" if current_player == "black" else "black"
                    # Skip turn if opponent has no valid moves
                    if not get_valid_moves(board, current_player):
                        current_player = "white" if current_player == "black" else "black"

        draw_board(screen, board, valid_moves)
        pygame.display.flip()