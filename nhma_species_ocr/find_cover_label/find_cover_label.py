import cv2
import os
from nhma_species_ocr.ocr.tesseract import OCR
from nhma_species_ocr.cv.cv import find_largest_contour
from nhma_species_ocr.find_cover_label.is_label import is_label


def find_cover_label(img: cv2.Mat) -> tuple[cv2.Mat, bool]:
    """
    
    """
    scale = 0.3
    img = cv2.resize(src=img, dsize=(0, 0), fx=scale, fy=scale)

    img_bottom = img[(img.shape[0]-img.shape[0]/5).__round__():, :(img.shape[1]/2).__round__()]

    gray = cv2.cvtColor(img_bottom, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, rect_kernel)

    outer_contour = find_largest_contour(opening)
    if outer_contour is not None:
        x1, y1, w1, h1 = cv2.boundingRect(outer_contour)
        crop1 = opening[y1:y1 + h1, x1:x1 + w1]
    else:
        crop1 = opening
    crop1_inverted = cv2.bitwise_not(crop1)

    inner_contour = find_largest_contour(crop1_inverted)
    if inner_contour is not None:
        x2, y2, w2, h2 = cv2.boundingRect(inner_contour)
        crop2 = img_bottom[y1+y2:y1+y2 + h2, x1+x2:x1+x2 + w2]
    else:
        crop2 = img_bottom[y1:y1 + h1, x1:x1 + w1]

    return crop2, is_label(img, crop2)

    #cv2.imshow("img", img)
    #cv2.imshow("gray", gray)
    #cv2.imshow("thresh", thresh1)
    #cv2.imshow("opening", opening)
    #cv2.imshow("crop1", crop1)
    #cv2.imshow("crop1_inverted", crop1_inverted)
    #cv2.imshow("crop2", crop2)
    #cv2.imshow("img", img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()


#img = cv2.imread("/Users/akselb/Documents/DASSCO/test_billeder/TilUdvikling00591.tif")
#print(read_cover(img))
#label = read_cover(img)
#os.chdir("/Users/akselb/Documents/DASSCO/labels")
#cv2.imwrite("label.png", label)