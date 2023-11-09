import os
import shutil
import statistics

import cv2
from google.cloud import vision

from nhma_species_ocr.util.util import show_image_debug
from nhma_species_ocr.util.variables import (
    google_credentials,
    label_threshold_folder,
    threshold_block_size,
    threshold_subtract_constant,
)

if os.path.exists(label_threshold_folder):
    shutil.rmtree(label_threshold_folder)
os.mkdir(label_threshold_folder)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials


def read_label(img_path: str, debug: bool = False) -> list:
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    threshold = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        threshold_block_size,
        threshold_subtract_constant,
    )
    if debug:
        show_image_debug("threshold", threshold)

    cv2.imwrite(
        "{0}/{1}".format(label_threshold_folder, img_path.split("/")[-1]), threshold
    )

    is_success, im_buf_arr = cv2.imencode(".png", threshold)
    content = im_buf_arr.tobytes()

    client = vision.ImageAnnotatorClient(
        client_options={"api_endpoint": "eu-vision.googleapis.com"}
    )  # Use EU google service
    response = vision.AnnotateImageResponse(
        client.document_text_detection(image=vision.Image(content=content))
    )  # Performs text detection on the image file
    text_blocks = response.full_text_annotation.pages[0].blocks

    paragraphs = []
    for block in sorted(
        text_blocks, key=lambda block: block.bounding_box.vertices[0].y
    ):
        for paragraph in block.paragraphs:
            if paragraph.confidence > 0.82:
                words = []
                for index, word in enumerate(paragraph.words):
                    word_text = "".join(
                        [
                            symbol.text
                            for symbol in word.symbols
                            if symbol.confidence > 0.3
                        ]
                    )
                    word_text = word_text.replace("×", "x")
                    if (
                        word.confidence > 0.5 or word_text.lower() == "x"
                    ):  # Sometimes an "x" can have a low confidence because of font
                        if (
                            words.__len__() > 0
                            and paragraph.words[index - 1]
                            .symbols[-1]
                            .property.detected_break.type_
                            == 0
                        ):
                            words[-1]["text"] += word_text
                            words[-1]["confidence"] = statistics.fmean(
                                [words[-1]["confidence"], word.confidence]
                            )
                        else:
                            words.append(
                                {"confidence": word.confidence, "text": word_text}
                            )
                paragraphs.append({"confidence": paragraph.confidence, "words": words})

    return paragraphs
