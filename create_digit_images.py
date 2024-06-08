import tkinter as tk
from PIL import Image as PILImage, ImageDraw
import os

class DigitDrawerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0

        # Create elements
        self.canvas = tk.Canvas(self, width=200, height=200, bg="white")
        self.label = tk.Label(self, text="Draw a digit and save it")
        self.save_button = tk.Button(self, text="Save", command=self.save_image)
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_canvas)
        self.digit_entry = tk.Entry(self)
        self.label2 = tk.Label(self, text="Enter digit:")

        # Pack elements
        self.canvas.pack()
        self.label.pack()
        self.label2.pack()
        self.digit_entry.pack()
        self.save_button.pack()
        self.clear_button.pack()

        # Events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.image = PILImage.new("L", (200, 200), (255))
        self.draw = ImageDraw.Draw(self.image)

        # Directory to save images
        self.save_dir = "my_digits"

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle((0, 0, 200, 200), fill=(255))

    def paint(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill="black")
        self.draw.ellipse([self.x - r, self.y - r, self.x + r, self.y + r], fill="black")

    def save_image(self):
        digit = self.digit_entry.get()
        if digit.isdigit() and 0 <= int(digit) <= 9:
            digit_dir = os.path.join(self.save_dir, f"digit_{digit}")
            if not os.path.exists(digit_dir):
                os.makedirs(digit_dir)
            file_count = len(os.listdir(digit_dir))
            file_path = os.path.join(digit_dir, f"{file_count + 1}.png")
            self.image.save(file_path)
            self.clear_canvas()
            print(f"Saved {file_path}")
        else:
            print("Please enter a valid digit (0-9)")

if __name__ == "__main__":
    app = DigitDrawerApp()
    app.title("Digit Drawer")
    app.mainloop()