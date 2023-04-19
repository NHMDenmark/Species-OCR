import cv2


def show_image_debug(title: str, img: cv2.Mat):
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()