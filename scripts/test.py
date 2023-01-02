import cv2
import os
#from nhma_species_ocr.is_cover.is_cover import is_cover
#from nhma_species_ocr.find_cover_label.find_cover_label2 import find_cover_label2
img_names = [
    "TilUdvikling00732.tif",
    "TilUdvikling00733.tif",
    "TilUdvikling00734.tif",
    "TilUdvikling00735.tif",
    "TilUdvikling00737.tif",
    "TilUdvikling00738.tif",
    "TilUdvikling00739.tif",
    "TilUdvikling00741.tif",
    "TilUdvikling00742.tif",
    "TilUdvikling00743.tif",
    "TilUdvikling00745.tif",
    "TilUdvikling00746.tif",
    "TilUdvikling00747.tif"
]

img = cv2.imread("/Users/akselb/Documents/DASSCO/test_billeder/TilUdvikling00590.tif")

img_middle = (img.shape[1]/2).__round__()
crop_y_start = img.shape[0]-750
crop_y_end = img.shape[0]-420
crop_x_start = img_middle+250
crop_x_end = img_middle+950
img_crop = img[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

for image in img_names:
    print(image)
    img = cv2.imread("/Users/akselb/Documents/DASSCO/test_billeder/" + image)
    img[crop_y_start:crop_y_end, crop_x_start:crop_x_end] = img_crop
    os.chdir("/Users/akselb/Documents/DASSCO/test_billeder_2")
    cv2.imwrite(image, img)

