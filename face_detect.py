import os
import cv2
import argparse
import numpy as np
from PIL import Image

def detect_faces(image_path, save_directory):
    """
    Detect and save faces from all the images in 
    `image_path` and save it `save_directory`.
    """
    # Create Directory if not already exists
    os.makedirs(save_directory, exist_ok=True)
    assert os.path.isfile(image_path), "Image path does not exist or is invalid"
    assert image_path.lower().endswith("jpg") or \
           image_path.lower().endswith("jpeg") or \
           image_path.lower().endswith("png"), "Specified path is not a valid image"

    # Load the cascade classifier
    face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

    # Read the input image
    image = cv2.imread(image_path)
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, minNeighbors=6, minSize=(120,120))

    # Iterate over the detected faces and save each as a separate image
    for i, (x, y, w, h) in enumerate(faces):
        # Crop the face and convert to PIL image
        face = Image.fromarray(image[y:y+h, x:x+w])

        # Save the face
        face.save(f"{save_directory}/face_{i}.jpg")

    # Return the number of faces detected
    print(f"Number of faces detetced: {len(faces)}")
    return len(faces)

if __name__ == "__main__":
    # Argument parser for CLI
    parser = argparse.ArgumentParser(description="Detect, crop and save faces from images in a directory")
    parser.add_argument("--image-path", type=str, help="path to the input image.")
    parser.add_argument("--save-directory", type=str, help="path of the directory to save the headshots.")

    # Parse args and detect faces!
    args = parser.parse_args()
    detect_faces(args.image_path, args.save_directory)