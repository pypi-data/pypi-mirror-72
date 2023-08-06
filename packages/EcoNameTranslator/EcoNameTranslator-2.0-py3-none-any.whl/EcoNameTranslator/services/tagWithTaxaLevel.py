from ..externalAPIs import Gnr
import itertools
from .services import writeApiResultsToIndex
from .consensus import backed_up

def tagInputWithTaxaLevel(names):
    try:
        taxonomyAPIResults = Gnr.scientificNameToFullTaxonomy(names)
        return list(map(backed_up,taxonomyAPIResults))
    except Exception as e:
        print("Caught fatal exception in taxonomic indexer")
        print(str(e))
        return list(map(lambda x: ('',x),names))


    
