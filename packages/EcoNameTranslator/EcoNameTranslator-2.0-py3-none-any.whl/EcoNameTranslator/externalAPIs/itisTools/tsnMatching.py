
def constructUrls(name):
    return "https://www.itis.gov/ITISWebService/jsonservice/searchByScientificName?srchKey="+name

def processIndividualResult(nameAndResTuple):
    name,res = nameAndResTuple
    errorCode = (name,-1)
    if 'scientificNames' not in res: return errorCode
    if res['scientificNames'] is None: return errorCode
    if len(res['scientificNames']) == 0: return errorCode

    for item in res['scientificNames']:
        if 'combinedName' not in item: continue
        if item['combinedName'] is None: continue
        if item['combinedName'].lower() == name.lower():
            if item['tsn'] is None: return errorCode 
            return (name,item['tsn'])
    
    return errorCode