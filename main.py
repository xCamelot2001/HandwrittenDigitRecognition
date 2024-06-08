import os
import cnn_model
import gui

MODEL_FILE = 'digit_recognition_model.keras'

if __name__ == "__main__":
    # Check if the model file exists
    if not os.path.exists(MODEL_FILE):
        # If the model does not exist, train the models
        cnn_model.train_model()

    # Run the GUI application
    gui.run_app()
