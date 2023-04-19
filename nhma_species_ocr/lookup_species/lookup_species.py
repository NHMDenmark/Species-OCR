from pygbif import species as GBIF_species


def lookup_species(species):
    res = GBIF_species.name_lookup(q=species, rank="species", limit=1)
    if res['count'] == 0 or 'canonicalName' not in  res['results'][0]:
        return None
    else:
        return res['results'][0]