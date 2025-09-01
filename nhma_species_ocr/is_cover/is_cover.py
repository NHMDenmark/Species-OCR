import base64

import cv2
import requests
import stamina

from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    read_specimen_data_matrix,
)
from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    zxing_barcode_detector,
)
from nhma_species_ocr.util.variables import huggingface_api_key


@stamina.retry(on=Exception, attempts=20, timeout=360, wait_max=120)
def zero_shot_classification(img: cv2.Mat) -> bool:
    """Takes an image and determines whether it is a cover of a specimen collection.
    Works by inferencing on a zero-shot classification model.

    Args:
        img (cv2.Mat): Image to process

    Returns:
        bool: Whether or not the image is a specimen cover
    """
    f1 = 720 / img.shape[1]  # max width
    f2 = 1280 / img.shape[0]  # max height
    f = min(f1, f2)  # resizing factor
    dim = (int(img.shape[1] * f), int(img.shape[0] * f))
    resized = cv2.resize(img, dim)

    url = "https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14"
    headers = {"Authorization": f"Bearer {huggingface_api_key}"}

    retval, buffer = cv2.imencode(".tif", resized)
    payload = {
        "parameters": {"candidate_labels": ["specimen", "specimen folder"]},
        "inputs": base64.b64encode(buffer).decode("utf-8"),
    }
    response = requests.post(url, headers=headers, json=payload)
    classes = response.json()
    return classes[0]["label"] == "specimen folder"



def is_cover(img: cv2.Mat) -> bool:
    """Takes an image and determines whether it is a cover of a specimen collection.
    Works by trying to detect a data matrix that specimen are marked with.

    Args:
        img (cv2.Mat): Image to process

    Returns:
        bool: Whether or not the image is a specimen cover
    """
    decoding = read_specimen_data_matrix(img)
    barcode_detected = zxing_barcode_detector(img)
    
    return (
        False
        if decoding or barcode_detected
        else (zero_shot_classification(img) if huggingface_api_key else True)
    )
