import copy
import json
import statistics

from nhma_species_ocr.util.area_authority_list import area_authority_list
from nhma_species_ocr.util.util import flatten
from nhma_species_ocr.util.variables import output_file

with open(output_file) as file:
    grouped_specimen_list = json.load(file)

for index, group in enumerate(grouped_specimen_list):
    print(
        "CATEGORIZE LABEL TEXT: group #{0} of {1}: {2}...".format(
            index + 1, len(grouped_specimen_list), group["cover"]["image_file"]
        )
    )

    paragraphs = copy.copy(group["cover"]["full_paragraphs"])

    area = family = genus = species = variety = subsp = {"confidence": 0, "text": ""}
    error = False
    for index, paragraph in enumerate(paragraphs):
        paragraph_text = " ".join([word["text"] for word in paragraph["words"]])
        if paragraph_text in area_authority_list:
            area = {
                "confidence": statistics.fmean(
                    [word["confidence"] for word in paragraph["words"]]
                ),
                "text": paragraph_text,
            }
            paragraphs.pop(index)

    if area["text"] == "":
        area = {
            "confidence": statistics.fmean(
                [word["confidence"] for word in paragraphs[0]["words"]]
            ),
            "text": " ".join([word["text"] for word in paragraphs[0]["words"]]),
        }
        paragraphs.pop(0)
        error = True

    words_left = flatten([paragraph["words"] for paragraph in paragraphs])

    for index, word in enumerate(words_left):
        if word["text"][-4:].lower() == "ceae":
            family = word
            words_left.pop(index)
        elif word["text"].lower() == "var.":
            try:
                variety = words_left[index + 1]
            except IndexError:
                variety["text"] = "ERROR"
                error = True
            words_left = words_left[:index]
            break
        elif word["text"].lower() in ["subsp.", "ssp."]:
            subsp = words_left[index + 1]
            words_left = words_left[:index]
            break

    # remove remaining author names
    for index, word in enumerate(words_left):
        if word["text"][0].isupper() and word["text"][-1] == "." or "(" in word["text"]:
            words_left = words_left[:index]
            break

    for index, word in enumerate(words_left):
        if word["text"].lower() == "x":
            species = {
                "confidence": statistics.fmean(
                    [word["confidence"] for word in words_left[index - 1 : index + 1]]
                ),
                "text": " ".join(
                    [word["text"] for word in words_left[index - 1 : index + 2]]
                ),
            }
            try:
                words_left.pop(index - 1)
                words_left.pop(index - 1)
                words_left.pop(index - 1)
            except Exception:
                error = True

    if words_left.__len__() > 0:
        genus = words_left[0]
        words_left.pop(0)
    if words_left.__len__() > 0:
        if species["text"] == "":
            species = words_left[0]
            words_left.pop(0)
        else:
            error = True

    if genus["text"] != "" and species["text"] != "":
        species = {
            "confidence": statistics.fmean(
                [string["confidence"] for string in [genus, species]]
            ),
            "text": " ".join([string["text"] for string in [genus, species]]),
        }

    if area["text"] != "":
        for word in words_left:
            if word["text"][0].isupper():
                break
            else:
                error = True

    group["cover"]["area"] = area
    group["cover"]["family"] = family
    group["cover"]["genus"] = genus
    group["cover"]["species"] = species
    group["cover"]["variety"] = variety
    group["cover"]["subsp"] = subsp
    group["cover"]["error"] = error

    highest_classification_level = None
    for index, classification_level in enumerate(
        ["subsp", "variety", "species", "genus", "family"]
    ):
        if group["cover"][classification_level]["text"] != "":
            highest_classification_level = classification_level
            break
    group["cover"]["highest_classification_level"] = highest_classification_level

with open(output_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
