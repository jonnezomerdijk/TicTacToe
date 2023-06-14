import pygame as pg
import sys
import numpy as np
from IPython import get_ipython
from game import Game
from config import *


def main(sim=False,model=None):

    # --- OBJECTS ---
    game = Game(sim=sim,model=model)
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
                    # 1-random ai
                    if event.key == pg.K_1:
                        ai.level = 1
                        
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

        # AI initial call
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
        
        # AI secondary call
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

        if not game.sim:
            pg.display.update()


if __name__ == '__main__':
    
    main(
        sim = False,
        model = 0
        )
