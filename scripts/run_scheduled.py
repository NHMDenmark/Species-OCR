import os
import shutil
import subprocess
from time import localtime, strftime

from decouple import config

from nhma_species_ocr.util.variables import (
    cover_detection_scale,
    cover_detection_timeout,
    dev_only_covers,
    dilation_rect_size,
    google_credentials,
    label_extra_border,
    label_scale,
    refinery_metadata,
    refinery_pass,
    refinery_user,
    test_upload,
    threshold_block_size,
    threshold_subtract_constant,
    web_host,
    web_secret,
)


def find_folder_with_tif_files(root_folder):
    for folder_name, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".tif"):
                return folder_name

time_format = "%Y-%m-%d %H:%M"

image_root_folder = config("IMAGE_ROOT_FOLDER")
folder_with_tif_files = find_folder_with_tif_files(image_root_folder)

if not folder_with_tif_files:
    raise Exception("No unprocessed folder with .tif files found")

session_root_folder = config("SESSION_ROOT_FOLDER")
session_folder = f"{os.path.join(session_root_folder, folder_with_tif_files)}"
session_folder = session_folder.replace(f"/{image_root_folder}", "")
session_folder_new = session_folder

session_exists = os.path.exists(session_folder_new)
session_number = 1

while session_exists:
    session_folder_new = f"{session_folder}-{session_number}"
    session_exists = os.path.exists(session_folder_new)
    session_number += 1

os.makedirs(session_folder_new)

log_file = os.path.join(session_folder_new, "log.txt")

session_time = strftime(time_format, localtime(os.path.getctime(folder_with_tif_files)))
process_time = strftime(time_format, localtime())
with open(log_file, "a") as f:
    f.write(f"Session started: {session_time}\n")
    f.write(f"Process started: {process_time}\n\n")

python_path = config("PYTHON_PATH")
script_folder = config("SCRIPT_FOLDER")
scripts = [
    "1_group_images.py",
    "2_read_labels.py",
    "3_categorize_label_text.py",
    "4_gbif_lookup.py",
    "5_upload_to_web.py",
]

env = os.environ.copy()
env["GOOGLE_APPLICATION_CREDENTIALS"] = str(google_credentials)
env["WEB_HOST"] = str(web_host)
env["WEB_SECRET"] = str(web_secret)
env["REFINERY_USER"] = str(refinery_user)
env["REFINERY_PASS"] = str(refinery_pass)
env["REFINERY_METADATA"] = str(refinery_metadata)
env["IMAGE_FOLDER"] = str(folder_with_tif_files)
env["SESSION_FOLDER"] = str(session_folder_new)
env["COVER_DETECTION_SCALE_PERCENT"] = str(cover_detection_scale)
env["COVER_DETECTION_TIMEOUT_MS"] = str(cover_detection_timeout)
env["FIND_COVER_LABEL_DILATION_RECT_SIZE"] = str(dilation_rect_size)
env["LABEL_SCALE_PERCENT"] = str(label_scale)
env["LABEL_EXTRA_BORDER_PIXELS"] = str(label_extra_border)
env["LABEL_THRESHOLD_BLOCK_SIZE"] = str(threshold_block_size)
env["LABEL_THRESHOLD_SUBTRACT_CONSTANT"] = str(threshold_subtract_constant)
env["DEV_ONLY_COVERS"] = str(dev_only_covers)
env["TEST_UPLOAD"] = str(test_upload)

for script in scripts:
    output = subprocess.run(
        [python_path, os.path.join(script_folder, script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout.decode("utf-8")

    with open(log_file, "a") as f:
        f.write(f"Running {script}\n")
        f.write(output)
        f.write("\n")

    if output.find("Error") > -1:
        break

with open(log_file, "r") as f:
    log = f.read()
    if not log.find("Error") > -1:
        shutil.rmtree(folder_with_tif_files)

with open(log_file, "a") as f:
    f.write(f"Process finished: {strftime(time_format, localtime())}\n")
