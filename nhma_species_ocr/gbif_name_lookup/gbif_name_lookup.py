import requests


def gbif_name_lookup(name: str, rank: str):
    params = {'name': name, 'rank': rank, 'limit': 1}
    res = requests.get("https://api.gbif.org/v1/species?", params).json()
    # print(res)
    if not res['results'] or res['results'].__len__() == 0:
        return None
    else:
        result = res['results'][0]
        if rank.lower() in ['species', 'variety', 'subsp']:
            if 'species' not in result and 'canonicalName' in result:
                result['species'] = result['canonicalName']
            if 'species' in result:
                result['species'] = result['species'].replace('\u00d7', 'x')
            if 'canonicalName' in result:
                result['canonicalName'] = result['canonicalName'].replace('\u00d7', 'x')
            if 'species' in result and 'genus' not in result:
                result['genus'] = result['species'].split(' ')[0]
            if 'species' in result and 'canonicalName' not in result:
                result['canonicalName'] = result['species']
            if rank.lower() == "variety" and 'canonicalName' in result:
                result['variety'] = result['canonicalName'].split(' ')[2]
                result['species'] = ' '.join(result['canonicalName'].split(' ')[:2])
        return result
