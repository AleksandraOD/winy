import pymongo

url = 'mongodb://localhost:27017/wines'
mongoClient = pymongo.MongoClient(url)
winesDB = mongoClient['wines']
winesCol = winesDB['wines']

regionsCol = winesDB['regions']
grapesTypesCol = winesDB['grapesTypes']

def getElements(nameOfElement):
    global winesCol
    els = []
    for wineDoc in winesCol.find():
        if 'description' not in wineDoc:
            print(wineDoc)
            continue
        if nameOfElement not in wineDoc['description']:
            continue
        for el in wineDoc['description'][nameOfElement]:
            if el not in els:
                els.append(el)
    return els

def addElementsToDB(elements, colName):
    for el in elements:
        colName.insert_one({"name": el})

def genRegions():
    global regionsCol
    regions = getElements('Регион:')
    addElementsToDB(regions, regionsCol)

def genGrapesTypes():
    global grapesTypesCol
    grapesTypes = getElements('Сорт винограда:')
    addElementsToDB(grapesTypes, grapesTypesCol)

genRegions()
genGrapesTypes()
