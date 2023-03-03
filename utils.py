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
def clear_terminal():
    system(defis.CLEAR_TERMINAL)

# gives an explanation of UCI notation to terminal
def explain_UCI():
    print(defis.UCI_EXPLANATION)

'''
BOARD UTILS
'''
# checks if the game has ended in checkmate or stalemate
def is_game_over(board: chess.Board = None):
    assert board is not None
    return board.is_checkmate() or board.is_stalemate()

'''
AI UTILS
'''

# stand-in for AI function (TODO)
def AI_move(board: chess.Board = None):
    assert board is not None
    return 'test'