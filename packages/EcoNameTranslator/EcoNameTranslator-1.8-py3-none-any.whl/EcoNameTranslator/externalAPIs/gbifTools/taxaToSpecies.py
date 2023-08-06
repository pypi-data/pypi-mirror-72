
def constructUrls(nameAndTaxaTuple):
    rank,value = nameAndTaxaTuple
    return 'https://api.gbif.org/v1/species/search?q='+value+'&rank=species'

def processIndividualResult(identifiedResponse):
    inTuple, response = identifiedResponse
    rank, value = inTuple
    if 'results' in response:
        potentialSpecies = list(map(lambda x: x.get('species',''),response['results']))
        potentialSpecies = list(filter(lambda x: x != '',potentialSpecies))
        if rank == "genus": potentialSpecies = list(filter(lambda x: x.split(" ")[0].lower() == value.lower(),potentialSpecies))
        return (rank,value,list(set(potentialSpecies)))
    return (rank,value,[])