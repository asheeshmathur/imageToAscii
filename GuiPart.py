import os.path
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.scrolledtext as st
from tkinter import END

import processing as prcs

root = tk.Tk()
root.title("Isha's Cornucopia")
# Set the geometry
root.geometry("900x650")
asciiText = tk.StringVar(value='ASCII Part will coe here')
imageFileName = tk.StringVar(value="Dog.jpg")
asciiFileName = tk.StringVar(value="")


def generate(fileName):
    global scrolledText
    # Check for valid image file name
    # set scale default as 0.43 which suits
    scale = 0.43
    aimg = prcs.covertImageToAscii(fileName.get(),"B", 80, scale)
    # Explode to line -

    for row in aimg:
        scrolledText.insert(END, row+'\n')
        previewText.insert(END, row+'\n')
    # scrolledText.config(text=convertedText)
    # previewText.config(text=convertedText)


# Define Four Frames
# frame
frameOne = ttk.Frame(root, width=800, height=55, borderwidth=5, relief=tk.GROOVE)
frameTwo = ttk.Frame(root, width=800, height=50, borderwidth=5, relief=tk.GROOVE)
frameThree = ttk.Frame(root, width=500, height=180, borderwidth=5, relief=tk.GROOVE)
frameFour = ttk.Frame(root, width=800, height=50, borderwidth=5, relief=tk.GROOVE)
# Declare global variables
scrolledText = st.Text(frameThree, font=('Courier', 14), wrap=NONE)
scrolledText.pack(side=LEFT, padx=25, pady=5)
previewText = Text(frameThree, font=('Courier', 2), width=45, height=21, wrap=NONE)
previewText.pack(side=LEFT, padx=25, pady=5)
# Buttons
generateBtn = Button(frameFour, text="Generate", command=lambda: generate(imageFileName))
saveFileBtn = Button(frameFour, text="Save To" , command=lambda: saveTo())
generateBtn.pack(side=LEFT, pady=5)
saveFileBtn.pack(side=LEFT, pady=5)

# Pack these frames
frameOne.pack(fill=BOTH, expand=True)
frameTwo.pack(fill=BOTH, expand=True)
frameThree.pack(fill=BOTH, expand=True)
frameFour.pack(fill=BOTH, expand=True)


def saveTo():
    global scrolledText, imageFileName
    asciiFileName = filedialog.asksaveasfilename()
    file = open(asciiFileName, 'a+')
    file.write(scrolledText.get("1.0",END))
    file.close()


'''
Image to ascii art display
'''


def asciiArt():
    print("I am in asciiArt")
    global scrolledText, root, previewText
    root.mainloop()
    # Add a Scrollbar(horizontal)
    hScrollBar = Scrollbar(frameThree, orient='horizontal')
    hScrollBar.pack(side=BOTTOM, fill='x')
    scrolledText.config(parent=frameThree, xscrollcommand=hScrollBar)
    previewText.config(parent=frameThree)
    generateBtn.config(command=generateBtn)
    # Add a text widget

    # Attach the scrollbar with the text widget
    hScrollBar.config(command=previewText.xview)


def main():
    global root
    print("About Launch")
    asciiArt()
    root.mainloop()


main()
