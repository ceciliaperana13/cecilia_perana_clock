import tkinter as tk
from tkinter import messagebox
import time
import math

class AnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Horloge de Mamie Jeannine")
        self.geometry("400x550")

        # Alarm variables
        self.alarm_hour = tk.IntVar(value=7)
        self.alarm_minute = tk.IntVar(value=0)
        self.alarm_active = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # Canvas for analog clock
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        # Digital clock
        self.digital_clock_label = tk.Label(
            self, text="", font=("Helvetica", 20)
        )
        self.digital_clock_label.pack(pady=5)

        # Alarm controls
        alarm_frame = tk.Frame(self)
        alarm_frame.pack(pady=10)

        tk.Label(alarm_frame, text="Alarm:").grid(row=0, column=0, padx=5)

        tk.Spinbox(
            alarm_frame, from_=0, to=23, width=3,
            textvariable=self.alarm_hour, format="%02.0f"
        ).grid(row=0, column=1)

        tk.Label(alarm_frame, text=":").grid(row=0, column=2)

        tk.Spinbox(
            alarm_frame, from_=0, to=59, width=3,
            textvariable=self.alarm_minute, format="%02.0f"
        ).grid(row=0, column=3)

        tk.Checkbutton(
            alarm_frame, text="Enable",
            variable=self.alarm_active
        ).grid(row=0, column=4, padx=10)

        self.update_clock()

    def update_clock(self):
         self.canvas.delete("all")

         current_time = time.localtime()
         seconds = current_time.tm_sec
         minutes = current_time.tm_min
         hours = current_time.tm_hour % 12

        # Clock face
         self.canvas.create_oval(50, 50, 350, 350, width=5)

        # Hour markers
         for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = 200 + 130 * math.cos(angle)
            y1 = 200 + 130 * math.sin(angle)
            x2 = 200 + 150 * math.cos(angle)
            y2 = 200 + 150 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, width=4)

        # Numbers 1–12
         for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = 200 + 110 * math.cos(angle)
            y = 200 + 110 * math.sin(angle)
            self.canvas.create_text(
                x, y,
                text=str(i),
                font=("Helvetica", 14, "bold")
            )

        # Clock hands
            self.draw_hand(200, 200, hours * 30 + minutes * 0.5 - 90, 70, 6, "blue")
            self.draw_hand(200, 200, minutes * 6 - 90, 100, 4, "green")
            self.draw_hand(200, 200, seconds * 6 - 90, 120, 2, "red")

        # Digital clock display
         digital_time = time.strftime("%H:%M:%S", current_time)
         self.digital_clock_label.config(text=digital_time)

        # Alarm check
         if self.alarm_active.get():
            if (current_time.tm_hour == self.alarm_hour.get() and
                current_time.tm_min == self.alarm_minute.get() and
                current_time.tm_sec == 0):

                self.trigger_alarm()

         self.after(1000, self.update_clock)

    def draw_hand(self, x, y, angle, length, width, color):
                rad = math.radians(angle)
                end_x = x + length * math.cos(rad)
                end_y = y + length * math.sin(rad)
                self.canvas.create_line(x, y, end_x, end_y, width=width, fill=color)

    def trigger_alarm(self):
        # Disable alarm to avoid repetition
        self.alarm_active.set(False)

        # Visual feedback
        self.canvas.config(bg="lightyellow")

        # Popup message
        messagebox.showinfo("Alarm", " Debout Mamie!")

        # Reset background color
        self.canvas.config(bg="white")

if __name__ == "__main__":
    app = AnalogClock()
    app.mainloop()


