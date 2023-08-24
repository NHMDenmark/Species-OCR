from nhma_species_ocr.util.env import env_config


# Required
image_folder = env_config.get('IMAGE_FOLDER')
label_folder = env_config.get('LABEL_FOLDER')
label_threshold_folder = env_config.get('LABEL_THRESHOLD_FOLDER')
output_file = env_config.get('OUTPUT_FILE_JSON')
google_credentials = env_config.get('GOOGLE_APPLICATION_CREDENTIALS')

db_host = env_config.get('DB_HOST')
db_user = env_config.get('DB_USER')
db_password = env_config.get('DB_PASSWORD')
db_database = env_config.get('DB_DATABASE')

# Optional
dilation_rect_size = env_config.get('FIND_COVER_LABEL_DILATION_RECT_SIZE', default=8, cast=int)
label_extra_border = env_config.get('LABEL_EXTRA_BORDER_PIXELS', default=100, cast=int)
cover_detection_scale = env_config.get('COVER_DETECTION_SCALE_PERCENT', default=50, cast=int)
threshold_block_size = env_config.get('LABEL_THRESHOLD_BLOCK_SIZE', default=91, cast=int)
threshold_subtract_constant = env_config.get('LABEL_THRESHOLD_SUBTRACT_CONSTANT', default=18, cast=int)
dev_only_covers = env_config.get('DEV_ONLY_COVERS', default=False, cast=bool)