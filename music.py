import pygame
from time import sleep

def init_music(start:float, music:str):
    pygame.mixer.init()
    pygame.mixer.music.load(music) 
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0, start=start)

def BRRRRRLAA():
    """
    BBBBBRRRRRRR LAA
    """
    init_music(45.9,"musics/charge.mp3")
    sleep(1.5)
    stop_music()

def charge():
    """
    CHARGEE ! CHARGEEE ! 
    """
    init_music(68.7,"musics/charge.mp3")
    sleep(0.9)
    stop_music()

def goofy_fart():
    """
    Prout
    """
    init_music(0.1,"musics\goofy-ahh-fart.mp3")
    sleep(0.6)
    stop_music()



def stop_music():
    pygame.mixer.music.stop()

if __name__ == "__main__":
    while(1):
        BRRRRRLAA()
        charge()
        goofy_fart()