from nhma_species_ocr.lookup_species.lookup_species import lookup_species
import cv2
from nhma_species_ocr.find_cover_label.find_cover_label import find_cover_label
from nhma_species_ocr.read_label.read_label_google import read_label_google


#name = "Dicranopteris flexuosa"
#result = lookup_species(name)
#print(result["canonicalName"])

#image = cv2.imread("/Users/akselbirko/Documents/DASSCO/test_billeder_3/Axel omslag01201.tif")
#cover_label = find_cover_label(image, True)

image = "/Users/akselbirko/Documents/DASSCO/labels/Axel omslag01231.png"
text = read_label_google(image)
print(text)