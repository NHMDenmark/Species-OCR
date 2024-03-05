import json
import os
import shutil

import cv2
import requests

from nhma_species_ocr.util.variables import (
    label_folder,
    label_scale,
    label_threshold_folder,
    output_file,
    session_started_at,
    web_host,
    web_secret,
)

label_temp_folder = f"{label_folder}_temp"

if os.path.exists(label_temp_folder):
    shutil.rmtree(label_temp_folder)
os.makedirs(label_temp_folder)

with open(output_file) as file:
    grouped_specimen_list = json.load(file)

covers = []
specimen = []

for index, group in enumerate(grouped_specimen_list):
    print(f"UPLOAD TO WEB: group #{index + 1} of {len(grouped_specimen_list)}...")

    cover = group["cover"]

    data = {
        "image_cover": cover["image_file"],
        "image_label": f"{cover['image_file'][:-4]}.png",
        "ocr_read_json": json.dumps(cover["full_paragraphs"]),
        "area": cover["area"]["text"],
        "family": cover["family"]["text"],
        "genus": cover["genus"]["text"],
        "species": cover["species"]["text"],
        "variety": cover["variety"]["text"],
        "subsp": cover["subsp"]["text"],
        "gbif_match_json": json.dumps(cover["gbif_match"]),
        "highest_classification": cover["highest_classification_level"],
        "flagged": cover["error"],
        "approved": False,
        "session_started_at": session_started_at,
        "specimen": [
            {
                "guid": specimen["guid"],
                "digitiser": specimen["metadata"]["digitiser"],
                "date_asset_taken": specimen["metadata"]["date_asset_taken"],
                "image_file": specimen["image_file"],
                "checksum": specimen["checksum"],
            }
            for specimen in group["specimen"]
        ],
    }

    scale = label_scale / 100

    label = cv2.imread(f"{label_folder}/{cover['image_file'][:-4]}.png")
    label_downscaled = cv2.resize(label, (0, 0), fx=scale, fy=scale)

    cv2.imwrite(f"{label_temp_folder}/{cover['image_file'][:-4]}.png", label_downscaled)

    files = {
        "label": open(f"{label_temp_folder}/{cover['image_file'][:-4]}.png", "rb"),
        "label_threshold": open(
            f"{label_threshold_folder}/{cover['image_file'][:-4]}.png", "rb"
        ),
    }

    headers = {"Authorization": web_secret}

    r = requests.post(
        web_host + "/api/folderupload", files=files, data=data, headers=headers
    )
    if not r.ok:
        print(r.content)
        raise Exception(r.json())
