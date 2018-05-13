'''
Created on 7 mars 2018

@author: flo-1
'''

class Constante():
    '''
    classdocs
    '''
    
    NOMBRE_INDIVIDUS = 75 #il faut au minimum 8 individus par generation pour pouvoir recreer (NOMBRE_INDIVIDU - NOMBRE_INDIVIDU//2) nouveaux individus sans avoir deux paires de parents identiques
    NOMBRE_INDIVIDUS_CROISEMENT = NOMBRE_INDIVIDUS//2 #il s'agit du nombre d'individus qui seront pris pour parents de la nouvelle generation
    POSSIB_DAVOIR_MOINS_DINDIVIDUS = False #si True : possibilite davoir moins de 8 indivs mais risque non nul d'avoir des paires de parents identiques
    
    NUMERO_CIRCUIT = 2
    VITESSE = 1
    DISTANCE_MAX_CAPTEURS = 60
    
    NOMBRE_INDIVIDUS_GRAPHE = 3
    
    DEGRE_POLYNOME_APPROXIMATION = 3
    NOMBRE_GENERATIONS_MAX = 12
    
    NOMBRE_NEURONES_IN = 5
    NOMBRE_NEURONES_HIDDEN = 7
    NOMBRE_NEURONES_OUT = 1
    
    CHANCE_MUTATION = 0.01
    MUTATIONS_DECROISSANTES = 'N' #O pour oui, N pour non
    
    METHODE_SELECTION = 'TE' #TE = tres ellitiste, E = ellitiste
    
    METHODE_CROISEMENT = 'hybride' #hybride, moyenne ou crossover
    
    FONCTION_ACTIVATION = 'identity' #tanh ou identity
    
    DETECTION_POIDS = 0
