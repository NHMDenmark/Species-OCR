import cv2
import numpy as np

from nhma_species_ocr.rotated_rect_crop.rotated_rect_crop import crop_rotated_rectangle
from nhma_species_ocr.util.util import show_image_debug
from nhma_species_ocr.util.variables import dilation_rect_size, label_extra_border


def find_cover_label(img: cv2.Mat, debug: bool = False) -> tuple[cv2.Mat, bool]:
    """ """
    img_bottom_left = img[
        (img.shape[0] - img.shape[0] / 4).__round__() :,
        : (img.shape[1] / 2).__round__(),
    ]

    blur = cv2.bilateralFilter(img_bottom_left, 11, 1000, 75)
    if debug:
        show_image_debug("blur", blur)

    img_center = img[
        (img.shape[0] / 4).__round__() : (img.shape[0] - img.shape[0] / 4).__round__(),
        (img.shape[1] / 4).__round__() : (img.shape[1] - img.shape[1] / 4).__round__(),
    ]

    img_gray = cv2.cvtColor(img_center, cv2.COLOR_BGR2GRAY)
    thresh, thresh_im = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    canny = cv2.Canny(blur, 0, max(0.2 * thresh, 0))
    if debug:
        show_image_debug("canny", canny)

    rect = cv2.getStructuringElement(
        cv2.MORPH_RECT, (dilation_rect_size, dilation_rect_size)
    )
    closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, rect)
    if debug:
        show_image_debug("closing", closing)

    contours, hierarchy = cv2.findContours(
        closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    img_with_candidate_rectangles = img_bottom_left.copy()
    candidate_rectangles = []
    for i, contour in enumerate(contours):
        approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # Approximate polygon is rectangle
            ((x, y), (width, height), angle) = rect = cv2.minAreaRect(contour)
            a = width * height
            if (
                a > 2000000 and hierarchy[0][i][2] > 0
            ):  # Meets area requirement and is a closed rectangle
                candidate_rectangles.append((rect, a))
                cv2.drawContours(
                    img_with_candidate_rectangles,
                    [np.int0(cv2.boxPoints(rect))],
                    0,
                    (0, 0, 255),
                    6,
                )
    if debug:
        show_image_debug("candidate rectangles", img_with_candidate_rectangles)

    if candidate_rectangles.__len__() == 0:
        label_crop = img_bottom_left
    else:
        winner = candidate_rectangles[
            np.argmin(np.array([x[1] for x in candidate_rectangles]))
        ][0]

        if debug:
            img_with_contour = img_bottom_left.copy()
            cv2.drawContours(
                img_with_contour, [np.int0(cv2.boxPoints(winner))], 0, (0, 0, 255), 6
            )
            show_image_debug("label_contour", img_with_contour)

        ((x, y), (width, height), angle) = winner

        min_rect = (
            (x, y),
            (width + label_extra_border, height + label_extra_border),
            angle,
        )
        label_crop = crop_rotated_rectangle(img_bottom_left, min_rect)
        if label_crop is None:
            min_rect = ((x, y), (width, height), angle)
            label_crop = crop_rotated_rectangle(img_bottom_left, min_rect)
        if label_crop.shape[0] > label_crop.shape[1]:
            label_crop = cv2.rotate(label_crop, cv2.ROTATE_90_CLOCKWISE)

    return label_crop
