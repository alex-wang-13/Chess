'''
This is a definitions module.
Authors: 
Wang, Alex
'''

# used to clear the command window (i.e. os.system(clear_terminal))
CLEAR_TERMINAL = 'clear'

# used as a delimiter between boards printed to terminal
BOARD_BREAK = '- - - - - - - -'

# used to explain the rules of UCI chess notation
# SOURCE: https://www.dcode.fr/uci-chess-notation
UCI_EXPLANATION = 'Enter moves in UCI notation, which describes moves with the start and end coordinates of the piece (i.e. 4 characters: letter, digit, letter, digit.). To undo a move type "undo."'

# evaluation engine
STOCKFISH = r"C:\Users\15043\Spring2023Project\Chess-Bot\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"