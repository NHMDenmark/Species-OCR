import os
from os.path import join
import cv2
import shutil
import json
from nhma_species_ocr.is_cover.is_cover import is_cover
from nhma_species_ocr.find_cover_label.find_cover_label import find_cover_label


labels_file = "/Users/akselbirko/Documents/DASSCO/labels.txt"
labels_folder = "/Users/akselbirko/Documents/DASSCO/labels"
output_file = "/Users/akselbirko/Documents/DASSCO/output.json"

file = open(labels_file, "w+")
file.write("")
file.close()

if os.path.exists(labels_folder):
    shutil.rmtree(labels_folder)
os.mkdir(labels_folder)

image_path = "/Users/akselbirko/Documents/DASSCO/test_billeder_3"
image_names = [f for f in os.listdir(image_path) if (f[-3:] == 'tif')]

grouped_specimen_list = []

for index, image_name in enumerate(sorted(image_names)):
    print("processing image #{0} of {1}: {2}...".format(index+1, len(image_names), image_name))
    image = cv2.imread(join(image_path, image_name))
    cover = is_cover(image)
    if cover:
        cover_label = find_cover_label(image)

        file = open(labels_file, "a")
        file.write(image_name)
        file.write("\n")
        file.close()

        cv2.imwrite("{0}/{1}.png".format(labels_folder, image_name[:-4]), cover_label)

        grouped_specimen_list.append({
                "cover": {
                    "image_file": image_name,
                },
                "specimen": []
            }
        )
    else:
        grouped_specimen_list[-1]['specimen'].append({
                "image_file": image_name
            }
        )

with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))