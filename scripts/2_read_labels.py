import json
from nhma_species_ocr.util.variables import label_folder, output_file
from nhma_species_ocr.read_label.read_label import read_label


with open(output_file) as file:
    grouped_specimen_list = json.load(file)


for index, group in enumerate(grouped_specimen_list):
    print("READ LABEL: group #{0} of {1}: {2}...".format(index+1, len(grouped_specimen_list), group['cover']['image_file']))

    label_path = "{0}/{1}.png".format(label_folder, group['cover']['image_file'][:-4])
    text = read_label(label_path)
    
    group['cover']['full_paragraphs'] = text
    
    
with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
