
import itertools 
import operator
from .services import createIndex,crushIndexInput,writeApiResultsToIndex,ensureUniqueInIndex,profile_taxonomy

def classify(uncheckedNames):
    index = createIndex(uncheckedNames)
    results = profile_taxonomy([x[0] for x in crushIndexInput(index)])
    results = list(map(runConsensusForSingleSpecies,results))
    writeApiResultsToIndex(index,results)
    return index

def runConsensusForSingleSpecies(nameAndResTuple):
    finalMapping = {}
    name,individualDictionaryMappings = nameAndResTuple
    remove = set(['','no rank'])
    ranks = list(set(itertools.chain(*list(map(lambda x: x.keys(),individualDictionaryMappings)))) - remove)
    for taxaRank in ranks:
        finalMapping[taxaRank] = runConsensusOnSingleTaxa(taxaRank,individualDictionaryMappings)
    return (name,finalMapping)

def runConsensusOnSingleTaxa(taxaRank,individualDictionaryMappings):
    allItemsOfTaxa = []
    for singleMapping in individualDictionaryMappings:
        val = singleMapping.get(taxaRank,'')
        if len(val) > 0: allItemsOfTaxa.append(val)
    
    if len(allItemsOfTaxa) == 0: return ''
    return mostCommonInList(allItemsOfTaxa)

def warnSpeciesNameFailure(individualResult):
    print("Could not index " + str(individualResult['supplied_name_string']))

def mostCommonInList(L):
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  return max(groups, key=_auxfun)[0]