import numpy as np
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Input # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from PIL import Image
import os

def load_my_digits(data_dir):
    images = []
    labels = []
    for label in range(10):
        digit_dir = os.path.join(data_dir, f"digit_{label}")
        for filename in os.listdir(digit_dir):
            if filename.endswith(".png"):
                img_path = os.path.join(digit_dir, filename)
                img = Image.open(img_path).convert('L')  # convert to grayscale
                img = img.resize((8, 8), Image.LANCZOS)
                img = np.array(img)
                images.append(img)
                labels.append(label)
    images = np.array(images)
    labels = np.array(labels)
    return images, labels

def train_model(data_dir=None):
    # Load and preprocess the sklearn digits dataset
    digits = load_digits()
    X = digits.images
    y = to_categorical(digits.target)

    # Normalize the pixel values
    X = X / 16.0

    if data_dir:
        # Load and preprocess your dataset
        my_X, my_y = load_my_digits(data_dir)
        my_y = to_categorical(my_y)
        my_X = my_X / 16.0

        # Combine with sklearn digits dataset
        X = np.concatenate((X, my_X), axis=0)
        y = np.concatenate((y, my_y), axis=0)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Reshape the data to fit the model
    X_train = X_train.reshape(X_train.shape[0], 8, 8, 1)
    X_test = X_test.reshape(X_test.shape[0], 8, 8, 1)

    # Build the CNN model
    model = Sequential()
    model.add(Input(shape=(8, 8, 1)))
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test accuracy: {accuracy:.4f}')

    # Save the model in the new format
    model.save('digit_recognition_model.keras')

if __name__ == "__main__":
    train_model(data_dir='my_digits')