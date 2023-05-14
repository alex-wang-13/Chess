'''
This is a board utility module.
Contains the AI functionality for the bot.
Authors:
Wang, Alex
'''

import chess
import chess.engine
import defis
import math
import sys

from os import system

'''
I/O UTILS
'''

''' Prints an explanation of UCI notation. '''
def explain_UCI() -> None:
    print(f"{defis.UCI_EXPLANATION}\n")

'''
BOARD UTILS
'''

''' Prints the result of the current board. '''
def check_result(board: chess.Board):
    result = 'in progress'
    if board.is_repetition():
        result = 'stalemate (repetition)'
    if board.is_fifty_moves():
        result = 'stalemate (fifty moves)'
    if board.is_insufficient_material():
        result = 'stalemate (insufficient material)'
    if board.is_stalemate():
        result = 'stalemate'
    if board.is_checkmate():
        result = 'checkmate'
    if result != 'in progress':
        print(f'The result is {result}.')

''' Prompts the user to type a move. A valid move is in UCI notation. '''
def get_player_move(board: chess.Board) -> chess.Move:
    while 1:
        test_move = input()
        if test_move == 'undo':
            return test_move
        else:
            try:
                test_move = chess.Move.from_uci(test_move)
                if test_move not in board.legal_moves:
                    raise chess.InvalidMoveError
                return test_move
            except chess.InvalidMoveError:
                print(f"'{test_move}' is an invalid move\n")

'''
AI UTILS
'''

''' Simple evaluation based on the weighted sum of pieces. '''
def simple_eval(board: chess.Board) -> int:
    # board: chess.Board = chess.Board()
    color: chess.Color = board.turn
    material_score: float = 0
    mobility_score: float = 0
    
    # calculate the value of the pieces
    material_score += defis.PAWN_WT * (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK)))
    material_score += defis.ROOK_WT * (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK)))
    material_score += defis.KNIGHT_WT * (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK)))
    material_score += defis.BISHOP_WT * (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK)))
    material_score += defis.QUEEN_WT * (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK)))
    material_score += defis.KING_WT * (len(board.pieces(chess.KING, chess.WHITE)) - len(board.pieces(chess.KING, chess.BLACK)))

    # calculate the mobility score TODO add the isolated + doubled pawns
    board.turn = chess.WHITE
    white_mobility = board.legal_moves.count()
    board.turn = chess.BLACK
    black_mobility = board.legal_moves.count()
    mobility_score += defis.MOBILITY_WT * (white_mobility - black_mobility)

    # aggregate the two scores
    score = (material_score + mobility_score)

    return score

# h = chess.Board("r1b1kbnr/p1pp1ppp/8/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")
# f = simple_eval(h)
# print(f)
# print(h)

''' Prompts the AI to play a move. '''
def AI_play_move(board: chess.Board):
    # perform minimax on each of the possible moves
    results = {}
    for move in board.legal_moves:
        results.update({move: ultra_alphabeta(board, 4, -math.inf, math.inf, board.turn == chess.WHITE)})
    
    # get the best move for the given color
    optimal = max(results, key=results.get) if board.turn else min(results, key=results.get)
    print(f"{results}, {optimal}")
    board.push(optimal)

''' Simple alpha-beta pruning function taken from Wikipedia. '''
def ultra_alphabeta(board: chess.Board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return simple_eval(board) # TODO improve this static eval funtcion

    if maximizing_player:
        max_eval = -sys.maxsize
        for move in board.legal_moves:
            board.push(move)
            eval = ultra_alphabeta(board, depth-1, alpha, beta, chess.BLACK)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = sys.maxsize
        for move in board.legal_moves:
            board.push(move)
            eval = ultra_alphabeta(board, depth-1, alpha, beta, chess.WHITE)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval