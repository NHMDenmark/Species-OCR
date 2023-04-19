import json
import cv2
from nhma_species_ocr.read_label.read_label import read_label
from nhma_species_ocr.read_label.read_label_google import read_label_google
from nhma_species_ocr.util.area_authority_list import area_authority_list


labels_folder = "/Users/akselbirko/Documents/DASSCO/labels"
grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print("processing group #{0} of {1}...".format(index+1, len(grouped_specimen_list)))

    label_path = "{0}/{1}.png".format(labels_folder, group['cover']['image_file'][:-4])
    text = read_label_google(label_path)
    #img = cv2.imread(label_path, cv2.IMREAD_GRAYSCALE)
    #text = read_label(img)
    
    area = ""
    species = ""
    for index, line in enumerate(text):
        if line in area_authority_list:
            area = line
            text.pop(index)

    species = ' '.join(text)
    #if len(text) > 0:
    #    area = text[0]
    #if len(text) > 1:
    #    for line in text[1:]:
    #        for word in line:
    #            if word[-3:] != "eae":
    #                species.append(word)
    
    group['cover']['area'] = area
    group['cover']['species'] = species
    

with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))