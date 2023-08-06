from ..externalAPIs import Gbif
import itertools

def mapKnownTaxaLevelToSpecies(nameAndTaxaTuples):
    try:
        names = list(map(lambda x: x[0], nameAndTaxaTuples))
        taxaTuples = list(map(lambda x: x[1], nameAndTaxaTuples))
        speciesNamesOnly = Gbif.higherTaxaToSpecies(taxaTuples)
        speciesNamesOnly = list(zip(names,speciesNamesOnly))
        return speciesNamesOnly
    except Exception as e:
        print("Caught fatal exception in taxonomic level resolver")
        print(str(e))
        return list(map(lambda x: (x[0],[]), nameAndTaxaTuples))