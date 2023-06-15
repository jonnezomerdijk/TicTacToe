from config import *
from board import Board
from AI import AI


class Game:

    def __init__(self, sim=False, model=None):
        'game settings'
        self.sim = sim
        if sim:
            # if simulate we want to save all the moves
            self.history = []
        else:
            # otherwise we want to initialize pygame
            pg.init()
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        # initialize the board
        self.board = Board()

        # initialize the AI for player 1
        self.ai = AI(level=0, player=2)
        self.ai2 = None
        
        # initialize the AI for player 2
        if sim:
            if model is not None:
                if model=='random' or model==0:
                    self.ai2 = AI(level=0,player=1)
                elif model=='minmax' or model==1:
                    self.ai2 = AI(level=1,player=1)
                elif model=='nn' or model==2:
                    self.ai2 = AI(level=2,player=1,model=modelNN)
                else:
                    self.ai2 = AI(level=2,player=1,model=model)
        else:
            if model is not None:
                if model=='random' or model==0:
                    self.ai = AI(level=0,player=2)
                elif model=='minmax' or model==1:
                    self.ai = AI(level=1,player=2)
                elif model=='nn' or model==2:
                    self.ai = AI(level=2,player=2,model=modelNN)
                else:
                    self.ai = AI(level=2,player=2,model=model)

        # game variables
        self.player = 1                                            # 1-cross, 2-circles
        self.running = True
        self.gamemode = 'human' if not sim and not model else 'ai' # play against 'ai' or 'human'
        if not sim:
            self.draw_board()


    # --- DRAW METHODS ---
    def draw_board(self):
        'draws the board on the screen'
        if ROWS == 3:
            self.screen.blit(field_image, (0, 0))
        else:
            self.screen.fill('white')
            # vertical
            pg.draw.line(self.screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_WIDTH)
            for i in range(ROWS - 1):
                pg.draw.line(self.screen, LINE_COLOR, (SQ_SIZE * (i + 2), 0), (SQ_SIZE * (i + 2), HEIGHT), LINE_WIDTH)
            # horizontal
            pg.draw.line(self.screen, LINE_COLOR, (0, SQ_SIZE), (WIDTH, SQ_SIZE), LINE_WIDTH)
            for i in range(COLS - 1):
                pg.draw.line(self.screen, LINE_COLOR, (0, SQ_SIZE * (i + 2)), (WIDTH, SQ_SIZE * (i + 2)), LINE_WIDTH)

    def draw_fig(self, x, y):
        'draws the figure on the screen'
        if self.player == 1:
            # draw cross
            self.screen.blit(x_img, vec2(y, x) * SQ_SIZE)
        elif self.player == 2:
            # draw circle
            self.screen.blit(o_img, vec2(y, x) * SQ_SIZE)


    # --- OTHER METHODS ---
    def make_move(self, x, y):
        'makes a move on the board'
        self.board.mark_square(x, y, self.player)
        if self.sim:
            self.history.append((self.player,(x,y)))
        else:
            self.draw_fig(x, y)
        self.next_turn()

    def next_turn(self):
        'changes the player'
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        'changes the gamemode'
        self.gamemode = 'ai' if self.gamemode == 'human' else 'human'

    def isover(self):
        'checks if the game is over'
        # check if someone won
        if self.board.check_wins(show=True) != 0:
            if not self.sim:
                label = font.render(f'{self.board.winner} won!', True, 'white', 'black')
                self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
                pg.draw.line(self.screen, LINE_COLOR, self.board.iPos, self.board.fPos, LINE_WIDTH)
            return True
        # check if the board is full and it's a draw
        elif self.board.isfull():
            if not self.sim:
                label = font.render(f'Draw!', True, 'white', 'black')
                self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
            return True

    def reset(self):
        self.__init__(sim=self.sim, model=self.ai.model)
        