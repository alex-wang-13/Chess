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

''' Checks that a current move is valid. '''
def validate_move(board: chess.Board, move: chess.Move) -> chess.Move:
    legal_moves = board.legal_moves
    for legal_move in legal_moves:
        if legal_move == move:
            return move
    # if the provided move is not a legal move
    return None

''' Prompts the user to type a move. A valid move is in UCI notation. '''
def get_player_move(board: chess.Board) -> chess.Move:
    while 1:
        user_input = input()
        if user_input == 'undo':
            return user_input
        else:
            test_move = chess.Move.from_uci(user_input)
            move = validate_move(board, test_move)
            if move != None:
                return move

'''
AI UTILS
'''

''' Simple evaluation based on the number of pieces of the relevant color. '''
def simple_eval(board: chess.Board) -> int:
    board: chess.Board = chess.Board()
    color: chess.Color = board.turn
    score: int = 0
    
    # add pieces
    score += str(board.pieces(chess.PAWN, color)).count("1")
    score += str(board.pieces(chess.ROOK, color)).count("1")
    score += str(board.pieces(chess.KNIGHT, color)).count("1")
    score += str(board.pieces(chess.BISHOP, color)).count("1")
    score += str(board.pieces(chess.QUEEN, color)).count("1")

    # return score and modify based on player color
    return score if color else -score

''' Prompts the AI to play a move. '''
def play_move(board: chess.Board):
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