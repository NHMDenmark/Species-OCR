import requests


def standardize_result(result: dict, rank: str):
    if rank.lower() in ["species", "variety", "subsp"]:
        if "species" not in result and "canonicalName" in result:
            result["species"] = result["canonicalName"]
        if "species" in result:
            result["species"] = result["species"].replace("\u00d7", "x")
        if "canonicalName" in result:
            result["canonicalName"] = result["canonicalName"].replace("\u00d7", "x")
        if "species" in result and "genus" not in result:
            result["genus"] = result["species"].split(" ")[0]
        if "species" in result and "canonicalName" not in result:
            result["canonicalName"] = result["species"]
        if (
            rank.lower() == "variety"
            and "canonicalName" in result
            and len(result["canonicalName"].split(" ")) > 2
        ):
            result["variety"] = result["canonicalName"].split(" ")[2]
            result["species"] = " ".join(result["canonicalName"].split(" ")[:2])
        if (
            rank.lower() == "subspecies"
            and "canonicalName" in result
            and len(result["canonicalName"].split(" ")) > 2
        ):
            result["subsp"] = result["canonicalName"].split(" ")[2]
            result["species"] = " ".join(result["canonicalName"].split(" ")[:2])
    return result


def gbif_name_lookup(name: str, rank: str):
    params = {"name": name.lower(), "rank": rank, "kingdom": "plantae", "limit": 1}
    result = requests.get("https://api.gbif.org/v1/species/match?", params).json()

    if not result:
        return None
    else:
        result = standardize_result(result, rank)

        if (
            "synonym" in result
            and result["synonym"] is True
            and "acceptedUsageKey" in result
        ):
            synonym = requests.get(
                f"https://api.gbif.org/v1/species/{result['acceptedUsageKey']}"
            ).json()
            if synonym:
                result["synonymResult"] = standardize_result(synonym, rank)

        return result
