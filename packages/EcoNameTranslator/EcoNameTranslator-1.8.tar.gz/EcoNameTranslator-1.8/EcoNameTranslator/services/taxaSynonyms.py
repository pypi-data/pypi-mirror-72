from ..externalAPIs import Itis


def get_synonyms(names):
    try:
        tsns = Itis.retrieveTSNs(names)
        synonyms = Itis.getSynonymsFromTSNs([x[1] for x in tsns])
        tsnToNameMap = dict(list(map(lambda x: (x[1],x[0]),tsns)))
        return list(map(lambda x: (tsnToNameMap[x[0]],x[1]),synonyms))
    except Exception as e:
        print("Caught fatal exception in common name resolver")
        print(str(e))
        return list(map(lambda x: (x,[]),names))
