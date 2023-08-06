import itertools 

def constructUrls(name):
    return "https://www.itis.gov/ITISWebService/jsonservice/getITISTermsFromScientificName?srchKey="+name

def processIndividualResult(nameAndResTuple):
    name,res = nameAndResTuple
    if 'itisTerms' not in res: return []
    if res['itisTerms'] is None: return []
    if res['itisTerms'][0] is None: return []
    nameTranslation = res['itisTerms']
    resultsToReturn = []
    for item in nameTranslation:
        if 'commonNames' not in item: continue 
        if item['commonNames'] is None: continue 
        cleanResults = list(filter(lambda x: x is not None,item['commonNames']))
        cleanResults = list(map(lambda x: " ".join(list(map(lambda y: y.capitalize(),x.split(" ")))),cleanResults))
        resultsToReturn.append(cleanResults)
    
    return (name,list(itertools.chain(*resultsToReturn)))