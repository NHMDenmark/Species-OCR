import json
import hashlib
import requests
import os

from nhma_species_ocr.util.variables import image_folder, output_file, ingestion_api

with open(output_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print(f"SPECIMEN METADATA: group #{index + 1} of {len(grouped_specimen_list)}...")

    for image in group["specimen"]:

        # Retrieve image metadata
        asset_name = image['image_file']
        data = requests.get(f"{ingestion_api}/metadata/{asset_name}")
        metadata = json.loads(data.content)

        # Calculate checksum
        image_path = os.path.join(image_folder, image["image_file"])
        with open(image_path, "rb") as f:
            file_hash_source = hashlib.md5(f.read())
        checksum = file_hash_source.hexdigest()

        # Populate fields
        image["guid"] = metadata["asset_guid"]
        image["checksum"] = checksum
        image["metadata"] = metadata

with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
