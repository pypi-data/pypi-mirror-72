
def constructUrls(tsn):
    return 'https://www.itis.gov/ITISWebService/jsonservice/getHierarchyDownFromTSN?tsn='+tsn

def processIndividualResult(nameResTuple):
    name,result = nameResTuple
    if 'hierarchyList' not in result or len(result['hierarchyList']) == 0:
        return (name,[])
    
    return (name,list(map(lambda x: (x['rankName'].lower(),x['taxonName']),result['hierarchyList'])))
