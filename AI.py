import pygame as pg
import numpy as np
import random
import copy


class AI:

    def __init__(self, level=1, player=2, model=None):
        # AI settings
        self.level = level
        self.player = player
        self.model = model
    
    # --- RANDOM ---
    def rnd(self, board):
        'returns a random move'
        empty_sqrs = board.get_empty_squares()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]
    
    # --- MINMAX ---
    def minmax(self, board, maximizing):
        'returns the best move for the minmax AI'
        # which moves are available on the board
        empty_sqrs = board.get_empty_squares()
        best_move = None
        
        # terminal case
        case = board.check_wins()

        # player 1 (player) wins
        if case == 1:
            return 1, None
        # player 2 (AI) wins
        elif case == 2:
            return -1, None
        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            for (x, y) in empty_sqrs:
                tmp_board = copy.deepcopy(board)
                tmp_board.mark_square(x, y, 1)
                eval = self.minmax(tmp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            for (x, y) in empty_sqrs:
                tmp_board = copy.deepcopy(board)
                tmp_board.mark_square(x, y, self.player)
                eval = self.minmax(tmp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)

            return min_eval, best_move


    # --- NEURAL NETWORK ---
    def neuralnet(self, board, maximizing):
        'returns the best move for the neuralnet AI'
        # which moves are available on the board
        empty_sqrs = board.get_empty_squares()
        scores = []
            
        # Make predictions for each possible move
        for i in range(len(empty_sqrs)):
            future = np.array(board.canvas)
            future[empty_sqrs[i][0]][empty_sqrs[i][1]] = self.player
            prediction = self.model.predict(future.reshape((-1, 9)),verbose=0)[0]
            if maximizing:
                winPrediction = prediction[1]
                lossPrediction = prediction[2]
            else:
                winPrediction = prediction[2]
                lossPrediction = prediction[1]
            drawPrediction = prediction[0]
            if winPrediction - lossPrediction > 0:
                scores.append(winPrediction - lossPrediction)
            else:
                scores.append(drawPrediction - lossPrediction)

        # Choose the best move with a random factor
        bestMoves = np.flip(np.argsort(scores))
        for i in range(len(bestMoves)):
            return max(scores), empty_sqrs[bestMoves[i]]


    def eval(self, main_board):
        'returns the evaluation of the board, resulting in the best move'
        if self.level==0:
            # random choice
            move = self.rnd(main_board)
        elif self.level==1:
            # minmax algo choice
            eval, move = self.minmax(main_board,maximizing=False)
        elif self.level==2:
            # neuralnet algo choice
            eval, move = self.neuralnet(main_board,maximizing=False)
        
        return move
