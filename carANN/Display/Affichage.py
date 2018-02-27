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
                        
            self.window.fill(pygame.Color("black")) #remet tout en noir
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
                self.window.set_at((i,(int(100*math.sin(i*0.01))+y)), pygame.Color("white"))

            
    def getValeursCapteurs(self):
        
        #44, 42 et 32 correspondent a des constantes pour la position des capteurs sur la voiture
        RAVD = (int(self.positionVoiture.center[0] + 44*math.cos(math.radians(self.angle)) + 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 32*math.cos(math.radians(self.angle)) - 44*math.sin(math.radians(self.angle))))
        RAVG = (int(self.positionVoiture.center[0] + 44*math.cos(math.radians(self.angle)) - 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] - 32*math.cos(math.radians(self.angle)) - 44*math.sin(math.radians(self.angle))))
        RARD = (int(self.positionVoiture.center[0] - 42*math.cos(math.radians(self.angle)) + 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 32*math.cos(math.radians(self.angle)) + 42*math.sin(math.radians(self.angle))))
        RARG = (int(self.positionVoiture.center[0] - 42*math.cos(math.radians(self.angle)) - 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] - 32*math.cos(math.radians(self.angle)) + 42*math.sin(math.radians(self.angle))))
        
        
        #Solution qui fonctionne mais avec des problemes d optimisation
        intersection = [self.positionVoiture.center]*5
        distanceCapteur = [0]*5 #renvoie la distance entre le centre de la voiture et le circuit pour chaque capteur

        for capteur in range (5): #capteur 0 a gauche, capteur 2 en face et capteur 3 a droite de la voiture
            angleCapteur = 90 - capteur*45 
            
            debutRayon = translationCentre(self.positionVoiture.center, self.angle, angleCapteur, capteur) #pour faire un lancer de rayon, on initialise tous les rayons au centre de la voiture

                        
            i=0
            
            #self.window.get_at(self.positionVoiture.center)
            #self.window.set_at(self.positionVoiture.center, (0,0,0))
            
            #on part du centre pour chaque rayon et on ajoute respectivement aux coordonnees x et y des fonction de cos et de sin a chaque iteration
            #self.angle est l'angle du vehicule (- vers la droite, + vers la gauche, cad sens trigo), on lui ajoute l'angle du capteur (= a 0 pour le capteur du milieu car capteur = 2)
            #on multiplie par -sin car l'axe des ordonnees est oriente vers le bas
            
            #try:
            
            print(capteur)
            
            if capteur == 1:
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                print(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur))))))
                print(sommeRGB(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur)))))))
            
            while ((sommeRGB(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur)))))) < 715) and (i <= 60)) :
                
                i+=1                
                                
                """if capteur == 1:
                    print(i)
                    print(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur))))))
                    print(sommeRGB(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur)))))))
                """
            intersection = (int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur))))
        
            if i<=60:
                pygame.draw.line(self.window, pygame.Color("red"), debutRayon, intersection, 1)
            else:
                pygame.draw.line(self.window, pygame.Color("white"), debutRayon, intersection, 1)
                            
            #distanceCapteur[capteur] = math.sqrt((intersection[capteur][0] - self.positionVoiture.center[0])**2+(intersection[capteur][1]-self.positionVoiture.center[1])**2)

            #except IndexError:
            #    pass

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
        
        """for capteur in [RAVD, RAVG, RARD, RARG]:
            if capteur in self.circuit:
                print("sortie de piste")
                self.window.set_at(capteur, pygame.Color("red"))
            else:
                self.window.set_at(capteur, pygame.Color("green"))
           """          
        
    #fonction permettant de faire tourner la voiture
    def rotation(self, angle):
        self.voiture = pygame.transform.rotate(self.orig_voiture, angle)
        self.positionVoiture = self.voiture.get_rect(center = self.positionVoiture.center)
        self.angle = angle
    
def translationCentre(posCentre, angleVoiture, angleCapteur, capteur):
    
    if (capteur == 0 or capteur == 4):
        newPos = (posCentre[0]+31*math.cos(math.radians(angleVoiture + angleCapteur)), posCentre[1]-31*math.sin(math.radians(angleVoiture + angleCapteur)))
    elif (capteur == 1 or capteur == 3):
        newPos = (posCentre[0]+44*math.cos(math.radians(angleVoiture + angleCapteur)), posCentre[1]-44*math.sin(math.radians(angleVoiture + angleCapteur)))
    else:
        newPos = (posCentre[0]+74*math.cos(math.radians(angleVoiture + angleCapteur)), posCentre[1]-74*math.sin(math.radians(angleVoiture + angleCapteur)))
   
    return newPos
    
def sommeRGB(tab):
        return (tab[0]+tab[1]+tab[2])    

Affichage()
        
