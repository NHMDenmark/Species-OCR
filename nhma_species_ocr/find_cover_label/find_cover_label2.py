import cv2
from nhma_species_ocr.find_cover_label.is_label import is_label


def find_cover_label2(img: cv2.Mat) -> tuple[cv2.Mat, bool]:
    """
    
    """
    scale = 0.3
    img = cv2.resize(src=img, dsize=(0, 0), fx=scale, fy=scale)

    img_bottom_left = img[(img.shape[0]-img.shape[0]/5).__round__():, :(img.shape[1]/2).__round__()]

    canny = cv2.Canny(img_bottom_left, 100, 200)

    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    dilation = cv2.dilate(canny, rect, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    parent_contours_with_subchildren = [cnt[3] for cnt in hierarchy[0] if cnt[2] != -1 and cnt[3] != -1]
    label_contour = most_frequent(parent_contours_with_subchildren)

    x1, y1, w1, h1 = cv2.boundingRect(contours[label_contour])
    label_crop = img_bottom_left[y1:y1 + h1, x1:x1 + w1]

    return label_crop, is_label(img, label_crop)

def most_frequent(List):
    counter = 0
    element = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            element = i
 
    return element