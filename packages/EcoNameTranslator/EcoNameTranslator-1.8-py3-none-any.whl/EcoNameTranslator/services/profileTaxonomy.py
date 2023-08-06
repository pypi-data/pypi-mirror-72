from ..externalAPIs import Gnr
import itertools
from .constants import taxa_ordering
from .services import writeApiResultsToIndex

def profile_taxonomy(names):
    try:
        return Gnr.scientificNameToFullTaxonomy(names)
    except Exception as e:
        print("Caught fatal exception in taxonomic indexer")
        print(str(e))
        return {}    
