import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import logging

# Step 1: Setting up logging using a decorator
def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Running {func.__name__}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise e
    return wrapper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Step 2: ModelHandler class for managing AI models
class ModelHandler:
    def __init__(self):
        # Encapsulation: Hiding the details of model loading
        self.model = self.load_model()

    @log_decorator
    def load_model(self):
        """Load the pre-trained MobileNetV2 model"""
        return tf.keras.applications.MobileNetV2(weights="imagenet")

    @log_decorator
    def preprocess_image(self, img):
        """Resize and preprocess image for classification"""
        img = img.resize((224, 224))  # MobileNetV2 requires 224x224 size
        img_array = np.expand_dims(np.array(img), axis=0)
        return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    @log_decorator
    def predict_image(self, img_array):
        """Run the model prediction and return top prediction"""
        predictions = self.model.predict(img_array)
        predicted_class = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0][0][1]
        return predicted_class


# Step 3: Main Application Class (Multiple Inheritance)
class ImageClassifierApp(tk.Tk, ModelHandler):
    def __init__(self):
        # Initializing both Tkinter and ModelHandler
        tk.Tk.__init__(self)
        ModelHandler.__init__(self)
        
        self.title("Image Classifier Application")
        self.geometry("600x400")
        self.file_path = ""
        
        # Creating the GUI components
        self.create_widgets()

    # Encapsulation: Keeping GUI logic separate in a method
    def create_widgets(self):
        self.label = tk.Label(self, text="Upload an image to classify", font=("Arial", 14))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        self.classify_button = tk.Button(self, text="Classify Image", command=self.classify_image_in_app)
        self.classify_button.pack(pady=10)

    # Method overriding: Customizing behavior for image upload
    @log_decorator
    def upload_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if self.file_path:
            img = Image.open(self.file_path)
            img.thumbnail((150, 150))
            self.img_display = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img_display)

    # Polymorphism and method overriding: Classify image using loaded model
    @log_decorator
    def classify_image_in_app(self):
        if self.file_path:
            img = Image.open(self.file_path)
            img_array = self.preprocess_image(img)  # Preprocessing the image
            predicted_class = self.predict_image(img_array)  # Using ModelHandler method to predict
            self.label.config(text=f"Prediction: {predicted_class}")
        else:
            self.label.config(text="Please upload an image first.")

# Running the Application
if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
