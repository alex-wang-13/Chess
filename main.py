'''
This is a chess program.
Authors: 
Wang, Alex
'''

import chess
import chess.engine
import utils

''' This is a bad chess game. '''
if __name__ == "__main__":
    arg = "-"
    player_is_white = None

    # Choose play mode.
    while arg not in ["b", "w"]:
        arg = input("Play as black or white? (b/w) ")
        if arg == "w":
            player_is_white = True
        elif arg == "b":
            player_is_white = False
        if arg not in ["b", "w"]:
            print(f"Enter b or w. You entered {arg}.")
    
    # Initialize the game variables.
    player_turn = player_is_white
    board = chess.Board()

    # Print initial board state.
    utils.explain_UCI()
    print(f"{board}\n\n----------------\n")

    # Start game loop.
    while not board.is_game_over():
        if player_turn:
            # Get the player's move. Note: 'undo' returns to the player's last move.
            print("Play move...\n")
            move = utils.get_player_move(board)
            if move == "undo":
                # Undo last player and AI move.
                board.pop()
                board.pop()
                print(f"{board}\n")
            else:
                # Push the move and toggle player_turn.
                try:
                    board.push(move)
                    player_turn = not player_turn
                    print(f"{board}\n")
                except chess.InvalidMoveError:
                    print("Invalid Move, Try Again - Should Not Reach Here")
        else:
            print("AI is thinking...\n")
            # Get the AI's move and push it.
            utils.play_move(board)
            player_turn = not player_turn
            print(f"{board}\n")
            print("AI played move...\n")
    
    # Game Over. Print result.
    utils.check_result(board)