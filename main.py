import urllib.request
from bs4 import BeautifulSoup
import pymongo
import ssl

mongoClient = pymongo.MongoClient('mongodb://localhost:27017/wines')
wineDB = mongoClient['wines']
winesCol = wineDB['wines']

def wineExists(vendorCode):
    global winesCol
    docs = winesCol.find({'_id': vendorCode})
    return docs.count() > 0

def addWineToDB(doc):
    global winesCol
    winesCol.insert_one(doc)

def getVendorCode(form):
    vendorCodeEls = form.select('span[title="Артикул"]')
    if len(vendorCodeEls) < 1:
        return None
    return vendorCodeEls[0].text[len('Артикул:'):]

def getTitle(form):
    els = form.select('p.title')
    if len(els) < 1:
        return ''
    return els[0]['data-prodname']

def getDescriptionFields(form):
    els = form.select('.list-description li')
    res = {}
    for el in els:
        nameEls = el.select('span.name')
        if len(nameEls) < 1:
            continue
        fieldName = nameEls[0].text
        valuesEls = el.select('a')
        values = list(map(lambda x: x.text, valuesEls))
        res[fieldName] = values
    return res

def getImageURL(vendorCode):
    if len(vendorCode) < 1:
        return ''
    urlStart = 'https://s.winestyle.ru/images_gen/'
    return urlStart + vendorCode[1:] + '/0_0_cat.jpg'

def parseByIndex(ind):
    url = 'https://winestyle.ru/wine/all/?page=' + str(ind)
    print(url)
    context = ssl._create_unverified_context()
    page = urllib.request.urlopen(url, context=context)
    soup = BeautifulSoup(page)
    for form in soup.find_all('form', {'class': 'item-block'}):
        vendorCode = getVendorCode(form)
        if vendorCode is None:
            continue
        if wineExists(vendorCode):
            continue
        title = getTitle(form)
        description = getDescriptionFields(form)
        imageURL = getImageURL(vendorCode)
        document = {}
        document['_id'] = vendorCode
        document['title'] = title
        document['description'] = description
        document['imageURL'] = imageURL
        addWineToDB(document)

def parse(start, end):
    for ind in range(start, end + 1):
        parseByIndex(ind)

#python3 -m pip install
#parse(start=1, end=3285)
parse(start=1, end=3285)
