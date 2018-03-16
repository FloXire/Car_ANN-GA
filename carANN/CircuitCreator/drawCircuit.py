'''
Created on 15 mars 2018

@author: Guillaume
'''

import pygame
from pygame.locals import *

class DrawCircuit(object):


    def __init__(self):
        
        name = "Dessinateur de circuit"
        
        pygame.init()
                
        self.windowSize = (1600,900)
        
        self.window = pygame.display.set_mode(self.windowSize)
        
        pygame.display.set_caption(name)
        pygame.display.flip()
        
        self.epaisseurCircuit = 150
        
        self.run = True
        self.update()
        
        
    def update(self):
        
        while self.run:
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                
                if event.type == KEYDOWN:
                    
                    if event.key == K_s:
                        self.save()
                        
            if pygame.key.get_pressed()[K_SPACE]:
                pygame.draw.circle(self.window, pygame.Color("white"), pygame.mouse.get_pos(), int(self.epaisseurCircuit/2), int(self.epaisseurCircuit/2))
                
            if pygame.key.get_pressed()[K_LEFT]:
                pass
            
            pygame.display.flip() #On affiche tous les elements a l ecran 
            
            
    def save(self):
        circuit = []
        
        for j in range(1, self.windowSize[1]-1):
            for i in range(1, self.windowSize[0]-1):
                point = False
                if self.window.get_at((i, j)) == (0, 0, 0, 255):
                    for a in [-1,0,1]:
                        for b in [-1,0,1]:
                            if self.window.get_at((i+a, j+b)) == (255, 255, 255, 255):
                                point = True
                    if point == True:
                        circuit.append((i,j))
                        self.window.set_at((i,j), pygame.Color("red"))
                        pygame.display.flip()
                        
                        
        self.window.fill(pygame.Color("white"))
        for pos in circuit:
            self.window.set_at(pos, pygame.Color("black"))
            
        pygame.display.flip()
         
        print(circuit)
            
        
        
        
DrawCircuit()