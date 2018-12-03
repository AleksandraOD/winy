import shutil

import pymongo
import requests

url = 'mongodb://localhost:27017/wines'
mongoClient = pymongo.MongoClient(url)
winesDB = mongoClient['wines']
winesCol = winesDB['wines']


def mkFileName(wineID):
    return 'images/' + wineID + '.jpg'


def downloadImage(url, fileName):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(fileName, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def downloadImages():
    global winesCol
    # context = ssl._create_unverified_context()
    for wineDoc in winesCol.find():
        if 'imageURL' not in wineDoc:
            continue
        wineID = wineDoc['_id']
        imURL = wineDoc['imageURL']
        imFileName = mkFileName(wineID)
        downloadImage(imURL, imFileName)


downloadImages()
