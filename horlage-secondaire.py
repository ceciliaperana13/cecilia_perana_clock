import time
import os
from datetime import datetime

class Clock:
    def __init__(self):
        self.time = [0, 0, 0]  # [hours, minutes, seconds]
        self.alarm = None
        self.mode_24h = True
        self.alarm_triggered = False
        
    def set_time(self, time_tuple):
        
        hours, minutes, seconds = time_tuple
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            self.time = [hours, minutes, seconds]
            self.alarm_triggered = False
        else:
            print(" invalide ")
    
    def set_alarm(self, time_tuple):
        
        hours, minutes, seconds = time_tuple
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            self.alarm = [hours, minutes, seconds]
            self.alarm_triggered = False
            print(f" Alarm set for {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            print(" invalide!")
    # a revoir
    def change_display_mode(self, mode_24h=True):
        """change de mode 12h/24h"""
        self.mode_24h = mode_24h
        print(f" Display mode: {'24 hours' if mode_24h else '12 hours (AM/PM)'}")
    
    def format_time(self):
        h, m, s = self.time
        
        if self.mode_24h:
            return f"{h:02d}:{m:02d}:{s:02d}"
        else:
            # mode 12h
            period = "AM" if h < 12 else "PM"
            h_12 = h % 12
            if h_12 == 0:
                h_12 = 12
            return f"{h_12:02d}:{m:02d}:{s:02d} {period}"
    
    def display_time(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print(" GRANDMA JEANNINE'S CLOCK ".center(40))
        print("=" * 40)
        print()
        print(f"   {self.format_time()}".center(40))
        print()
        
        if self.alarm:
            alarm_str = f"{self.alarm[0]:02d}:{self.alarm[1]:02d}:{self.alarm[2]:02d}"
            print(f" Alarm set: {alarm_str}".center(40))
        
        print()
        print("=" * 40)
        print("Press Ctrl+C to stop")
    
    def check_alarm(self):
        if self.alarm and not self.alarm_triggered:
            if self.time == self.alarm:
                self.alarm_triggered = True
                print("\n" + "." * 20)
                print(" WAKE UP GRANDMA JEANNINE! ".center(40))
                print("." * 20)
                time.sleep(3)
    #a revoir aussi 
    def increment_time(self):
        """Increments time by one second"""
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
        try:
            while True:
                self.display_time()
                self.check_alarm()
                time.sleep(1)
                self.increment_time()
        except KeyboardInterrupt:
            print("\n\n Clock stopped.  Grandma Jeannine! ")


# Main 
if __name__ == "__main__":
    
    clock = Clock()
    
    
    now = datetime.now()
    clock.set_time((now.hour, now.minute, now.second))
    
    # Configuration
    print(" Configuring the clock")
    print()
    
    # a revoir pour le moment cest une alarme de 10seconde 
    alarm_h = now.hour
    alarm_m = now.minute
    alarm_s = (now.second + 10) % 60
    if now.second + 10 >= 60:
        alarm_m = (alarm_m + 1) % 60
        if alarm_m == 0:
            alarm_h = (alarm_h + 1) % 24
    
    clock.set_alarm((alarm_h, alarm_m, alarm_s))
    
    # demande de changer de mode d'affichage 
    choice = input("12-hour mode (AM/PM)? (y/n): ").lower()
    if choice == 'y':
        clock.change_display_mode(False)
    
    time.sleep(2)
    
    
    clock.start()