import itertools
from .apiUtils import safeMapResToJson, concurrentExecRequests
from .gnrTools import taxaProfiling

class Gnr:
    def __init__(self):
        pass

    # [Names] => [SuccessfulResponses], [FailedNames]
    @staticmethod
    def scientificNameToFullTaxonomy(names):
        capnames = list(map(lambda x: x.capitalize(),names))
        urls = list(map(taxaProfiling.constructUrls,capnames))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(names,results))
        results = list(map(taxaProfiling.processIndividualResult,results))
        results = list(map(taxaProfiling.parseSingleTaxonomyFromAPI,results))
        return results
    