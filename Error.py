import os

class ExitGame(Exception):
    pass

def testInt(prompt="", allow_exit=False):
    while True:
        raw = input(prompt)
        if allow_exit and raw.strip().lower() == "exit":
            return ExitGame()
        try:
            return int(raw)
        except ValueError:
            print("\nErreur, le nombre n'est pas un entier !")

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

   