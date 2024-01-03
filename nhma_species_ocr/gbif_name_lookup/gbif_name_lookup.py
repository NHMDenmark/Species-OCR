import requests


def standardize_result(result: dict, rank: str) -> dict:
    """Cleans the return value from GBIF, and makes sure the value for the rank
    specified is set

    Args:
        result (dict): GBIF result dict
        rank (str): Taxonomical rank searched for

    Returns:
        dict: Standardized GBIF result dict value
    """
    if rank.lower() in ["species", "variety", "subspecies"]:
        if "species" in result:
            result["species"] = result["species"].replace("\u00d7", "x")
        if "canonicalName" in result:
            result["canonicalName"] = result["canonicalName"].replace("\u00d7", "x")
        if "canonicalName" in result and len(result["canonicalName"].split(" ")) > 1:
            result["species"] = " ".join(result["canonicalName"].split(" ")[:2])
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
        if (
            rank.lower() == "subspecies"
            and "canonicalName" in result
            and len(result["canonicalName"].split(" ")) > 2
        ):
            result["subsp"] = result["canonicalName"].split(" ")[2]
    return result


def gbif_name_lookup(name: str, rank: str) -> dict:
    """Searches GBIF for a result within the 'plantae' kingdom matching the name and
    rank specified

    Args:
        name (str): query name
        rank (str): query rank

    Returns:
        dict: GBIF result, else None
    """
    params = {"name": name.lower(), "rank": rank, "limit": 3}
    data: list = requests.get("https://api.gbif.org/v1/species?", params).json()

    if not (data and "results" in data and len(data["results"]) > 0):
        return None

    results = [
        result
        for result in data["results"]
        if "kingdom" in result and result["kingdom"].lower() == "plantae"
    ]

    return standardize_result(results[0], rank) if len(results) > 0 else None
