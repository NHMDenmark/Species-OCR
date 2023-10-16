import cv2
import copy
import numpy as np
from nhma_species_ocr.util.variables import dilation_rect_size, label_extra_border, label_scale
from nhma_species_ocr.rotated_rect_crop.rotated_rect_crop import crop_rotated_rectangle
from nhma_species_ocr.util.util import most_frequent
from nhma_species_ocr.util.util import show_image_debug


def find_cover_label(img: cv2.Mat, debug: bool = False) -> tuple[cv2.Mat, bool]:
    """
    
    """
    img_bottom_left = img[(img.shape[0]-img.shape[0]/4).__round__():, (img.shape[1]/16).__round__():(img.shape[1]/2).__round__()]

    canny = cv2.Canny(img_bottom_left, 100, 200)
    if debug: show_image_debug("canny", canny)

    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (dilation_rect_size, dilation_rect_size))
    dilation = cv2.dilate(canny, rect, iterations=1)
    if debug: show_image_debug("dilation", dilation)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    parent_contours_with_subchildren = [cnt[3] for cnt in hierarchy[0] if cnt[2] != -1 and cnt[3] != -1]
    if parent_contours_with_subchildren.__len__() == 0:
        label_crop = img_bottom_left
    else:
        label_contour = most_frequent(parent_contours_with_subchildren)

        ((x, y), (width, height), angle) = cv2.minAreaRect(contours[label_contour])
        if debug: 
            img_with_contour = copy.copy(img_bottom_left)
            rect = cv2.minAreaRect(contours[label_contour])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img_with_contour, [box], 0, (0, 0, 255), 10)
            show_image_debug("label_contour", img_with_contour)

        min_rect = ((x, y), (width + label_extra_border, height + label_extra_border), angle)
        label_crop = crop_rotated_rectangle(img_bottom_left, min_rect)
        if label_crop is None:
            min_rect = ((x, y), (width, height), angle)
            label_crop = crop_rotated_rectangle(img_bottom_left, min_rect)
        if label_crop.shape[0] > label_crop.shape[1]:
            label_crop = cv2.rotate(label_crop, cv2.ROTATE_90_CLOCKWISE)

    return label_crop