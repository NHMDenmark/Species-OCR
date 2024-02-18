import json

import exifread
from DaSSCoUtils.guid import guidHandler
from DaSSCoUtils.metadata import metadataHandler

from nhma_species_ocr.util.variables import refinery_metadata


def image_metadata(image_path: str) -> any:
    with open(refinery_metadata) as file:
        meta = json.load(file)

    with open(image_path, "rb") as image_file:
        tags = exifread.process_file(image_file)

    val = str(tags["EXIF DateTimeOriginal"])
    print(val)
    time = (
        val[:4]
        + "-"
        + val[5:7]
        + "-"
        + val[8:10]
        + "T"
        + val[11:13]
        + ":"
        + val[14:16]
        + ":"
        + val[17:19]
        + "+02:00"
    )
    print(time)
    guid = guidHandler()
    guid_name = guid.createGuid(
        time,
        meta["institution"],
        meta["collection"],
        meta["workstation_name"],
    )

    meta["date_asset_taken"] = time
    meta["asset_guid"] = guid_name

    metadata = metadataHandler(**meta)

    return metadata.getMetadata()
