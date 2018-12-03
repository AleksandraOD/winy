import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
from winesSearcher import Searcher
from pathlib import Path

searcher = Searcher()

mainWindow = tkinter.Tk()
mainWindow.title("Wine")

infoContainer = tkinter.PanedWindow


def changeInfo(wine):
    txt = 'Артикул: ' + wine['_id'] + '\n'
    txt += 'Название: ' + wine['title'] + '\n'
    if 'description' in wine:
        for attrName, attrValue in wine['description'].items():
            txt += attrName + ' '
            for i in range(len(attrValue)):
                txt += attrValue[i]
                if i != len(attrValue) - 1:
                    txt += ', '
            txt += '\n'
    global lblInfo
    lblInfo['text'] = txt

def changeImage(wine):
    # меняем картинку
    global cv
    global cv2
    global img

    pathToImg = 'images/' + wine['_id'] + '.jpg'
    pth = Path(pathToImg)

    if not pth.is_file():
        pathToImg = 'empty.jpg'
    img = ImageTk.PhotoImage(file=pathToImg)
    cv.itemconfig(cv2, image=img)


def showInformation(wine):
    changeInfo(wine)
    changeImage(wine)



def searchWineByRegion():
    global searcher
    regionName = lbRegions.get(tkinter.ACTIVE)
    wine = searcher.searchRandomByRegion(regionName)
    showInformation(wine)


def searchWineByType():
    global searcher
    grapeTypeName = lbGrapeTypes.get(tkinter.ACTIVE)
    wine = searcher.searchRandomByType(grapeTypeName)
    showInformation(wine)


def createListBox(wind, listOfEls):
    lbRegions = tkinter.Listbox(wind)
    for item in listOfEls:
        lbRegions.insert(tkinter.END, item)
    return lbRegions

regions = searcher.getRegions()
lbRegions = createListBox(mainWindow, regions)
lbRegions.grid(row=0, column=0)

grapeTypes = searcher.getTypes()
lbGrapeTypes = createListBox(mainWindow, grapeTypes)
lbGrapeTypes.grid(row=0, column=1)


btnSearchByRegion = tkinter.Button(mainWindow, text="Найти вино по региону", command=searchWineByRegion)
btnSearchByRegion.grid(row=1, column=0)
btnSearchByType = tkinter.Button(mainWindow, text="Найти вино по сорту", command=searchWineByType)
btnSearchByType.grid(row=1, column=1)



# Картинка
img = ImageTk.PhotoImage(file="empty.jpg")
cv = tkinter.Canvas(mainWindow, width=70, height=300)
cv.grid(row=2, column=0)
cv2 = cv.create_image(0, 0, image=img, anchor='nw')

# Информация о выбранном вине
lblInfo = tkinter.Label(mainWindow)
lblInfo.grid(row=2, column=1)


# tbRegion = tkinter.Text(mainWindow)

mainWindow.mainloop()
