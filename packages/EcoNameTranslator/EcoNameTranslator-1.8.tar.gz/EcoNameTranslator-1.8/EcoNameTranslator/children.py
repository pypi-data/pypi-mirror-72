from .services import createIndex,crushIndexInput,writeApiResultsToIndex,ensureUniqueInIndex,findDownstreamChildren,tagInputWithTaxaLevel,findDownstreamChildren,taxa_ordering
from collections import defaultdict

def children(names):
    index = createIndex(names)
    taggedInput = tagInputWithTaxaLevel([x[0] for x in crushIndexInput(index)])
    groupedByLevel = defaultdict(list)
    writeApiResultsToIndex(index,taggedInput) 
    nameAndRankTuple = crushIndexInput(index)
    for cleanedName,(rank,value) in nameAndRankTuple:
        groupedByLevel[rank].append((cleanedName,(rank,value)))

    for rank in groupedByLevel:
        groupedByLevel[rank] = list(zip(first(groupedByLevel[rank]),findDownstreamChildren(second(groupedByLevel[rank]),nextLowestRank(rank))))
    
    results = []
    for rank in groupedByLevel:
        for cleanedName,(correctedName,res) in groupedByLevel[rank]:
            results.append((cleanedName,res))
    writeApiResultsToIndex(index,results)
    return index

def second(nameRankTuples):
    return list(map(lambda x: x[1], nameRankTuples))

def first(nameRankTuples):
    return list(map(lambda x: x[0], nameRankTuples))

def nextLowestRank(rank):
    previous = "species"
    for item in taxa_ordering:
        if item == rank:
            return previous
        previous = item
    return "species"
    