from .services import scientificToCommon,tagInputWithTaxaLevel,createIndex,mapKnownTaxaLevelToSpecies,crushIndexInput,writeApiResultsToIndex,ensureUniqueInIndex

def to_common(uncheckedNames,includeCommon=True):
    index = createIndex(uncheckedNames)

    results = tagInputWithTaxaLevel([x[0] for x in crushIndexInput(index)])
    writeApiResultsToIndex(index,results)
    results = mapKnownTaxaLevelToSpecies([x for x in crushIndexInput(index) if x[1][0] not in ['species','']])
    results = list(map(lambda x: (x[0],x[1][2]),results))
    writeApiResultsToIndex(index,results)
    for item in index:
        cleanedName, resultSoFar = index[item]
        if len(resultSoFar) == 0:
            index[item] = [cleanedName,[]]
        elif resultSoFar[0] == 'species':
            index[item] = [cleanedName,[resultSoFar[1]]]
        elif resultSoFar == ('',''):
            index[item] = [cleanedName,[]]

    failedDirectScientific = [x[0] for x in crushIndexInput(index) if len(x[1]) > 0]
    results = scientificToCommon(failedDirectScientific)
    writeApiResultsToIndex(index,results)
    
    ensureUniqueInIndex(index)

    return index