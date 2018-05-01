'''
Created on 30 avr. 2018

@author: flo-1
'''

import os
import glob
import json
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

def moyenneNuage(pathFolder):
    
    emplacementTabs = []
    tabMeilleurs = []
    tab3Meilleurs = []
    
    for path, dirs, files in os.walk(pathFolder):
        for dir in dirs:
            emplacementTabs.append(os.path.normpath(glob.glob(pathFolder+'/'+dir+'/tab*.txt')[0]))
    
    for pathTab in emplacementTabs:
        f = open(pathTab, 'r')
        tabTout = json.load(f)
        tabMeilleurs.append(tabTout[0])
        tab3Meilleurs.append(tabTout[1])
        f.close()
    
    meilleursParGen = zip(*tabMeilleurs) #[0] renvoie le tuble des meilleurs de la generation 0
    meilleurs3ParGen = zip(*tab3Meilleurs)
    
    tabMoyenneMeilleurs = []
    tabMoyenne3Meilleurs = []
    
    for meilleurs in meilleursParGen:
        i = 0
        moyenne = 0
        for meilleur in meilleurs:
            moyenne += meilleur
            i += 1
        moyenne /= i
        tabMoyenneMeilleurs.append(moyenne)

    for meilleurs3 in meilleurs3ParGen:
        j = 0
        moyenne3 = 0
        for meilleur3 in meilleurs3:
            moyenne3 += meilleur3
            j += 1
        moyenne3 /= j
        tabMoyenne3Meilleurs.append(moyenne3)
    
    x = np.arange(1, len(tabMoyenneMeilleurs)+1)
    
    for k in range(2):
        
        plt.close()
        fig = plt.figure()
        ax = plt.axes()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer = True)) #que des entiers sur l'axe des abscisses
        
        if k == 0:
            plt.title("Moyenne sur 5 experiences du score moyen des 3 meilleurs individus\nde chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score moyen")
            plt.plot(x, tabMoyenne3Meilleurs, 'x')
            plt.savefig(os.path.normpath(pathFolder + '/moyenne5Exp3Meilleurs'))
        
        elif k == 1:
            plt.title("Moyenne sur 5 experiences du score du meilleur individu\nde chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score")
            plt.plot(x, tabMoyenneMeilleurs, 'x')
            plt.savefig(os.path.normpath(pathFolder + '/moyenne5ExpMeilleurs'))
     
        
moyenneNuage('../graphes/Tanh')
