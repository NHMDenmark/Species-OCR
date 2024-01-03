import base64
import json

import cv2

from nhma_species_ocr.report.report_entry import report_entry
from nhma_species_ocr.report.report_template import report_template
from nhma_species_ocr.util.variables import (
    label_folder,
    output_file,
    report_error,
    report_success,
)

with open(output_file) as file:
    grouped_specimen_list = json.load(file)

report_entries_success = []
report_entries_error = []

list_success = [
    group
    for group in grouped_specimen_list
    if group["cover"]["gbif_match"] is not None and group["cover"]["error"] is False
]
list_error = [
    group
    for group in grouped_specimen_list
    if group["cover"]["gbif_match"] is None or group["cover"]["error"] is True
]

img_scaling = 0.4

for list in [list_success, list_error]:
    for index, group in enumerate(list):
        label_path = f"{label_folder}/{group['cover']['image_file'][:-4]}.png"
        img = cv2.imread(label_path)
        img = cv2.resize(img, (0, 0), fx=img_scaling, fy=img_scaling)
        retval, buffer = cv2.imencode(".png", img)
        encoded_string = base64.b64encode(buffer).decode()

        success = (
            group["cover"]["gbif_match"] is not None
            and group["cover"]["error"] is False
        )

        gbif_family = ""
        gbif_genus = ""
        gbif_species = ""
        gbif_variety = ""
        gbif_subsp = ""

        if group["cover"]["gbif_match"] is not None:
            if "family" in group["cover"]["gbif_match"]:
                gbif_family = group["cover"]["gbif_match"]["family"]
            if "genus" in group["cover"]["gbif_match"]:
                gbif_genus = group["cover"]["gbif_match"]["genus"]
            if "species" in group["cover"]["gbif_match"]:
                gbif_species = group["cover"]["gbif_match"]["species"]
            if "variety" in group["cover"]["gbif_match"]:
                gbif_variety = group["cover"]["gbif_match"]["variety"]
            if "subsp" in group["cover"]["gbif_match"]:
                gbif_subsp = group["cover"]["gbif_match"]["subsp"]

        entry = report_entry(
            id=group["id"],
            number=index + 1,
            total=len(list),
            png_base64=encoded_string,
            full_paragraphs=group["cover"]["full_paragraphs"],
            area=group["cover"]["area"]["text"],
            classification={
                "family": group["cover"]["family"]["text"],
                "genus": group["cover"]["genus"]["text"],
                "species": group["cover"]["species"]["text"],
                "variety": group["cover"]["variety"]["text"],
                "subsp": group["cover"]["subsp"]["text"],
            },
            classification_gbif={
                "family": gbif_family,
                "genus": gbif_genus,
                "species": gbif_species,
                "variety": gbif_variety,
                "subsp": gbif_subsp,
            },
            highest_classification_level=group["cover"]["highest_classification_level"],
        )
        if success:
            report_entries_success.append(entry)
        else:
            report_entries_error.append(entry)


html_success = report_template(report_entries_success)
html_error = report_template(report_entries_error)

with open(report_success, "w+", encoding="utf-8") as outfile:
    outfile.write(html_success)
with open(report_error, "w+", encoding="utf-8") as outfile:
    outfile.write(html_error)
