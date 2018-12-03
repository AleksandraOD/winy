from random import randint

import pymongo


class Searcher:
    def __init__(self):
        url = 'mongodb://localhost:27017/wines'
        mongoClient = pymongo.MongoClient(url)
        winesDB = mongoClient['wines']
        self.__winesCol = winesDB['wines']
        self.__initialize()

    def __initialize(self):
        winesByRegion = {}
        winesByType = {}
        regionDescName = 'Регион:'
        typesDescName = 'Сорт винограда:'
        for wineDoc in self.__winesCol.find():
            if 'description' not in wineDoc:
                continue
            wineDescription = wineDoc['description']
            if regionDescName in wineDescription:
                for reg in wineDescription[regionDescName]:
                    if reg in winesByRegion:
                        winesByRegion[reg].append(wineDoc)
                    else:
                        winesByRegion[reg] = [wineDoc]
            if typesDescName in wineDescription:
                for typ in wineDescription[typesDescName]:
                    if typ in winesByType:
                        winesByType[typ].append(wineDoc)
                    else:
                        winesByType[typ] = [wineDoc]
        self.__winesByRegion = winesByRegion
        self.__winesByType = winesByType

    def getRegions(self):
        regions = list(self.__winesByRegion.keys())
        regions.sort()
        return regions

    def getTypes(self):
        types = list(self.__winesByType.keys())
        types.sort()
        return types

    def searchRandomByRegion(self, region):
        if region not in self.__winesByRegion:
            return None
        wines = self.__winesByRegion[region]
        wineInd = randint(0, len(wines) - 1)
        return wines[wineInd]

    def searchRandomByType(self, typ):
        if typ not in self.__winesByType:
            return None
        wines = self.__winesByType[typ]
        wineInd = randint(0, len(wines) - 1)
        return wines[wineInd]
