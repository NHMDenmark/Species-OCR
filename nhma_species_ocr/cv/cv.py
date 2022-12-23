import cv2


def find_largest_contour(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    largest_contour = {"area": 0, "cnt": None}
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > largest_contour["area"]:
            largest_contour["area"] = area
            largest_contour["cnt"] = cnt

    return largest_contour["cnt"]

def find_text_boxes(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours