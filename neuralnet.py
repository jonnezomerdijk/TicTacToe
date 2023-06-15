import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import to_categorical,plot_model

np.random.seed(1234)

class NN:

    def __init__(self):
        self.model = self.getModel()

    def getModel(self):
        'builds the neural network setup'
        outcomes = 3
        '''
        Dense layers receive input from all neurons of the previous layer
        Dropout layers remove the noise that may be present in the input to prevent over-fitting
        ReLU function - max(0,z)max(0,z): mostly used for hidden layers, returns 0 if z is negative, otherwise returns z
        Softmax function - mostly used for output layers, returns a probability distribution of the possible outcomes
        '''
        model = Sequential()
        model.add(Dense(200, activation='relu', input_shape=(9, ))) 
        model.add(Dropout(0.2))
        model.add(Dense(125, activation='relu'))
        model.add(Dense(75, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(25, activation='relu'))
        model.add(Dense(outcomes, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
        return model


    def gameStats(self, games, player=2):
        'prints the stats of the games played'
        stats = {"win": 0, "loss": 0, "draw": 0}
        for game in games:
            result = game[0]
            if result == player:
                stats["win"] += 1
            elif result == 0:
                stats["draw"] += 1
            else:
                stats["loss"] += 1
        
        winPct = stats["win"] / len(games) * 100
        lossPct = stats["loss"] / len(games) * 100
        drawPct = stats["draw"] / len(games) * 100

        print("Results for player %d:" % (player))
        print("Wins: %d (%.1f%%)" % (stats["win"], winPct))
        print("Loss: %d (%.1f%%)" % (stats["loss"], lossPct))
        print("Draw: %d (%.1f%%)" % (stats["draw"], drawPct))

    
    def movesToBoard(self, moves):
        'converts a list of moves to a board'
        board = np.zeros((3,3))
        for move in moves:
            player = move[0]
            coords = move[1]
            board[coords[0]][coords[1]] = player
        return board


    def gamesToWinLossData(self, games, trainsetsize=.8):
        'converts a list of games to a dataset for training'
        X = []
        y = []
        for game in games:
            winner = game[0]
            gameplay = game[1]
            for move in range(len(gameplay)):
                X.append(self.movesToBoard(gameplay[:(move + 1)]))
                y.append(winner)

        X = np.array(X).reshape((-1, 9))
        y = to_categorical(y)
        
        # Return an appropriate train/test split
        trainNum = int(len(X) * trainsetsize)
        return (X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:])

    def plot_model(self):
        'plots the model'
        return plot_model(self.model, show_shapes=True, show_layer_names=True, dpi=60)
