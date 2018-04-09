'''
Created on 15 mars 2018

@author: Guillaume
'''

import pygame
from pygame.locals import*
import json
import math

class DrawCircuit(object):

    def __init__(self):
        
        name = "Dessinateur de circuit"
        
        pygame.init()
        
        self.windowSize = (1600,900)
        
        self.window = pygame.display.set_mode(self.windowSize)

        pygame.display.set_caption(name)
        pygame.display.flip()
        
        self.imgVoiture = "../car.png"
        self.voiture = pygame.image.load(self.imgVoiture)
        self.orig_voiture = self.voiture
        
        self.positionVoiture = self.voiture.get_rect()
        
        self.epaisseurCircuit = 150
        
        self.circuit = []
        self.positionVoiture = (0,0)
        self.angleVoiture = 0
        self.depart = []
        
        self.circuitOK = False
        self.voitureOK = False
        
        self.run = True
        self.update()
        
        
        
    def update(self):
        
        while self.run:
        
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    
                if event.type == KEYDOWN:
                    if event.key == K_c:
                        self.creerCircuit()
                        
                    if event.key == K_s and self.circuitOK == True and self.voitureOK == True:
                        self.save()
                        
                    if event.key == K_SPACE and self.circuitOK == True:
                        print(self.positionVoiture)
                        print(pygame.mouse.get_pos())
                        print(self.angleVoiture)
                        print(self.depart)
                        self.voitureOK = True

            if pygame.key.get_pressed()[K_SPACE] and self.circuitOK == False:
                pygame.draw.circle(self.window, pygame.Color("white"), pygame.mouse.get_pos(), int(self.epaisseurCircuit/2), int(self.epaisseurCircuit/2))
            
            if self.circuitOK == True:
                
                if pygame.key.get_pressed()[K_LEFT]:
                    self.rotation(self.angleVoiture+1)
                    
                if pygame.key.get_pressed()[K_RIGHT]:
                    self.rotation(self.angleVoiture-1)
                    
                self.positionnerVoiture()
            
            pygame.display.flip() #On affiche tous les elements a l ecran 
            
            
    def creerCircuit(self):

        for j in range(1, self.windowSize[1]-1):
            for i in range(1, self.windowSize[0]-1):
                point = 0
                if self.window.get_at((i, j)) == (0, 0, 0, 255):
                    for a in [-1,0,1]:
                        for b in [-1,0,1]:
                            if self.window.get_at((i+a, j+b)) == (255, 255, 255, 255):
                                point += 1
                    if point > 0 and point < 7:
                        self.circuit.append((i, j))
                        self.window.set_at((i, j), pygame.Color("red"))
                        pygame.display.flip()
                        
                        
        self.window.fill(pygame.Color("white"))
        for pos in self.circuit:
            self.window.set_at(pos, pygame.Color("black"))
            
        pygame.display.flip()
        
        print(self.circuit)
        
        self.circuitOK = True
        
        
    def positionnerVoiture(self):
        
        self.window.fill(pygame.Color("white"))
        
        for pos in self.circuit:
            self.window.set_at(pos, pygame.Color("black"))
            
        self.positionVoiture = self.voiture.get_rect(center = pygame.mouse.get_pos())
        
        posVoiture = (self.positionVoiture[0],self.positionVoiture[1])
        debutLigne = (int(self.positionVoiture.center[0] + 75*math.cos(math.radians(self.angleVoiture)) - 100*math.sin(math.radians(self.angleVoiture))), int(self.positionVoiture.center[1] - 100*math.cos(math.radians(self.angleVoiture)) - 75*math.sin(math.radians(self.angleVoiture))))
        finLigne = (int(self.positionVoiture.center[0] + 75*math.cos(math.radians(self.angleVoiture)) + 100*math.sin(math.radians(self.angleVoiture))), int(self.positionVoiture.center[1] + 100*math.cos(math.radians(self.angleVoiture)) - 75*math.sin(math.radians(self.angleVoiture))))
        
        #on dessine la ligne de depart devant la voiture
        pygame.draw.line(self.window, pygame.Color("blue"), debutLigne, finLigne, 1)
        
        self.window.blit(self.voiture, self.positionVoiture)
        
        
        
    def save(self):
        
        if self.circuit != [] and self.voiture != []:
            
            file = open("circuits.txt", "w")
        
            json.dump(self.circuit, file)
            
            file.close()
        
        else:
            print("Veuillez vous assurer d avoir creer un circuit et d avoir possitionner la voiture.")
            
    
    def rotation(self, angle):
        self.voiture = pygame.transform.rotate(self.orig_voiture, angle)
        self.positionVoiture = self.voiture.get_rect(center = self.positionVoiture.center)
        self.angleVoiture = angle
 

DrawCircuit()