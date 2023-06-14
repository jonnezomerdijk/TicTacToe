# importing the required libraries
import pygame as pg
import numpy as np
import keras

modelNN = keras.models.load_model('NNwinner')
 
# storing the winner's value at any instant of code
winner = draw = None

# to set the number of cells per row/col
ROWS = COLS = 3

# to set dimensions of the game window
WIDTH = HEIGHT = 512

# to get the number of squares total
nSquares = ROWS * COLS

# get size of a cell
SQ_SIZE = WIDTH / ROWS

# set line width and radius
LINE_WIDTH = WIDTH // (20 * ROWS)
OFFSET = WIDTH / 12
RADIUS = SQ_SIZE // ROWS

# vector function
vec2 = pg.math.Vector2
 
# setting up a ROWS * COLS board in canvas
new_canvas = np.zeros((ROWS, COLS))

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (0, 0, 0)
CIRC_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

def get_scaled_image(path, res):
    img = pg.image.load(path)
    return pg.transform.smoothscale(img, res)

pg.init()

# Images
field_image = get_scaled_image("images/bkefield.png", res=(WIDTH,HEIGHT))
x_img = get_scaled_image("images/custom_x.png", res=[SQ_SIZE] * 2)
o_img = get_scaled_image("images/custom_o.png", res=[SQ_SIZE] * 2)
font = pg.font.SysFont('Verdana', int(SQ_SIZE // 4), True)
