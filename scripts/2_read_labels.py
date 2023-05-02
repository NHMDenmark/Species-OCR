import json
from nhma_species_ocr.read_label.read_label import read_label


labels_folder = "/Users/akselbirko/Documents/DASSCO/labels"
grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print("processing group #{0} of {1}...".format(index+1, len(grouped_specimen_list)))

    label_path = "{0}/{1}.png".format(labels_folder, group['cover']['image_file'][:-4])
    text = read_label(label_path)
    
    group['cover']['full_paragraphs'] = text
    
with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
