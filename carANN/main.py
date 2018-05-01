'''
Created on 6 mars 2018

@author: flo-1
'''

from Display.affichage import Affichage
import os
import json
import numpy as np


def launchRandomANN():
    Affichage()


def launchANN(emplacement):
    
    """newEmplacement = []
    i=0
    for caract in stringEmplacement:
        if caract == "\":
            newEmplacement.append("/")
        else:
            newEmplacement.append(caract)
        
        i+=1
    """      
    
    fileParams = open(emplacement, 'r')
    tabParams = json.load(fileParams)[2]
    paramsAvecNp = []
    
    for param in tabParams:
        paramsAvecNp.append(np.array(param))
    
    Affichage(tabParamsATester=paramsAvecNp)
    
    
def creationDossierGraphes():
    
    if not(os.path.exists('graphes')):
        os.makedirs('graphes')
        


if __name__ == '__main__':
    creationDossierGraphes()
    launchANN("graphes/Mutations_decroissantes/fig_Date-1525143502.5899553_Indiv-10_Mut-0.3_NeurHidden-7_Selection-E_Capteur-60/tabMeilleurs_Date-1525143502.5899553_Indiv-10_Mut-0.3_NeurHidden-7_Selection-E_Capteur-60.txt")
    #launchANN("graphes/Mutations_0.1/fig_Date-1524293659.6648533_Indiv-10_Mut-0.001_NeurHidden-7_Selection-E_Capteur-60/tabMeilleurs_Date-1524293659.6648533_Indiv-10_Mut-0.001_NeurHidden-7_Selection-E_Capteur-60.txt")
    #launchRandomANN()