import json
import os
from Error import *
from coordinates import *
from plateau import *
import random


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
                gameExists()
            case 3 :
                os.system('clear')
                historicGames()
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
                game(5, 10, 3)
            case 2 :
                os.system('clear')
                width, height, depth = personalizedBoard()
                game(width, height, depth)
            case _ :
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")

def personalizedBoard() :
    while True : 
        print("\nQuel largeur pour le plateau ? ")
        width = testInt()
        print("\nQuel longueur pour le plateau ? ")
        height = testInt()
        print("\nQuel profondeur pour le plateau ? ")
        depth = testInt()
        return (width, height, depth)

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

def gameExists() :
    return

def historicGames() :
    return

## WIP start game and place boat aleatorily
def game(width: int, height: int, depth: int) :

    plateaujoueur1 = Plateau(5, 10, 3)
    plateaujoueur2 = Plateau(5, 10, 3)

    boatPlacement(plateaujoueur1,1)
    boatPlacement(plateaujoueur2,2)

    while True :
        # Lancement de la game ici
        
            
        return


# Place random boats on the plateau
def boatPlacement(plateau: Plateau,player_id: int) : 

    # WIP -> create random boat placement but not for all player yet 
    boat_sizes = [3, 2, 1]
    
    for size in boat_sizes:
        placed = False
        
        while not placed:
            is_horizontal = random.choice([True, False])
            
            if is_horizontal:
                x = random.randint(0, plateau.width - size)
                y = random.randint(0, plateau.height - 1)
            else:
                x = random.randint(0, plateau.width - 1)
                y = random.randint(0, plateau.height - size)
            
            z = random.randint(0, plateau.depth - 1)
            boat = Boat(f"Boat_{size}")
            
            if plateau.is_within_bounds(x, y, z):
                try:
                    plateau.place_boat((x, y, z), size, is_horizontal, boat)
                    placed = True
                except :
                    continue
    print(f"Plateau du joueur {player_id} :")
    plateau.display(True)
    