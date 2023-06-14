import pygame as pg
from config import *


class Board:

    def __init__(self):
        # board settings
        self.canvas = new_canvas.copy()
        self.empty_squares = self.canvas
        self.marked_squares = 0

    def check_wins(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        # vertical wins
        for y in range(COLS):
            if self.canvas[0][y] == self.canvas[1][y] == self.canvas[2][y] != 0:
                self.winner = "OX"[int(self.canvas[0][y])%2]
                if show:
                    self.iPos = (y * SQ_SIZE + SQ_SIZE // 2, 20)
                    self.fPos = (y * SQ_SIZE + SQ_SIZE // 2, HEIGHT - 20)
                return self.canvas[0][y]

        # horizontal wins
        for x in range(ROWS):
            if self.canvas[x][0] == self.canvas[x][1] == self.canvas[x][2] != 0:
                self.winner = "OX"[int(self.canvas[x][0])%2]
                if show:
                    self.iPos = (20, x * SQ_SIZE + SQ_SIZE // 2)
                    self.fPos = (WIDTH - 20, x * SQ_SIZE + SQ_SIZE // 2)
                return self.canvas[x][0]

        # desc diagonal
        if self.canvas[0][0] == self.canvas[1][1] == self.canvas[2][2] != 0:
            self.winner = "OX"[int(self.canvas[1][1])%2]
            if show:
                self.iPos = (20, 20)
                self.fPos = (WIDTH - 20, HEIGHT - 20)
            return self.canvas[1][1]

        # asc diagonal
        if self.canvas[2][0] == self.canvas[1][1] == self.canvas[0][2] != 0:
            self.winner = "OX"[int(self.canvas[1][1])%2]
            if show:
                self.iPos = (20, HEIGHT - 20)
                self.fPos = (WIDTH - 20, 20)
            return self.canvas[1][1]

        # no win yet
        return 0

    def mark_square(self, x, y, player):
        self.canvas[x][y] = player
        self.marked_squares += 1

    def empty_square(self, x, y):
        return self.canvas[x][y] == 0

    def get_empty_squares(self):
        empty_sqrs = []
        for x in range(ROWS):
            for y in range(COLS):
                if self.empty_square(x, y):
                    empty_sqrs.append((x, y))
        
        return empty_sqrs

    def isfull(self):
        return self.marked_squares == nSquares

    def isempty(self):
        return self.marked_squares == 0

    def show_actualboard(self):
        current = self.canvas
        self.actual = current.tolist()
        for rownr,row in enumerate(self.actual):
            self.actual[rownr] = [" " if col==0 else "X" if col==1 else "O" for col in row]
        print(f'\n{"|".join(self.actual[0])}\n-----\n{"|".join(self.actual[1])}\n-----\n{"|".join(self.actual[2])}\n')
        
        