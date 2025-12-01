import os
import string

while True:
    print("--------Menu Bataille naval--------")
    print("0- Nouvelle partie")
    print("1- Reprendre une partie")
    print("2- Historiques des parties")
    print("3- Quitter")

    while True:
        try : 
            choice = int(input())
            break
        except ValueError : 
            print("\n Erreur, le nombre n'est pas un entier !\n")
    
    match choice : 
        case 0 : 
            os.system('clear')
        case 1 :
            os.system('clear')
        case 2 :
            os.system('clear')
        case 3 : 
            break
        case _:
            os.system('clear')
            print("Vous devez choisir un numéro par rapport aux propositions ci-dessous !")
    print("")