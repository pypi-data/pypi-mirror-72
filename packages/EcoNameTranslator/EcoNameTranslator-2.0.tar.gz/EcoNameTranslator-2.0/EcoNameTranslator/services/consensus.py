
from .constants import taxa_ordering
import itertools 
import operator
from collections import defaultdict
# "Back up" a claim of a taxonomic generalisation
# with at least ONE other source

def backed_up(nameResTuple):
    name,dataFromMultipleSources = nameResTuple
    if len(dataFromMultipleSources) < 2:
        return short_circuit(nameResTuple)
    taxonomicClasses = defaultdict(list)
    for item in taxa_ordering:
        for taxaMap in dataFromMultipleSources:
            if taxaMap.get(item,'').strip() != '': 
                taxonomicClasses[item].append(taxaMap[item].strip().lower())

    
    for item in taxa_ordering:
        if len(taxonomicClasses.get(item,'')) > 1: #percentage of data sources?
            return (name,(item,mostCommonInList(taxonomicClasses[item])))
    return short_circuit(nameResTuple)

def short_circuit(nameResTuple):
    name,dataFromMultipleSources = nameResTuple
    for item in taxa_ordering:
        for taxaMap in dataFromMultipleSources:
            if (item in taxaMap) and (taxaMap[item].strip() != ''): 
                return (name,(item,taxaMap[item].strip()))
    return (name,('',''))

def highest_count_wins_multi_cat(inputStruct):
    dataFromMultipleSources = []
    if len(inputStruct) == 2:
        name,dataFromMultipleSources = inputStruct
    else:
        dataFromMultipleSources = inputStruct
    grouped = {item: \
                mostCommonInList( \
                    list( \
                        filter( \
                            lambda groupVal: groupVal != '', \
                            map( \
                                lambda taxaDict: taxaDict.get(item,''), \
                                dataFromMultipleSources \
                            ) \
                        ) \
                    ) \
                )
                for item in taxa_ordering}
    
    if len(inputStruct) == 2:
        return (name,grouped)
    
    return grouped

def mostCommonInList(L,emptyOnDefault=''):
  if len(L) == 0: return emptyOnDefault
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  return max(groups, key=_auxfun)[0]