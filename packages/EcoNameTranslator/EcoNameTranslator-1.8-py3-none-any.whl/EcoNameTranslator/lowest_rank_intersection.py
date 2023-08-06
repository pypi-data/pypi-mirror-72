from .classify import classify
from .services import createIndex,crushIndexInput,writeApiResultsToIndex,ensureUniqueInIndex

def lowest_rank_intersection(species):
    index = createIndex(species)
    for item in index:
        ranks = classify([index[item][0]])
        selectedSpeciesRank = ranks[index[item][0]][1]
        index[item] = [index[item][0],selectedSpeciesRank]
    
    data = list(map(lambda x: set(index[x][1].items()),index.keys()))
    common = list(set.intersection(*data))
    return selectLowestCategory(common)

def selectLowestCategory(intersected):
    rankVals = {}
    intersected = dict(intersected) 
    validRanks = ['species','genus','family','order','class','phylum','kingdom','domain']
    for item in validRanks:
        if item in intersected:
            return (item,intersected[item]) 

    return intersected[-1]