
import os
import pickle
import csv 
import itertools
from .dataCleaning import cleanSingleSpeciesString
from .constants import taxa_ordering

def writeApiResultsToIndex(index,taxonomyAPIResults):
    taxaAPIDict = {}
    newIndex = {}
    for cleanedName,result in taxonomyAPIResults:
        taxaAPIDict[cleanedName] = result
    
    for name in index:
        newIndex[name] = index[name]
        if index[name][0] in taxaAPIDict:
            newIndex[name][1] = taxaAPIDict[index[name][0]]
    
    return newIndex
    
def ensureUniqueInIndex(index):
    for name in index:
        species = index[name][1]
        species = list(set(species))
        index[name][1] = species

def createIndex(uncheckedNames):
    index = {}
    for item in uncheckedNames:
        index[item] = [cleanSingleSpeciesString(item),'']
    
    return index
        
def crushIndexInput(index):
    return list(map(lambda x: (index[x][0],index[x][1]),index.keys()))