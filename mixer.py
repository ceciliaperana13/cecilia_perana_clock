from pygame import mixer
import tkinter as tk


def mixer ():
    mixer.init()
    mixer.music.load('alarm_sound.mp3')
    mixer.music.set_volume(0.7)
    return mixer