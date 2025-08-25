import json
import os
import shutil
from os.path import join

import cv2

from nhma_species_ocr.find_cover_label.find_cover_label import find_cover_label
from nhma_species_ocr.is_cover.is_cover import is_cover
from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    read_specimen_data_matrix,
)
from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    zxing_barcode_detector,
)
from nhma_species_ocr.util.variables import (
    dev_only_covers,
    image_folder,
    label_folder,
    output_file,
)

image_names = [f for f in os.listdir(image_folder) if (f[-3:] == "tif")]

if os.path.exists(label_folder):
    shutil.rmtree(label_folder)
os.makedirs(label_folder)

grouped_specimen_list = []

for index, image_name in enumerate(sorted(image_names)):
    print(
        "GROUP IMAGE: image #{0} of {1}: {2}...".format(
            index + 1, len(image_names), image_name
        )
    )
    image = cv2.imread(join(image_folder, image_name))
    cover = dev_only_covers or is_cover(image)
    if cover:
        cover_label = find_cover_label(image)

        cv2.imwrite("{0}/{1}.png".format(label_folder, image_name[:-4]), cover_label)

        grouped_specimen_list.append(
            {
                "id": index + 1,
                "cover": {
                    "image_file": image_name,
                },
                "specimen": [],
            }
        )
    else:
        grouped_specimen_list[-1]["specimen"].append(
            {
                "image_file": image_name,
                "id": read_specimen_data_matrix(image, no_timeout=True) or zxing_barcode_detector(image),
            }
        )

with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
