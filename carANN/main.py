'''
Created on 6 mars 2018

@author: flo-1
'''

from Display.affichage import Affichage
import os

def launchRandomANN():
    Affichage()
    
def creationDossierGraphes():
    
    if not(os.path.exists('graphes')):
        os.makedirs('graphes')


if __name__ == '__main__':
    creationDossierGraphes()
    launchRandomANN()