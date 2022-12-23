import os
from os.path import join
import cv2
import shutil
from nhma_species_ocr.is_cover.is_cover import is_cover
from nhma_species_ocr.find_cover_label.find_cover_label import find_cover_label

labels_file = "/Users/akselb/Documents/DASSCO/labels.txt"
labels_folder = "/Users/akselb/Documents/DASSCO/labels"
label_errors_file = "/Users/akselb/Documents/DASSCO/label-errors.txt"
label_errors_folder = "/Users/akselb/Documents/DASSCO/label-errors"

file = open(labels_file, "w+")
file.write("")
file.close()
file = open(label_errors_file, "w+")
file.write("")
file.close()

if os.path.exists(labels_folder):
    shutil.rmtree(labels_folder)
if os.path.exists(label_errors_folder):
    shutil.rmtree(label_errors_folder)
os.mkdir(labels_folder)
os.mkdir(label_errors_folder)

image_path = "/Users/akselb/Documents/DASSCO/test_billeder"
image_names = [f for f in os.listdir(image_path) if (f[-3:] == 'tif')]

for index, image_name in enumerate(sorted(image_names)):
    print("processing image #{0} of {1}: {2}...".format(index+1, len(image_names), image_name))
    image = cv2.imread(join(image_path, image_name))
    cover = is_cover(image)
    if cover:
        cover_label, is_label = find_cover_label(image)
        if is_label:
            file = open(labels_file, "a")
            os.chdir("/Users/akselb/Documents/DASSCO/labels")
        else:
            file = open(label_errors_file, "a")
            os.chdir("/Users/akselb/Documents/DASSCO/label-errors")
        file.write(image_name)
        file.write("\n")
        file.close()
        cv2.imwrite("{0}-label.png".format(image_name), cover_label)
