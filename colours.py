# -*- coding: utf-8 -*-

from PyQt5.QtGui import QColor, QBrush
from matplotlib import cm

bg = "white"
fg = "#000000fff"
readonlybackground="black"

def qbrush_from_perc(value, palette=cm.gist_earth):
    ''' return a brush from value. coolwarm is the default'''
    colour = palette

    N = colour.N -1
    if value is None:
        rgb = colour(0)
    else:
        rgb = colour(int(value*N))
        
    brush_colour = QColor(rgb[0]*255, rgb[1]*255, rgb[2]*255)
    brush = QBrush(brush_colour)
    return brush