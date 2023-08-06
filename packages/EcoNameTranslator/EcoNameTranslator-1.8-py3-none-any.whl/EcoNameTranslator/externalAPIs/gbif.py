from .apiUtils import safeMapResToJson,concurrentExecRequests
from .gbifTools import taxaToSpecies,taxaProfiling,diveDownTaxaTree

class Gbif:
    def __init__(self):
        pass 

    @staticmethod
    def higherTaxaToSpecies(originalNamesWithTaxa):
        urls = list(map(taxaToSpecies.constructUrls,originalNamesWithTaxa))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(originalNamesWithTaxa,results))
        results = list(map(taxaToSpecies.processIndividualResult,results))
        return results

    @staticmethod
    def scientificNameToFullTaxonomy(names):
        capNames = list(map(lambda x: x.capitalize(),names))
        urls = list(map(taxaProfiling.constructTaxaProfilingUrl,capNames))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(names,results))
        results = list(map(taxaProfiling.processTaxaProfilingIndividualResult,results))
        return results
    
    @staticmethod
    def downstreamToRank(nameRankTuples,rank):
        capNames = list(map(lambda x: (x[0].capitalize(),x[1]),nameRankTuples))
        urls = list(map(lambda x: diveDownTaxaTree.constructUrls(x,rank),capNames))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(nameRankTuples,results))
        results = list(map(lambda x: diveDownTaxaTree.processIndividualResult(x,rank),results))
        return results