import cv2
import statistics
from google.cloud import vision
from nhma_species_ocr.util.util import show_image_debug


def read_label_google_vision(img: cv2.Mat, debug: bool = False) -> list:
    client = vision.ImageAnnotatorClient(client_options={'api_endpoint': 'eu-vision.googleapis.com'}) # Use EU google service

    threshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 17)

    if debug: show_image_debug("threshold", threshold)

    is_success, im_buf_arr = cv2.imencode(".jpg", threshold)
    content = im_buf_arr.tobytes()

    image = vision.Image(content=content)

    response = vision.AnnotateImageResponse(client.document_text_detection(image=image)) # Performs text detection on the image file
    text_blocks = response.full_text_annotation.pages[0].blocks

    paragraphs = []
    for block in text_blocks:
        for paragraph in block.paragraphs:
            if paragraph.confidence > 0.82:
                words = []
                for index, word in enumerate(paragraph.words):
                    if word.confidence > 0.7:
                        word_text = ''.join([symbol.text for symbol in word.symbols if symbol.confidence > 0.3])
                        if words.__len__() > 0 and paragraph.words[index-1].symbols[-1].property.detected_break.type_ == 0:
                            words[-1]['text'] += word_text
                            words[-1]['confidence'] = statistics.fmean([words[-1]['confidence'], word.confidence])
                        else:
                            words.append({ "confidence": word.confidence, "text": word_text })
                paragraphs.append({ "confidence": paragraph.confidence, "words": words })

    return paragraphs
