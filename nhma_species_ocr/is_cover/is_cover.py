import cv2
from pylibdmtx.pylibdmtx import decode


def is_cover(img) -> bool:
    """
    Method that takes an image, and determines whether it is a cover of a species collection.
    Works by trying to detect a data matrix that species are marked with.

    Args:
        img: image to process
    """
    # downscale image to improve speed
    scale = 0.5
    img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    img = img[(img.shape[0]-img.shape[0]/4).__round__():, :(img.shape[1]/1).__round__()]

    # detect QR code
    decoding = decode(img, max_count=1, timeout=2000)
    return not decoding