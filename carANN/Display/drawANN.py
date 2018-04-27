'''
Created on 27 avr. 2018

@author: flo-1
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import json

from Commun.constantes import Constante

"""emplacement = "../graphes/Identity/fig_Date-1524598213.7492716_Indiv-10_Mut-0.15_NeurHidden-7_Selection-TE_Capteur-60/tabMeilleurs_Date-1524598213.7492716_Indiv-10_Mut-0.15_NeurHidden-7_Selection-TE_Capteur-60.txt"
filePoids = open(emplacement, 'r')
poids = json.load(filePoids)[2]
print(poids)"""

def schemaANN(nbEntree, nbHidden, poids, save = False, emplacement = ""):
    
    ecartX = 800
    ecartY = 150
    rayon = 30
    
    plt.close("all")
    fig = plt.figure()
    ax = plt.axes()
    plt.axis("scaled")
    plt.axis("off")
    plt.axis([0, (ecartX+50)*2-ecartX/2.5, 0, ecartY*(1+max(nbEntree, nbHidden))])
    
    if save:
        plt.title("Schema reseau de neurones du meilleur individu")
    else:
        plt.title("Schema reseau de neurones de l'individu sur le circuit")
    
    if max(nbEntree, nbHidden) == nbEntree:        
        coordCentreEntree = []
        for i in range(1, nbEntree+1):
            coordCentreEntree.append((50, ecartY*i))
        
        coordYNeuroneMilieu = (nbEntree*ecartY)/2 + ecartY/2 
        
        if nbHidden%2 == 0:
            decalage = ecartY/2
        else:
            decalage = 0
        
        coordCentreHidden = []
        for j in range(1, nbHidden+1):
            coordCentreHidden.append((ecartX+50, coordYNeuroneMilieu + decalage + ecartY*(j-(nbHidden//2)-1)))
            
    else:
        coordCentreHidden = []
        for j in range(1, nbHidden+1):
            coordCentreHidden.append((ecartX+50, ecartY*j))
        
        coordYNeuroneMilieu = (nbHidden*ecartY)/2 + ecartY/2
        
        if nbEntree%2 == 0:
            decalage = ecartY/2
        else:
            decalage = 0
        
        coordCentreEntree = []
        for i in range(1, nbEntree+1):
            coordCentreEntree.append((50, coordYNeuroneMilieu + decalage + ecartY*(i-(nbEntree//2)-1)))
    
    coordCentreSortie = [[50+ecartX*2-ecartX/2.5, coordYNeuroneMilieu]]
    tabCoord = coordCentreEntree + coordCentreHidden + coordCentreSortie
    
    i = 0
    for poidsNeuroneEntreeToHidden in poids[0]:
        j = 0
        for Poids in poidsNeuroneEntreeToHidden:
            if Poids > Constante.DETECTION_POIDS:
                ax.add_line(lines.Line2D([coordCentreEntree[-i-1][0]+rayon+4, coordCentreHidden[-j-1][0]-rayon-4], [coordCentreEntree[-i-1][1], coordCentreHidden[-j-1][1]], linewidth = 12*abs(Poids), color = (0,1,0)))
            elif Poids < - Constante.DETECTION_POIDS:
                ax.add_line(lines.Line2D([coordCentreEntree[-i-1][0]+rayon+4, coordCentreHidden[-j-1][0]-rayon-4], [coordCentreEntree[-i-1][1], coordCentreHidden[-j-1][1]], linewidth = 12*abs(Poids), color = (1,0,0)))
            j += 1
        i += 1        
    
    k = 0
    for poidsNeuroneHiddenToSortie in poids[2]:
        l = 0
        for Poids in poidsNeuroneHiddenToSortie:
            if Poids > Constante.DETECTION_POIDS:
                ax.add_line(lines.Line2D([coordCentreHidden[-k-1][0]+rayon+4, coordCentreSortie[-l-1][0]-rayon-4], [coordCentreHidden[-k-1][1], coordCentreSortie[-l-1][1]], linewidth = 12*abs(Poids), color = (0,1,0)))
            elif Poids < - Constante.DETECTION_POIDS:
                ax.add_line(lines.Line2D([coordCentreHidden[-k-1][0]+rayon+4, coordCentreSortie[-l-1][0]-rayon-4], [coordCentreHidden[-k-1][1], coordCentreSortie[-l-1][1]], linewidth = 12*abs(Poids), color = (1,0,0)))
            l += 1
        k += 1
    
    for coord in tabCoord:
        ax.add_patch(patches.Circle(coord, rayon, fill=False, linewidth = 4, ec = (0,0,1,0.7)))

    if save:
        plt.savefig(emplacement)
    else:
        plt.show()
    
#schemaANN(5,7, poids)
    
    
    