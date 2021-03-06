'''
Created on 17 avr. 2018

@author: flo-1
'''

import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
import time
import os
import json

from Commun.constantes import Constante
from ApresResultats.drawANN import schemaANN

def afficherResultats(compteurGenerations, tabResults):
    
    tabMax = []
    for i in range(compteurGenerations-1) :
        tabMax.append(max([tabResults[i][j][0] for j in range(Constante.NOMBRE_INDIVIDUS-1)]))

    plt.close()
    fig = plt.figure()
    ax = plt.axes()
    plt.title("Score du meilleur individu en fonction de la generation")
    ax = ax.set(xlabel="Numero de la generation", ylabel="Score moyen")
    plt.plot(np.arange(1, len(tabResults)), tabMax, 'x')
    plt.show()
    
def takeFirst(tabResults):
    return tabResults[0]

def enregistrerResultats(compteurGenerations, tabResults):
    
    tabResultsOrdonne = []
    for i in range(compteurGenerations-1):
        tabResultsOrdonne.append(sorted(tabResults[i], key = takeFirst, reverse = True))
    
    tabMoyenneAll = []
    tabMoyenne3meilleurs = []
    tabMeilleurs = []
    tabMeilleursCircuitFini = []
    tabMeilleursCircuitNonFini = []
    tabMeilleursEtParams = []    
    
    for i in range(compteurGenerations-1) :
        moyenne3 = 0
        moyenneAll = 0
        for j in range(Constante.NOMBRE_INDIVIDUS_GRAPHE):
            moyenneAll += tabResultsOrdonne[i][j][0]
            
            if j < (Constante.NOMBRE_INDIVIDUS_GRAPHE): #si c'est un des 3 meilleurs indivs
                moyenne3 += tabResultsOrdonne[i][j][0]
            
            if j == 0: #si c'est le meilleur indiv
                tabMeilleurs.append(tabResultsOrdonne[i][j][0])
                tabMeilleursEtParams.append((tabResultsOrdonne[i][j][0], tabResultsOrdonne[i][j][1]))
                
                if tabResultsOrdonne[i][j][2]: #si circuit fini
                    tabMeilleursCircuitFini.append((i+1, tabResultsOrdonne[i][j][0]))
                else:
                    tabMeilleursCircuitNonFini.append((i+1, tabResultsOrdonne[i][j][0]))
                
                
        moyenne3 /= Constante.NOMBRE_INDIVIDUS_GRAPHE
        moyenneAll /= Constante.NOMBRE_INDIVIDUS
        tabMoyenne3meilleurs.append(moyenne3)
        tabMoyenneAll.append(moyenneAll)
    
    tabMeilleursRanges = sorted(tabMeilleursEtParams, key = takeFirst, reverse = True)
    meilleursParams = tabMeilleursRanges[0][1]
    meilleursParamsSansNp = []
        
    for param in meilleursParams:
        meilleursParamsSansNp.append(param.tolist())
    
    date = time.time()
    
    x = np.arange(1, Constante.NOMBRE_GENERATIONS_MAX+1)
    xLeastSquare = np.arange(1, Constante.NOMBRE_GENERATIONS_MAX+0.01, 0.01)
    
    xCircuitFini = [tabMeilleursCircuitFini[i][0] for i in range(len(tabMeilleursCircuitFini))]
    yCircuitFini = [tabMeilleursCircuitFini[i][1] for i in range(len(tabMeilleursCircuitFini))]
    
    xCircuitNonFini = [tabMeilleursCircuitNonFini[i][0] for i in range(len(tabMeilleursCircuitNonFini))]
    yCircuitNonFini = [tabMeilleursCircuitNonFini[i][1] for i in range(len(tabMeilleursCircuitNonFini))]
    
    #coeffs3Meilleurs = self.coeffsMoindresCarres(tabMoyenne3meilleurs)
    #coeffsMeilleurs = self.coeffsMoindresCarres(tabMeilleurs)

    #coeffs3Meilleurs = np.polyfit(x, tabMoyenne3meilleurs, Constante.DEGRE_POLYNOME_APPROXIMATION)
    #coeffsMeilleurs = np.polyfit(x, tabMeilleurs, Constante.DEGRE_POLYNOME_APPROXIMATION)
    
    #tabY3Meilleurs = yMoindresCarres(xLeastSquare, coeffs3Meilleurs)
    #tabYMeilleurs = yMoindresCarres(xLeastSquare, coeffsMeilleurs)
     
    os.makedirs('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN, Constante.METHODE_SELECTION, Constante.DISTANCE_MAX_CAPTEURS))
    
    for k in range(3):
        plt.close()
        
        fig = plt.figure()
        ax = plt.axes()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer = True)) #que des entiers sur l'axe des abscisses
        
        if k == 0:
            plt.title("Score moyen des 3 meilleurs individus de chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score moyen")
            plt.plot(x, tabMoyenne3meilleurs, 'x')
            plt.savefig('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}/fig3Meilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection{4}_Capteur{5}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN, Constante.METHODE_SELECTION, Constante.DISTANCE_MAX_CAPTEURS))
        
        elif k == 1:
            plt.title("Score du meilleur individu de chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score")
            plt.plot(xCircuitFini, yCircuitFini, 'rx')
            plt.plot(xCircuitNonFini, yCircuitNonFini, 'x')
            plt.savefig('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}/figMeilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN, Constante.METHODE_SELECTION, Constante.DISTANCE_MAX_CAPTEURS))
        
        elif k == 2:
            plt.title("Score moyen des individus de chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score moyen")
            plt.plot(x, tabMoyenneAll, 'x')
            plt.savefig('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}/figMoyenneAll_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN, Constante.METHODE_SELECTION, Constante.DISTANCE_MAX_CAPTEURS))
        
        
        #moindres carres, peu pertinent
        """"elif k == 2:
            plt.title("Score moyen des 3 meilleurs individus en fonction de la generation, \n approximation par un polynome de degre {}".format(Constante.DEGRE_POLYNOME_APPROXIMATION))
            ax = ax.set(xlabel="Numero de la generation", ylabel="Approximation score moyen")
            plt.plot(xLeastSquare, tabY3Meilleurs)
            plt.savefig('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}/figApproximation3Meilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN))
        
        elif k == 3:
            plt.title("Score du meilleur individu en fonction de la generation, \n approximation par un polynome de degre {}".format(Constante.DEGRE_POLYNOME_APPROXIMATION))
            ax = ax.set(xlabel="Numero de la generation", ylabel="Approximation score")
            plt.plot(xLeastSquare, tabYMeilleurs, 'r')
            plt.savefig('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}/figApproximationMeilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN))
        """
        
    arboFic = 'graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}/schemaMeilleurReseau_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN, Constante.METHODE_SELECTION, Constante.DISTANCE_MAX_CAPTEURS)
    schemaANN(Constante.NOMBRE_NEURONES_IN, Constante.NOMBRE_NEURONES_HIDDEN, meilleursParamsSansNp, save = True, emplacement = arboFic)
    
    fileTabs = open('graphes/fig_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}/tabMeilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}_Selection-{4}_Capteur-{5}.txt'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN, Constante.METHODE_SELECTION, Constante.DISTANCE_MAX_CAPTEURS), "w")
    dataFileTabs = [tabMeilleurs, tabMoyenne3meilleurs, meilleursParamsSansNp] #pb de compatibilite json et np, il faudra reformer les params sous forme de tableau np
    
    json.dump(dataFileTabs, fileTabs)    
    

def J(points):
    
    x = np.arange(1, Constante.NOMBRE_GENERATIONS_MAX+1)
    J = np.eye(len(points), Constante.DEGRE_POLYNOME_APPROXIMATION + 1)

    for i in range(len(points)):
        for j in range(Constante.DEGRE_POLYNOME_APPROXIMATION,-1,-1):
            J[i][Constante.DEGRE_POLYNOME_APPROXIMATION - j] = x[i]**j

    return J

def transpose(J):

    transposee = np.eye(len(J[0]), len(J))
    for i in range(len(J)):
        for j in range(len(J[0])):
            transposee[j][i] = J[i][j]

    return transposee

def coeffsMoindresCarres(points):
    
    #try:
    J = J(points)
    transposeeJ = transpose(J)
    produit = np.matmul(transposeeJ,J)
    inverse = np.linalg.inv(produit)
    produitV2 = np.matmul(inverse, transposeeJ)
            
    y = np.eye(len(points), 1)
    for i in range(len(points)):
        y[i] = points[i]

    THETA = np.matmul(produitV2, y)

    #print THETA

    """"S = "Y = "
    for i in range(degPolynomeRecherche):
        S += str(THETA[i][0]) + "X^" + str(degPolynomeRecherche-i) + " + "
    S += str(THETA[degPolynomeRecherche][0])

    print S"""
    
    #except:
    #    print("degre du polynome recherche trop grand par rapport au nombre de points donnes")
    
    return THETA
 

def yMoindresCarres(x, coeffs):
    
    tabY = []
    
    for pt in x:
        y = 0
        
        for j in range(0, len(coeffs)):
            y += coeffs[len(coeffs)-1- j] * (pt ** j)
            
        tabY.append(y)
    
    return tabY
        
 