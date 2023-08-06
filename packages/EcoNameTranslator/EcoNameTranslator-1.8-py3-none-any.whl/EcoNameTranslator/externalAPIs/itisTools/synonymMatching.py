

def constructUrls(id_):
    return "https://www.itis.gov/ITISWebService/jsonservice/getSynonymNamesFromTSN?tsn="+id_

def processIndividualResult(idAndResTuple):
    id_,res = idAndResTuple
    errorCode = (id_,[])
    results = []
    if 'synonyms' not in res: return errorCode
    if res['synonyms'] is None: return errorCode
    if res['synonyms'][0] is None: return errorCode
    if len(res['synonyms']) == 0: return errorCode

    for item in res['synonyms']:
        if 'sciName' not in item: continue
        if item['sciName'] is None: continue
        results.append(item['sciName'])
    
    return (id_,results)