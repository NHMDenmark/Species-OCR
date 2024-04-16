# NHMASpeciesOCR
Python package for processing images of species at the Natural History Museum Aarhus. It is used to automatically retrieve taxonomical information about specimen from the label of the containing folder.

The package is designed as a pipeline of 5 scripts that persist data in a local output file between runs. The last task uploads the persisted data to an instance of [NHMASpeciesWeb](https://github.com/Aksel147/NHMASpeciesWeb).

#### Images
Images for processing must be in .tif format. The images used have a resolution of 8736 × 11648. An image of a folder is followed by images of all the specimen inside the folder, sorted with the file names (e.g. image_0001, image_0002...). Below is an example image of a folder and a specimen.
![examples](./docs/image_examples.png)

## Getting started

### 1. Install dependencies

**Optional**: It is recommended to install dependencies in a python virtual environment. To create and activate a virtual environment, use:
```
python -m venv venv
source ./venv/bin/activate
```

Install dependencies with:
```
pip install -r requirements.txt
```

### 2. Get Google Credentials

The package uses Google Vision API to perform OCR on the images. For this, google credentials are required. Create in [google console](https://console.cloud.google.com/apis/credentials) (free usage up to 1000 images/month). Download the credentials in json format.

### 3. Configure environment

Copy the .env.example file in this directory to .env (which will be ignored by Git):

```
cp .env.example .env
```

Fill in the variables marked as required:

| Variable                       | Description                                    |
|--------------------------------|------------------------------------------------|
| GOOGLE_APPLICATION_CREDENTIALS | Path to the credentials downloaded in step 2.  |
| WEB_HOST                       | URL to [NHMASpeciesWeb](https://github.com/Aksel147/NHMASpeciesWeb) instance (Can be omitted for testing. Instead run the html_report.py script to get local html report) |
| WEB_SECRET                   | Secret for using the upload endpoint of WEB_HOST      |
| REFINERY_USER                 | Username for authenticating for upload with NHMA image server       |
| REFINERY_PASS                 | Password for authenticating for upload with NHMA image server       |
| REFINERY_METADATA                 | Path to template metadata file with some fields set (see metadata-example.json)   |

#### Running with run_scheduled.py

If the processing is done with run_scheduled.py, the following variables are also required:

| Variable                       | Description                                    |
|--------------------------------|------------------------------------------------|
| IMAGE_ROOT_FOLDER | Path to folder, that contains folders of images to process |
| SESSION_ROOT_FOLDER                   | Path to folder where processing sessions will be stored            |
| PYTHON_PATH                 | Path to python for executing the processing scripts  |
| SCRIPT_FOLDER                       | Path to the processing scripts in this package |

#### Running scripts manually

If the scripts are run manually, the following variables are also required:

| Variable                       | Description                                    |
|--------------------------------|------------------------------------------------|
| IMAGE_FOLDER                    | Path to folder of images to process |
| SESSION_FOLDER                   | Path to folder for persisting the session data            |
| SESSION_STARTED_AT                 | ISO8601 Timestamp of when the image session started. Is used to identify a folder of images, once they are uploaded to [NHMASpeciesWeb](https://github.com/Aksel147/NHMASpeciesWeb) |

### 4. Run scripts

To run all five steps, navigate to the scripts folder and use:

```
python 1_group_images.py && python 2_read_labels.py && python 3_categorize_label_text.py && python 4_gbif_lookup.py && python 5_upload_to_web.py
```

## Scripts

To ease the testing and reusability of the package, the steps included are separated in scripts. 

### 1_group_images.py

This script opens all images to determine if they are covers or specimen. A cropped image of the cover is saved. Then the output.json file is created with the following format:

```json
[
  {
    "id": 1,
    "cover": {
      "image_file": "image_0001.tif"
    },
    "specimen": [
      {
        "image_file": "image_0002.tif",
        "id": "AU00100577"
      }
    ]
  }
]
```

The id for a specimen is extracted from the data matrix.

### 2_read_labels.py

This script creates a threshold image from each cover label, reads the full text, and adds it to the output file.

### 3_categorize_label_text.py

This script uses a rule-based approach to attempt to categorize the text read in the previous script. Information about area, family, genus, species, variety and subspecies is added to the output file after this script.

### 4_gbif_lookup.py

This script searches the GBIF database for a match of the highest classification level found in the previous script.

### 5_specimen_metadata.py

This script attaches metadata to all specimen files

### 6_upload_to_web.py

This script uploads the data from the session to [NHMASpeciesWeb](https://github.com/Aksel147/NHMASpeciesWeb).

### 7_upload_images.py

This script uploads the image files of all specimen to an image server of Natural History Museum Denmark

### html_report.py

This script can be used for testing purposes to create a local HTML report of the results, when no [NHMASpeciesWeb](https://github.com/Aksel147/NHMASpeciesWeb) is available.

### run_scheduled.py

This script processes ONE folder in IMAGE_ROOT_FOLDER that contains one or more .tif files. All 7 steps are run, and the outputs saved in a folder with the same name in the SESSION_ROOT_FOLDER. Use this as a scheduled job to run processing automatically.

## Configuration

The package is configured for best performance with the setup and specimen of Aarhus University Herbarium. It is possible to configure environment variables to tweak for other usage. See this description of optional configuration environment variables:

| Variable                            | Description                                                                                                                                                                                          | Default value |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| COVER_DETECTION_SCALE_PERCENT       | 0-100% scale when detecting if image is cover. Lower values yield faster detection, but may cause inability to detect.                                                                               | 75            |
| COVER_DETECTION_TIMEOUT_MS          | Timeout in ms used for cover detection. If timing out, the image is considered a cover. Increase if timing out on specimen.                                                                          | 4000          |
| COVER_DETECTION_THRESHOLD           | "Edge Strength Threshold". Lowering the threshold can increase the number of features to be scanned (thereby slowing performance) but may be necessary if image is blurry or has low contrast.       | 30            |
| COVER_DETECTION_SHRINK              | "Internal Image Shrinking / Fast Pixel Skipping". Sometimes provides dramatic performance benefit. Often helps when image is high resolution but blurry focus.                                       | 3             |
| FIND_COVER_LABEL_DILATION_RECT_SIZE | Rect size for use in morphological closing. Change if processing images of different resolutions.                                                                                                    | 15            |
| LABEL_SCALE_PERCENT                 | 0-100% scale for the label image that is uploaded to web app.                                                                                                                                        | 35            |
| LABEL_EXTRA_BORDER_PIXELS           | Pixel padding for the label crop of covers.                                                                                                                                                          | 100           |
| LABEL_THRESHOLD_BLOCK_SIZE          | Block size used for adaptive threshold of the label for OCR. See [opencv.adaptiveThreshold](https://docs.opencv.org/3.4/d7/d1b/group__imgproc__misc.html#ga72b913f352e4a1b1b397736707afcde3)         | 91            |
| LABEL_THRESHOLD_SUBTRACT_CONSTANT   | Constant subtract used for adaptive threshold of the label for OCR. See [opencv.adaptiveThreshold]( https://docs.opencv.org/3.4/d7/d1b/group__imgproc__misc.html#ga72b913f352e4a1b1b397736707afcde3) | 18            |
| DEV_ONLY_COVERS                     | Set to TRUE when testing on covers, to omit the timeout used in cover detection.                                                                                                                     | FALSE         |
| TEST_UPLOAD                         | Uses a dedicated test endpoint on the image server of NHMA for specimen image upload.                                                                                                                | FALSE         |
| DELETE_IMAGE_FOLDER                 | [Only impacts run_scheduled.py] When this is enabled the folder of a session is removed if all scripts run successfully.                                                                             | FALSE         |
| ALLOW_PREVIOUS_SESSION              | [Only impacts run_scheduled.py] If this is set to FALSE, an image folder is not processed if there is already a session with that name in SESSION_ROOT_FOLDER.                                                              | TRUE          |
