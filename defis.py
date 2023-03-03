'''
This is a definitions module.
Authors: 
Ghosh, Trisha
Wang, Alex
'''

from os import system

# used to clear the command window (i.e. os.system(clear_terminal))
_clear_terminal = 'clear'

# used to explain the rules of UCI chess notation
# SOURCE: https://www.dcode.fr/uci-chess-notation
_notation = 'Enter moves in UCI notation, which describes moves with the start and end coordinates of the piece (i.e. 4 characters: letter, digit, letter, digit.)'

def clear_terminal():
    system(_clear_terminal)

def explain_UCI():
    print(_notation)