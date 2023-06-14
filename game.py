from config import *
from board import Board
from AI import AI


class Game:

    def __init__(self, sim=False, model=None):
        self.sim = sim
        if sim:
            self.history = []
        else:
            pg.init()
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
            self.clock = pg.time.Clock()

        self.board = Board()
        self.ai = AI(level=0, player=1)
        self.ai2 = None
        
        if model is not None:
            if model=='random' or model==0:
                self.ai2 = AI(level=0,player=2)
            elif model=='minmax' or model==1:
                self.ai2 = AI(level=1,player=2)
            elif model=='nn' or model==2:
                self.ai2 = AI(level=2,player=2,model=modelNN)
            else:
                self.ai2 = AI(level=2,player=2,model=model)

        self.player = 1          # 1-cross, 2-circles
        self.running = True
        self.gamemode = 'human' if not sim else 'ai' # 'ai' or 'human'
        if not sim:
            self.draw_board()

    # --- DRAW METHODS ---
    def draw_board(self):
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
        if self.player == 1:
            # draw cross
            self.screen.blit(x_img, vec2(y, x) * SQ_SIZE)
        elif self.player == 2:
            # draw circle
            self.screen.blit(o_img, vec2(y, x) * SQ_SIZE)

    # --- OTHER METHODS ---
    def make_move(self, x, y):
        self.board.mark_square(x, y, self.player)
        if self.sim:
            self.history.append((self.player,(x,y)))
        else:
            self.draw_fig(x, y)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        if self.board.check_wins(show=True) != 0:
            if not self.sim:
                label = font.render(f'{self.board.winner} won!', True, 'white', 'black')
                self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
                pg.draw.line(self.screen, LINE_COLOR, self.board.iPos, self.board.fPos, LINE_WIDTH)
            return True
        elif self.board.isfull():
            if not self.sim:
                label = font.render(f'Draw!', True, 'white', 'black')
                self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
            return True

    def reset(self):
        self.__init__()
        