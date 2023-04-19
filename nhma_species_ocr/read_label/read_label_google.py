import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

def read_label_google(img_path: str) -> list:
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    #file_name = os.path.abspath("/Users/akselbirko/Documents/DASSCO/labels/Axel omslag01219.png")
    file_name = os.path.abspath(img_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    text = response.text_annotations

    return text[0].description.splitlines()
    #print([x.split() for x in text[0].description.splitlines()])