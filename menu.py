import json
import os
from Error import *
from coordinates import *
from plateau import *
from animation_shell import *
import random
import time

#region Menu Function
def Menu() :
    print(AscciNameBatailleNavale())
    input("Appuyez sur Entrée pour continuer...")
    os.system('clear')
    while True:
        print(
            "┌───────────────────────────┐\n"
            "│      MENU PRINCIPAL       │\n"
            "├───────────────────────────┤\n"
            "│  1 · Nouvelle partie      │\n"
            "│  2 · Reprendre une partie │\n"
            "│  3 · Historique des jeux  │\n"
            "│  4 · Supprimer sauvegardes│\n"
            "│  0 · Quitter              │\n"
            "└───────────────────────────┘"
        )

        choiceMenu = testInt()

        os.system('clear')
        match choiceMenu : 
            
            case 0 : 
                break
            case 1 : 
                newGame()
            case 2 :
                resumeGame()
            case 3 :
                historicGames()
            case 4 :
                deleteGame()
            case _:
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")
#endregion

#region New Game Functions
def newGame(): 
    while True : 
        print(
            "┌──────────────────────────────────────┐\n"
            "│           NOUVELLE  PARTIE           │\n"
            "├──────────────────────────────────────┤\n"
            "│           Choix du plateau           │\n"
            "│     Largeur × Longueur × Hauteur     │\n"
            "│                                      │\n"
            "│  1 · Plateau 5 × 10 × 3              │\n"
            "│  2 · (Expérimental) Taille au choix  │\n"
            "│  0 · Retour                          │\n"
            "└──────────────────────────────────────┘"
        )


        choiceNewGame = testInt()
        
        os.system('clear')
        match choiceNewGame : 
            case 0 :
                return 
            case 1 :
                game(5, 10, 3)
            case 2 :
                width, height, depth = personalizedBoard()
                game(width, height, depth)
            case _ :
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")
#endregion

#region Personalized Board Functions
def personalizedBoard() :
    while True : 
        print("\nQuel largeur pour le plateau ? ")
        width = testInt()
        print("\nQuel longueur pour le plateau ? ")
        height = testInt()
        print("\nQuel profondeur pour le plateau ? ")
        depth = testInt()
        return (width, height, depth)
#endregion

#region Delete Game Functions
def deleteGame() : 
    while True: 
        print(
            "┌─────────────────────────────────────────────┐\n"
            "│      SUPPRESSION DES  PARTIES EN COURS      │\n"
            "├─────────────────────────────────────────────┤\n"
            "│  1 · Supprimer une partie précisément       │\n"
            "│  2 · Supprimer toutes les parties en cours  │\n"
            "│  0 · Retour                                 │\n"
            "└─────────────────────────────────────────────┘"
        )


        choiceDeleteGame = testInt()

        os.system('clear')
        match choiceDeleteGame : 
            case 0 : 
                return 
            case 1 : 
                try : 
                    folder = "saved_games/"
                    files = [f for f in os.listdir(folder) if f.endswith(".json")]

                    if not files :
                        print("Aucune partie en cours à supprimer !")
                        return
                    
                    print("Voici les parties en cours disponibles :\n")
                    for index, file in enumerate(files):
                        print(f"{index + 1} · {file}")

                    print("\nChoisissez le numéro de la partie à supprimer : ")
                    choiceDelete = testInt() - 1
                    if 0 <= choiceDelete < len(files):
                        filePath = os.path.join(folder, files[choiceDelete])
                        os.remove(filePath)

                        os.system('clear')
                        print(f"\nLa partie '{files[choiceDelete]}' a été supprimée.\n")

                    else:
                        print("\nNuméro invalide. Aucune partie supprimée.\n")
                    
                    return
                except :

                    print("\nUne erreur a eu lieu pendant la suppression de la partie en cours\n")

            case 2 :
                try : 
                    folder = "saved_games/"
                    choiceDeleteAll = input("Voulez-vous vraiment supprimer toutes les parties en cours ? (o/n) : ")
                    
                    if choiceDeleteAll == "o" : 
                        filesDelete = False
                        print()
                        for file in os.listdir(folder):
                            if file.endswith(".json") :
                                filePath = os.path.join(folder,file)
                                if get_state() is False:
                                    filesDelete = True
                                    print(f"Suppression du fichier : {file}")
                                    os.remove(filePath)
                        if filesDelete == False : 
                            print("Aucune partie n'a été supprimé !")
                        print()
                    else : 
                        print("Suppression Annulé")
                    return
                except : 
                    print("Une erreur a eu lieu pendant la suppression des parties en cours")
            case _ : 
                os.system('clear')
                print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")
#endregion

# WIP resume game function
def resumeGame() :
    return

#region Historic Games Functions
def historicGames() :
    try : 
        folder = "saved_games/"
        files = [f for f in os.listdir(folder) if f.endswith(".json")]

        if not files :
            print("Aucune partie en cours à consulter !")
            return
                    
        print("Voici les parties en cours disponibles :\n")
        for index, file in enumerate(files):
            print(f"{index + 1} · {file}")

        print("\nQuelle partie voulez-vous consulter ?")
        choiceVisible = testInt() - 1
        print("\nVoulez-vous ouvrir cette partie dans un fichier texte (sinon dans le terminal) ? (o/n)")
        choiceFile = input()
        if 0 <= choiceVisible < len(files):
            filePath = os.path.join(folder, files[choiceVisible])
            os.system('clear')
            if choiceFile == "o" :
                os.system(f'xdg-open "{filePath}" >/dev/null 2>&1')
            else :
                print(f"\nContenu de la partie '{files[choiceVisible]}':\n")
                with open(filePath, 'r') as file:
                    data = json.load(file)
                    print(json.dumps(data, indent=4))
                print("\nFin de la consultation de la partie.\n")
        else:
            print("\nNuméro invalide. Aucune partie consulté.\n")
                    
        return
    except :
        print("\nUne erreur a eu lieu pendant la consultation de la partie\n")
#endregion

## WIP start game and place boat aleatorily
def game(width: int, height: int, depth: int) :

    plateaujoueur1 = Plateau(width, height, depth)
    plateaujoueur2 = Plateau(width, height, depth)

    boatPlacement(plateaujoueur1,1)
    boatPlacement(plateaujoueur2,2)

    player1Boat1Name = "Alpha"
    player1Boat2Name = "Beta"
    player1Boat3Name = "Charlie"
    player2Boat1Name = "Red force"
    player2Boat2Name = "Oro Jackson"
    player2Boat3Name = "Thousand sunny"
    
    os.system('clear')

    player1Name = input("Quel est le nom du 1e joueur ?\n")
    player2Name = input("Quel est le nom du 2e joueur ?\n")
    
    tour = player1Name
    while True :
        if tour == plateaujoueur1 :
            plateaujoueur1.display()
            plateaujoueur1.display(False)
        else : 
            plateaujoueur2.display()
            plateaujoueur2.display(False)

        print(f"Au tour de {tour} de jouer :")

        print("Où voulez-vous tirer ?")

        print("\n case largeur ? ")
        caseWidth = testInt()
        print("\ncase longueur ? ")
        caseHeight = testInt()
        print("\n case profondeur ? ")
        caseDepth = testInt()

        os.system('clear')

        if tour == player1Name : 
            plateaujoueur1.shoot(caseHeight,caseWidth,caseDepth)
        else : 
            plateaujoueur2.shoot(caseHeight,caseWidth,caseDepth)
        
        plateaujoueur1.display(False)

        time.sleep(5)

        tour = player2Name if tour == player1Name else player1Name

# Place random boats on the plateau (revoir si le fonctionnement est nickel ou si supperposition de bateau)
def boatPlacement(plateau: Plateau,player_id: int) : 

    # WIP -> create random boat placement but not for all player yet 
    boat_sizes = [1,2,3]
    
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
    