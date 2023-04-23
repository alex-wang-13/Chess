'''
This is a board utility module.
Contains the AI functionality for the bot.
Authors:
Ghosh, Trisha
Wang, Alex
'''

import chess
import chess.engine
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

# evaluates a board position
async def evaluate(board: chess.Board, engine: chess.engine.UciProtocol) -> float:
    # get evaluation from engine
    info = await engine.analyse(board, chess.engine.Limit(time=0.1, depth=20))

    return info["score"]


# stand-in for AI function (TODO)
async def get_AI_move(board: chess.Board, engine: chess.engine) -> Node:
    assert board is not None
    result = await engine.play(board, chess.engine.Limit(time=3))
    return result.move
    # evaluation = alphabeta(node, 5, -math.inf, math.inf, True)


async def play_game(player_is_white: bool):
    
    # Initialize the game variables.
    playerTurn = player_is_white
    board = chess.Board()
    _, engine = await chess.engine.popen_uci(defis.STOCKFISH)
    depth = 20

    # Print initial board state.
    explain_UCI()
    print(f"{board}\n")

    # Start game loop.
    if playerTurn:
        # Get the player's move. Note: 'undo' returns to the player's last move.
        move = get_player_move()
        if move == "undo":
            # Undo last player and AI move.
            board.pop()
            board.pop()
        else:
            # Push the move and toggle playerTurn.
            board.push(move)
            playerTurn = not playerTurn
    else:
        # Get the AI's move and push it.
        board.push(get_AI_move(board, engine, depth))
        playerTurn = not playerTurn
        









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
    