'''
Created on 24 dec. 2017

@author: flo-1
'''

from Principal.constante import Constante
import pygame


class Ellipse:
    '''
    classdocs
    '''


    def __init__(self, pos, larg, haut, col, angle=360):
        '''
        Constructor
        '''
        
        self.position = pos
        self.largeur = larg
        self.hauteur = haut
        self.col = col
        self.angle = angle
        
    def affiche(self):
        #pygame.display.update()
        pass
    def reset(self):
        pass