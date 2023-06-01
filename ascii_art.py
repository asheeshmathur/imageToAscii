'''
GUI for  RGB image to corresponding Grayscale.
Invokes the processing part, core engine for image processing

It's configurable

For finer details of core processing, please refer to processing.py
We would like to execute imge conversion part in a separate thread, without
bothering GUI part.
Since Python does not have a mechanism to return and value from the function being
executed by thread.

So we had to extend core Thread module and incorporate this functionality in
a custom thread with instance variable to hold that value and returns it.
Please CustomThread.py.


References :
http://paulbourke.net/dataformats/asciiart/
https://afsanchezsa.github.io/vc/docs/workshops/w1_3
https://github.com/electronut/pp/blob/master/ascii/ascii.py
https://coderslegacy.com/python/get-return-value-from-thread/

'''
import os.path
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.scrolledtext as st
from tkinter import END

# Threading Support
from threading import Thread
import time

import processing as prcs
import CustomThread as cthread

root = tk.Tk()
root.title("Isha's Cornucopia")
# Set the geometry
root.geometry("900x650")
# Set Resizable false
root.resizable(False, False)

# List of Text Char to drive application

# Default list of characters to be used, use can provide his own 70 here
asciiText = tk.StringVar(value="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
imageFileName = tk.StringVar(value="guitar.jpg")
asciiFileName = tk.StringVar(value="ascii_Image.txt")
radioVar = tk.StringVar(value="tb")
channelColor = tk.StringVar(value="B")

# Int variable to select Font Size,Char Width & Height
charHeight = tk.IntVar(value=14)
charWidth = tk.IntVar(value=6)
fntSize = tk.IntVar(value=11)


def showFileDialog():
    global imageFileName, entry
    entry.grid_forget()
    fileName = filedialog.askopenfilename()
    imageFileName.set(fileName)


def generate():
    global scrolledText, imageFileName
    # Check for valid image file name
    # set scale default as 0.43 which suits
    scale = 0.43
    # Get Selected Font Size
    fontTwo = fntSize.get()

    # Channel Color

    # Get List of Characters to replace
    charList = asciiText.get()

    # Extract height & width of a Tile
    tileHt = charHeight.get()
    tileWidth = charWidth.get()
    output = []

    # Receives list of characters and channel color from string var
    processingThread = \
        cthread.CustomThread(target=prcs.covertImageToAscii,
               args=(imageFileName.get(), channelColor.get(), 80, scale, charList, tileWidth,
                     tileHt))
    start = time.time()
    # Start Thread
    processingThread.start()

    # Joins back GUI thread
    output=processingThread.join()
    print('Two thread total time: ', time.time() - start)

    scrolledText.config(font=('Courier', fontTwo))
    scrolledText.delete("1.0", "end")
    previewText.delete("1.0", "end")

    # Explode to line - introduce line break
    for row in output:
        scrolledText.insert(END, row + '\n')
        previewText.insert(END, row + '\n')


# Define Four Frames
frameOne = ttk.Frame(root, width=800, height=20, borderwidth=5, relief=tk.GROOVE)
frameTwo = ttk.Frame(root, width=800, height=50, borderwidth=5, relief=tk.GROOVE)
frameThree = ttk.Frame(root, width=650, height=180, borderwidth=5, relief=tk.GROOVE)
frameFour = ttk.Frame(root, width=800, height=50, borderwidth=5, relief=tk.GROOVE)

# Configure four Rows within frameTwo
frameTwo.rowconfigure(0, weight=1)
frameTwo.rowconfigure(1, weight=1)
frameTwo.rowconfigure(2, weight=1)



# Radio Buttons to select entry for image path or file dialog
selectImage = Label(frameOne, text="Select Valid Image (RBG)").grid(row=0, column=0, pady=14)
entry = tk.Entry(frameOne, textvariable=imageFileName)

# Two Radio Buttons to select source of image
entryRadio = Radiobutton(
    frameOne,
    value="tb",
    text="Image File Name",
    variable=radioVar,
    command=lambda: entry.grid(row=0, column=4))
entryRadio.grid(row=0, column=1, pady=14)

showFileDialogRadio = Radiobutton(
    frameOne,
    value="fd",
    text="Select via File Dialog",
    variable=radioVar,
    command=lambda: showFileDialog()).grid(row=0, column=2, pady=14)

# Radio Buttons to Pick Color Channel
channelColLabel = ttk.Label(frameTwo, text="Channel Color To Use  ").grid(row=1,column=1,padx=10,sticky=E)
redRadio = Radiobutton(
    frameTwo,
    value="R",
    text="Red",
    variable=channelColor).grid(row=1, column=2
                                ,sticky=W)

greenRadio = Radiobutton(
    frameTwo,
    value="G",
    text="Green",
    variable=channelColor).grid(row=1, column=3,sticky=W)

blueRadio = Radiobutton(
    frameTwo,
    value="B",
    text="Blue",
    variable=channelColor).grid(row=1, column=4, sticky=W)

heightLabel = ttk.Label(frameOne, text="Height")
heightLabel.grid(row=1, column=0, sticky=W)
heightEntry = ttk.Entry(frameOne, textvariable=charHeight, width=2).grid(row=1, column=1, sticky=W)

widthLabel = ttk.Label(frameOne, text="Width")
widthLabel.grid(row=1, column=2, sticky=EW)
widthEntry = ttk.Entry(frameOne, width=2, textvariable=charWidth)
widthEntry.grid(row=1, column=3, sticky=W)

fontSize = ttk.Label(frameOne, text="Font Size")
fontSize.grid(row=1, column=4, sticky=W)
fontEntry = ttk.Entry(frameOne, width=2, textvariable=fntSize).grid(row=1, column=5,sticky=W)

# Widgets to accept set of characters
listOfCharacters = ttk.Label(frameTwo, text="Input List of Characters to Used for Conversion - Preferably 70").grid(
    row=0, column=0, sticky=W)
charListEntry = ttk.Entry(frameTwo, width=50, textvariable=asciiText).grid(row=1, column=0, sticky=W)

hScrollBar = Scrollbar(frameThree, orient='horizontal')
scrolledText = st.ScrolledText(frameThree, wrap=NONE, xscrollcommand=hScrollBar.set)

hScrollBar.config(command=scrolledText.xview)

hScrollBar.grid(row=1, column=0, sticky=EW, padx=15)
scrolledText.grid(row=0, column=0, padx=10)
# Attach the scrollbar with the text widget
previewText = st.ScrolledText(frameThree, font=('Courier', 2), width=45, height=30, wrap=NONE)
previewText.grid(row=0, column=1)
# Plan for Labels and entry fields

# Buttons
generateBtn = Button(frameFour, text="Generate", command=lambda: generate())
saveFileBtn = Button(frameFour, text="Save To", command=lambda: saveTo())
generateBtn.place(x=325, y=5)
saveFileBtn.place(x= 420, y=5)
# Pack these frames
frameOne.pack(fill=BOTH, expand=True)
frameTwo.pack(fill=BOTH, expand=True)
frameThree.pack(fill=BOTH, expand=True)
frameFour.pack(fill=BOTH, expand=True)


def saveTo():
    global scrolledText, imageFileName
    asciiFileName = filedialog.asksaveasfilename()
    file = open(asciiFileName, 'a+')
    file.write(scrolledText.get("1.0", END))
    file.close()


'''
Image to ascii art display
'''


def asciiArt():
    # Start Main Loop
    root.mainloop()


def main():
    global root
    asciiArt()
    root.mainloop()


main()
