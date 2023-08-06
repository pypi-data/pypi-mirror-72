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
from .speciesValidation import sanityCheckOutput
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
