# -*- coding: utf-8 -*-
from collections import OrderedDict
import inspect
from symbols import *
from debug_cp import *
from gb_utils.greenberry_search import GreenBerrySearch

L_USER = 'dear berry'

# another lex would be to identify blobks first this is a side effect
MATH_OPS = ['+', '-', '*', '/']
BOOLS = [S.TRUE, S.FALSE]
BOOL_OPS = [S.GREATER, S.LESS]
EOS = [S.NL, S.EOF]

class GreenBerryPlot(object):
    def __init__(self):
        print(self, 'does not have an initialiser')

    def linear_plot(self, dataX, labelX, dataY, labelY):
        '''simple line plot'''
        try:
            import matplotlib.pyplot as plt
            plt.plot(dataX, dataY)
            plt.xlabel(labelX)
            plt.ylabel(labelY)
            plt.show()
        except ImportError:
            print('matplotlib unimported')

    def plot_handling(self, i, words, line):
        '''
        handles plotting of points
        '''
        try:
            comma_i = GreenBerrySearch.search_symbol(i, 1, words, S.COMMA)[1]
            if words[i+1][0] != "\'" and words[i+1][0] != "\"":
                dataX = list(map(float, words[i+1].split('-')))
            else:
                file_name = words[i+1][1:-1]
                with open(file_name, 'r') as file:
                    dataX =  list(map(float, file.read().split('-')))

            if words[comma_i+1][0] != "\'" and words[comma_i+1][0] != "\"":
                dataY = list(map(float, words[comma_i+1].split('-')))
            else:
                file_name = words[comma_i+1][1:-1]
                with open(file_name, 'r') as file:
                    dataY = list(map(float, file.read().split('-')))

            labelX = GreenBerrySearch.search(i, 1, words, S.COMMA)
            labelY = GreenBerrySearch.search(comma_i, 1, words, [S.NL, S.EOF])
            self.linear_plot(dataX, labelX, dataY, labelY)
        except:
            print(E.PLOT, line)


            
