'''
Created on 23 fevr. 2018

@author: flo-1
'''
from audioop import reverse

'''
Created on 17 janv. 2018

@author: Guillaume
'''

import pygame
from pygame.locals import *
import math
import numpy as np
import theano
import theano.tensor as T
import lasagne
from Commun.constantes import Constante
from AlgoGen import algorithme_genetique

tabScoresEtParams = []
compteurIndividus = 1
compteurGenerations = 1
name = "TIPE : generation " + str(compteurGenerations) + ", individu " + str(compteurIndividus)
paramA0 = [np.zeros((Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN)), np.zeros((Constante.NOMBRE_NEURONES_HIDDEN)), np.zeros((Constante.NOMBRE_NEURONES_HIDDEN, Constante.NOMBRE_NEURONES_OUT)), np.zeros((Constante.NOMBRE_NEURONES_OUT))]
#paramA0 represente les parametres d'un reseau de neurone initialises a 0

class Affichage():
    
    def __init__(self, tabParamsANN = []):
        
        global name
        global compteurIndividus
        global compteurGenerations
        
        name = "TIPE : generation " + str(compteurGenerations) + ", individu " + str(compteurIndividus)

        
        #on initialise pygame
        pygame.init()
                
        self.windowSize = (1280,720)
        self.imgVoiture = "car.png"
        self.icon = pygame.image.load(self.imgVoiture)
        self.voiture = pygame.image.load(self.imgVoiture)
        self.orig_voiture = self.voiture
        
        self.window = pygame.display.set_mode(self.windowSize)
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(name)
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
        
        self.score = 0
        
        self.tabParamsAllIndiv = tabParamsANN
        
        if compteurGenerations > 1:
            self.tabParamsCurrentIndiv = self.tabParamsAllIndiv[compteurIndividus-1]
        
        self.f = self.BuildNeuralNetwork()
                
        self.run = True
        self.update()
        
        
    def update(self):
        
        global compteurIndividus
        global compteurGenerations
        
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
        
            """self.tabRetourReseau.append(retourReseau(self.distances)[0][0])
            print(sum(self.tabRetourReseau)/float(len(self.tabRetourReseau)))"""
            
            
            self.rotation(self.angle + self.retourReseau(self.distances)[0][0])
            
            #print(self.score)
            
            pygame.display.flip() #On affiche tous les elements a l ecran 
            
            
        if not(self.run):
            
            tabScoresEtParams.append((self.score, self.paramsReseau))
        
            if compteurIndividus % Constante.NOMBRE_INDIVIDUS == 0:
                compteurGenerations += 1
                compteurIndividus = 0
                
                listeTriee = algorithme_genetique.triIndividus(tabScoresEtParams)
                self.tabParamsAllIndiv = algorithme_genetique.croisements(listeTriee)
                
            compteurIndividus += 1
            Affichage(self.tabParamsAllIndiv)
    
    
    def initCircuit(self):
        
        #on remplit la liste circuit avec tous les points composant le circuit
        self.circuit = []
        for i in range(self.windowSize[0]):
            for y in [199,200,201,399,400,401]: #ajoute les 6 fonctions au tableau
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
            debutRayon = self.translationCentre(self.positionVoiture.center, self.angle, angleCapteur, capteur) #pour faire un lancer de rayon, on initialise tous les rayons au centre de la voiture

            i=0
            
            #self.window.get_at(self.positionVoiture.center)
            #self.window.set_at(self.positionVoiture.center, (0,0,0))
            
            #on part du centre pour chaque rayon et on ajoute respectivement aux coordonnees x et y des fonction de cos et de sin a chaque iteration
            #self.angle est l'angle du vehicule (- vers la droite, + vers la gauche, cad sens trigo), on lui ajoute l'angle du capteur (= a 0 pour le capteur du milieu car capteur = 2)
            #on multiplie par -sin car l'axe des ordonnees est oriente vers le bas
            
            try:
            
                #on lance un rayon jusqu'a ce qu'il rencontre le circuit ou qu'il soit superieur a une certaine valeur
                while ((self.sommeRGB(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur)))))) < 715) and (i <= 60)) :
                    
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
                    pygame.draw.line(self.window, pygame.Color("green"), debutRayon, intersection, 1)
                                
                distanceCapteur[capteur] = math.sqrt((intersection[0] - debutRayon[0])**2+(intersection[1] - debutRayon[1])**2)
    
    
                """for capteur in [RAVD, RAVG, RARD, RARG]:
                    if capteur in self.circuit:
                        #print("sortie de piste")
                        self.window.set_at(capteur, pygame.Color("red"))
                    else:
                        self.window.set_at(capteur, pygame.Color("green"))"""
                
                self.distances = distanceCapteur #tableau 1*5 
                
                self.scoreTmp = self.positionVoiture.center[0]
                
                if self.scoreTmp > self.score:
                    self.score = self.scoreTmp
                    
            except IndexError:
                self.run = False
        
        for distance in self.distances:
            if distance <= 2:
                self.run = False
                #return self.score
            
        
    #fonction permettant de faire tourner la voiture
    def rotation(self, angle):
        self.voiture = pygame.transform.rotate(self.orig_voiture, angle)
        self.positionVoiture = self.voiture.get_rect(center = self.positionVoiture.center)
        self.angle = angle
    
    
    def translationCentre(self, posCentre, angleVoiture, angleCapteur, capteur):
        
        if (capteur == 0 or capteur == 4):
            newPos = (posCentre[0]+31*math.cos(math.radians(angleVoiture + angleCapteur)), posCentre[1]-31*math.sin(math.radians(angleVoiture + angleCapteur)))
        elif (capteur == 1 or capteur == 3):
            newPos = (posCentre[0]+44*math.cos(math.radians(angleVoiture + angleCapteur)), posCentre[1]-44*math.sin(math.radians(angleVoiture + angleCapteur)))
        else:
            newPos = (posCentre[0]+74*math.cos(math.radians(angleVoiture + angleCapteur)), posCentre[1]-74*math.sin(math.radians(angleVoiture + angleCapteur)))
       
        return newPos
    
        
    def sommeRGB(self, tab):
        return (tab[0]+tab[1]+tab[2])
    
    
    def BuildNeuralNetwork(self):        
        
        global compteurGenerations
        
        W_init = np.random.normal(0, 0.1, (Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN))
        #b_init = np.random.normal(0, 0.1, (10,))
        
        #print(W_init)
        #print(b_init)
        
        W_output = np.random.normal(0, 0.1, (Constante.NOMBRE_NEURONES_HIDDEN, Constante.NOMBRE_NEURONES_OUT))
        #b_output = np.random.normal(0, 0.1, (1,))
            
        x = T.matrix('x')
        
        l_in = lasagne.layers.InputLayer((1, Constante.NOMBRE_NEURONES_IN), name="input_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), input_var=x)
        l_hidden = lasagne.layers.DenseLayer(l_in, Constante.NOMBRE_NEURONES_HIDDEN, name="hidden_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), W=W_init)
        l_out = lasagne.layers.DenseLayer(l_hidden, Constante.NOMBRE_NEURONES_OUT, name="output_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), W=W_output)
        y = lasagne.layers.get_output(l_out)
        
        f = theano.function([x], y)
        
        if compteurGenerations > 1:
            lasagne.layers.set_all_param_values(l_out, self.tabParamsCurrentIndiv)
        
        self.paramsReseau = lasagne.layers.get_all_param_values(l_out)
        
        return f
    
    
    def retourReseau(self, distances):
        inputNet = np.array([distances])
        #print(f(inputNet))
        return self.f(inputNet)
    
Affichage()