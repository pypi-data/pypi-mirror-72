def constructUrls(req):
    return f'http://resolver.globalnames.org/name_resolvers.json?names={req}'

def processIndividualResult(nameResTuple):
    name,response = nameResTuple
    topLevelMapping = (name,response \
                                .get('data',[{}]) \
                                [0] \
                                .get('results',[])) 
    return topLevelMapping

def parseSingleTaxonomyFromAPI(nameResTuple):
    name,taxonomicAPIres = nameResTuple
    dataFromMultipleSources = list(map(extractTaxaData,taxonomicAPIres))
    return (name,dataFromMultipleSources)
    
def extractTaxaData(singleTaxaSource):
    mappingDict = {}
    try: mappingDict = dict(zip(singleTaxaSource['classification_path_ranks'].lower().split("|"),\
                                singleTaxaSource['classification_path'].lower().split("|")))
    except: pass
    return mappingDict
