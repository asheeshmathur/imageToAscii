'''
Core Processing Module to convert an RGB image to corresponding Grayscale.
Use a tile based approach to convert it to an ASCII character.
A tile composed of collection of Pixels (rows & cols) to be converted to Ascii character
Instead of converting individual pixel.

Using default 80, as columns for ascii art, this helps in better ascii images.
It's configurable

Uses numpy  for arrays

'''
import numpy as np
from PIL import Image

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

"""
Given PIL Image, returns average value of grayscale value
"""


def getAverageL(image):
    # get image as numpy array
    im = np.array(image)
    # get shape
    w, h = im.shape
    # get average
    return np.average(im.reshape(w * h))


"""
Given Image and its dimensions (rows, cols) returns an m*n list of Images
"""


def covertImageToAscii(fileName, colorCode, cols, scale):
    # declare globals
    global gscale

    # open image and convert to grayscale based on color choice
    # Check & Split base on channels
    tempImage = Image.open(fileName)
    if (("R", "G", "B") != tempImage.getbands()):
        image = tempImage.convert('L')
    else:
        red, green, blue = tempImage.split()
        # Iterate to check for color code
        if (colorCode == "B" or colorCode == "b"):
            image = blue
        elif (colorCode == "R" or colorCode == "r"):
            image = red
        elif (colorCode == "G" or colorCode == "g"):
            image = green

    image = Image.open(fileName).convert('L')
    # Extract & store dimensions
    W, H = image.size[0], image.size[1]

    print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []

    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            gsval = gscale[int((avg * 69) / 255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image (row and columns matrix
    return aimg


# main() function
def main():
    # set output file
    outFile = 'out.txt'

    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.43

    # set cols
    cols = 80

    print('Generating ASCII art...')

    # convert image to ascii txt
    aimg = covertImageToAscii("Dog.jpg", "B", cols, scale)

    # Write this output to a stream
    f = open(outFile, 'w')

    # write to file
    for row in aimg:
        f.write(row + '\n')

    # cleanup
    f.close()
    print("ASCII art written to %s" % outFile)


# call main
if __name__ == '__main__':
    main()
