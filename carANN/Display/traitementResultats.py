'''
Created on 17 avr. 2018

@author: flo-1
'''

import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
import time

from Commun.constantes import Constante

def afficherResultats(compteurGenerations, tabResults):
    
    tabMoyenne = []
    for i in range(compteurGenerations-1) :
        moyenne = 0
        
        for j in range(Constante.NOMBRE_INDIVIDUS-1):
            moyenne += tabResults[i][j][0]
        
        moyenne /= Constante.NOMBRE_INDIVIDUS
        tabMoyenne.append(moyenne)
    
    plt.close()
    fig = plt.figure()
    ax = plt.axes()
    plt.title("Score moyen en fonction de la generation")
    ax = ax.set(xlabel="Numero de la generation", ylabel="Score moyen")
    plt.plot(np.arange(1, len(tabResults)), tabMoyenne, 'x')
    plt.show()
    
def takeFirst(tabResults):
    return tabResults[0]

def enregistrerResultats(compteurGenerations, tabResults):
    
    tabResultsOrdonne = []
    for i in range(compteurGenerations-1):
        tabResultsOrdonne.append(sorted(tabResults[i], key = takeFirst, reverse = True))
    
    tabMoyenne3meilleurs = []
    tabMeilleurs = []
    
    for i in range(compteurGenerations-1) :
        moyenne = 0
        
        for j in range(Constante.NOMBRE_INDIVIDUS_GRAPHE):
            moyenne += tabResultsOrdonne[i][j][0]
            
            if j == 0:
                tabMeilleurs.append(tabResultsOrdonne[i][j][0])
        
        moyenne /= Constante.NOMBRE_INDIVIDUS_GRAPHE
        tabMoyenne3meilleurs.append(moyenne)
    
    date = time.time()
    
    x = np.arange(1, Constante.NOMBRE_GENERATIONS_MAX)
    xLeastSquare = np.arange(1, Constante.NOMBRE_GENERATIONS_MAX-1, 0.01)
    
    #coeffs3Meilleurs = self.coeffsMoindresCarres(tabMoyenne3meilleurs)
    #coeffsMeilleurs = self.coeffsMoindresCarres(tabMeilleurs)

    coeffs3Meilleurs = np.polyfit(x, tabMoyenne3meilleurs, Constante.DEGRE_POLYNOME_APPROXIMATION)
    coeffsMeilleurs = np.polyfit(x, tabMeilleurs, Constante.DEGRE_POLYNOME_APPROXIMATION)
    
    
    tabY3Meilleurs = yMoindresCarres(xLeastSquare, coeffs3Meilleurs)
    tabYMeilleurs = yMoindresCarres(xLeastSquare, coeffsMeilleurs)
     
    
    for k in range(4):
        plt.close()
        
        fig = plt.figure()
        ax = plt.axes()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer = True)) #que des entiers sur l'axe des abscisses
        
        if k == 0:
            plt.title("Score moyen des 3 meilleurs individus de chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score moyen")
            plt.plot(x, tabMoyenne3meilleurs, 'x')
            plt.savefig('graphes/fig3Meilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN))
        
        elif k == 1:
            plt.title("Score du meilleur individu de chaque generation")
            ax = ax.set(xlabel="Numero de la generation", ylabel="Score")
            plt.plot(x, tabMeilleurs, 'rx')
            plt.savefig('graphes/figMeilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN))
        
        elif k == 2:
            plt.title("Score moyen des 3 meilleurs individus en fonction de la generation, \n approximation par un polynome de degre {}".format(Constante.DEGRE_POLYNOME_APPROXIMATION))
            ax = ax.set(xlabel="Numero de la generation", ylabel="Approximation score moyen")
            plt.plot(xLeastSquare, tabY3Meilleurs)
            plt.savefig('graphes/figApproximation3Meilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN))
        
        elif k == 3:
            plt.title("Score du meilleur individu en fonction de la generation, \n approximation par un polynome de degre {}".format(Constante.DEGRE_POLYNOME_APPROXIMATION))
            ax = ax.set(xlabel="Numero de la generation", ylabel="Approximation score")
            plt.plot(xLeastSquare, tabYMeilleurs, 'r')
            plt.savefig('graphes/figApproximationMeilleurs_Date-{0}_Indiv-{1}_Mut-{2}_NeurHidden-{3}.png'.format(date, Constante.NOMBRE_INDIVIDUS, Constante.CHANCE_MUTATION, Constante.NOMBRE_NEURONES_HIDDEN))
        

def J(points):
    
    x = np.arange(1, Constante.NOMBRE_GENERATIONS_MAX)
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
        
 