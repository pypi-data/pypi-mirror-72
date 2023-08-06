
from .services import commonToScientific, \
                      tagInputWithTaxaLevel, \
                      createIndex, \
                      mapKnownTaxaLevelToSpecies, \
                      crushIndexInput, \
                      writeApiResultsToIndex, \
                      ensureUniqueInIndex, \
                      profile_taxonomy, \
                      highest_count_wins_multi_cat, \
                      findDownstreamChildren \

from .speciesValidation import sanityCheckOutput

def to_scientific(names,sanityCheck=False):
    index = createIndex(names)
    results = commonToScientific(names)
    writeApiResultsToIndex(index,results)
    if sanityCheck: 
        index = sanityCheckOutput(index)
    ensureUniqueInIndex(index)
    return index
