import cv2
from pylibdmtx.pylibdmtx import decode
import zxingcpp

from nhma_species_ocr.util.variables import (
    cover_detection_scale,
    cover_detection_shrink,
    cover_detection_threshold,
    cover_detection_timeout,
)


def read_specimen_data_matrix(img: cv2.Mat, no_timeout: bool = False) -> str:
    """Takes an image, and tries to read any data matrix present

    Args:
        img (cv2.Mat): Image to process
        no_timeout (bool, optional): Run without timeout causing a full scan.
        Defaults to false

    Returns:
        str: the data read, else None
    """
    scale = cover_detection_scale / 100
    img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    img = img[: (img.shape[0] / 5).__round__(), : (img.shape[1] / 1).__round__()]

    decoding = decode(
        img,
        max_count=1,
        timeout=(None if no_timeout else cover_detection_timeout),
        threshold=cover_detection_threshold,
        shrink=cover_detection_shrink,
        deviation=25,
    )
    return (
      None if not decoding or not "".join([str(bit.data, "utf-8") for bit in decoding]).startswith("AU") else "".join([str(bit.data, "utf-8") for bit in decoding])

    )

def zxing_barcode_detector(img) -> str:
    """
    Checks if a barcode is present in the given image.

    Args:
        img (cv2.Mat): The input image.

    Returns:
        bool: True if a barcode is found, False otherwise.
    """
    # Read barcodes from the image
    results = zxingcpp.read_barcodes(img)

    # Keep barcode if it starts with "AU"
    if not results:
        return None

    decoded = "".join([bit.text for bit in results if bit.text])
    return decoded if decoded.startswith("AU") else None