import os
from Error import *

def Menu() :
    while True:
        print("\n-------- Menu Bataille naval --------")
        print("1- Nouvelle partie")
        print("2- Reprendre une partie")
        print("3- Historiques des parties")
        print("0- Quitter")

        choiceMenu = TestInt()
        
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
            case _:
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")

def newGame(): 
    while True : 
        print("\n-------- Nouvelle partie --------")
        print("\n-------- Choix du plateau --------")
        print("LargeurxLongueurxHauteur")
        print("1- Plateau de 5x10x3")
        print("2- Plateau de 5x10x2")
        print("3- Plateau de 5x10x1")
        print("4- (Experimentale) Taille du plateau au choix")
        print("0- Retour")

        choiceNewGame = TestInt()

        match choiceNewGame : 
            case 0 :
                os.system('clear')
                return 
            case 1 :
                os.system('clear')
            case 2 :
                os.system('clear')
            case 3 :
                os.system('clear')
            case 4 :
                os.system('clear')
                width, length, height = personalizedBoard()
            case _ :
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")

def personalizedBoard() :
    while True : 
        print("\nQuel largeur pour le plateau ? ")
        width = TestInt()
        print("\nQuel largeur pour le plateau ? ")
        length = TestInt()
        print("\nQuel largeur pour le plateau ? ")
        height = TestInt()
        return (width, length, height)
