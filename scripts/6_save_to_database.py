import json
import mysql.connector
from nhma_species_ocr.util.variables import output_file, db_host, db_user, db_password, db_database


with open(output_file) as file:
    grouped_specimen_list = json.load(file)

covers = []
specimen = []

for index, group in enumerate(grouped_specimen_list):
    print("SAVE TO DB: group #{0} of {1}...".format(index+1, len(grouped_specimen_list)))

    cover = group['cover']

    covers.append((
        #group['id'],
        cover['image_file'],
        f"{cover['image_file'][:-4]}.png",
        json.dumps(cover['full_paragraphs']),
        cover['area']['text'],
        cover['family']['text'],
        cover['genus']['text'],
        cover['species']['text'],
        cover['variety']['text'],
        cover['subsp']['text'],
        json.dumps(cover['gbif_match']),
        cover['highest_classification_level'],
        cover['error'],
        False,
    ))

mydb = mysql.connector.connect(
  host = db_host,
  user = db_user,
  password = db_password,
  database = db_database
)

mycursor = mydb.cursor()

sql = """
INSERT INTO covers (
    image,
    label,
    ocr_read_json,
    area,
    family,
    genus,
    species,
    variety,
    subsp,
    gbif_match_json,
    highest_classification,
    flagged,
    approved
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
 
mycursor.executemany(sql, covers)
mydb.commit()

mydb.close()