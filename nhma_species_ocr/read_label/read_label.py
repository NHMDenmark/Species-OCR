import cv2
from nhma_species_ocr.ocr.tesseract import OCR
from nhma_species_ocr.util.util import most_frequent, merge_rects_by_distance


def read_label(img):
    canny = cv2.Canny(img, 10, 130)

    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilation = cv2.dilate(canny, rect, iterations=1)

    #cv2.imshow('', dilation)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    parent_contours_with_subchildren = [cnt[3] for cnt in hierarchy[0] if cnt[2] != -1 and cnt[3] != -1]
    label_contour = most_frequent(parent_contours_with_subchildren)

    text_contours = [contours[index] for index, cnt in enumerate(hierarchy[0]) if cnt[3] == label_contour]

    #cv2.drawContours(img, text_contours, -1, (255,0,0), 3)
    #cv2.imshow('', img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    text_rects = [cv2.boundingRect(cnt) for cnt in text_contours if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 20000]

    text_rects_merged = merge_rects_by_distance(text_rects, 80)

    text = []
    for rect in sorted(text_rects_merged, key=lambda x: (x[1]+x[3]/2)+(x[0]+x[2]/2)/10):
        extra_border = 30
        img_crop = img[rect[1]-extra_border:rect[1]+rect[3]+extra_border, rect[0]-extra_border:rect[0]+rect[2]+extra_border]
        #img_crop = cv2.medianBlur(img_crop, 5)

        #cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (255,0,0), 2)
        cv2.imshow('', img_crop)
        cv2.waitKey()
        cv2.destroyAllWindows()
    
        ocr = OCR(language='eng+dan', config='-c tessedit_char_blacklist=0123456789')
        ocr.read_image(img_crop)
        result = ocr.get_text()
        if len(result) == 0:
            ocr = OCR(language='eng+dan', config='--psm 10 -c tessedit_char_blacklist=0123456789')
            ocr.read_image(img_crop)
            result = ocr.get_text()
        text.extend(result)

    return text


labels_file = "/Users/akselbirko/Documents/DASSCO/labels/TilUdvikling00644.png"
img = cv2.imread(labels_file, cv2.IMREAD_GRAYSCALE)
text = read_label(img)
print(text)