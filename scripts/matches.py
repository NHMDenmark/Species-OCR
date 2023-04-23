import json


grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

matches = 0
for group in grouped_specimen_list:
    if group['cover']['species_match_gbif'] is not None:
        matches = matches + 1
    else:
        area = ""
        species = ""
        if group['cover']['area']:
            area = group['cover']['area']['text']
        if group['cover']['species']:
            species = group['cover']['species']['text']
        print(group['cover']['image_file'] + " - " + area + " - " + species)

print(matches)
