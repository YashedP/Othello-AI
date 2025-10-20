import pygame
import asyncio
import copy
import time
from board import draw_board, get_valid_moves, make_move

BOARD_SIZE = 8
CELL_SIZE = 80
BOARD_OFFSET_Y = 40


async def dummy_ai_move(board, valid_moves):
    """Simulate AI thinking asynchronously."""
    await asyncio.sleep(2)
    if valid_moves:
        return valid_moves[0]
    return None


async def run_ai(board, valid_moves, timeout=30):
    """Run the AI with a time limit (async-safe)."""
    try:
        move = await asyncio.wait_for(dummy_ai_move(board, valid_moves), timeout)
        return move
    except asyncio.TimeoutError:
        print("AI took too long! Choosing fallback move.")
        return valid_moves[0] if valid_moves else None


async def start_game(screen, player_color="black"):
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3] = "white"
    board[3][4] = "black"
    board[4][3] = "black"
    board[4][4] = "white"

    current_player = "black"  # always start black
    ai_color = "white" if player_color == "black" else "black"

    previous_states = []

    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()
    running = True

    ai_task = None
    ai_start_time = None
    ai_move = None

    # --- Button Positions ---
    back_rect = pygame.Rect(10, 5, 80, 30)
    undo_rect = pygame.Rect(280, 685, 80, 30)  # Bottom center

    # If player chose white, AI moves first
    if player_color == "white":
        ai_start_time = time.time()
        ai_task = asyncio.create_task(
            run_ai(copy.deepcopy(board), get_valid_moves(board, ai_color))
        )

    while running:
        dt = clock.tick(60) / 1000.0
        screen.fill((0, 128, 0))

        valid_moves = get_valid_moves(board, current_player)
        time_remaining = 0

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MENU"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Back button
                if back_rect.collidepoint(x, y):
                    return "MENU"

                # Undo button logic (same as before)
                if undo_rect.collidepoint(x, y) and previous_states:
                    # Cancel AI task if it exists
                    if ai_task is not None and not ai_task.done():
                        ai_task.cancel()
                        try:
                            await ai_task
                        except asyncio.CancelledError:
                            pass
                        ai_task = None
                        ai_start_time = None

                    board, current_player = previous_states.pop()

                    # If undo restores AI's turn, trigger it
                    if current_player == ai_color:
                        ai_start_time = time.time()
                        ai_task = asyncio.create_task(
                            run_ai(copy.deepcopy(board), get_valid_moves(board, ai_color))
                        )
                    continue

                # Player move
                if current_player == player_color and ai_task is None and BOARD_OFFSET_Y <= y <= 680:
                    row, col = (y - BOARD_OFFSET_Y) // CELL_SIZE, x // CELL_SIZE
                    if (row, col) in valid_moves:
                        previous_states.append((copy.deepcopy(board), current_player))
                        make_move(board, row, col, current_player)
                        current_player = ai_color

                        # Start AI move
                        ai_start_time = time.time()
                        ai_task = asyncio.create_task(
                            run_ai(copy.deepcopy(board), get_valid_moves(board, ai_color))
                        )

        # --- Handle AI move ---
        if ai_task is not None:
            elapsed = time.time() - ai_start_time
            time_remaining = max(0, 30 - elapsed)

            if ai_task.done():
                ai_move = ai_task.result()
                if ai_move:
                    previous_states.append((copy.deepcopy(board), ai_color))
                    make_move(board, ai_move[0], ai_move[1], ai_color)
                current_player = player_color
                ai_task = None

        # --- Draw Board & UI ---
        draw_board(screen, board, valid_moves, current_player, time_remaining)

        # Get mouse position
        mx, my = pygame.mouse.get_pos()

        # --- Draw Buttons ---
        # --- Draw Back button ---
        back_color = (225, 225, 225)
        back_hover_color = (200, 200, 200)
        color = back_hover_color if back_rect.collidepoint(mx, my) else back_color
        pygame.draw.rect(screen, color, back_rect, border_radius=5)
        back_text = font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # --- Draw Undo button ---
        undo_color = (0, 100, 0)
        undo_hover_color = (0, 140, 0)
        color = undo_hover_color if undo_rect.collidepoint(mx, my) else undo_color
        pygame.draw.rect(screen, color, undo_rect, border_radius=5)
        undo_text = font.render("Undo", True, (255, 255, 255))
        undo_text_rect = undo_text.get_rect(center=undo_rect.center)
        screen.blit(undo_text, undo_text_rect)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()