import cv2
import os
from nhma_species_ocr.ocr.tesseract import OCR
from nhma_species_ocr.cv.cv import find_largest_contour


def is_label(img: cv2.Mat, label: cv2.Mat) -> bool:
    """
    
    """
    img_height = img.shape[0]
    img_width = img.shape[1]
    label_height = label.shape[0]
    label_width = label.shape[1]

    #print("width: {0}".format(label_width/img_width))
    #print("height: {0}".format(label_height/img_height))

    return 0.24 <= label_width/img_width <= 0.31 and 0.1 <= label_height/img_height

    