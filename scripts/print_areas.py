import json


grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

areas = set()
for group in grouped_specimen_list:
    areas.add(group['cover']['area'])

for area in areas:
    print(area)