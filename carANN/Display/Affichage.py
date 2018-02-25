'''
Created on 23 fevr. 2018

@author: flo-1
'''

'''
Created on 17 janv. 2018

@author: Guillaume
'''

import pygame
from pygame.locals import *

import math
import numpy as np
import theano
import lasagne

class Affichage():
    
    def __init__(self):
        
        #on initialise pygame
        pygame.init()
        
        self.windowSize = (1280,720)
        self.name = "TIPE"
        self.icon = pygame.image.load("car.png")
        self.voiture = pygame.image.load("car.png")
        self.orig_voiture = self.voiture
        
        self.window = pygame.display.set_mode(self.windowSize)
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.name)
        pygame.display.flip()
        
        self.initCircuit()
        
        self.positionVoiture = self.voiture.get_rect()
        self.window.blit(self.voiture, (0,0))
        self.positionVoiture.move_ip(0, 300)
        
        #position X et Y de la voiture en flotant
        self.positionX = 0.0
        self.positionY = 300.0
        
        #position de la voiture en entiers
        self.oldPosX = 0
        self.oldPosY = 300
        
        self.vitesse = 1
        
        self.angle = 0
        
        self.run = True
        self.update()
        
    def update(self):        
        while self.run:
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    
                if event.type == KEYDOWN:
                    
                    if event.key == K_SPACE:
                        print("bouton espace presse")
                        
            if pygame.key.get_pressed()[K_RIGHT]:
                self.rotation(self.angle-1)
                
            if pygame.key.get_pressed()[K_LEFT]:
                self.rotation(self.angle+1)
            
            self.move()
                        
            self.window.fill(pygame.Color("white")) #remet tout en blanc
            self.afficherCircuit()
            self.window.blit(self.voiture, self.positionVoiture)
            self.getValeursCapteurs()
            pygame.display.flip() #On affiche tous les elements a l ecran 
    
        
    def initCircuit(self):
        
        #on remplit la liste circuit avec tous les points composant le circuit
        self.circuit = []
        for i in range(self.windowSize[0]):
            for y in [199,200,201,399,400,401]: #ajoute les 6 fonction au tableau
                self.circuit.append((i,(int(100*math.sin(i*0.01))+y)))
        
        for i in range(200): #ajoute les lignes de depart et d arrivee
            self.circuit.append((0,200+i))
            self.circuit.append((1280,200+i))
            
    # fonction gerant le deplacement
    def move(self):
        
        # pour chaque tour de boucle pygame on ajoute une position en fonction de l angle
        self.positionX += self.vitesse*math.cos(math.radians(self.angle))
        self.positionY += self.vitesse*-math.sin(math.radians(self.angle)) #sinus negatif car axe des y inverse dans pygame
        
        #on verifie si la position de la voiture depasse de 1 son ancienne position
        if self.positionX >= self.oldPosX + 1:
            self.positionVoiture = self.positionVoiture.move(1,0)
            self.oldPosX += 1
        if self.positionX <= self.oldPosX - 1:
            self.positionVoiture = self.positionVoiture.move(-1,0)
            self.oldPosX -= 1
        if self.positionY >= self.oldPosY + 1:
            self.positionVoiture = self.positionVoiture.move(0,1)
            self.oldPosY += 1
        if self.positionY <= self.oldPosY - 1:
            self.positionVoiture = self.positionVoiture.move(0,-1)
            self.oldPosY -= 1
            
    def afficherCircuit(self):
        for i in range(self.windowSize[0]):
            for y in [199,200,201,399,400,401]:
                self.window.set_at((i,(int(100*math.sin(i*0.01))+y)), pygame.Color("black"))

            
    def getValeursCapteurs(self):
        
        #44, 42 et 32 correspondent a des constantes pour la position des capteurs sur la voiture
        RAVD = (int(self.positionVoiture.center[0] + 44*math.cos(math.radians(self.angle)) + 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 32*math.cos(math.radians(self.angle)) - 44*math.sin(math.radians(self.angle))))
        RAVG = (int(self.positionVoiture.center[0] + 44*math.cos(math.radians(self.angle)) - 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] - 32*math.cos(math.radians(self.angle)) - 44*math.sin(math.radians(self.angle))))
        RARD = (int(self.positionVoiture.center[0] - 42*math.cos(math.radians(self.angle)) + 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 32*math.cos(math.radians(self.angle)) + 42*math.sin(math.radians(self.angle))))
        RARG = (int(self.positionVoiture.center[0] - 42*math.cos(math.radians(self.angle)) - 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] - 32*math.cos(math.radians(self.angle)) + 42*math.sin(math.radians(self.angle))))
        
        
        #Solution qui fonctionne mais avec des problemes d optimisation
        intersection = [self.positionVoiture.center] * 5 #pour faire un lancer de rayon
        
        for capteur in range (5):
            angleCapteur = 90 - capteur*45
            
            i=0
            while ((int(intersection[capteur][0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(intersection[capteur][1]+i*-math.sin(math.radians(self.angle + angleCapteur)))) in self.circuit) and (i <= 100) :
                i+=1
                
            intersection[capteur] = (int(intersection[capteur][0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(intersection[capteur][1]+i*-math.sin(math.radians(self.angle + angleCapteur))))
        
        
        #solution qui ne fonctionne pas trop mais est fluide
        """
        angle = math.radians(self.angle)
        intersection = self.positionVoiture.center
        for i in range(1280):
            if (int(intersection[0]+i*math.cos(angle)), int(intersection[1]+i*-math.sin(angle))) in self.circuit:
                intersection = (int(intersection[0]+i*math.cos(angle)), int(intersection[1]+i*-math.sin(angle)))
                break
            """
    
        """
        intersection = self.positionVoiture.center
    
        #Si l angle n est pas egal a +90 ou - 90 degres
        if -math.sin(math.radians(self.angle)) != 0:
                a = -math.sin(math.radians(self.angle))/math.cos(math.radians(self.angle)) # calcul pour le coefficient directeur
        else:
            a = 0
        b = self.positionVoiture.center[1] - a*self.positionVoiture.center[0] #calcul pour l ordonnee a l origine
        
        
        #on parcourt la fenetre et si l equation est validee, alors intersection prend la position
        for x in range(self.windowSize[0]):
                if int(a*x - 100*math.sin(x*0.01)) == int(200-b):
                    intersection = (x, int(a*x+b))
                    break
                if int(a*x - 100*math.sin(x*0.01)) == int(200-b):
                    intersection = (x, int(a*x+b))
                    print("BIen joue")
                    break
                elif int(a*x - 100*math.sin(x*0.01)) == int(400-b):
                    intersection = (x, int(a*x+b))
                    break
        """
        
        for capteur in [RAVD, RAVG, RARD, RARG]:
            if capteur in self.circuit:
                print("sortie de piste")
                self.window.set_at(capteur, pygame.Color("red"))
            else:
                self.window.set_at(capteur, pygame.Color("green"))
                
        valeurCapteur = [0]*5
        for capteur in range(5):
            pygame.draw.line(self.window, pygame.Color("blue"), self.positionVoiture.center, intersection[capteur], 1)
            valeurCapteur[capteur] = math.sqrt((intersection[capteur][0] - self.positionVoiture.center[0])**2+(intersection[capteur][1]-self.positionVoiture.center[1])**2)
        
        print(valeurCapteur)
    #fonction permettant de faire tourner la voiture
    def rotation(self, angle):
        self.voiture = pygame.transform.rotate(self.orig_voiture, angle)
        self.positionVoiture = self.voiture.get_rect(center = self.positionVoiture.center)
        self.angle = angle
        

Affichage()
        
