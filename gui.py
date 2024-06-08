import tkinter as tk
from tkinter import *
import numpy as np
from PIL import Image as PILImage, ImageDraw, ImageOps
from tensorflow.keras.models import load_model # type: ignore

class DigitRecognizerApp(tk.Tk):
    def __init__(self, model):
        tk.Tk.__init__(self)
        self.model = model
        self.x = self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=200, height=200, bg="white")
        self.label = tk.Label(self, text="Draw a digit and click 'Predict'")
        self.prediction_label = tk.Label(self, text="Predicted Digit: None")
        self.predict_button = tk.Button(self, text="Predict", command=self.predict_digit)
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_canvas)

        # Pack elements
        self.canvas.pack()
        self.label.pack()
        self.prediction_label.pack()
        self.predict_button.pack()
        self.clear_button.pack()

        # Events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.image = PILImage.new("L", (200, 200), (255))
        self.draw = ImageDraw.Draw(self.image)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle((0, 0, 200, 200), fill=(255))
        self.prediction_label.config(text="Predicted Digit: None")

    def paint(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill="black")
        self.draw.ellipse([self.x - r, self.y - r, self.x + r, self.y + r], fill="black")

    def preprocess_image(self):
        # Save the image and preprocess it
        self.image.save("drawn_digit.png")
        img = self.image.resize((8, 8), PILImage.LANCZOS)
        img = ImageOps.invert(img)
        img = img.convert('L')
        img = np.array(img)

        # Centering the image by finding the bounding box and cropping
        bbox = PILImage.fromarray(img).getbbox()
        if bbox:
            img = PILImage.fromarray(img).crop(bbox)

        # Resize to 8x8 again after centering
        img = img.resize((8, 8), PILImage.LANCZOS)
        img = np.array(img)

        # Normalize the pixel values
        img = img / 16.0

        # Reshape the image for the model
        img = img.reshape(1, 8, 8, 1)
        return img

    def predict_digit(self):
        img = self.preprocess_image()
        prediction = self.model.predict(img)
        digit = np.argmax(prediction)
        self.prediction_label.config(text=f"Predicted Digit: {digit}")

def run_app():
    model = load_model('digit_recognition_model.keras')
    app = DigitRecognizerApp(model)
    app.title("Digit Recognizer")
    app.mainloop()

if __name__ == "__main__":
    run_app()