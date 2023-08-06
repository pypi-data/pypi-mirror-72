from .services import createIndex,crushIndexInput,writeApiResultsToIndex,ensureUniqueInIndex,get_synonyms

def synonyms(names):
    index = createIndex(names)
    results = get_synonyms([x[0] for x in crushIndexInput(index)])
    writeApiResultsToIndex(index,results)
    return index
