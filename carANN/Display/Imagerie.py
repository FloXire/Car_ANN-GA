'''
Created on 25 fevr. 2018

@author: flo-1
'''

import cv2
import numpy as np

class Imagerie():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        # Create a black image
        circuit = np.zeros((650,1024,3), np.uint8)
        #centre, longueur axes, rotation, debut et fin
        cv2.ellipse(circuit,(512,325),(350,190),0,0,360,(255,255,255),2) #petite ellipse
        cv2.ellipse(circuit,(512,325),(500,300),0,0,360,(255,255,255),2)
        
        cv2.imshow('circuit',circuit)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
Imagerie()