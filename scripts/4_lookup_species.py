import json
from nhma_species_ocr.lookup_species.lookup_species import lookup_species
from nhma_species_ocr.util.util import similar


grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)


for index, group in enumerate(grouped_specimen_list):
    print("processing group #{0} of {1}: {2}...".format(index+1, len(grouped_specimen_list), group['cover']['image_file']))
    species_name = group['cover']['species']['text']

    result = lookup_species(species_name)
    if result and similar(result['canonicalName'].lower(), species_name.lower()) == 1:
        group['cover']['species_match_gbif'] = result
    else:
        group['cover']['species_match_gbif'] = None


with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
