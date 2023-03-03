'''
This is a chess program.
Authors: 
Ghosh, Trisha
Wang, Alex
'''

import chess
import defis # TODO resolve this

if __name__ == '__main__':

    player = True; # TODO player = 1 => white's turn; = 0 => black's turn
    board = chess.Board()

    # TODO how do you access these functions defined in the definitions module? (see above in line 2)
    # clear_terminal()
    # explain_UCI()

    while 1:
        # try to play a move
        # TODO check for valid move
        # TODO check that the correct player is making a move (black cannot move a white piece)
        # TODO check for valid en passant + castling
        # TODO check if game is over (i.e. from repetition, 50-move, dead position, etc.)
        try:
            test_move = chess.Move.from_uci(input())
            board.push(test_move)
        except chess.InvalidMoveError:
            print('Invalid Move, Try Again')