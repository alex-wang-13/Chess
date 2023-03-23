'''
This is a board utility module.
Contains the AI functionality for the bot.
Authors:
Ghosh, Trisha
Wang, Alex
'''

import chess
import defis
import math

from os import system

'''
I/O UTILS
'''
# clears the terminal
def clear_terminal() -> None:
    system(defis.CLEAR_TERMINAL)

# gives an explanation of UCI notation to terminal
def explain_UCI() -> None:
    print(defis.UCI_EXPLANATION)

'''
BOARD UTILS
'''

def validate_move(board: chess.Board, move: chess.Move) -> chess.Move:
    #piece: chess.PieceType = board.piece_at(move.from_square).piece_type
    legal_moves = board.legal_moves
    for legal_move in legal_moves:
        if legal_move == move:
            return move
    # if the provided move is not a legal move
    return None

def get_move(board: chess.Board) -> chess.Move:
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

# represents a node on the minimax search tree
class Node:

    def __init__(self, board: chess.Board):
        self.board: chess.Board = board
        self.evaluation: float = static_eval(board)
        self.children: list[Node] = []

    # adds a child Node to this Node
    def add_child(self, child_node) -> None:
        self.children.append(child_node)
    
    # checks if there are no children for this Node
    def is_terminal(self) -> bool:
        return self.children.__len__ == 0
    
    # gets the evaluation for this Node
    def eval(self) -> float:
        return self.evaluation

# creates a Node based on a given board
def create_node(board: chess.Board = None) -> Node:
    return Node(board)

'''
AI UTILS
'''

# stand-in for AI function (TODO)
def AI_move(board: chess.Board = None, depth: int = 5) -> Node:
    assert board is not None
    node = create_node(board)
    alphabeta()

# alpha-beta function (shamelessly stolen from wikipedia)
# initial call: alphabeta(origin, depth, -inf, inf, True)
def alphabeta(node, depth, a, b, maximizingPlayer) -> float:
    if depth == 0 or node.is_terminal():
        return node.eval() # return the heuristic evaluation
    if maximizingPlayer:
        value = -math.inf
        for child in node.children:
            value = max(value, alphabeta(child, depth - 1, a, b, False))
            if value > b:
                break # beta cutoff
            a = max(a, value)
        return value
    else:
        value = math.inf
        for child in node.children:
            value = min(value, alphabeta(child, depth - 1, a, b, True))
            if value < a:
                break # alpha cutoff
            b = min(b, value)
        return value

# TODO determine if fail-soft pruning is worth it
def soft_alphabeta(node, depth, a, b, maximizingPlayer) -> int:
    if depth == 0 or node.is_terminal():
        return node.eval()
    