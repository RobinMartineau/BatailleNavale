import json
import os
from Error import *
from coordinates import *

def Menu() :
    while True:
        print("\n-------- Menu Bataille naval --------")
        print("1- Nouvelle partie")
        print("2- Reprendre une partie")
        print("3- Historiques des parties")
        print("4- Supprimer les parties en cours")
        print("0- Quitter")

        choiceMenu = testInt()
        
        match choiceMenu : 
            
            case 0 : 
                break
            case 1 : 
                os.system('clear')
                newGame()
            case 2 :
                os.system('clear')
            case 3 :
                os.system('clear')
            case 4 :
                os.system('clear')
                deleteGame()
            case _:
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")

def newGame(): 
    while True : 
        print("\n-------- Nouvelle partie --------")
        print("\n-------- Choix du plateau --------")
        print("LargeurxLongueurxHauteur")
        print("1- Plateau de 5x10x3")
        print("2- (Experimentale) Taille du plateau au choix")
        print("0- Retour")

        choiceNewGame = testInt()

        match choiceNewGame : 
            case 0 :
                os.system('clear')
                return 
            case 1 :
                os.system('clear')
            case 2 :
                os.system('clear')
                width, length, height = personalizedBoard()
            case _ :
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")

def personalizedBoard() :
    while True : 
        print("\nQuel largeur pour le plateau ? ")
        width = testInt()
        print("\nQuel largeur pour le plateau ? ")
        length = testInt()
        print("\nQuel largeur pour le plateau ? ")
        height = testInt()
        return (width, length, height)

def deleteGame() : 
    while True: 
        print("\n-------- Suppression Parties en cours --------")
        print("1- Supprimer une partie précisemment")
        print("2- Supprimer l'ensemble des parties en cours")
        print("0- Retour")

        choiceDeleteGame = testInt()

        match choiceDeleteGame : 
            case 0 : 
                os.system('clear')
                return 
            case 1 : 
                os.system('clear')
            case 2 :
                os.system('clear')
                try : 
                    folder = "historicGames/"
                    choiceDeleteAll = input("Voulez-vous vraiment supprimer toutes les parties en cours ?")
                    
                    if choiceDeleteAll == "o" : 
                        filesDelete = False
                        for file in os.listdir(folder):
                            if file.endswith(".json") :
                                filePath = os.path.join(folder,file)
                                if get_state() is False:
                                    filesDelete = True
                                    print(f"Suppression du fichier : {file}")
                                    os.remove(filePath)
                        if filesDelete == False : 
                            print("Aucune partie n'a été supprimé !")
                    else : 
                        print("Suppression Annulé")
                    return
                except : 
                    print("Une erreur a eu lieu pendant la suppression des parties en cours")
            case _ : 
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")

