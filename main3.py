import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
from winesSearcher import Searcher
from pathlib import Path

searcher = Searcher()

mainWindow = tkinter.Tk()

infoContainer = tkinter.PanedWindow


def showInformation(wine):
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

    # меняем картинку
    global cv
    global cv2
    global img

    pathToImg = 'images/' + wine['_id'] + '.jpg'
    pth = Path(pathToImg)

    if pth.is_file():
        img = ImageTk.PhotoImage(file=pathToImg)
        cv.itemconfig(cv2, image=img)



def searchWine():
    global searcher
    global var
    wine = None
    if var.get() == 1:
        regionName = lbRegions.get(tkinter.ACTIVE)
        wine = searcher.searchRandomByRegion(regionName)
    else:
        grapeTypeName = lbGrapeTypes.get(tkinter.ACTIVE)
        wine = searcher.searchRandomByType(grapeTypeName)
    showInformation(wine)
    # tkinter.messagebox.showinfo("Hello Python", "Hello World")


def createListBox(wind, listOfEls):
    lbRegions = tkinter.Listbox(wind)
    lbRegions.pack()
    for item in listOfEls:
        lbRegions.insert(tkinter.END, item)
    return lbRegions


btnSearch = tkinter.Button(mainWindow, text="Search", command=searchWine)
btnSearch.pack()

regions = searcher.getRegions()
lbRegions = createListBox(mainWindow, regions)

grapeTypes = searcher.getTypes()
lbGrapeTypes = createListBox(mainWindow, grapeTypes)

var = tkinter.IntVar()
rbRegions = tkinter.Radiobutton(mainWindow, text='По региону', variable=var, value=1)
rbTypes = tkinter.Radiobutton(mainWindow, text='По сорту', variable=var, value=2)
rbRegions.pack()
rbTypes.pack()
var.set(1)

lblInfo = tkinter.Label(mainWindow)
lblInfo.pack()

# Картинка
img = ImageTk.PhotoImage(file="images/в77677.jpg")
cv = tkinter.Canvas(mainWindow)
cv.pack(side='top', fill='both', expand='yes')
cv2 = cv.create_image(0, 0, image=img, anchor='nw')

# tbRegion = tkinter.Text(mainWindow)

mainWindow.mainloop()
