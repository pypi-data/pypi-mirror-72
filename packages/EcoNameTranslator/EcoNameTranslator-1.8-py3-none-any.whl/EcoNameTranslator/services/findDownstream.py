from ..externalAPIs import Gbif,Itis

def findDownstreamChildren(nameRankTuples,targetRank):
    try:
        finalRankMapping = {}
        targetRank = targetRank.lower()
        callsNeeded = True
        nameRankTuples = list(map(lambda x: (*x,[x[1]]),nameRankTuples))
        for rank,name,workingNames in nameRankTuples:
            finalRankMapping[name] = []
            if rank == targetRank:
                finalRankMapping[name] = workingNames

        failsafe = 10
        while callsNeeded and failsafe > 0:
            callsNeeded = False
            for k,item in enumerate(nameRankTuples):
                rank,name,workingNames = item
                if len(workingNames) == 0: continue
                callsNeeded = True
                tsns = Itis.retrieveTSNs(workingNames)
                tsns = list(filter(lambda x: x[0] != '',tsns)) # error code is ('',-1)
                if len(tsns) == 0: 
                    nameRankTuples[k] = (rank,name,[])
                    continue
                childrenWithRanks = Itis.downstreamToNextRank([x[1] for x in tsns])
                holding = []
                for childrenResponsesWithTsn in childrenWithRanks:
                    tsn, childrenWithRanks = childrenResponsesWithTsn
                    for childRank,childName in childrenWithRanks:
                        if childRank == targetRank:
                            finalRankMapping[name].append(childName)
                        else:
                            holding.append(childName)
                nameRankTuples[k] = (rank,name,holding)
            failsafe = failsafe - 1
        
        return finalRankMapping.items()
    except Exception as e:
        print("Caught fatal exception in common name resolver")
        print(str(e))
        return list(map(lambda x: (x,[]),nameRankTuples))
