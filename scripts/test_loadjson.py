import json
import os

from nhma_species_ocr.util.variables import (
    label_folder,
    label_scale,
    label_threshold_folder,
    output_file,
    session_started_at,
)

#output_file = "path_to_your_output_file.json"  # Path to your existing JSON file
output_dir = "C:/Users/jpc843/Documents/auWorkflow/testSessionData"  # Directory to save the new JSON files
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Load grouped_specimen_list from the existing JSON file
try:
    with open(output_file) as file:
        grouped_specimen_list = json.load(file)
        print(f"Loaded data: {grouped_specimen_list}")
except FileNotFoundError:
    print(f"Error: The file {output_file} was not found.")
    grouped_specimen_list = []
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {output_file}.")
    grouped_specimen_list = []
    
session_started_at = "2024-10-31T10:00:00Z"  # Example session start time

# Loop through each group and create a separate JSON file
for index, group in enumerate(grouped_specimen_list):
    print(f"Preparing JSON for group #{index + 1} of {len(grouped_specimen_list)}...")

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
                "barcode": specimen["id"],
                #"guid": specimen["guid"],
                #"digitiser": specimen["metadata"]["digitiser"],
                #"date_asset_taken": specimen["metadata"]["date_asset_taken"],
                "image_file": specimen["image_file"],
                #"checksum": specimen["checksum"],
            }
            for specimen in group["specimen"]
        ],
    }

# Define the output path for the JSON file
json_file_path = os.path.join(output_dir, f"group_{index + 1}.json")

# Write the data dictionary to a JSON file
try:
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON saved to {json_file_path}")
except Exception as e:
    print(f"Error writing JSON file for group #{index + 1}: {e}")