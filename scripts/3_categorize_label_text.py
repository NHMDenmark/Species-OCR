import json
import copy
import statistics
from nhma_species_ocr.util.util import flatten
from nhma_species_ocr.util.area_authority_list import area_authority_list


labels_folder = "/Users/akselbirko/Documents/DASSCO/labels"
grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    paragraphs = copy.copy(group['cover']['full_paragraphs'])
    
    area =    { "confidence": 0, "text": "" }
    family =  { "confidence": 0, "text": "" }
    genus =   { "confidence": 0, "text": "" }
    species = { "confidence": 0, "text": "" }
    for index, paragraph in enumerate(paragraphs):
        paragraph_text = ' '.join([word['text'] for word in paragraph['words']])
        if paragraph_text in area_authority_list:
            area = { "confidence": statistics.fmean([word['confidence'] for word in paragraph['words']]), "text": paragraph_text }
            paragraphs.pop(index)

    words_left = flatten([paragraph['words'] for paragraph in paragraphs])

    for index, word in enumerate(words_left):
        if word['text'][-4:].lower() == "ceae":
            family = word
            words_left.pop(index)

    if words_left.__len__() > 0:
        genus   = { "confidence": statistics.fmean([word['confidence'] for word in words_left[:1]]), "text": ' '.join([word['text'] for word in words_left[:1]]) }
    if words_left.__len__() > 1:
        species = { "confidence": statistics.fmean([word['confidence'] for word in words_left[:2]]), "text": ' '.join([word['text'] for word in words_left[:2]]) }
    
    group['cover']['area'] = area
    group['cover']['family'] = family
    group['cover']['genus'] = genus
    group['cover']['species'] = species
    

with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
