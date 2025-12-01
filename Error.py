def TestInt() :
    while True:
            try : 
                choice = int(input())
                break
            except ValueError : 
                print("\nErreur, le nombre n'est pas un entier !")
    return choice