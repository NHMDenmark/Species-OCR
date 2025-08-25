import cv2
import zxingcpp
import os
import sys
from datetime import datetime
from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    read_specimen_data_matrix,
)

def zxing_barcode_detector(img) -> str:
    """
    Checks if a barcode is present in the given ima
    Args:
        img (cv2.Mat): The input image.

    Returns:
        bool: True if a barcode is found, False otherwise.
    """
    # Read barcodes from the image
    results = zxingcpp.read_barcodes(img)
    
    # Return True if any barcode is found, otherwise False
    return (
        None if not results else "".join([result.text for result in results])
    )
# Ensure the user provides an input folder
if len(sys.argv) != 2:
    print("Usage: python zxing_test.py /path/to/input_folder >> output.txt 2>> error.txt")
    sys.exit(1)

# Get input folder from command-line argument
input_folder = sys.argv[1]

# List all .tif files in the folder
tif_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

# Iterate through each .tif file
for tif_file in tif_files:
    file_path = os.path.join(input_folder, tif_file)
    print(f"{datetime.now()} - Processing file: {file_path}")
    
    # Read the image
    img = cv2.imread(file_path)
    str=zxing_barcode_detector(img) 
    if str.startswith("AU"):
        print(f"{datetime.now()} - Barcode detected with zxing: {str}")
    else:
        print(f" {datetime.now()} - {str} - wrong barcode or No barcode detected or barcode does not start with 'AU'")
    
    str2=read_specimen_data_matrix(img, no_timeout=True)
    if str2.startswith("AU"):
        print(f"{datetime.now()} - Barcode detected with pylibdmtx: {str2}")
    else:
        print(f" {datetime.now()} - {str2} - wrong barcode or No barcode detected or barcode does not start with 'AU'")