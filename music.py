import pygame
from time import sleep

#region Initialize and play music from a specific start time
def init_music(start:float, music:str):
    pygame.mixer.init()
    pygame.mixer.music.load(music) 
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0, start=start)
#endregion

#region Play sound on a specific channel
def play_sound_on_channel(channel_id, file_path, volume=1.0):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    channel = pygame.mixer.Channel(channel_id)
    channel.set_volume(volume)
    channel.play(sound)
    return channel  # return the channel so we can stop it later
#endregion

#region Specific sound effects functions
def BRRRRRLAA():
    """
    BBBBBRRRRRRR LAA
    """
    play_sound_on_channel(
            channel_id = 2,
            file_path = "musics/bbbrrraaa.mp3",
            volume = 0.8,
        )

def charge():
    """
    CHARGEE ! CHARGEEE ! 
    """
    play_sound_on_channel(
            channel_id = 3,
            file_path = "musics/charge.mp3",
            volume = 0.8,
        )

def goofy_fart():
    """
    Prout
    """
    goofy = init_music(0.1,"musics\goofy-ahh-fart.mp3")
    sleep(0.6)
    stop_music(goofy)

def background_music():
    """
    Musique de fond
    """
    init_music(0.0,"musics/backmusic.mp3")

def game_music():
    stop_music()
    """
    Musique de jeu
    """
    init_music(0.0,"musics/game/gamemusic.mp3")
#endregion

#region Music control functions
def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()
#endregion
