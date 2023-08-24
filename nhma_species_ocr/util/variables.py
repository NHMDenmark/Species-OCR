from decouple import config


# Required
image_folder = config('IMAGE_FOLDER')
label_folder = config('LABEL_FOLDER')
label_threshold_folder = config('LABEL_THRESHOLD_FOLDER')
output_file = config('OUTPUT_FILE_JSON')
google_credentials = config('GOOGLE_APPLICATION_CREDENTIALS')

db_host = config('DB_HOST')
db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_database = config('DB_DATABASE')

# Optional
dilation_rect_size = config('FIND_COVER_LABEL_DILATION_RECT_SIZE', default=8, cast=int)
label_extra_border = config('LABEL_EXTRA_BORDER_PIXELS', default=100, cast=int)
cover_detection_scale = config('COVER_DETECTION_SCALE_PERCENT', default=50, cast=int)
threshold_block_size = config('LABEL_THRESHOLD_BLOCK_SIZE', default=91, cast=int)
threshold_subtract_constant = config('LABEL_THRESHOLD_SUBTRACT_CONSTANT', default=18, cast=int)
dev_only_covers = config('DEV_ONLY_COVERS', default=False, cast=bool)