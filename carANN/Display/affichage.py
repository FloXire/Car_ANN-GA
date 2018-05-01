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
import theano.tensor as T
import lasagne
import json
import sys

from Commun.constantes import Constante
from AlgoGen import algorithme_genetique
from Display.traitementResultats import afficherResultats, enregistrerResultats, takeFirst
from Display.drawANN import schemaANN

tauxMutations = Constante.CHANCE_MUTATION

tabScoresEtParams = []
paramA0 = [np.zeros((Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN)), np.zeros((Constante.NOMBRE_NEURONES_HIDDEN)), np.zeros((Constante.NOMBRE_NEURONES_HIDDEN, Constante.NOMBRE_NEURONES_OUT)), np.zeros((Constante.NOMBRE_NEURONES_OUT))]
#paramA0 represente les parametres d'un reseau de neurone initialises a 0

compteurIndividus = 1
compteurGenerations = 1

circuitTermine = False
scorePremierArrive = 0

name = "TIPE : generation " + str(compteurGenerations) + ", individu " + str(compteurIndividus)


tabResults = []
tabResults.append([0]*Constante.NOMBRE_INDIVIDUS)

#theano.config.compute_test_value = 'warn'
#print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

class Affichage():
    
    def __init__(self, tabParamsANN = [], tabParamsATester = []):

        global name
        global compteurIndividus
        global compteurGenerations
        
        name = "TIPE : generation " + str(compteurGenerations) + ", individu " + str(compteurIndividus)

        #on initialise pygame
        pygame.init()
   
        self.windowSize = (1600,900)
        self.imgVoiture = "car.png"
        self.icon = pygame.image.load(self.imgVoiture)
        self.voiture = pygame.image.load(self.imgVoiture)
        self.orig_voiture = self.voiture
        
        self.window = pygame.display.set_mode(self.windowSize)
        
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(name)
        pygame.display.flip()
        
        self.numeroCircuit = Constante.NUMERO_CIRCUIT #permet de pouvoir changer de circuit a tout moment, par exemple quand un individu a termine un circuit, on peut le faire rouler sur un autre
        self.initCircuit()
        
        self.positionVoiture = self.voiture.get_rect()
        self.window.blit(self.voiture, (0,0))
        self.positionVoiture.move_ip(self.initCarPosition[0],self.initCarPosition[1])
        
        #position X et Y de la voiture en flotant
        self.positionX = self.initCarPosition[0]
        self.positionY = self.initCarPosition[1]
        
        #position de la voiture en entiers
        self.oldPosX = self.initCarPosition[0]
        self.oldPosY = self.initCarPosition[1]
        
        self.vitesse = Constante.VITESSE
        
        self.score = 0
        
        self.tabParamsAllIndiv = tabParamsANN
        
        self.tourComplet = False
        
        if compteurGenerations > 1:
            self.tabParamsCurrentIndiv = self.tabParamsAllIndiv[compteurIndividus-1]
            
        if tabParamsATester != []:
            self.tabParamsCurrentIndiv = tabParamsATester
            self.paramsATester = True  
        else:
            self.paramsATester = False
        
        self.f = self.BuildNeuralNetwork(self.paramsATester)
        
        self.coordTestBoucleInf = self.positionVoiture.center
        
        self.run = True
        
        if compteurIndividus == 1 and compteurGenerations > 1:
            tabResultsPrecGenDansLordre = sorted(tabResults[compteurGenerations-2], key = takeFirst, reverse = True)
            self.score = tabResultsPrecGenDansLordre[0][0]
            self.tourComplet = tabResultsPrecGenDansLordre[0][2]
            if (self.tourComplet):
                print(self.tourComplet)
            self.run = False
            
        self.update()
        
        
    def update(self):
        
        global compteurIndividus
        global compteurGenerations
        global tabScoresEtParams
        global tabResults
        global tauxMutations
        
        while self.run:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        afficherResultats(compteurGenerations, tabResults)
                    if event.key == K_e:
                        schemaANN(Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN, self.paramsReseau)
                                
            self.move()
            
            self.window.fill(pygame.Color("black")) #remet tout en noir
            self.afficherCircuit()
            self.window.blit(self.voiture, self.positionVoiture)
            
            self.getValeursCapteurs()
            
            self.rotation(self.angle + self.retourReseau(self.distances)[0][0])
            
            self.score += 1
            
            if self.score % 100 == 0:
                if self.testBoucleInfinie(self.coordTestBoucleInf):
                    self.score -= 100 #malus
                    self.run = False
                else:
                    self.coordTestBoucleInf = self.positionVoiture.center
            
            pygame.display.flip() #On affiche tous les elements a l ecran 
            
            
        if not(self.run):
            
            if self.tourComplet and not((self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]-89 <= self.angle <= self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]+89) \
                                        or (self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]-89 <= self.angle - 365 <= self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]+89) \
                                        or (self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]-89 <= self.angle + 365 <= self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]+89)):
                self.score = 100
                self.tourComplet = False
                print("Un individu malin a tente de dejouer le systeme, heureusement la police l'a intercepte dans les temps")
            
            if self.paramsATester == True:
                print("score : "+str(self.score))
                sys.exit()
            
            if self.score > 10000:
                self.score = 100
            
            tabScoresEtParams.append((self.score, self.paramsReseau))
            
            tabResults[compteurGenerations-1][compteurIndividus-1] = [self.score, self.paramsReseau, self.tourComplet]
            
            if compteurIndividus % Constante.NOMBRE_INDIVIDUS == 0:
                
                if (compteurGenerations > 1) and (Constante.MUTATIONS_DECROISSANTES == 'O'):
                    tauxMutations /= 1.12
                    
                compteurGenerations += 1
                compteurIndividus = 0
                                
                tabResults.append([0]*Constante.NOMBRE_INDIVIDUS)
                
                listeTriee = algorithme_genetique.triIndividus(tabScoresEtParams)
                listeCroisee = algorithme_genetique.croisements(listeTriee)
                self.tabParamsAllIndiv = algorithme_genetique.mutations(listeCroisee, tauxMutations)
                
                """doit on faire la selection sur tous les indivs de toutes les generations? oui : 'TE', non : 'E' (a changer dans les constantes"""
                if Constante.METHODE_SELECTION == 'E':
                    tabScoresEtParams = []

                
            if compteurGenerations == Constante.NOMBRE_GENERATIONS_MAX+1: #On arrete le programme quand on a genere 50 generations
                enregistrerResultats(compteurGenerations, tabResults)
                sys.exit()
            
            compteurIndividus += 1
            
            Affichage(self.tabParamsAllIndiv)
    
    
    def initCircuit(self):
        
        file = open("CircuitCreator/circuits.txt", "r")
        self.donneesCircuits = json.load(file)
        
        self.circuit = self.donneesCircuits[self.numeroCircuit]["Circuit"]
        self.angle = self.donneesCircuits[self.numeroCircuit]["AngleVoiture"]
        self.initCarPosition = self.donneesCircuits[self.numeroCircuit]["PositionVoiture"]
        self.ligneDepart = self.donneesCircuits[self.numeroCircuit]["LigneDepart"]
        
        file.close()
        

    def afficherCircuit(self):
        
        #affiche le circuit
        for pos in self.circuit:
            self.window.set_at(pos, pygame.Color("white"))
            
        #affiche la ligne de depart
        for pos in self.ligneDepart:
            self.window.set_at(pos, pygame.Color("blue"))

        
    # fonction gerant le deplacement
    def move(self):
        
        # pour chaque tour de boucle pygame on ajoute une position en fonction de l angle
        self.positionX += self.vitesse*math.cos(math.radians(self.angle))
        self.positionY += self.vitesse*-math.sin(math.radians(self.angle)) #sinus negatif car axe des y inverse dans pygame
        
        #on verifie si la position de la voiture depasse de self.vitesse son ancienne position
        if self.positionX >= self.oldPosX + self.vitesse:
            self.positionVoiture = self.positionVoiture.move(self.vitesse,0)
            self.oldPosX += self.vitesse
        if self.positionX <= self.oldPosX - self.vitesse:
            self.positionVoiture = self.positionVoiture.move(-self.vitesse,0)
            self.oldPosX -= self.vitesse
        if self.positionY >= self.oldPosY + self.vitesse:
            self.positionVoiture = self.positionVoiture.move(0,self.vitesse)
            self.oldPosY += self.vitesse
        if self.positionY <= self.oldPosY - self.vitesse:
            self.positionVoiture = self.positionVoiture.move(0,-self.vitesse)
            self.oldPosY -= self.vitesse
            
            
    def getValeursCapteurs(self):
        
        global circuitTermine
        global scorePremierArrive
        
        #44, 42 et 32 correspondent a des constantes pour la position des capteurs sur la voiture
        """RAVD = (int(self.positionVoiture.center[0] + 44*math.cos(math.radians(self.angle)) + 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 32*math.cos(math.radians(self.angle)) - 44*math.sin(math.radians(self.angle))))
        RAVG = (int(self.positionVoiture.center[0] + 44*math.cos(math.radians(self.angle)) - 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] - 32*math.cos(math.radians(self.angle)) - 44*math.sin(math.radians(self.angle))))
        RARD = (int(self.positionVoiture.center[0] - 42*math.cos(math.radians(self.angle)) + 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 32*math.cos(math.radians(self.angle)) + 42*math.sin(math.radians(self.angle))))
        RARG = (int(self.positionVoiture.center[0] - 42*math.cos(math.radians(self.angle)) - 32*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] - 32*math.cos(math.radians(self.angle)) + 42*math.sin(math.radians(self.angle))))
        """
        
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
                while ((self.sommeRGB(self.window.get_at((int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur)))))) < 715) and (i <= Constante.DISTANCE_MAX_CAPTEURS)) :
                    
                    i+=1                
                                    
                intersection = (int(debutRayon[0]+i*math.cos(math.radians(self.angle + angleCapteur))), int(debutRayon[1]+i*-math.sin(math.radians(self.angle + angleCapteur))))
            
                if i <= Constante.DISTANCE_MAX_CAPTEURS:
                    pygame.draw.line(self.window, pygame.Color("red"), debutRayon, intersection, 1)
                else:
                    pygame.draw.line(self.window, pygame.Color("green"), debutRayon, intersection, 1)
                                
                distanceCapteur[capteur] = math.sqrt((intersection[0] - debutRayon[0])**2+(intersection[1] - debutRayon[1])**2)
                
                #inutile, ne touche jamais ces capteurs
                """for capteur in [RAVD, RAVG, RARD, RARG]:
                    if capteur in self.circuit:
                        #print("sortie de piste")
                        self.run = False
                        print(self.sommeRGB(self.window.get_at(capteur)))"""
                
                self.distances = distanceCapteur #tableau 1*5 
                
            except IndexError:
                self.run = False
        
        i=0
        for distance in self.distances:
            i += 1
            if distance <= 2*self.vitesse or ((distance <= 3*self.vitesse) and i == 3):
                self.run = False
                
        #self.window.set_at((int(self.positionVoiture.center[0] + 75*math.cos(math.radians(self.angle)) + 0*math.sin(math.radians(self.angle))), int(self.positionVoiture.center[1] + 0*math.cos(math.radians(self.angle)) - 75*math.sin(math.radians(self.angle)))), pygame.Color("blue"))
        if self.sommeRGB(self.window.get_at(self.positionVoiture.center)) > 496 and self.score > 100:
            
            if self.score < 2500:
                print("Individu qui est retourne en arriere")
                self.score /= 4
                self.run = False
            
            else:
                print("Circuit termine")
                self.tourComplet = True
                
                if not(circuitTermine):
                    scorePremierArrive = self.score
                    circuitTermine = True
                    
                diff = scorePremierArrive - self.score
                self.score += 4*diff #Plus d'influence de la trajectoire pour les petits circuit car pour les grands le score est de lui meme plus espace
                self.score += (10*self.score)/100 #Ajout d'un bonus de score de 10 pourcent pour tous les indivs ayant fini le circuit (pour eviter le cas ou des indivs n'ayant pas termine le circuit de peu passent devant des indivs ayant fini le circuit)
                
                self.run = False
                
        
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
    
    
    def testBoucleInfinie(self, coordTest):
        
        if (abs(coordTest[0]-self.positionVoiture.center[0]) < 5 and (abs(coordTest[1]-self.positionVoiture.center[1])) < 5):
            return True
        else:
            return False
        
        
    def BuildNeuralNetwork(self, paramsATester):        
        
        global compteurGenerations
        
        W_init = np.random.normal(0, 0.1, (Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN))
        #b_init = np.random.normal(0, 0.1, (10,))
        
        #print(W_init)
        #print(b_init)
        
        W_output = np.random.normal(0, 0.1, (Constante.NOMBRE_NEURONES_HIDDEN, Constante.NOMBRE_NEURONES_OUT))
        #b_output = np.random.normal(0, 0.1, (1,))
            
        x = T.matrix('x')
        
        l_in = lasagne.layers.InputLayer((1, Constante.NOMBRE_NEURONES_IN), name="input_layer", input_var=x)
        
        if Constante.FONCTION_ACTIVATION == 'tanh':
            l_hidden = lasagne.layers.DenseLayer(l_in, Constante.NOMBRE_NEURONES_HIDDEN, name="hidden_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), W=W_init)
        elif Constante.FONCTION_ACTIVATION == 'identity':
            l_hidden = lasagne.layers.DenseLayer(l_in, Constante.NOMBRE_NEURONES_HIDDEN, name="hidden_layer", W=W_init)

        l_out = lasagne.layers.DenseLayer(l_hidden, Constante.NOMBRE_NEURONES_OUT, name="output_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), W=W_output)
        
        if compteurGenerations > 1 or paramsATester:
            lasagne.layers.set_all_param_values(l_out, self.tabParamsCurrentIndiv)
        
        y = lasagne.layers.get_output(l_out)
        
        f = theano.function([x], y)
                
        self.paramsReseau = lasagne.layers.get_all_param_values(l_out)
        
        return f
    
    
    def retourReseau(self, distances):
        inputNet = np.array([distances])
        #print(f(inputNet))
        return self.f(inputNet)
    