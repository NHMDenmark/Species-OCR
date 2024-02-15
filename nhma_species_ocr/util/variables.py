from os import path

from decouple import UndefinedValueError, config

# Required
try:
    google_credentials = config("GOOGLE_APPLICATION_CREDENTIALS")
    image_folder = config("IMAGE_FOLDER")
    session_folder = config("SESSION_FOLDER")
    web_host = config("WEB_HOST")
    web_secret = config("WEB_SECRET")
except UndefinedValueError as e:
    raise Exception(
        f"""Required environment variable '{e.__str__().split(' ')[0]}' not found.
 Reference the .env.example file of this project for required variables"""
    )

label_folder = path.join(session_folder, "labels")
label_threshold_folder = path.join(session_folder, "labels_threshold")
output_file = path.join(session_folder, "output.json")
report_success = path.join(session_folder, "report_success.html")
report_error = path.join(session_folder, "report_error.html")

# Optional
dilation_rect_size = config("FIND_COVER_LABEL_DILATION_RECT_SIZE", default=15, cast=int)
label_scale = config("LABEL_SCALE_PERCENT", default=40, cast=int)
label_extra_border = config("LABEL_EXTRA_BORDER_PIXELS", default=100, cast=int)
cover_detection_scale = config("COVER_DETECTION_SCALE_PERCENT", default=75, cast=int)
cover_detection_timeout = config("COVER_DETECTION_TIMEOUT_MS", default=4000, cast=int)
threshold_block_size = config("LABEL_THRESHOLD_BLOCK_SIZE", default=91, cast=int)
threshold_subtract_constant = config(
    "LABEL_THRESHOLD_SUBTRACT_CONSTANT", default=18, cast=int
)
dev_only_covers = config("DEV_ONLY_COVERS", default=False, cast=bool)
