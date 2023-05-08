'''
This is a board utility module.
Contains the AI functionality for the bot.
Authors:
Wang, Alex
'''

import asyncio
import chess
import chess.engine
import defis
import math

from os import system

simple_engine = chess.engine.SimpleEngine.popen_uci(defis.STOCKFISH)

'''
I/O UTILS
'''
# clears the terminal
def clear_terminal() -> None:
    system(defis.CLEAR_TERMINAL)

# gives an explanation of UCI notation to terminal
def explain_UCI() -> None:
    print(f"{defis.UCI_EXPLANATION}\n")

'''
BOARD UTILS
'''

def check_result(board: chess.Board):
    # prints out the current result of a board
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

def validate_move(board: chess.Board, move: chess.Move) -> chess.Move:
    #piece: chess.PieceType = board.piece_at(move.from_square).piece_type
    legal_moves = board.legal_moves
    for legal_move in legal_moves:
        if legal_move == move:
            return move
    # if the provided move is not a legal move
    return None

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

# checks if the game has ended in checkmate or stalemate
def is_game_over(board: chess.Board = None) -> bool:
    assert board is not None
    return board.is_checkmate() or board.is_stalemate()

# TODO make BASIC evaluation function
# TODO (later) make evaluation function better
def static_eval(board: chess.Board) -> float:
    eval: float = 0
    return (eval + 1) if (board.turn == chess.WHITE) else (eval - 1)


'''
AI UTILS
'''

# evaluates a board position
async def evaluate(board: chess.Board) -> float:
    # get evaluation from engine
    transport, engine = await chess.engine.popen_uci(defis.STOCKFISH)
    info = await engine.analyse(board, chess.engine.Limit(time=0.1, depth=20))

    # return evaluation
    return info["score"].relative.score()

def simple_eval(board: chess.Board):
    info = simple_engine.analyse(board, chess.engine.Limit(time=0.1, depth=20))
    # return evaluation
    return info["score"].relative.score()

# stand-in for AI function (TODO)
async def get_AI_move(board: chess.Board, engine: chess.engine) -> Node:
    assert board is not None
    result = await engine.play(board, chess.engine.Limit(time=3))
    return result.move
    # evaluation = alphabeta(node, 5, -math.inf, math.inf, True)


def play_move(board: chess.Board):

    # perform minimax
    result = ultra_alphabeta(board, 3, -math.inf, math.inf, board.turn == chess.WHITE)
    board.push(result)

def ultra_alphabeta(board: chess.Board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return simple_eval(board) # TODO redo this evaluation function based on heuristics

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = ultra_alphabeta(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = ultra_alphabeta(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def wack_alphabeta(node: chess.Board, depth, a, b, maximizingPlayer) -> float:
    print ("run")
    print(type(node))
    if depth == 0 or node.legal_moves.count() == 0:
        asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
        return asyncio.run(evaluate(node))
    if maximizingPlayer:
        value = -math.inf
        for child in node.legal_moves:
            value = max(value, wack_alphabeta(node.push(child), depth - 1, a, b, False))
            if value > b:
                break # beta cutoff
            a = max(a, value)
        return value
    else:
        value = math.inf
        for child in node.legal_moves:
            value = min(value, wack_alphabeta(node.push(child), depth - 1, a, b, True))
            if value < a:
                break # alpha cutoff
            b = min(b, value)
        return value
