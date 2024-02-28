import json
import os

from DaSSCoUtils.checksum import checksumHandler

from nhma_species_ocr.util.image_metadata import image_metadata
from nhma_species_ocr.util.variables import image_folder, output_file

with open(output_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print(f"SPECIMEN METADATA: group #{index + 1} of {len(grouped_specimen_list)}...")

    for image in group["specimen"]:
        image_path = os.path.join(image_folder, image["image_file"])

        checksum = checksumHandler(image_path).getChecksum()
        metadata = image_metadata(image_path)
        asset_name = image["image_file"]
        image["guid"] = metadata["asset_guid"]
        image["checksum"] = checksum
        image["metadata"] = metadata

with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
