'''
Created on 4 mai 2018

@author: flo-1
'''

import os
import glob
import json

cwd = os.getcwd()
mainDirectory = os.path.abspath(os.path.join(cwd, os.pardir))
pathGraphes = os.path.normpath(mainDirectory+'/graphes')


def testMeilleursParams(pathFolder):
    
    print(os.listdir(pathFolder))
    
    dicoListePath = {dir : [] for dir in os.listdir(pathFolder)}
    dicoTabAllMoyennes5Exp = {dir : [] for dir in os.listdir(pathFolder)}
    dicoMoyenneDesMoyennes = {dir : [] for dir in os.listdir(pathFolder)}
    dicoValeursDistancesMoy = {dir : {'meilleurs' : [], '3meilleurs' : []} for dir in os.listdir(pathFolder)}
    dicoReponseQuiEstLeMeilleur = {dir : {'meilleurs' : [], '3meilleurs' : []} for dir in os.listdir(pathFolder)}
    associationSousDossierNumero = {dir : {i : dir2 for dir2, i in zip(os.listdir(os.path.normpath(pathFolder+'/'+dir)), range(len(os.listdir(os.path.normpath(pathFolder+'/'+dir)))))} for dir in os.listdir(pathFolder)}
    
    for dir in os.listdir(pathFolder):
        for dir2 in os.listdir(os.path.normpath(pathFolder+'/'+dir)):
            dicoListePath[dir].append(glob.glob(os.path.normpath(pathFolder+'/'+dir+'/'+dir2+'/tabsMoyenne*.txt'))[0])
    
    for item in dicoListePath.items(): #item[0] = key
        dicoTabAllMoyennes5Exp[item[0]] = extractionTabsMoyenne5Exp(item) #dicoTabMoyenne5Exp[key][0] contient les tabsMoyenneMeilleurs pour toutes les sous experiences (ex capteur 40, 60, 90, 150 pour key = capteurs) de key        
    
    for item in dicoTabAllMoyennes5Exp.items():
        dicoMoyenneDesMoyennes[item[0]] = moyenneDesMoyennes(item)
        meilleurs = diffMoyenne5ExpToMoyenneAll(item, dicoMoyenneDesMoyennes[item[0]])
        dicoValeursDistancesMoy[item[0]]['meilleurs'] = meilleurs[0]
        dicoValeursDistancesMoy[item[0]]['3meilleurs'] = meilleurs[1]

    for item in dicoValeursDistancesMoy.items():
        for item2 in item[1].items():
            dicoReponseQuiEstLeMeilleur[item[0]][item2[0]] = quiEstLeMeilleur(associationSousDossierNumero, item[0], item2[1])
    
    print(dicoReponseQuiEstLeMeilleur)
    
    resultats = "Les resultats des tests sont les suivants : \n\n"
    for item in dicoReponseQuiEstLeMeilleur.items():
        for item2 in item[1].items():
            resultats += "    - parametre : " + str(item[0]) + ", categorie : " + str(item2[0]) + ", le meilleur sous-parametre est : " + str(item2[1]) + "\n"
        resultats += "\n"        
    
    print(resultats)
    
    fileEnregistrementDico = open(os.path.normpath(mainDirectory+'/DictionnaireResultatsDesTests_QuelsSontLesMeilleursParams.txt'), 'w')
    json.dump(dicoReponseQuiEstLeMeilleur, fileEnregistrementDico)
    fileEnregistrementDico.close()
    
    fileEnregistrementResultats = open(os.path.normpath(mainDirectory+'/QuelsSontLesMeilleursParams.txt'), 'w')
    fileEnregistrementResultats.write(resultats)
    fileEnregistrementResultats.close()
    
    
def extractionTabsMoyenne5Exp(itemDico):
    
    tabAllMoyennesMeilleurs5Exp = []
    tabAllMoyennes3Meilleurs5Exp = []
    
    for path in itemDico[1]:
        f = open(path, 'r')
        tabMoyennes = json.load(f)
        tabAllMoyennesMeilleurs5Exp.append(tabMoyennes[0])
        tabAllMoyennes3Meilleurs5Exp.append(tabMoyennes[1])
        f.close()
    
    return (tabAllMoyennesMeilleurs5Exp, tabAllMoyennes3Meilleurs5Exp)
    
    
def moyenneDesMoyennes(itemDicoAll): #doit renvoyer pour chaque item les tabs de la moyenne des moyennes pour les meilleurs et pour les 3 meilleurs
    
    tabMoyenneDesMoyennes = [[],[]]
    
    i = 0
    for tabAll in itemDicoAll[1]: #tab = tabMeilleurs puis tab3Meilleurs
        
        for points in zip(*tabAll):
            moyenne = 0
            j = 0
            
            for point in points:
                moyenne += point
                j += 1
            moyenne /= j
            
            tabMoyenneDesMoyennes[i].append(moyenne)
            
        i+=1
            
    return tabMoyenneDesMoyennes


def diffMoyenne5ExpToMoyenneAll(itemsDicoAllMoy, valeurDicoMoydesMoy):
    
    tabDiff = [[0]*len(itemsDicoAllMoy[1][0]),[0]*len(itemsDicoAllMoy[1][0])]
    
    i = 0
    for tabAll in itemsDicoAllMoy[1]:
        j = 0
        for tab in tabAll:
            diff = 0
            for point in zip(tab, valeurDicoMoydesMoy[i]):
                diff += distanceALaMoyenne(point[0], point[1])
            tabDiff[i][j] = diff
            j+=1
        i+=1
                
    return tabDiff


def distanceALaMoyenne(pt, ptMoyenne): 
    return pt-ptMoyenne


def quiEstLeMeilleur(dicoNumeroSousDossier, param, tabEcartsMoy):
    return(dicoNumeroSousDossier[param][tabEcartsMoy.index(max(tabEcartsMoy))])


testMeilleursParams(pathGraphes)