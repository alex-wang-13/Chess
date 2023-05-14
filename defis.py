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

# defining the values of board pieces
PAWN_WT   = 1
KNIGHT_WT = 3
BISHOP_WT = 3
ROOK_WT   = 5
QUEEN_WT  = 9
KING_WT   = 999

# defining values of doubled, blocked, and isolated pawns
DPAWNS_WT = -0.5
BPAWNS_WT = -0.5
IPAWNS_WT = -0.5

# defining value of the cardinality of board mobility (i.e. legal moves)
MOBILITY_WT = 0.1