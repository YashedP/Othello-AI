import copy
import math
import asyncio
import time
from board import make_move, get_valid_moves, get_score

MAX_DEPTH = 4  # Technically 5 ply since it stops at 0


async def start_minimax_async(board, player_color, ai_color, time_limit=30):
    start_time = time.time()
    score, move, _ = await minimax_async(board, MAX_DEPTH, True, player_color, ai_color, start_time, time_limit)
    return score, move


node_counter = 0  # global or passed in context


async def minimax_async(board, depth, maximizing_player, player_color, ai_color, start_time, time_limit=30, alpha=-math.inf, beta=math.inf):
    global node_counter
    node_counter += 1
    if node_counter % 1000 == 0:  # yield every 500 nodes
        await asyncio.sleep(0)

    if time.time() - start_time > time_limit:
        return 0, None, True  # timed out

    # Recursive base case
    valid_moves = get_valid_moves(board, ai_color if maximizing_player else player_color)
    if depth == 0 or not valid_moves:
        return evaluate_board(board, ai_color, player_color), None, False

    best_move = None
    timed_out = False

    # --- Alpha-Beta pruning ---
    if maximizing_player:
        max_eval = -math.inf
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], ai_color)
            eval_score, _, child_timed_out = await minimax_async(new_board, depth-1, False, player_color, ai_color, start_time, time_limit, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
            if child_timed_out:
                timed_out = True
                break

        return max_eval, best_move, timed_out
    else:
        min_eval = math.inf
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], player_color)
            await asyncio.sleep(0)
            eval_score, _, child_timed_out = await minimax_async(new_board, depth-1, True, player_color, ai_color, start_time, time_limit, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
            if child_timed_out:
                timed_out = True
                break

        return min_eval, best_move, timed_out


# Corner positions
CORNERS = [(0, 0), (0, 7), (7, 0), (7, 7)]
# Positions directly adjacent to corners
NEARBY_OFFSETS = [(0,1),(1,0),(1,1), (0,-1),(-1,0),(-1,-1), (1,-1),(-1,1)]


def evaluate_board(board, ai_color, player_color):

    num_discs = sum(1 for row in board for cell in row if cell is not None)
    phase = num_discs / 64.0  # 0 = start, 1 = end

    # Coefficients
    PIECE_DIFFERENCE_WEIGHT = 0             # Piece difference weight
    MOBILITY_WEIGHT = 0                     # Mobility weight
    CORNER_CONTROL_WEIGHT = 0               # Corner control weight
    EDGE_CONTROL_WEIGHT = 0                 # Edge control weight
    NEARBY_CORNERS_PENALTY_WEIGHT = 0       # Penalty for pieces near corners

    # --- Game phase detection ---
    if phase < 0.4:
        # Opening: prioritize mobility and corner potential
        PIECE_DIFFERENCE_WEIGHT, MOBILITY_WEIGHT, CORNER_CONTROL_WEIGHT, EDGE_CONTROL_WEIGHT, NEARBY_CORNERS_PENALTY_WEIGHT = 5, 30, 60, 10, 10
    elif phase < 0.8:
        # Mid-game: balance mobility and edge control
        PIECE_DIFFERENCE_WEIGHT, MOBILITY_WEIGHT, CORNER_CONTROL_WEIGHT, EDGE_CONTROL_WEIGHT, NEARBY_CORNERS_PENALTY_WEIGHT = 10, 15, 80, 20, 5
    else:
        # Endgame: raw piece advantage and corner control matters
        PIECE_DIFFERENCE_WEIGHT, MOBILITY_WEIGHT, CORNER_CONTROL_WEIGHT, EDGE_CONTROL_WEIGHT, NEARBY_CORNERS_PENALTY_WEIGHT = 40, 5, 100, 20, 2

    # --- Piece difference ---
    black_score, white_score = get_score(board)
    if ai_color == "black":
        piece_diff = black_score - white_score
    else:
        piece_diff = white_score - black_score

    # --- Mobility ---
    ai_moves = len(get_valid_moves(board, ai_color))
    player_moves = len(get_valid_moves(board, player_color))
    mobility = ai_moves - player_moves

    # --- Corner control ---
    player_corners = sum(1 for r, c in CORNERS if board[r][c] == ai_color)
    opp_corners = sum(1 for r, c in CORNERS if board[r][c] == player_color)
    corner_control = player_corners - opp_corners

    # --- Edge control ---
    ai_edges = 0
    player_edges = 0

    # Top and bottom rows (excluding corners)
    for j in range(1, 7):
        if board[0][j] == ai_color:
            ai_edges += 1
        elif board[0][j] == player_color:
            player_edges += 1
        if board[7][j] == ai_color:
            ai_edges += 1
        elif board[7][j] == player_color:
            player_edges += 1

    # Left and right columns (excluding corners)
    for i in range(1, 7):
        if board[i][0] == ai_color:
            ai_edges += 1
        elif board[i][0] == player_color:
            player_edges += 1
        if board[i][7] == ai_color:
            ai_edges += 1
        elif board[i][7] == player_color:
            player_edges += 1

    edge_control = ai_edges - player_edges

    # --- Nearby corners penalty ---
    ai_near = 0
    player_near = 0
    for (cRow, cCol) in CORNERS:
        corner_owner = board[cRow][cCol]
        for dRow, dCol in NEARBY_OFFSETS:
            nRow, nCol = cRow + dRow, cCol + dCol
            if 0 <= nRow < 8 and 0 <= nCol < 8:
                cell = board[nRow][nCol]
                # Only penalize nearby squares if the corner is NOT owned by that player
                if cell == ai_color and corner_owner != ai_color:
                    ai_near += 1
                elif cell == player_color and corner_owner != player_color:
                    player_near += 1

    nearby_corners = ai_near - player_near

    # --- Final evaluation ---
    score = (PIECE_DIFFERENCE_WEIGHT * piece_diff +
             MOBILITY_WEIGHT * mobility +
             CORNER_CONTROL_WEIGHT * corner_control +
             EDGE_CONTROL_WEIGHT * edge_control -
             NEARBY_CORNERS_PENALTY_WEIGHT * nearby_corners)

    return score
