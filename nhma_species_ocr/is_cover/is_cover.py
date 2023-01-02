import cv2
from pylibdmtx.pylibdmtx import decode


def is_cover(img) -> bool:
    """
    Method that takes an image, and determines whether it is a cover of a species collection.
    Works by measuring the percentage of pixels inside boundary values of the cardboard cover color.

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

    # lower bound and upper bound for brown cardboard color
    #lower_bound = np.array([100, 130, 180])
    #upper_bound = np.array([180, 210, 240])

    # find the colors within the boundaries
    #mask = cv2.inRange(img, lower_bound, upper_bound)
    #brown_pixels = cv2.countNonZero(mask)
    #brown_pixels_coverage = (brown_pixels / (img.shape[0] * img.shape[1])) * 100

    #return brown_pixels_coverage > 50