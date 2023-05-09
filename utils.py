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
                continue

'''
AI UTILS
'''

''' Simple evaluation based on the weighted sum of pieces. '''
def simple_eval(board: chess.Board) -> int:
    board: chess.Board = chess.Board()
    color: chess.Color = board.turn
    score: int = 0
    
    # add pieces
    score += str(board.pieces(chess.PAWN, color)).count("1")
    score += str(board.pieces(chess.ROOK, color)).count("1") * 5
    score += str(board.pieces(chess.KNIGHT, color)).count("1") * 3
    score += str(board.pieces(chess.BISHOP, color)).count("1") * 3
    score += str(board.pieces(chess.QUEEN, color)).count("1") * 9
    score += str(board.pieces(chess.KING, color)).count("1") * 999

    # return score and modify based on player color
    return score if color else -score

''' Prompts the AI to play a move. '''
def AI_play_move(board: chess.Board):
    # perform minimax on each of the possible moves
    results = {}
    for move in board.legal_moves:
        results.update({move: ultra_alphabeta(board, 3, -math.inf, math.inf, board.turn == chess.WHITE)})
    
    # get the best move for the given color
    optimal = max(results, key=results.get) if board.turn else min(results, key=results.get)
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