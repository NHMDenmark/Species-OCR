import os
import shutil
import subprocess
from time import localtime, strftime

from decouple import config

from nhma_species_ocr.util.variables import delete_image_folder


def find_folder_with_tif_files(root_folder):
    for folder_name, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".tif"):
                return folder_name


time_format = "%Y-%m-%d %H:%M"

image_root_folder = config("IMAGE_ROOT_FOLDER")
folder_with_tif_files = find_folder_with_tif_files(image_root_folder)

if not folder_with_tif_files:
    raise Exception("No folder with .tif files found")

session_root_folder = config("SESSION_ROOT_FOLDER")
session_folder = (
    f"{os.path.join(session_root_folder, os.path.basename(folder_with_tif_files))}"
)
session_folder_new = f"{session_folder}-00"

session_exists = os.path.exists(session_folder_new)
session_number = 1

while session_exists:
    session_folder_new = (
        f"{session_folder}-{'0' if session_number < 10 else ''}{session_number}"
    )
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
    "6_upload_images.py",
]

env = os.environ.copy()
env["IMAGE_FOLDER"] = str(folder_with_tif_files)
env["SESSION_FOLDER"] = str(session_folder_new)

for script in scripts:
    output = subprocess.run(
        [python_path, os.path.join(script_folder, script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout.decode("utf-8")

    with open(log_file, "a") as f:
        f.write(f"Running {script}\n")
        f.write(output.replace("\n\n", "\n"))
        f.write("\n")

    if output.find("Error") > -1:
        break

with open(log_file, "r") as f:
    log = f.read()
    if delete_image_folder and not log.find("Error") > -1:
        shutil.rmtree(folder_with_tif_files)

with open(log_file, "a") as f:
    f.write(f"Process finished: {strftime(time_format, localtime())}\n")
