
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

def to_scientific(names):
    index = createIndex(names)
    results = commonToScientific(names)
    writeApiResultsToIndex(index,results)
    return index
