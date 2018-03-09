'''
Created on 8 mars 2018

@author: flo-1
'''

from Commun.constantes import Constante
import numpy as np

    
def takeFirst(scoreEtParams):
    return scoreEtParams[0]

def triIndividus(tabScoresEtParams):
    return [sorted(tabScoresEtParams, key = takeFirst, reverse = True)[i][1] for i in range(len(tabScoresEtParams))] #retourne le tab des params ranges dans l'ordre du meilleur individu au moins bon

def croisements(tabParams):
        
    """selection elitiste, on prend les meilleurs individus (la moitie)"""
    """croisement des poids uniquement puisque les biais sont a 0"""
            
    tabParamsCroisement = tabParams[:Constante.NOMBRE_INDIVIDUS_CROISEMENT] #pas d'effets de bords
    tabParamsApresCroisement = tabParamsCroisement[:]
    tabPairesParents = []
    
    """a faire : checker si une paire de darons a deja ete realisee"""
    
    for i in range(Constante.NOMBRE_INDIVIDUS - Constante.NOMBRE_INDIVIDUS_CROISEMENT): #nous allons creer (Constante.NOMBRE_INDIVIDUS - Constante.NOMBRE_INDIVIDUS//2) nouveaux individus afin de toujours garder le meme nombre d'individus
        
        nouvelIndividu = [np.zeros((Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN)), np.zeros((Constante.NOMBRE_NEURONES_HIDDEN)), np.zeros((Constante.NOMBRE_NEURONES_HIDDEN, Constante.NOMBRE_NEURONES_OUT)), np.zeros((Constante.NOMBRE_NEURONES_OUT))]
                    
        individu1 = np.random.randint(Constante.NOMBRE_INDIVIDUS_CROISEMENT) #nombre entre 0 et (NOMBRE_INDIVIDUS_CROISEMENT-1)
        individu2 = np.random.randint(Constante.NOMBRE_INDIVIDUS_CROISEMENT)
                    
        while (individu2 == individu1) or ([individu1, individu2] in tabPairesParents) or ([individu2, individu1] in tabPairesParents): #ainsi, individu1 != individu2
            individu1 = np.random.randint(Constante.NOMBRE_INDIVIDUS_CROISEMENT) 
            individu2 = np.random.randint(Constante.NOMBRE_INDIVIDUS_CROISEMENT)
        
        tabPairesParents.append([individu1, individu2])
        
        j=0
        for param in zip(tabParamsCroisement[individu1], tabParamsCroisement[individu2]): #param[0][0] designe les poids de la couche d'entree a la couche cachee du premier individu et param[0][1] ces memes poids pour le second                 
            
            if j == 0: #il s'agit des poids des connections entre la couche d'entree et la couche cachee
                
                for poidsOneInToAllHidden in range(Constante.NOMBRE_NEURONES_IN): #pour chaque ensemble de poids d'un neurone en entree a TOUS les neurones de la couche cachee
                    for poidsOneInToOneHidden in range(Constante.NOMBRE_NEURONES_HIDDEN): #pour chaque poids d'un neurone en entree a UN neurone de la couche cachee
                        meanOrCrossover = np.random.random_integers(0, 1) #soit 0, soit 1
                        
                        if meanOrCrossover == 0: #on fait la moyenne des parametres
                            newParam = (param[0][poidsOneInToAllHidden][poidsOneInToOneHidden] + param[1][poidsOneInToAllHidden][poidsOneInToOneHidden]) / 2
                                        
                        elif meanOrCrossover == 1: #on recopie le parametre d'un des deux parents a l'identique
                            parent = np.random.random_integers(0, 1) #on choisit aleatoirement de quel parent le nouvel individu va recevoir le parametre
                            newParam = param[parent][poidsOneInToAllHidden][poidsOneInToOneHidden]
                        
                        nouvelIndividu[j][poidsOneInToAllHidden][poidsOneInToOneHidden] = newParam
                        
            elif j == 2: #il s'agit des poids des connections entre la couche cachee et la couche de sortie
                
                for poidsOneHiddenToAllOut in range(Constante.NOMBRE_NEURONES_HIDDEN): #pour chaque ensemble de poids d'un neurone de la couche cachee a TOUS les neurones de la couche de sortie
                    for poidsOneHiddenToOneOut in range(Constante.NOMBRE_NEURONES_OUT): #pour chaque poids d'un neurone de la couche cachee a UN neurone de la couche de sortie
                        meanOrCrossover = np.random.random_integers(0, 1)
                        
                        if meanOrCrossover == 0: #on fait la moyenne des parametres des deux parents
                            newParam = (param[0][poidsOneHiddenToAllOut][poidsOneHiddenToOneOut] + param[1][poidsOneHiddenToAllOut][poidsOneHiddenToOneOut]) / 2
                            
                        elif meanOrCrossover == 1: #on recopie le parametre d'un des deux parents a l'identique
                            parent = np.random.random_integers(0, 1) #on choisit aleatoirement de quel parent le nouvel individu va recevoir le parametre
                            newParam = param[parent][poidsOneHiddenToAllOut][poidsOneHiddenToOneOut]
                            
                        nouvelIndividu[j][poidsOneHiddenToAllOut][poidsOneHiddenToOneOut] = newParam

            j += 1
        
        tabParamsApresCroisement.append(nouvelIndividu)
        
    return tabParamsApresCroisement


def mutations(listeCroisee):
    
    tabAvecMutations = listeCroisee[:] #limitation des effets de bords
        
    for i in range(1, len(listeCroisee)): #on ne veut pas de mutations pour le meilleur individu qui reste identique a la generation suivante
        for j in range(0, 4, 2):
            
            if j == 0:
                for k in range(Constante.NOMBRE_NEURONES_IN):
                    for l in range(Constante.NOMBRE_NEURONES_HIDDEN):
                        if np.random.random() < Constante.CHANCE_MUTATION:
                            tabAvecMutations[i][j][k][l] = np.random.normal(0, 0.1)
                            print("une mutation a eu lieu en : " + str(i) + ", " + str(j) + ", " + str(k) + ", " + str(l))
            
            elif j == 2:
                for k in range(Constante.NOMBRE_NEURONES_HIDDEN):
                    for l in range(Constante.NOMBRE_NEURONES_OUT):
                        if np.random.random() < Constante.CHANCE_MUTATION:
                            tabAvecMutations[i][j][k][l] = np.random.normal(0, 0.1)
                            print("Une mutation a eu lieu en : " + str(i) + ", " + str(j) + ", " + str(k) + ", " + str(l))
                            
    return tabAvecMutations

