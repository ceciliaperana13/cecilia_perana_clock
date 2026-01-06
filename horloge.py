import time
import threading
from datetime import datetime
from typing import Tuple

# Variables globales
alarme = None
mode_12h = False
pause = False


def afficher_heure(heure: tuple[int, int,int]):
    """
    Affiche l'heure passée en paramètre
    """
    h, m, s = heure #compo du tuple

    if mode_12h:
        suffixe = "AM" if h < 12 else "PM"
        h = h % 12
        if h == 0:
            h = 12
        print(f"{h:02d}:{m:02d}:{s:02d} {suffixe}")
    else:
        print(f"{h:02d}:{m:02d}:{s:02d}")

    # Vérification de l'alarme
    if alarme == heure:
        print("HEY! Réveil toi bon sang!")


def regler_alarme(heure):
    """Règle l'alarme"""
    global alarme
    alarme = heure
    print(" Alarme prête")


def changer_mode_affichage():
    """Choix du mode 12h / 24h """
    global mode_12h
    choix = input("Choisir le mode d'affichage (12 ou 24) : ")

    if choix == "12":
        mode_12h = True
        print("Mode 12h activé")
    elif choix == "24":
        mode_12h = False
        print("Mode 24h activé")
    else:
        print("Choix invalide")


def pause_horloge():
    """Pause ou relance l'horloge"""
    global pause
    pause = not pause
    print("⏸ Pause activée" if pause else "▶ Horloge relancée")


def horloge():
    """Récupère l'heure système et l'affiche"""
    while True:
        if not pause:
            maintenant = datetime.now()
            heure_pc = (maintenant.hour, maintenant.minute, maintenant.second)
            afficher_heure(heure_pc)
        time.sleep(1)



thread = threading.Thread(target=horloge, daemon=True)
thread.start()

while True:
    print("\n1 - Changer mode 12h / 24h")
    print("2 - Régler l'alarme")
    print("3 - Pause / Reprise")
    print("4 - Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        changer_mode_affichage()

    elif choix == "2":
        h = int(input("Heures : "))
        m = int(input("Minutes : "))
        s = int(input("Secondes : "))
        regler_alarme((h, m, s))

    elif choix == "3":
        pause_horloge()

    elif choix == "4":
        print("Arrêt du programme")
        break