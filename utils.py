'''
This is a board utility module.
Contains the AI functionality for the bot.
Authors:
Ghosh, Trisha
Wang, Alex
'''

import chess
import defis

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
        self.evaluation: int = static_eval(board)
        self.children: list[Node] = []

    # adds a child Node to this Node
    def add_child(self, child_node) -> None:
        self.children.append(child_node)
    
    # checks if there are no children for this Node
    def is_terminal(self) -> bool:
        return self.children.__len__ == 0

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

# TODO FINISH THIS FUNCTION
def alphabeta(node, depth, α, β, maximizingPlayer) -> Node:
    if depth == 0 or node.is_terminal():
        return None # placeholder
    return None # placeholder