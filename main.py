'''
This is a chess program.
Authors: 
Ghosh, Trisha
Wang, Alex
'''

import asyncio
import chess
import chess.engine
import defis
import utils    

async def get_AI_move(board):
    transport, engine = await chess.engine.popen_uci(defis.STOCKFISH)

    result = await engine.play(board, chess.engine.Limit(time=3))
    board.push(result.move)

# asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
# asyncio.run(evaluate(board))

if __name__ == "__main__":
    arg = "-"
    player_is_white = None

    # Choose play mode.
    while arg not in ["b", "w", "a"]:
        arg = input("Play as black or white? (b/w) ")
        if arg == "w":
            player_is_white = True
        elif arg == "b":
            player_is_white = False
        if arg not in ["b", "w", "a"]:
            print(f"Enter b or w. You entered {arg}.")
    
    # Play the game.
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    
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
            asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
            asyncio.run(get_AI_move(board))
            player_turn = not player_turn
            print(f"{board}\n")
            print("AI played move...\n")
    
    # Game Over. Print result.
    utils.check_result(board)





# START
if 0:

    # Explaining the rules.
    # useless: Todo but not urgent: fix this -> utils.clear_terminal()
    utils.explain_UCI()

    # TODO create functionality for AI to play as white
    player = 1 # player = 1 => white's turn; = 0 => black's turn
    board = chess.Board()
    # print the board
    print(board)
    print(defis.BOARD_BREAK)

    while 1:
        # try to play a move
        try:
            if player:  # if the player is playing
                move: chess.Move = utils.get_player_move(board)
                if move == 'undo':
                    board.pop()
                else:
                    board.push(move)
                    # alternate to the other player's turn
                    player = 0
            else:
                # if the AI is playing
                move: chess.Move = utils.get_AI_move(board)
                board.push(move)
                '''
                if move == 'undo':
                    board.pop()
                else:
                    board.push(move)
                '''
                # alternate to the other player's turn
                player = 1
        except chess.InvalidMoveError:
            print('Invalid Move, Try Again - Should Not Reach Here')
        
        # check if game is over
        utils.check_result(board)

        # print the board after the move
        print(board)
        print(defis.BOARD_BREAK)

elif 0:
    board = chess.Board()

    
    # print the board
    # board.push(chess.Move.from_uci("g1f3")) # first move
    # board.push(chess.Move.from_uci("g8f6"))
    # board.push(chess.Move.from_uci("f3g1"))
    # board.push(chess.Move.from_uci("f6g8")) # first repetition
    # board.push(chess.Move.from_uci("g1f3"))
    # board.push(chess.Move.from_uci("g8f6"))
    # board.push(chess.Move.from_uci("f3g1"))
    # board.push(chess.Move.from_uci("f6g8")) # second repetition (third time this position occurred)

    # for x in range(30):
    #     board.push(chess.Move.from_uci("g1f3")) # first move
    #     board.push(chess.Move.from_uci("g8f6"))
    #     board.push(chess.Move.from_uci("f3g1"))
    #     board.push(chess.Move.from_uci("f6g8"))
    #     utils.check_result(board)

    # pawn_mask = board.pieces(chess.PAWN, chess.WHITE).mask
    
    # prints out a 64-bit representation of the positions of the white pawns
    # print(bin(pawn_mask)[2:].zfill(64))