import itertools 

def constructUrls(name):
    return "https://itis.gov/ITISWebService/jsonservice/getITISTermsFromCommonName?srchKey="+name

def processIndividualResult(nameAndResTuple):
    name,res = nameAndResTuple
    if 'itisTerms' not in res: return (name,[])
    if res['itisTerms'] is None: return (name,[])
    if res['itisTerms'][0] is None: return (name,[])
    nameTranslation = res['itisTerms']
    scientificNames = processTranslationToScientificName(name,nameTranslation)
    scientificNames = expandIfHigherLevelTaxaName(scientificNames)
    return (name,scientificNames)

def processTranslationToScientificName(name,nameTranslation):
    sNames = list(filter(containsUsableData,nameTranslation))
    sNames = list(filter(lambda x: containsValidCommonName(name,x['commonNames']), sNames))
    return list(map(lambda x: x['scientificName'],sNames))

def expandIfHigherLevelTaxaName(scientificNames):
    return list(filter(lambda x: len(x.strip().split(" ")) > 1,scientificNames))

def containsUsableData(individualCommonNameResult):
    return \
        'scientificName' in individualCommonNameResult and \
        'commonNames' in individualCommonNameResult and \
        individualCommonNameResult['commonNames'][0] is not None and \
        individualCommonNameResult['scientificName'] is not None

def containsValidCommonName(name,listOfCommonNames):
    if len(name.strip().split(" ")) > 1: return True
    return any(list(map(lambda x: checkIfCommonNameResultIsValid(name,x),listOfCommonNames)))

def checkIfCommonNameResultIsValid(name,result):
    result = result.lower().split(" ")
    stringPotential1 = name 
    stringPotential2 = name+'s' #plurals
    return stringPotential1 in result or stringPotential2 in result