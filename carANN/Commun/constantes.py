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
    
    NUMERO_CIRCUIT = 0
    VITESSE = 1
    DISTANCE_MAX_CAPTEURS = 60
    
    NOMBRE_INDIVIDUS_GRAPHE = 3
    
    DEGRE_POLYNOME_APPROXIMATION = 3
    NOMBRE_GENERATIONS_MAX = 35
    
    NOMBRE_NEURONES_IN = 5
    NOMBRE_NEURONES_HIDDEN = 7
    NOMBRE_NEURONES_OUT = 1
    
    CHANCE_MUTATION = 0.30
    
    METHODE_SELECTION = 'E' #TE = tres ellitiste, E = ellitiste
