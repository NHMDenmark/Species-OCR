import cv2
from pylibdmtx.pylibdmtx import decode
from nhma_species_ocr.util.variables import cover_detection_scale, cover_detection_timeout


def is_cover(img) -> bool:
    """
    Method that takes an image, and determines whether it is a cover of a species collection.
    Works by trying to detect a data matrix that specimen are marked with.

    Args:
        img: image to process
    """
    scale = cover_detection_scale / 100
    img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    img = img[:(img.shape[0]/5).__round__(), :(img.shape[1]/1).__round__()]

    decoding = decode(img, max_count=1, timeout=cover_detection_timeout)
    return not decoding
