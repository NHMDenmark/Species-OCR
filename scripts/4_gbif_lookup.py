import json
from nhma_species_ocr.gbif_name_lookup.gbif_name_lookup import gbif_name_lookup
from nhma_species_ocr.util.util import similar


grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)


for index, group in enumerate(grouped_specimen_list):
    print("processing group #{0} of {1}: {2}...".format(index+1, len(grouped_specimen_list), group['cover']['image_file']))

    group['cover']['gbif_match'] = None
    
    highest_classification_level = group['cover']['highest_classification_level']

    species_name = group['cover']['species']['text']
    if highest_classification_level == 'subsp':
        subsp = group['cover']['subsp']['text']
        lookup_name = "{0} subsp. {1}".format(species_name, subsp)
        result = gbif_name_lookup(lookup_name, 'subspecies')
        if result and similar(result['canonicalName'].lower(), ' '.join([species_name.lower(), subsp.lower()])) == 1:
            group['cover']['gbif_match'] = result
    elif highest_classification_level == 'variety':
        variety = group['cover']['variety']['text']
        lookup_name = "{0} var. {1}".format(species_name, variety)
        result = gbif_name_lookup(lookup_name, 'variety')
        if result and similar(result['canonicalName'].lower(), ' '.join([species_name.lower(), variety.lower()])) == 1:
            group['cover']['gbif_match'] = result
    elif highest_classification_level == 'species':
        result = gbif_name_lookup(species_name, 'species')
        if result and similar(result['canonicalName'].lower(), species_name.lower()) == 1:
            group['cover']['gbif_match'] = result
    elif highest_classification_level == 'genus':
        genus = group['cover']['genus']['text']
        result = gbif_name_lookup(genus, 'genus')
        if result and similar(result['canonicalName'].lower(), genus.lower()) == 1:
            group['cover']['gbif_match'] = result
    elif highest_classification_level == 'family':
        family = group['cover']['family']['text']
        result = gbif_name_lookup(family, 'family')
        if result and similar(result['canonicalName'].lower(), family.lower()) == 1:
            group['cover']['gbif_match'] = result


with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))