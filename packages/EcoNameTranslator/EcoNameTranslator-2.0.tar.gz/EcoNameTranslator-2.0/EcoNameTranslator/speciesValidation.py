from .services import profile_taxonomy, \
                      highest_count_wins_multi_cat

from collections import Counter

def sanityCheckOutput(index):
    index = indexToTuples(index)
    enrichedResults = list(map(lambda x: [x[0],x[1],profile_taxonomy(x[2])],index))
    enrichedResults = list(map(lambda x: [x[0],x[1],list(map(lambda x: highest_count_wins_multi_cat(x[1]),x[2]))],enrichedResults))
    enrichedResults = list(map(lambda x: [x[0],x[1],x[2]],enrichedResults))
    for k,(real,cleaned,lst) in enumerate(enrichedResults):
        groupingByOrder = summaryStatsPerCategory(lst).get('order','')            
        rankedGrouping = sorted(groupingByOrder.items(),key=lambda x: x[1],reverse=True)
        if len(rankedGrouping) == 0:
            enrichedResults[k] = [real,cleaned,[]]
        else:
            print(takeSpeciesMatchingGroupOnly(rankedGrouping[0][0],'order',lst))
            enrichedResults[k] = [real,cleaned,takeSpeciesMatchingGroupOnly(rankedGrouping[0][0],'order',lst)]
    
    return dict(list(map(lambda x:[x[0],[*x[1:]]],enrichedResults)))

def summaryStatsPerCategory(result):
    groups = {cat:list(map(lambda x: x.get(cat,''),result)) for cat in ['kingdom','phylum','order','class','family','genus']}
    summaryStats = {k:grouping(v) for (k,v) in groups.items()}
    return summaryStats

def grouping(values):
    return dict(Counter(values))

def indexToTuples(index):
    return list(map(lambda x: [x,*index[x]],list(index.keys())))

def takeSpeciesMatchingGroupOnly(group,level,data):
    species = []
    for item in data:
        if item[level] == group:
            species.append(item['species'])
    
    return species