from nhma_species_ocr.read_specimen_data_matrix.read_specimen_data_matrix import (
    read_specimen_data_matrix,
)


def is_cover(img) -> bool:
    """
    Method that takes an image, and determines whether it is a cover of a species
    collection. Works by trying to detect a data matrix that specimen are marked with.

    Args:
        img: image to process
    """
    decoding = read_specimen_data_matrix(img)
    return not decoding
