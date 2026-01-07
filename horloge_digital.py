import tkinter as tk
import time
import math

class AnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Horloge de Mamie Jeannine")
        self.geometry("400x500")

        self.create_widgets()

    def create_widgets(self):
        # Create the canvas for the analog clock
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        # Create the digital clock label
        self.digital_clock_label = tk.Label(
            self, text="", font=("Helvetica", 20)
        )
        self.digital_clock_label.pack(pady=10)

        # Start updating the clock
        self.update_clock()

    def update_clock(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Get the current local time
        current_time = time.localtime()
        seconds = current_time.tm_sec
        minutes = current_time.tm_min
        hours = current_time.tm_hour % 12

        # Draw the clock face
        self.canvas.create_oval(50, 50, 350, 350, width=5)

        # Draw hour markers
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = 200 + 130 * math.cos(angle)
            y1 = 200 + 130 * math.sin(angle)
            x2 = 200 + 150 * math.cos(angle)
            y2 = 200 + 150 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, width=4)

        # Draw the clock hands
        # Hour hand (moves smoothly with minutes)
        self.draw_hand(200, 200, hours * 30 + minutes * 0.5 - 90, 70, 6, "blue")

        # Minute hand
        self.draw_hand(200, 200, minutes * 6 - 90, 100, 4, "green")

        # Second hand
        self.draw_hand(200, 200, seconds * 6 - 90, 120, 2, "red")

        # Display the digital clock
        digital_time = time.strftime("%H:%M:%S", current_time)
        self.digital_clock_label.config(text=digital_time)

        # Update the clock every second
        self.after(1000, self.update_clock)

    def draw_hand(self, x, y, angle, length, width, color):
        # Convert angle to radians
        rad = math.radians(angle)

        # Calculate the end position of the hand
        end_x = x + length * math.cos(rad)
        end_y = y + length * math.sin(rad)

        # Draw the hand
        self.canvas.create_line(x, y, end_x, end_y, width=width, fill=color)

if __name__ == "__main__":
    app = AnalogClock()
    app.mainloop()


