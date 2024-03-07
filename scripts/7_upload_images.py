import json
import os

from DaSSCoUtils.upload import uploadHandler

from nhma_species_ocr.util.variables import (
    image_folder,
    output_file,
    refinery_pass,
    refinery_user,
    test_upload,
)

upload = uploadHandler(refinery_user, refinery_pass)

with open(output_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print(f"UPLOAD IMAGES: group #{index + 1} of {len(grouped_specimen_list)}...")

    for image in group["specimen"]:
        image_path = os.path.join(image_folder, image["image_file"])

        checksum = image["checksum"]
        metadata = image["metadata"]
        asset_name = metadata['asset_guid']

        if test_upload:
            print(f"Test upload: {image_path}")
            upload.uploadTest(
                checksum=checksum,
                metadata=metadata,
                assetName=asset_name,
                imagePath=image_path,
            )
        else:
            print(f"Upload: {image_path}")
            upload.upload(
                checksum=checksum,
                metadata=metadata,
                assetName=asset_name,
                imagePath=image_path,
            )
