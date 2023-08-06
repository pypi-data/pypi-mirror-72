

def constructUrls(nameRankTuple,rank):
    givenRank,name = nameRankTuple
    return 'https://api.gbif.org/v1/species/search?q='+name+'&rank='+rank

def processIndividualResult(identifiedResponse,rank):
    nameRankTuple, response = identifiedResponse
    givenRank,name = nameRankTuple
    if 'results' in response:
        potentialSpecies = list(map(lambda x: x.get(rank,''),response['results']))
        potentialSpecies = list(filter(lambda x: x != '',potentialSpecies))
        if givenRank == "genus": potentialSpecies = list(filter(lambda x: x.split(" ")[0].lower() == name.lower(),potentialSpecies))
        return (name,list(set(potentialSpecies)))
    return (name,[])
