from decouple import config, UndefinedValueError


# Required
try:
    image_folder = config('IMAGE_FOLDER')
    label_folder = config('LABEL_FOLDER')
    label_threshold_folder = config('LABEL_THRESHOLD_FOLDER')
    output_file = config('OUTPUT_FILE_JSON')
    google_credentials = config('GOOGLE_APPLICATION_CREDENTIALS')

    web_host = config('WEB_HOST')
except UndefinedValueError as e:
    raise Exception(
        f"Required environment variable '{e.__str__().split(' ')[0]}' not found. Reference the .env.example file of this project for required variables")

# Optional
dilation_rect_size = config('FIND_COVER_LABEL_DILATION_RECT_SIZE', default=16, cast=int)
canny_t1 = config('FIND_COVER_LABEL_CANNY_T1', default=100, cast=int)
canny_t2 = config('FIND_COVER_LABEL_CANNY_T2', default=200, cast=int)
label_scale = config('LABEL_SCALE_PERCENT', default=40, cast=int)
label_extra_border = config('LABEL_EXTRA_BORDER_PIXELS', default=100, cast=int)
cover_detection_scale = config('COVER_DETECTION_SCALE_PERCENT', default=40, cast=int)
cover_detection_timeout = config('COVER_DETECTION_TIMEOUT_MS', default=4000, cast=int)
threshold_block_size = config('LABEL_THRESHOLD_BLOCK_SIZE', default=91, cast=int)
threshold_subtract_constant = config('LABEL_THRESHOLD_SUBTRACT_CONSTANT', default=18, cast=int)
dev_only_covers = config('DEV_ONLY_COVERS', default=False, cast=bool)
