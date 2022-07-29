import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import cv2
import handTrackingModule as htm
import math
Finger_Counter = __import__('Fingers-Counter')


window = tk.Tk()
window.iconbitmap("icon.ico")
window.title('Number Kids')
window.geometry('1080x720')

background_image = Image.open('bg.jpg').resize((1080, 720))
background_image = ImageTk.PhotoImage(background_image)
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Title_Label = Label(window, text='Kids Learning Numbers', font=('Times New Roman', 30), fg='#f00')
Title_Label.pack(pady=50, anchor=CENTER)




def pressStart():
    if startButton['text'] == 'START':
        startButton['text'] = 'STOP'
        camera()
    else:
        startButton['text'] = 'START'
        camImg = ImageTk.PhotoImage(Image.fromarray(cv2.imread('Fingers.jpg')).resize((650, 482)))
        camLabel['image'] =  camImg


def aboutWin():
    AboutWindow = tk.Toplevel(window)
    AboutWindow.title('About Us')
    AboutWindow.geometry('720x720')


def chooseLang(choice):
    choice = choosed.get()
    return choice


def readImages(FolderPath='FingerImages'):
    ImageNames = os.listdir(FolderPath)
    ImagePaths = [os.path.join(FolderPath, imName) for imName in ImageNames]
    images = [cv2.imread(imPath) for imPath in ImagePaths]
    return images


OnVolumeIcon = ImageTk.PhotoImage(Image.open('volume-icon-on.png').resize((20, 20)))
OffVolumeIcon = ImageTk.PhotoImage(Image.open('volume-icon-off.png').resize((20, 20)))
def changeVolumeIcon():
    if volumeButton['text'] == 'ON ':
        volumeButton['text'] = 'OFF '
        volumeButton['image'] = OffVolumeIcon
    else:
        volumeButton['text'] = 'ON '
        volumeButton['image'] = OnVolumeIcon


startButton = Button(window, text='START', height=1, width=10, activeforeground='red', command=pressStart)
startButton.place(x=100, y=130)

aboutButton = Button(window, text='ABOUT', command=aboutWin, height=1, width=10)
aboutButton.place(x=200, y=130)


languages = ['English', 'Vietnamese']
# datatype of menu text
choosed = StringVar()
choosed.set(languages[0])
# Create Dropdown menu
drop = OptionMenu(window, choosed, *languages, command=chooseLang)
drop["highlightthickness"] = 0
drop.place(x=300, y=130)
drop.config(width=10, height=1)

autoSpeakButton = Button(window, text='AUTO SPEAK', height=1, width=10)
autoSpeakButton.place(x=420, y=130)

volumeButton = Button(window, text='ON ', image=OnVolumeIcon,
                      command=changeVolumeIcon, compound="right")
volumeButton.place(x=520, y=130)

fingerImages = readImages('FingerImages')
finImg = ImageTk.PhotoImage(Image.fromarray(fingerImages[0]).resize((175, 230)))
fingerLabel =  Label(image=finImg)
fingerLabel.place(x=100, y=200)

numberImages = readImages('NumberImages')
numImg = ImageTk.PhotoImage(Image.fromarray(numberImages[0]).resize((175, 230)))
numberLabel =  Label(image= numImg)
numberLabel.place(x=100, y=452)




camImg = ImageTk.PhotoImage(Image.fromarray(cv2.imread('Fingers.jpg')).resize((650, 482)))
camLabel =  Label(image=camImg)
camLabel.place(x=300, y=200)

def updateImage(Label, image):
    pass

def camera():
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector(detectionCon=0.75)
    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=False)
        tipId = [4, 8, 12, 16, 20]
        pipId = [3, 6, 10, 14, 18]
        mcpId = [17, 0, 0, 0, 0]
        num = 0
        
        if(len(lmList) != 0):
            fingers = []
            for i in range(5):
                TipToMcp = math.dist(lmList[tipId[i]][1:], lmList[mcpId[i]][1:])
                PipToMcp = math.dist(lmList[pipId[i]][1:], lmList[mcpId[i]][1:])
                if TipToMcp > PipToMcp:
                    fingers.append(1)
                else:
                    fingers.append(0)
            num = Finger_Counter.getNumber(fingers)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        camImg = ImageTk.PhotoImage(Image.fromarray(cv2.flip(img, 1)))
        camLabel['image'] = camImg
        
        finImg = ImageTk.PhotoImage(Image.fromarray(fingerImages[num]).resize((175, 230)))
        fingerLabel['image'] =  finImg
        
        numImg = ImageTk.PhotoImage(Image.fromarray(numberImages[num]).resize((175, 230)))
        numberLabel['image'] =  numImg
        
        window.update()              
window.mainloop()

