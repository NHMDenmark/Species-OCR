import json


grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

matches = 0
for group in grouped_specimen_list:
    if group['cover']['species_match_gbif'] is not None:
        matches = matches + 1
    else:
        print(group['cover']['species_joined'])

print(matches)