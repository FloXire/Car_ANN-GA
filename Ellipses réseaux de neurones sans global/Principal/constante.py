'''
Created on 24 dec. 2017

@author: flo-1
'''

import cv2
import numpy

class Constante:
    '''
    classdocs
    '''
    
    CHANCE_MUTATION = 0.001
    CHANCE_RETENIR_HIGH_FITNESS = 0.3
    CHANCE_RETENIR_LOW_FITNESS = 0.1
        
    POPULATION = 20
    NOMBRE_MAX_DE_GENERATIONS = 25000
        
    IMAGE_ATTENDUE = 'image2ellipses.jpg'
    
    IMGBGR = cv2.imread(IMAGE_ATTENDUE)
    IMGRGB = cv2.cvtColor(IMGBGR, cv2.COLOR_BGR2RGB)
    
    HAUTEUR = IMGRGB.shape[0]
    LARGEUR = IMGRGB.shape[1]
    
    NOMBRE_ELLIPSES = 5000    
    NOMBRE_HIGH_FITNESS_RETENUS = int(NOMBRE_ELLIPSES * CHANCE_RETENIR_HIGH_FITNESS)
    
    HINCHES = HAUTEUR * 0.010416666666819
    LINCHES = LARGEUR * 0.010416666666819
    
    """tabCouleurs = []
    
    with open("liste_couleurs", 'r') as file:
        for line in file:
            line = line.strip()
            a,b,c = line.split()
            tabCouleurs.append((float(a)/255, float(b)/255, float(c)/255))
            
    file.close()"""
    
    """tabCouleur = []
    
    for i in range(0, HAUTEUR, 3):
        for j in range(0, LARGEUR, 3):
            #if IMGRGB[i,j].tolist() not in tabCouleur:
            tabCouleur.append((float(IMGRGB[i,j].tolist()[0])/255, float(IMGRGB[i,j].tolist()[1])/255, float(IMGRGB[i,j].tolist()[2])/255)) #rgb inverse par rapporrt a la normale
            #print(len(tabCouleur))

    #numpy.savetxt("liste_couleurs", tabCouleur, fmt='%i')"""
    
    """for i in range(15):
        for j in range(15):
            IMGRGB[i, j] = [255,255,255]
    
    cv2.imshow("ssfd", IMGRGB)
    cv2.waitKey()"""