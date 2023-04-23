import cv2
import json
from nhma_species_ocr.read_label.read_label_google_vision import read_label_google_vision


labels_folder = "/Users/akselbirko/Documents/DASSCO/labels"
grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print("processing group #{0} of {1}...".format(index+1, len(grouped_specimen_list)))

    label_path = "{0}/{1}.png".format(labels_folder, group['cover']['image_file'][:-4])
    image = cv2.imread(label_path, cv2.IMREAD_GRAYSCALE)
    text = read_label_google_vision(label_path)
    
    group['cover']['full_paragraphs'] = text
    
with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
