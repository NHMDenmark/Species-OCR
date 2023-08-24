import cv2
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def flatten(l):
    return [item for sublist in l for item in sublist]


def most_frequent(list):
    counter = 0
    element = list[0]
     
    for i in list:
        curr_frequency = list.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            element = i
 
    return element


def show_image_debug(title: str, img: cv2.Mat):
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()