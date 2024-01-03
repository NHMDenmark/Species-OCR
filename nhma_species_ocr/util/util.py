import cv2


def flatten(list: list) -> list:
    """Flattens a list of lists

    Args:
        list (list): List to flatten

    Returns:
        list: Flattened list
    """
    return [item for sublist in list for item in sublist]


def most_frequent(list: list) -> object:
    """Returns the most frequently occuring object from a list

    Args:
        list (list): List of objects

    Returns:
        object: Most frequent item in list
    """
    counter = 0
    element = list[0]

    for i in list:
        curr_frequency = list.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            element = i

    return element


def show_image_debug(title: str, img: cv2.Mat):
    """Displays the provided image with the title provided for debugging

    Args:
        title (str): Display window title
        img (cv2.Mat): Image to display
    """
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()
