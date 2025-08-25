import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# STEP 1: LOAD DATASET
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Reshape for CNN (28x28x1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# One-hot encode labels
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# STEP 2: BUILD CNN MODEL
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(10, activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# STEP 3: TRAIN MODEL
model.fit(x_train, y_train, epochs=5, batch_size=128, validation_data=(x_test, y_test))

# Save model
model.save("handwritten_model.h5")


# STEP 4: TEST WITH OWN IMAGE
def predict_my_image(image_path):
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Resize to 28x28
    img = cv2.resize(img, (28, 28))

    # Invert colors if background is black
    img = cv2.bitwise_not(img)

    # Normalize
    img = img.astype("float32") / 255.0

    # Reshape for CNN
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)

    # Load trained model
    model = load_model("handwritten_model.h5")

    # Predict
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)

    print("Predicted digit:", predicted_class)
    plt.imshow(img[0, :, :, 0], cmap="gray")
    plt.title(f"Prediction: {predicted_class}")
    plt.show()

# Example usage:
# predict_my_image("my_digit.png")
