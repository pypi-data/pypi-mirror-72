import itertools
from .apiUtils import safeMapResToJson, concurrentExecRequests
from .itisTools import commonToScientific, \
                       scientificToCommon, \
                       tsnMatching, \
                       synonymMatching, \
                       downstreamHierarchy

class Itis:
    def __init__(self):
        pass 

    @staticmethod
    def commonToScientificName(names):
        urls = list(map(commonToScientific.constructUrls,names))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(names,results))
        results = list(map(commonToScientific.processIndividualResult,results))
        return results

    @staticmethod
    def scientificToCommonName(names):
        urls = list(map(scientificToCommon.constructUrls,names))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(names,results))
        results = list(map(scientificToCommon.processIndividualResult,results))
        return results
    
    @staticmethod
    def retrieveTSNs(names):
        urls = list(map(tsnMatching.constructUrls,names))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(names,results))
        results = list(map(tsnMatching.processIndividualResult,results))
        return results
    
    @staticmethod
    def getSynonymsFromTSNs(tsns):
        urls = list(map(synonymMatching.constructUrls,tsns))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(tsns,results))
        results = list(map(synonymMatching.processIndividualResult,results))
        return results
    
    @staticmethod
    def downstreamToNextRank(tsns):
        urls = list(map(downstreamHierarchy.constructUrls,tsns))
        results = concurrentExecRequests(urls)
        results = safeMapResToJson(results)
        results = list(zip(tsns,results))
        return list(map(downstreamHierarchy.processIndividualResult,results))
        

