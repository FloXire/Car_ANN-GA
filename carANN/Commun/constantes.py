'''
Created on 7 mars 2018

@author: flo-1
'''

class Constante():
    '''
    classdocs
    '''

    NOMBRE_INDIVIDUS = 10 #il faut au minimum 8 individus par generation pour que pouvoir recréer (NOMBRE_INDIVIDU - NOMBRE_INDIVIDU//2) nouveaux individus sans avoir deux paires de parents identiques
    NOMBRE_INDIVIDUS_CROISEMENT = NOMBRE_INDIVIDUS//2 #il s'agit du nombre d'individus qui seront pris pour parents de la nouvelle generation
        
    NOMBRE_NEURONES_IN = 5
    NOMBRE_NEURONES_HIDDEN = 3
    NOMBRE_NEURONES_OUT = 1
    
    CHANCE_MUTATION = 0.1