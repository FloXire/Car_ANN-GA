'''
Created on 6 mars 2018

@author: flo-1
'''

from Display.affichage import Affichage
import os
import json
import numpy as np


def paramsNp(tabParamsSansNp):
    paramsAvecNp = []
    for param in tabParamsSansNp:
        paramsAvecNp.append(np.array(param))
        
    return paramsAvecNp

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
    
    paramsAvecNp = paramsNp(tabParams)
    
    Affichage(tabParamsATester=paramsAvecNp)
    

def launchBestANN():
    
    cwd = os.getcwd()
    pathGraphes = os.path.normpath(cwd+'/graphes')
    
    listeParamsBestSansNp = []
    listeParamsBestAvecNp = []
    
    for dir in os.listdir(pathGraphes):
        if dir != "Mutations":
            for dir2 in os.listdir(os.path.normpath(pathGraphes+'/'+dir)):
                if dir2 != "FonctionHidden_Rectify" and dir2 != "FonctionHidden_Tanh" and dir2 != "NeuronesHidden_3" and dir2 != "NeuronesHidden_12" and dir2 != "NeuronesHidden_50":
                    for dir3 in os.listdir(os.path.normpath(pathGraphes+'/'+dir+'/'+dir2)):
                        if dir3[:3] == 'fig':
                            for dir4 in os.listdir(os.path.normpath(pathGraphes+'/'+dir+'/'+dir2+'/'+dir3)):
                                if dir4[:3] == 'tab':
                                    f = open(os.path.normpath(pathGraphes+'/'+dir+'/'+dir2+'/'+dir3+'/'+dir4))
                                    listeParamsBestSansNp.append(json.load(f)[2])
                                    f.close()
    
    for tabParams in listeParamsBestSansNp:
        listeParamsBestAvecNp.append(paramsNp(tabParams))                                    
    
    Affichage(tabParamsANN=listeParamsBestAvecNp)

def creationDossierGraphes():
    
    if not(os.path.exists('graphes')):
        os.makedirs('graphes')
        


if __name__ == '__main__':
    creationDossierGraphes()
    #launchANN("graphes/Mutations_0.1/fig_Date-1524280546.981705_Indiv-10_Mut-0.001_NeurHidden-7_Selection-E_Capteur-60/tabMeilleurs_Date-1524280546.981705_Indiv-10_Mut-0.001_NeurHidden-7_Selection-E_Capteur-60.txt")
    #launchANN("graphes/Elitiste/fig_Date-1524771742.6350503_Indiv-10_Mut-0.15_NeurHidden-7_Selection-E_Capteur-60/tabMeilleurs_Date-1524771742.6350503_Indiv-10_Mut-0.15_NeurHidden-7_Selection-E_Capteur-60.txt")
    launchBestANN()
    #launchRandomANN()