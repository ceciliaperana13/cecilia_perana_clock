import tkinter as tk
from tkinter import messagebox
import time
import math

def create_clock():
    root = tk.Tk()
    root.title("Horloge de Mamie Jeannine")
    root.geometry("400x550")
    
    mode_24h = tk.BooleanVar(value=True)
    alarm_hour = tk.IntVar(value=7)
    alarm_minute = tk.IntVar(value=0)
    alarm_second = tk.IntVar(value=0)
    alarm_active = tk.BooleanVar(value=False)
    
    # Canvas for analog clock
    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()

    # Digital clock
    digital_clock_label = tk.Label(root, text="", font=("Helvetica", 20))
    digital_clock_label.pack(pady=5)

    # Date label
    date_label = tk.Label(root, text="", font=("Helvetica", 16))
    date_label.pack(pady=2)

    # Alarm controls
    alarm_frame = tk.Frame(root)
    alarm_frame.pack(pady=10)

    tk.Label(alarm_frame, text="Alarm:").grid(row=0, column=0, padx=5)

    tk.Spinbox(
        alarm_frame, from_=0, to=23, width=3,
        textvariable=alarm_hour, format="%02.0f"
    ).grid(row=0, column=1)

    tk.Label(alarm_frame, text=":").grid(row=0, column=2)

    tk.Spinbox(
        alarm_frame, from_=0, to=59, width=3,
        textvariable=alarm_minute, format="%02.0f"
    ).grid(row=0, column=3)

    tk.Label(alarm_frame, text=":").grid(row=0, column=4)

    tk.Spinbox(
        alarm_frame, from_=0, to=59, width=3,
        textvariable=alarm_second, format="%02.0f"
    ).grid(row=0, column=5)

    tk.Checkbutton(
        alarm_frame, text="Enable",
        variable=alarm_active
    ).grid(row=0, column=8, padx=10)

    # Mode 24h checkbox
    tk.Checkbutton(
        root,
        text="Mode 24h",
        variable=mode_24h,
        onvalue=True,
        offvalue=False
    ).pack(pady=5)

    def draw_hand(x, y, angle, length, width, color):
        rad = math.radians(angle)
        end_x = x + length * math.cos(rad)
        end_y = y + length * math.sin(rad)
        canvas.create_line(x, y, end_x, end_y, width=width, fill=color)

    def trigger_alarm():
        alarm_active.set(False)
        canvas.config(bg="lightyellow")
        messagebox.showinfo("Alarm", "Debout Mamie!")
        canvas.config(bg="white")

    def update_clock():
        canvas.delete("all")

        current_time = time.localtime()
        seconds = current_time.tm_sec
        minutes = current_time.tm_min
        hours = current_time.tm_hour if mode_24h.get() else current_time.tm_hour % 12

        # Clock face
        canvas.create_oval(50, 50, 350, 350, width=5)

        # Hour markers
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = 200 + 130 * math.cos(angle)
            y1 = 200 + 130 * math.sin(angle)
            x2 = 200 + 150 * math.cos(angle)
            y2 = 200 + 150 * math.sin(angle)
            canvas.create_line(x1, y1, x2, y2, width=4)

        # Numbers 1–12
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = 200 + 110 * math.cos(angle)
            y = 200 + 110 * math.sin(angle)
            canvas.create_text(
                x, y,
                text=str(i),
                font=("Helvetica", 14, "bold")
            )

        # Clock hands
        draw_hand(200, 200, hours * 30 + minutes * 0.5 - 90, 70, 6, "blue")
        draw_hand(200, 200, minutes * 6 - 90, 100, 4, "green")
        draw_hand(200, 200, seconds * 6 - 90, 120, 2, "red")

        # Digital clock display
        if mode_24h.get():
            digital_time = time.strftime("%H:%M:%S", current_time)
        else:
            digital_time = time.strftime("%I:%M:%S %p", current_time)

        digital_clock_label.config(text=digital_time)

        # Date display
        months_fr = ["janvier", "février", "mars", "avril", "mai", "juin",
                     "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        date_str = f"{current_time.tm_mday} {months_fr[current_time.tm_mon - 1]} {current_time.tm_year}"
        date_label.config(text=date_str)

        # Alarm check
        if alarm_active.get():
            if (current_time.tm_hour == int(alarm_hour.get()) and
                current_time.tm_min == int(alarm_minute.get()) and
                current_time.tm_sec == int(alarm_second.get())):
                trigger_alarm()

        root.after(1000, update_clock)

    update_clock()
    root.mainloop()

if __name__ == "__main__":
    create_clock()

