import time
import os
from datetime import datetime
import threading
import sys

class Clock:
    def __init__(self):
        self.time = [0, 0, 0]  # [hours, minutes, seconds]
        self.alarm = None
        self.mode_24h = True
        self.alarm_triggered = False
        self.running = True
        self.paused = False
        
    def set_time(self, time_tuple):
        hours, minutes, seconds = time_tuple
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            self.time = [hours, minutes, seconds]
            self.alarm_triggered = False
            return True
        else:
            print(" Heure invalide!")
            return False
    
    def set_alarm(self, time_tuple):
        hours, minutes, seconds = time_tuple
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            self.alarm = [hours, minutes, seconds]
            self.alarm_triggered = False
            print(f" Alarme réglée pour {hours:02d}:{minutes:02d}:{seconds:02d}")
            return True
        else:
            print(" Heure d'alarme invalide!")
            return False
    
    def change_display_mode(self, mode_24h=True):
        self.mode_24h = mode_24h
        print(f"✓ Mode d'affichage: {'24 heures' if mode_24h else '12 heures (AM/PM)'}")
    
    def format_time(self):
        h, m, s = self.time
        
        if self.mode_24h:
            return f"{h:02d}:{m:02d}:{s:02d}"
        else:
            period = "AM" if h < 12 else "PM"
            h_12 = h % 12
            if h_12 == 0:
                h_12 = 12
            return f"{h_12:02d}:{m:02d}:{s:02d} {period}"
    
    def display_time(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(" HORLOGE DE MAMIE JEANNINE ".center(50))
        print("=" * 50)
        print()
        print(f"   {self.format_time()}".center(50))
        print()
        
        if self.alarm:
            alarm_str = f"{self.alarm[0]:02d}:{self.alarm[1]:02d}:{self.alarm[2]:02d}"
            print(f" Alarme: {alarm_str}".center(50))
        else:
            print(" Aucune alarme".center(50))
        
        print()
        mode_str = "24h" if self.mode_24h else "12h (AM/PM)"
        print(f"Mode: {mode_str}".center(50))
        print()
        print("=" * 50)
        print("\nCOMMANDES DISPONIBLES:")
        print("  m  - Changer de mode (12h/24h)")
        print("  t  - Régler l'heure")
        print("  a  - Définir une alarme")
        print("  d  - Supprimer l'alarme")
        print("  q  - Quitter")
        print("\nEntrez une commande: ", end='', flush=True)
    
    def check_alarm(self):
        if self.alarm and not self.alarm_triggered:
            if self.time == self.alarm:
                self.alarm_triggered = True
                print("\n" + "🔔" * 20)
                print(" RÉVEILLE-TOI MAMIE JEANNINE! ".center(40))
                print("🔔" * 20)
                time.sleep(3)
    
    def increment_time(self):
        self.time[2] += 1
        if self.time[2] >= 60:
            self.time[2] = 0
            self.time[1] += 1
            if self.time[1] >= 60:
                self.time[1] = 0
                self.time[0] += 1
                if self.time[0] >= 24:
                    self.time[0] = 0
                    self.alarm_triggered = False
    
    def start(self):
        # Démarrer un thread pour l'affichage et l'incrémentation du temps
        display_thread = threading.Thread(target=self._run_clock, daemon=True)
        display_thread.start()
        
        # Boucle principale pour les commandes utilisateur
        self._handle_commands()
    
    def _run_clock(self):
        """Thread qui gère l'affichage et l'incrémentation du temps"""
        while self.running:
            if not self.paused:
                self.display_time()
                self.check_alarm()
                time.sleep(1)
                self.increment_time()
    
    def _handle_commands(self):
        """Gère les commandes utilisateur en temps réel"""
        while self.running:
            try:
                command = input().strip().lower()
                self.paused = True
                
                if command == 'm':
                    self._change_mode_interactive()
                elif command == 't':
                    self._set_time_interactive()
                elif command == 'a':
                    self._set_alarm_interactive()
                elif command == 'd':
                    self._delete_alarm()
                elif command == 'q':
                    self.running = False
                    print("\n  Horloge arrêtée. Au revoir Mamie Jeannine!")
                    os._exit(0)
                else:
                    print("Commande inconnue!")
                    time.sleep(1)
                
                self.paused = False
                
            except EOFError:
                break
            except KeyboardInterrupt:
                self.running = False
                print("\n\n  Horloge arrêtée. Au revoir Mamie Jeannine!")
                os._exit(0)
    
    def _change_mode_interactive(self):
        """Change le mode d'affichage de manière interactive"""
        print("\n" + "-" * 50)
        print("CHANGER LE MODE D'AFFICHAGE")
        print("1. Mode 24 heures")
        print("2. Mode 12 heures (AM/PM)")
        choice = input("Votre choix (1 ou 2): ").strip()
        
        if choice == '1':
            self.change_display_mode(True)
        elif choice == '2':
            self.change_display_mode(False)
        else:
            print("Choix invalide!")
        
        time.sleep(1.5)
    
    def _set_time_interactive(self):
        """Règle l'heure de manière interactive"""
        print("\n" + "-" * 50)
        print("RÉGLER L'HEURE")
        try:
            time_str = input("Entrez l'heure (HH:MM:SS): ")
            parts = time_str.split(':')
            
            if len(parts) != 3:
                print("Format invalide! Utilisez HH:MM:SS")
                time.sleep(1.5)
                return
            
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            
            if self.set_time((h, m, s)):
                print(f"✓ Heure réglée sur: {h:02d}:{m:02d}:{s:02d}")
        except ValueError:
            print("Erreur de saisie! Utilisez des nombres.")
        
        time.sleep(1.5)
    
    def _set_alarm_interactive(self):
        """Définit une alarme de manière interactive"""
        print("\n" + "-" * 50)
        print("DÉFINIR UNE ALARME")
        try:
            time_str = input("Entrez l'heure de l'alarme (HH:MM:SS): ")
            parts = time_str.split(':')
            
            if len(parts) != 3:
                print(" Format invalide! Utilisez HH:MM:SS")
                time.sleep(1.5)
                return
            
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            self.set_alarm((h, m, s))
        except ValueError:
            print(" Erreur de saisie! Utilisez des nombres.")
        
        time.sleep(1.5)
    
    def _delete_alarm(self):
        """Supprime l'alarme"""
        self.alarm = None
        self.alarm_triggered = False
        print("\n✓ Alarme supprimée!")
        time.sleep(1.5)



if __name__ == "__main__":
    clock = Clock()
    
    # Configuration initiale
    now = datetime.now()
    clock.set_time((now.hour, now.minute, now.second))
    
    print("\n" + "=" * 50)
    print(" HORLOGE DE MAMIE JEANNINE ".center(50))
    print("=" * 50)
    print("\n✓ Horloge initialisée avec l'heure actuelle")
    print("\nDémarrage dans 2 secondes...")
    time.sleep(2)
    
    clock.start()