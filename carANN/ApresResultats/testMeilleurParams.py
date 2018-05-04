'''
Created on 4 mai 2018

@author: flo-1
'''

import os
import glob
import json

def testMeilleursParams(pathFolder):
    bool = True
    listePathCapteurs = []
    listePathCroisement = []
    listePathFonctionHidden = []
    listePathMutations = []
    listePathNeuronesHidden = []
    listePathSelection = []
    
    print(glob.glob(pathFolder + '/*.txt'))

    for path, dirs, files in os.walk(pathFolder):
        if bool == True:
            for dir in dirs:
                print(os.path.normpath(glob.glob(pathFolder+'/'+dir+'/*.txt')))
                print(os.path.normpath(glob.glob(pathFolder+'/'+dir+'/*.txt')))
            bool = False
                
testMeilleursParams('../graphes')