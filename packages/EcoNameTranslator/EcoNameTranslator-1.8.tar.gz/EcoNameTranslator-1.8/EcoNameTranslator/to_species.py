from .services import commonToScientific, \
                      tagInputWithTaxaLevel, \
                      createIndex, \
                      mapKnownTaxaLevelToSpecies, \
                      crushIndexInput, \
                      writeApiResultsToIndex, \
                      ensureUniqueInIndex, \
                      profile_taxonomy, \
                      highest_count_wins_multi_cat, \
                      findDownstreamChildren

from collections import Counter

def to_species(uncheckedNames,includeCommon=True,sanityCorrect=False):
    index = createIndex(uncheckedNames)
    results = tagInputWithTaxaLevel([x[0] for x in crushIndexInput(index)])
    writeApiResultsToIndex(index,results)
    higherTaxaOnly = [x for x in crushIndexInput(index) if x[1][0] not in ['species','']]
    namesOnly = first(higherTaxaOnly)
    rankTuples = second(higherTaxaOnly)
    results = list(zip(namesOnly,[x[1] for x in findDownstreamChildren(rankTuples,'species')]))
    writeApiResultsToIndex(index,results)
    for item in index:
        cleanedName, resultSoFar = index[item]
        if len(resultSoFar) == 0:
            index[item] = [cleanedName,[]]
        elif resultSoFar[0] == 'species':
            index[item] = [cleanedName,[resultSoFar[1]]]
        elif resultSoFar == ('',''):
            index[item] = [cleanedName,[]]

    failedDirectScientific = [x[0] for x in crushIndexInput(index) if len(x[1]) == 0]
    results = commonToScientific(failedDirectScientific)
    writeApiResultsToIndex(index,results)
    ensureUniqueInIndex(index)
    if sanityCorrect: 
        index = sanityCheckOutput(index)
    return index

def second(nameRankTuples):
    return list(map(lambda x: x[1], nameRankTuples))

def first(nameRankTuples):
    return list(map(lambda x: x[0], nameRankTuples))

def sanityCheckOutput(index):
    index = indexToTuples(index)
    enrichedResults = list(map(lambda x: [x[0],x[1],profile_taxonomy(x[2])],index))
    enrichedResults = list(map(lambda x: [x[0],x[1],list(map(lambda x: highest_count_wins_multi_cat(x[1]),x[2]))],enrichedResults))
    enrichedResults = list(map(lambda x: [x[0],x[1],x[2]],enrichedResults))
    for k,(real,cleaned,lst) in enumerate(enrichedResults):
        groupingByOrder = summaryStatsPerCategory(lst).get('order','')            
        rankedGrouping = sorted(groupingByOrder.items(),key=lambda x: x[1],reverse=True)
        if len(rankedGrouping) == 0:
            enrichedResults[k] = [real,cleaned,[]]
        else:
            enrichedResults[k] = [real,cleaned,takeSpeciesMatchingGroupOnly(rankedGrouping[0][0],'order',lst)]
    
    return dict(list(map(lambda x:[x[0],[*x[1:]]],enrichedResults)))

def summaryStatsPerCategory(result):
    groups = {cat:list(map(lambda x: x.get(cat,''),result)) for cat in ['kingdom','phylum','order','class','family','genus']}
    summaryStats = {k:grouping(v) for (k,v) in groups.items()}
    return summaryStats

def grouping(values):
    return dict(Counter(values))

def indexToTuples(index):
    return list(map(lambda x: [x,*index[x]],list(index.keys())))

def takeSpeciesMatchingGroupOnly(group,level,data):
    species = []
    for item in data:
        if item[level] == group:
            species.append(item['species'])
    
    return species