from nhma_species_ocr.util.area_authority_list import area_authority_list


def report_entry(
        id: int,
        number: int,
        total: int,
        area: str,
        classification: dict,
        classification_gbif: dict,
        highest_classification_level: str,
        png_base64: bytes = [],
        full_paragraphs: list = [], 
    ):
    full_paragraphs_html = "" 
    for paragraph in full_paragraphs:
        paragraph_text = ' '.join([word['text'] for word in paragraph['words']])
        full_paragraphs_html += "<div>" + paragraph_text + "</div>"

        if area in area_authority_list: 
            class_area = "equal"
        else:
            class_area = "error"

        class_classification = {
            'family':  "",
            'genus':   "",
            'species': "",
            'variety': "",
            'subsp':   "",
        }

        if highest_classification_level:
            if classification[highest_classification_level] != "" and classification_gbif[highest_classification_level] != "":
                if classification[highest_classification_level].lower() == classification_gbif[highest_classification_level].lower():
                    class_classification[highest_classification_level] = "equal"
                else:
                    class_classification[highest_classification_level] = "different"
            else:
                class_classification[highest_classification_level] = "error"
        
    return """

<div class="card-container">
<div class="card-top">
    <h4>
#""" + id.__str__() + """
    </h4>
    <h4>
""" + number.__str__() + " of " + total.__str__() + """
    </h4>
</div>
<div class="card">
    <div class="left">
        <img src="data:image/png;base64,""" + png_base64 + """" />
        <div class="ocr">
""" + full_paragraphs_html + """
        </div>
    </div>
    <div class="right">
        <table>
            <tr class="top-row">
                <th class="
""" + class_area + """
                ">
                    Area
                </th>
                <td class="
""" + class_area + """
                " colspan="2">
""" + area + """
                </td>
            </tr>
            <tr>
                <th></th>
                <th class="title">
                    Detected
                </th>
                <th class="title">
                    GBIF
                </th>
            </tr>
            <tr>
                <th class="
""" + class_classification['family'] + """"
                ">
                    Family
                </th>
                <td class="
""" + class_classification['family'] + """"
                ">
""" + classification['family'] + """
                </td>
                <td class="
""" + class_classification['family'] + """"
                ">
""" + classification_gbif['family'] + """
                </td>
            </tr>
            <tr>
                <th class="
""" + class_classification['genus'] + """"
                ">
                    Genus
                </th>
                <td class="
""" + class_classification['genus'] + """"
                ">
""" + classification['genus'] + """
                </td>
                <td class="
""" + class_classification['genus'] + """"
                ">
""" + classification_gbif['genus'] + """
                </td>
            </tr>
            <tr>
                <th class="
""" + class_classification['species'] + """"
                ">
                    Species
                </th>
                <td class="
""" + class_classification['species'] + """"
                ">
""" + classification['species'] + """
                </td>
                <td class="
""" + class_classification['species'] + """"
                ">
""" + classification_gbif['species'] + """
                </td>
            </tr>
            <tr>
                <th class="
""" + class_classification['variety'] + """"
                ">
                    Variety
                </th>
                <td class="
""" + class_classification['variety'] + """"
                ">
""" + classification['variety'] + """
                </td>
                <td class="
""" + class_classification['variety'] + """"
                ">
""" + classification_gbif['variety'] + """
                </td>
            </tr>
            <tr>
                <th class="
""" + class_classification['subsp'] + """"
                ">
                    Subsp.
                </th>
                <td class="
""" + class_classification['subsp'] + """"
                ">
""" + classification['subsp'] + """
                </td>
                <td class="
""" + class_classification['subsp'] + """"
                ">
""" + classification_gbif['subsp'] + """
                </td>
            </tr>
        </table>
    </div>
</div>
</div>

"""