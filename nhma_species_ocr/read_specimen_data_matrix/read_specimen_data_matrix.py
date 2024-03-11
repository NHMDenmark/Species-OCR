import cv2
from pylibdmtx.pylibdmtx import decode

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
        None if not decoding else "".join([str(bit.data, "utf-8") for bit in decoding])
    )
