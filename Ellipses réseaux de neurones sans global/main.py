'''
Created on 24 dec. 2017

@author: flo-1
'''
from math import sqrt
from _ast import Num

'''
Mutations sans effets de bord
'''

import numpy as np
import cv2
from Principal.constante import Constante
from Principal.ellipses import Ellipse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pygame
import matplotlib
from collections import OrderedDict

#imageVoulue = cv2.imread(Constante.IMAGE_ATTENDUE)
#print imageVoulue.shape
#print (Constante.HAUTEUR*Constante.LARGEUR)/25

"""cv2.imshow('objectif',imageVoulue)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()"""

a = 5
b = 1
theta = np.linspace(0, 2*np.pi, 40) #cercle de 0 a 2pi avec 40 points
x = a*np.cos(theta)
y = b*np.sin(theta)

#plt.plot(x,y)
#plt.xlim([0, Constante.LARGEUR])
#plt.ylim([0, Constante.HAUTEUR])
#axes = plt.gca()
#axes.set_xlim([0, Constante.LARGEUR])
#axes.set_ylim([0, Constante.HAUTEUR])
#circle1 = patches.Circle((0.3, 0.3), 0.03, fc='r', alpha=0.5)
#circle2 = patches.Circle((0.5, 0.3), 0.03, fc='r', alpha=0.5)
#ax.add_patch(circle1)
#ax.add_patch(circle2)
    
#ellipse1 = patches.Ellipse((-100, 0), 2, 1, angle=360)
#ax.add_patch(ellipse1)

#ellipse2 = patches.Ellipse((1, 100), 200, 1, angle=360)
#ax.add_patch(ellipse2)
    

#plt.axis('tight')
#plt.axis('equal')
#plt.axis('off')

#dicoEllipses = {}
listeEllipses = []
listePointsEllipses = []
listeWandHEllipses = []
dicoFitnessEllipses = {}
dicoFitnessEllipsesRangees = {}
listeCouleurs = [0]*Constante.NOMBRE_ELLIPSES
listePoints = [0]*Constante.NOMBRE_ELLIPSES
#plt.show()
dico1Ellipses = {}
listePointsPosEllipses = []
compteurNombreGen = 0

plt.ion()

"""running = True

pygame.init()
screen = pygame.display.set_mode((Constante.LARGEUR, Constante.HAUTEUR))
pygame.display.set_caption('GA Ellipses')
background_colour = (255,255,255)
screen.fill(background_colour)
pygame.draw.ellipse(screen, (255,   0,   0), [300, 100, 500, 20])    
pygame.display.flip() #Update the full display Surface to the screen
#surfBlanche = pygame.Surface((Constante.LARGEUR, Constante.HAUTEUR)).convert() 
#screen.fill(surfBlanche)

while running:
    
    
    #pygame.display.update(rectangle=None)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
#surfBlanche = pygame.Surface((Constante.LARGEUR, Constante.HAUTEUR)).convert()"""

def creationEllipses():
    
    dicoEllipses = {}
    
    """global listeEllipses
    global listePointsEllipses
    global listeWandHEllipses
    
    global listePointsPosEllipses"""

    for i in range(Constante.NOMBRE_ELLIPSES):
        pointPos = getRandomPos()
        W = getRandomWandH()
        H = getRandomWandH()
        color = pickARandomColorV2()
                
        pointSommetHaut = (pointPos[0], pointPos[1] + round(float(H)/2))
        pointSommetBas = (pointPos[0], pointPos[1] - round(float(H)/2))
        pointSommetGauche = (pointPos[0] - round(float(W)/2), pointPos[1])
        pointSommetDroit = (pointPos[0] + round(float(W)/2), pointPos[1])
        
        pointCentreHautEtMilieu = (pointPos[0], round(float(pointPos[1] + pointSommetHaut[1])/2))
        pointCentreBasEtMilieu = (pointPos[0], round(float(pointPos[1] + pointSommetBas[1])/2))
        pointCentreGaucheEtMilieu = (round(float(pointPos[0] + pointSommetGauche[0])/2), pointPos[1])
        pointCentreDroitEtMilieu = (round(float(pointPos[0] + pointSommetDroit[0])/2), pointPos[1])
        
        pointCentreHautEtGauche = (pointCentreGaucheEtMilieu[0], pointCentreHautEtMilieu[1])
        pointCentreHautEtDroit = (pointCentreDroitEtMilieu[0], pointCentreHautEtMilieu[1])
        pointCentreBasEtGauche = (pointCentreGaucheEtMilieu[0], pointCentreBasEtMilieu[1])
        pointCentreBasEtDroit = (pointCentreDroitEtMilieu[0], pointCentreBasEtMilieu[1])
        
        """listePointsEllipses.append((color,(pointPos, pointSommetHaut, pointSommetBas, pointSommetGauche, pointSommetDroit, 
                                    pointCentreHautEtMilieu, pointCentreBasEtMilieu, pointCentreGaucheEtMilieu, pointCentreDroitEtMilieu, 
                                    pointCentreHautEtGauche, pointCentreHautEtDroit, pointCentreBasEtGauche, pointCentreBasEtDroit)))
                
        listeWandHEllipses.append((W,H))       
                
        listeEllipses.append(patches.Ellipse(pointPos, W, H, angle=360, color = color))
        
        listePointsPosEllipses.append(pointPos)"""
        
        dicoEllipses[i] = [patches.Ellipse(pointPos, W, H, angle=360, color = color), 
                           color, W, H, pointPos, 
                           (pointPos, pointSommetHaut, pointSommetBas, pointSommetGauche, pointSommetDroit, 
                           pointCentreHautEtMilieu, pointCentreBasEtMilieu, pointCentreGaucheEtMilieu, pointCentreDroitEtMilieu, 
                           pointCentreHautEtGauche, pointCentreHautEtDroit, pointCentreBasEtGauche, pointCentreBasEtDroit)]
        
    
    addAndShowEllipses(dicoEllipses)
    
    return dicoEllipses
    
def addAndShowEllipses(dico):
    
    global compteurNombreGen    
    
    plt.close()
    fig = plt.figure(None, (Constante.LINCHES, Constante.HINCHES))
    ax = fig.add_subplot(111)
    plt.title('Generation numero ' + str(compteurNombreGen))     
    plt.axis([0, Constante.LARGEUR, 0, Constante.HAUTEUR])
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    
    if compteurNombreGen == 0:
        plt.ion()
        
    compteurNombreGen += 1

    for i in range(len(dico.values())):
        ax.add_patch(dico.values()[i][0])
        
    fig.canvas.draw()

    for i in range(len(dico.values())):
        dico.values()[i][0].remove()


def sommeW(ell):
    somme = 0
    listePointsW = (ell[5][3], ell[5][4], ell[5][7], ell[5][7])
    couleur = ell[1]
    
    for point in listePointsW:
        if 0 < point[0] < Constante.LARGEUR and 0 < point[1] < Constante.HAUTEUR:
            somme += diffCouleur(couleur, Constante.IMGRGB[changementDeRepere(point[1]), int(point[0])])
    
    return somme

def sommeH(ell):
    somme = 0
    listePointsH = (ell[5][1], ell[5][2], ell[5][5], ell[5][6])
    couleur = ell[1]
    
    for point in listePointsH:
        if 0 < point[0] < Constante.LARGEUR and 0 < point[1] < Constante.HAUTEUR:
            somme += diffCouleur(couleur, Constante.IMGRGB[changementDeRepere(point[1]), int(point[0])])
    
    return somme

def bestADN(dico):
    for ell in dico.values():
        if sommeW(ell) <= sommeH(ell):
            
            try:
                if ell[7] == 'W' or ell[7] == 'H':
                    del ell[7]
            except IndexError:
                pass
            
            ell.append('W')
                
        else:
            
            try:
                if ell[7] == 'W' or ell[7] == 'H':
                    del ell[7]
            except IndexError:
                pass
            
            ell.append('H')
    
    return dico
        
def getListeCouleurs(dico):
    
    global listeCouleurs
    
    for i in range(len(dico.values())):
        
        listeCouleurs[i] = dico.values()[i][1]
    
    return(listeCouleurs)
    
def getListePoints(dico):
    
    global listePoints
    
    for i in range(len(dico.values())):
        
        listePoints[i] = dico.values()[i][5]
    
    return(listePoints)
    
def testFitness(dicoEll):
    
    """retourne un dico range par ordre croissant contenant pour cle le num de l'ell et pour val la somme de la difference de couleur entre chaque pixel"""
    
    dicoEllipsesRangees = {}
        
    i=0
    
    for couleur, points in zip(getListeCouleurs(dicoEll), getListePoints(dicoEll)):
        somme = 0

        for point in points:
            
            if 0 < point[0] < Constante.LARGEUR and 0 < point[1] < Constante.HAUTEUR:
                #ici il y avait le somme = 0
                somme += diffCouleur(couleur, Constante.IMGRGB[changementDeRepere(point[1]), int(point[0])])
        
        try: #sert a suppr l'item s'il est deja dans le dico pour pouvoir faire append au bon endroit a la fin
            if dicoEll[i][6] != -1:
                del dicoEll[i][6]
        except IndexError:
            pass
        
        dicoEll[i].append(somme)
        i += 1
        
    dicoEllipsesRangees = OrderedDict(sorted(dicoEll.items(), key=lambda t: t[1][6])) #on peut appeler l'ellipse i, c'est un dico range par ordre croissant de fitness

    return dicoEllipsesRangees

def prendsLesMeilleurs(dicoEllRangees):

    newDicoEllipses = {}
    
    i=0
    
    for k in dicoEllRangees.keys()[:Constante.NOMBRE_HIGH_FITNESS_RETENUS]:
        newDicoEllipses[i] = dicoEllRangees[k] #changement i par k
        i += 1

    return newDicoEllipses        

def getVoisins(dico):
    
    listePointsPosEllipses = [dico[i][4] for i in dico.keys()]
    dicoVoisins = {}
    #setPointsPosEllipses = {dico[i][4] for i in dico.keys()}
    
    """"h = 0 
    for i,j in zip(listePointsPosEllipses, setPointsPosEllipses):
        if i == j:
            continue
        else:
            print i,j
            print listePointsPosEllipses[h-1], setPointsPosEllipses[h-1]
            print listePointsPosEllipses[h], setPointsPosEllipses[h]
        h += 1"""
    
    i = 0
    
    for pointPos, k in zip(listePointsPosEllipses, dico.keys()):
                
        listePointsProches = []
        listePointsPosEllipses.remove(pointPos)
        
        j = 0
        
        for autrePoint in (listePointsPosEllipses):
                        
            if distEntre2Points(pointPos, autrePoint) <= 15:
                
                if j >= i: #si l'indice du point Pos est plus petit que celui de l'autre point, (car on a tout qui descend d'un indice avec le remove)
                    listePointsProches.append((autrePoint, dico[j+1][1], dico[j+1][2], dico[j+1][3])) #pos autre point, col, W, H
                else: #s'il est plus grand cela ne change rien au niveau de l'indice
                    listePointsProches.append((autrePoint, dico[j][1], dico[j][2], dico[j][3])) #same
            
            j += 1 
        
        dicoVoisins[k] = listePointsProches
        listePointsPosEllipses.insert(i, pointPos)
        i += 1
        
        
    return dicoVoisins

def getMeilleurVoisin(dicoVoisins, dico): #donne le meilleur voisin ou soit meme
    
    """toujours appeler apres avoir fait le tri"""
    
    dicoMeilleurVoisin = {}
    meilleurVoisin = ()
    diffCouleurMeilleurVoisin = ()
    
    for numEll, voisins in dicoVoisins.items():
        
        if voisins != []:
        
            try:
                diffCouleurMeilleurVoisin = diffCouleur(dico[numEll][1], Constante.IMGRGB[changementDeRepere(dico[numEll][4][1]), dico[numEll][4][0]]) #a la base le best voisin c'est soit meme
                meilleurVoisin = (dico[numEll][4], dico[numEll][1], dico[numEll][2], dico[numEll][3]) #meilleur voisin = soit meme
            except IndexError:
                diffCouleurMeilleurVoisin = ()
            
            for voisin in voisins:
                
                try:
                    diffCouleurVoisin = diffCouleur(voisin[1], Constante.IMGRGB[changementDeRepere(voisin[0][1]), voisin[0][0]])
                    
                    if diffCouleurVoisin < diffCouleurMeilleurVoisin or diffCouleurMeilleurVoisin == ():
                        meilleurVoisin = voisin
                        diffCouleurMeilleurVoisin = diffCouleurVoisin
                except IndexError:
                    pass
                
            dicoMeilleurVoisin[numEll] = meilleurVoisin
            
        else:
            dicoMeilleurVoisin[numEll] = ()
            
    return dicoMeilleurVoisin

def croisement(dicoRange):
    
    """dico range en param"""
    
    dicoVoisins = getVoisins(dicoRange)
    dicoMeilleurVoisin = getMeilleurVoisin(dicoVoisins, dicoRange)
    
    for k, v in dicoMeilleurVoisin.items():
        if v != ():
            rc = randomCroisement()
            
            if rc == 1: #si 1 : croisement des couleurs
                dicoRange[k][1] = v[1]
                
            elif rc == 2: #si 2 : coisement de W ou de H
                
                if dicoRange[k][7] == 'W': #si le meilleur est le W, on change le H
                    dicoRange[k][3] = v[3] #on veut que ca soit le Height du meilleur voisin qui soit pris a la place du height
                    
                elif dicoRange[k][7] == 'H':
                    dicoRange[k][2] = v[2] #on remplace le width par celui du meilleur voisin
    
                dicoRange[k][5] = getNewTuplePoints(dicoRange[k]) #dans tous les cas ces points sont modifies
                
            elif rc == 3: #si 3 : croisement couleurs et W ou H
                
                if dicoRange[k][7] == 'W': #si le meilleur est le W, on change le H
                    dicoRange[k][3] = v[3] #on veut que ca soit le Height du meilleur voisin qui soit pris a la place du height
    
                elif dicoRange[k][7] == 'H':
                    dicoRange[k][2] = v[2] #on remplace le width par celui du meilleur voisin
    
                dicoRange[k][1] = v[1] #dans tous les cas on change la couleur
                dicoRange[k][5] = getNewTuplePoints(dicoRange[k])
                
            dicoRange[k][0] = patches.Ellipse(dicoRange[k][4], dicoRange[k][2], dicoRange[k][3], angle=360, color = dicoRange[k][1]) #dans tous les cas on change l'ellipse
        
        else:
            pass
        
    return dicoRange #dico avec les croisements
    
def mutation(dicoAMuter): 
    
    """fonction a appeler lorsque le dicoAMuter (newDicoEllipses) est rempli"""
    
    listeTrucsModifies = []
    
    #global dicoAMuter
    
    #for i in range(len(dicoAMuter.values())): # chaque ellipse peut etre mutee
    for key in dicoAMuter.keys():
        for j in range(1,5): #les genes sont les elements d'indice 1 a 4 (color, w, h, pos) pas genes: patch, points , fitness
        
            if testMutation():
                dicoAMuter[key][j] = changeGene(j)
                dicoAMuter[key][0] = patches.Ellipse(dicoAMuter[key][4], dicoAMuter[key][2], dicoAMuter[key][3], angle=360, color = dicoAMuter[key][1])
                dicoAMuter[key][5] = getNewTuplePoints(dicoAMuter[key])
                listeTrucsModifies.append((key,j))
            else:
                continue
        
    return dicoAMuter #le dico a ete mute

def testMutation():
    
    numChoisi = 42
    numHasard = np.random.randint(1,1+1/Constante.CHANCE_MUTATION)
    
    if numHasard == numChoisi:
        return True
    else:
        return False

def changeGene(j):
    
    if j == 1:
        return pickARandomColorV2()
    elif j == 2 or j == 3:
        return getRandomWandH()
    elif j == 4:
        return getRandomPos()
    else:
        print("erreur, mauvais j dans la fonction changeGene")

def diffCouleur(color1, color2):
    
    """la couleur 1 est toujours celle de l'ellipse, la 2 celle du pixel de l'image originale"""
    
    newColor1 = [0,0,0]
    
    newColor1[0] = color1[0]*255
    newColor1[1] = color1[1]*255
    newColor1[2] = color1[2]*255
    
    return (abs(newColor1[0] - color2[0]) + abs(newColor1[1] - color2[1]) + abs(newColor1[2] - color2[2]))

def changementDeRepere(coordY):
    return int(Constante.HAUTEUR - coordY)

def distEntre2Points(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
def pickARandomColor():
    return(Constante.tabCouleur[np.random.randint(0, len(Constante.tabCouleur))])

def pickARandomColorV2():
    col = Constante.IMGRGB[np.random.randint(0, Constante.HAUTEUR), np.random.randint(0, Constante.LARGEUR)] 
    return (float(col[0])/255, float(col[1])/255, float(col[2])/255)

def getRandomPos():
    return(np.random.randint(0, Constante.LARGEUR), np.random.randint(0, Constante.HAUTEUR))

def getRandomWandH():
    return(np.random.randint(1, float(Constante.LARGEUR)/20))

def randomCroisement():
    return np.random.random_integers(3)

def getNewTuplePoints(valeurDico):
    
    """valeur dico 2 = W, 3 = H, 4 = pos"""
    
    pointPos = valeurDico[4]
    
    pointSommetHaut = (pointPos[0], pointPos[1] + round(float(valeurDico[3])/2))
    pointSommetBas = (pointPos[0], pointPos[1] - round(float(valeurDico[3])/2))
    pointSommetGauche = (pointPos[0] - round(float(valeurDico[2])/2), pointPos[1])
    pointSommetDroit = (pointPos[0] + round(float(valeurDico[2])/2), pointPos[1])
    
    pointCentreHautEtMilieu = (pointPos[0], round(float(pointPos[1] + pointSommetHaut[1])/2))
    pointCentreBasEtMilieu = (pointPos[0], round(float(pointPos[1] + pointSommetBas[1])/2))
    pointCentreGaucheEtMilieu = (round(float(pointPos[0] + pointSommetGauche[0])/2), pointPos[1])
    pointCentreDroitEtMilieu = (round(float(pointPos[0] + pointSommetDroit[0])/2), pointPos[1])
    
    pointCentreHautEtGauche = (pointCentreGaucheEtMilieu[0], pointCentreHautEtMilieu[1])
    pointCentreHautEtDroit = (pointCentreDroitEtMilieu[0], pointCentreHautEtMilieu[1])
    pointCentreBasEtGauche = (pointCentreGaucheEtMilieu[0], pointCentreBasEtMilieu[1])
    pointCentreBasEtDroit = (pointCentreDroitEtMilieu[0], pointCentreBasEtMilieu[1])    
    
    return (pointPos, pointSommetHaut, pointSommetBas, pointSommetGauche, pointSommetDroit, 
                      pointCentreHautEtMilieu, pointCentreBasEtMilieu, pointCentreGaucheEtMilieu, pointCentreDroitEtMilieu, 
                      pointCentreHautEtGauche, pointCentreHautEtDroit, pointCentreBasEtGauche, pointCentreBasEtDroit)

def main():
    
    """effets de bord, c = a"""
    
    a = creationEllipses() #a contient le dico initial des ellipses
    b = testFitness(a) #b contient le dico avec les ellipses rangees
    c = bestADN(b) #c contient le dico avec les ellipses ranges et le meilleur adn (W ou H)
    d = croisement(c) #d contient le dico avec les croisements effectues
    e = mutation(d) #e contient le dico avec les mutations
    
    for i in range(30):
        addAndShowEllipses(e)
        b = testFitness(e)
        c = bestADN(b)
        d = croisement(c)
        e = mutation(d)
    
        
if __name__ == '__main__':
    main()
    
