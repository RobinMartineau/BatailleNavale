import os

class ExitGame(Exception):
    pass

def testInt(prompt="", allow_exit=False):
    while True:
        raw = input(prompt)
        if allow_exit and raw.strip().lower() == "exit":
            raise ExitGame()
        try:
            return int(raw)
        except ValueError:
            print("\nErreur, le nombre n'est pas un entier !")

def testCellInput(gamestate, prompt="", allow_exit=False):
    while True:
        raw = input(prompt)
        if allow_exit and raw.strip().lower() == "exit":
            raise ExitGame()
        try:
            if len(raw) != 3:
                raise ValueError("Invalid length")
            x_raw = ord(raw[0]) - ord('A')
            y_raw = int(raw[1])
            z_raw = int(raw[2]) - 1
            if x_raw < 0 or y_raw < 0 or z_raw < 0:
                raise ValueError("Coordonnées négatives")
            sizes = (gamestate.p1.plateau.width, gamestate.p1.plateau.height, gamestate.p1.plateau.depth)
            if x_raw >= sizes[0] or y_raw >= sizes[1] or z_raw >= sizes[2]:
                raise ValueError("Coordonnées hors limites")
            return (x_raw, y_raw, z_raw)
        except ValueError:
            print("\nErreur, les coordonnées ne sont pas valides !")

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

   