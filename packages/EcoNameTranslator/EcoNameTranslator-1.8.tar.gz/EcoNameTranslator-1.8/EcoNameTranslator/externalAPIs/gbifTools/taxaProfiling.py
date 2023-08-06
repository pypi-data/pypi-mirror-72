def constructTaxaProfilingUrl(name):
    return 'https://api.gbif.org/v1/species?name='+name

def processTaxaProfilingIndividualResult(nameResTuple):
    name,response = nameResTuple
    return (name,response['result'])