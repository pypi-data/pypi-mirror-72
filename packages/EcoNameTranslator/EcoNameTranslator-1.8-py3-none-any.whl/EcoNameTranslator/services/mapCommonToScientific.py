from ..externalAPIs import Itis
import itertools

def commonToScientific(names):
    try:
        return Itis.commonToScientificName(names)
    except Exception as e:
        print("Caught fatal exception in common name resolver")
        print(str(e))
        return list(map(lambda x: (x[0],[]),names))


