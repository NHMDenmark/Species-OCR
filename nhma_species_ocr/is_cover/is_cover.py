import cv2

from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    read_specimen_data_matrix,
)


def is_cover(img: cv2.Mat) -> bool:
    """Takes an image and determines whether it is a cover of a specimen collection.
    Works by trying to detect a data matrix that specimen are marked with.

    Args:
        img (cv2.Mat): Image to process

    Returns:
        bool: Whether or not the image is a specimen cover
    """
    decoding = read_specimen_data_matrix(img)
    return not decoding
