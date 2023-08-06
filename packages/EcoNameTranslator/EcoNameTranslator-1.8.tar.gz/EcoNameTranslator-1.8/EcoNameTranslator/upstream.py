from .services import commonToScientific,\
                      tagInputWithTaxaLevel,\
                      createIndex,\
                      mapKnownTaxaLevelToSpecies,\
                      crushIndexInput,\
                      writeApiResultsToIndex,\
                      ensureUniqueInIndex,taxa_ordering,\
                      findDownstreamChildren

from .classify import classify
from .downstream import downstream
from collections import defaultdict

def upstream(names,rank):
    index = createIndex(names)
    handlingRank = nextHighestRank(rank)
    classifications = crushIndexInput(classify(names))
    classifications = list(map(lambda x: (x[0],x[1][handlingRank]),classifications))
    writeApiResultsToIndex(index,classifications)

    results = crushIndexInput(index)
    namesOnly = [x[0] for x in results]
    handlingRankInput = [(handlingRank,x[1]) for x in results]
    results = list(zip(namesOnly,[x[1] for x in findDownstreamChildren(handlingRankInput,rank)]))
    writeApiResultsToIndex(index,results)
    return index

def nextHighestRank(rank):
    following = "species"
    newTaxaOrder = [x for x in taxa_ordering]
    newTaxaOrder.append("species")
    for i in range(len(newTaxaOrder)):
        if i == len(newTaxaOrder) - 1: break
        following = newTaxaOrder[i+1]
        if newTaxaOrder[i] == rank:
            break
    return following
