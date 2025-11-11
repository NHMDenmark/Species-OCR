import json
import os
import shutil
import cv2
import requests

from pathlib import Path
from os.path import join
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
    ingestion_api
)

folder = Path(image_folder)
image_paths = list(folder.glob("*.tif")) + list(folder.glob("*.tiff"))
image_names = [p.name for p in image_paths]

first_json = image_paths[0].with_suffix(".json")
if not first_json.exists():
    raise Exception(f"Missing JSON file for {image_paths[0].name}")
    
with first_json.open("r", encoding="utf-8") as f:
    metadata = json.load(f)
    
body = {
    "workstation": metadata['workstation_name'],
    "dateAssetTaken": metadata['date_asset_taken']
}
res = requests.post(f"{ingestion_api}/metadata/files/search", json=body)

if res.status_code != 200:
    raise Exception(f"Request Error: {res.content}")

images = [{ "image_name": item['filename'], "original_name": item['original_filename']} for item in res.json()]

# Validation
missing = set(image_names) - {d["image_name"] for d in images}
if missing:
    raise ValueError(f"Missing in API: {sorted(missing)}")

if os.path.exists(label_folder):
    shutil.rmtree(label_folder)
os.makedirs(label_folder)

grouped_specimen_list = []

for index, d in enumerate(images):
    image_name = d["image_name"]
    original_name = d["original_name"]
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
                    "original_name": original_name,
                },
                "specimen": [],
            }
        )
    else:
        grouped_specimen_list[-1]["specimen"].append(
            {
                "image_file": image_name,
                "original_name": original_name,
                "id": read_specimen_data_matrix(image, no_timeout=True) or zxing_barcode_detector(image),
            }
        )

with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
