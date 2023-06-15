import pygame as pg
import sys
import numpy as np
from IPython import get_ipython
from game import Game
from config import *


def main(sim=False, model=None):

    # --- OBJECTS ---
    game = Game(sim=sim, model=model)
    board = game.board
    ai = game.ai
    ai2 = game.ai2

    if not sim:
        if ai2 is not None:
            print(f"{game.gamemode} vs. AI level {ai2.level}")
        else:
            print(f"{game.gamemode} vs. {game.gamemode}")


    # --- MAINLOOP ---
    while True:

        if not game.sim:
            # pg events
            for event in pg.event.get():

                # quit event
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                # keydown event
                if event.type == pg.KEYDOWN:
                    # g-gamemode
                    if event.key == pg.K_g:
                        game.change_gamemode()
                    # r-restart
                    if event.key == pg.K_r:
                        game.reset()
                        board = game.board
                        ai = game.ai
                    # 0-random ai
                    if event.key == pg.K_0:
                        ai.level = 0
                    # 1-minmax ai
                    if event.key == pg.K_1:
                        ai.level = 1
                    # 2-nn ai
                    if event.key == pg.K_2:
                        ai.level = 2
                        
                # click event
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x = int(pos[1] // SQ_SIZE)
                    y = int(pos[0] // SQ_SIZE)
                    # human mark sqr
                    if board.empty_square(x, y) and game.running:
                        game.make_move(x, y)
                        if game.isover():
                            game.running = False

        # AI initial call, if playing against AI
        if ai is not None:
            if game.gamemode == 'ai' and game.player == ai.player and game.running:
                # update the screen
                if not game.sim:
                    pg.display.update()
                # eval
                x, y = ai.eval(board)
                # move
                game.make_move(x, y)
                # check if end
                if game.isover():
                    game.running = False
                    game.result = board.check_wins(show=True)
                    # show the winner and board if running in terminal
                    if not get_ipython().__class__.__name__ in ('TerminalInteractiveShell','ZMQInteractiveShell'):
                        if game.result == 0:
                            print("DRAW")
                        else:
                            print(board.winner)
                            board.show_actualboard()
                    # save the winner and board if running in script
                    else:
                        return game.result, game.history
        
        # AI secondary call, if two AIs are playing
        if ai2 is not None:
            if game.sim or game.player == ai2.player and game.running:
                # update the screen
                if not game.sim:
                    pg.display.update()
                # eval
                x, y  = ai2.eval(board)
                # move
                game.make_move(x, y)
                # check if end
                if game.isover():
                    game.running = False
                    game.result = board.check_wins(show=True)
                    # show the winner and board if running in terminal
                    if not get_ipython().__class__.__name__ in ('TerminalInteractiveShell','ZMQInteractiveShell'):
                        if game.result == 0:
                            print("DRAW")
                        else:
                            print(board.winner)
                            board.show_actualboard()
                    # save the winner and board if running in script
                    else:
                        return game.result, game.history

        # update the screen
        if not game.sim:
            pg.display.update()


# PLAY: Run the main loop
if __name__ == '__main__':

    # if no arguments, play what is specified here
    if len(sys.argv) == 1:
        main(sim = False, model = None)

    # if three arguments, play what is specified in the arguments
    elif len(sys.argv) == 3:
        sim = True if sys.argv[1].lower() in ('true','t','1') else False if sys.argv[1] in ('false','f','0') else None
        model = int(sys.argv[2]) if sys.argv[2].isnumeric() else sys.argv[2]
        main(sim = sim, model = model)

    # else, print error
    elif len(sys.argv) > 1:
        print("you need two arguments to the play the TicTacToe script: sim and model")
