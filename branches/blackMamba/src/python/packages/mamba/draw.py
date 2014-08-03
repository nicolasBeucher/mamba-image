"""
Drawing operators.

This module defines functions to draw inside Mamba images. Drawing functions
include lines, squares, ... The module also provides functions to extract
pixel information.
"""

import mamba

### DRAW FUNCTIONS ###

def drawLine(imOut, line, value):
    """
    Draws a line in 'imOut' using the tuple 'line' containing 4 values (starting
    and ending points (x1,y1,x2,y2)) using 'value' to set the pixels.
    
    This function uses the Bresenham algorithm.
    """
    x1,y1,x2,y2 = line
    steep = (abs(y2-y1) > abs(x2-x1))
    if steep:
        prov = x1
        x1 = y1
        y1 = prov
        prov = x2
        x2 = y2
        y2 = prov
    if x1>x2:
        prov = x1
        x1 = x2
        x2 = prov
        prov = y1
        y1 = y2
        y2 = prov
    deltax = x2-x1
    deltay = abs(y2-y1)
    error = deltax//2
    y = y1
    if y1<y2:
        ystep = 1 
    else:
        ystep = -1
    for x in range(x1,x2+1):
        if steep:
            imOut.fastSetPixel(value, (y,x))
        else:
            imOut.fastSetPixel(value, (x,y))
        error -= deltay
        if error<0:
            y += ystep
            error += deltax
    # Updates the image.
    imOut.update()
    
def drawBox(imOut, square, value):
    """
    Draws a box (empty square) in 'imOut' using the tuple 'square' containing 4
    values (upper left and down right corners (x1,y1,x2,y2)) using 'value' to
    set the pixels.
    """
    x1,y1,x2,y2 = square
    if x1>x2:
        prov = x1
        x1 = x2
        x2 = prov
    if y1>y2:
        prov = y1
        y1 = y2
        y2 = prov
    for x in range(x1,x2+1):
        imOut.fastSetPixel(value, (x,y1))
        imOut.fastSetPixel(value, (x,y2))
    for y in range(y1,y2+1):
        imOut.fastSetPixel(value, (x1,y))
        imOut.fastSetPixel(value, (x2,y))
    imOut.update()

def drawSquare(imOut, square, value):
    """
    Draws a square in 'imOut' using the tuple 'square' containing 4 values (upper
    left and down right corners (x1,y1,x2,y2)) using 'value' to set the pixels.
    """
    x1,y1,x2,y2 = square
    if x1>x2:
        prov = x1
        x1 = x2
        x2 = prov
    if y1>y2:
        prov = y1
        y1 = y2
        y2 = prov
    for x in range(x1,x2+1): 
        for y in range(y1,y2+1):
            imOut.fastSetPixel(value, (x,y))
    imOut.update()
    
def drawCircle(imOut, circle, value):
    """
    Draws a circle in 'imOut' using the tuple 'circle' containing 3 values
    (center and radius (x,y,r)) using 'value' to set the pixels.
    """
    x0 = circle[0]
    y0 = circle[1]
    radius = circle[2]
    f = 1-radius
    ddF_x = 1
    ddF_y = -2*radius
    x = 0
    y = radius
    imOut.fastSetPixel(value, (x0, y0 + radius))
    imOut.fastSetPixel(value, (x0, y0 - radius))
    imOut.fastSetPixel(value, (x0 + radius, y0))
    imOut.fastSetPixel(value, (x0 - radius, y0))
    while x<y:
        if f>=0: 
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x
        imOut.fastSetPixel(value, (x0 + x, y0 + y))
        imOut.fastSetPixel(value, (x0 - x, y0 + y))
        imOut.fastSetPixel(value, (x0 + x, y0 - y))
        imOut.fastSetPixel(value, (x0 - x, y0 - y))
        imOut.fastSetPixel(value, (x0 + y, y0 + x))
        imOut.fastSetPixel(value, (x0 - y, y0 + x))
        imOut.fastSetPixel(value, (x0 + y, y0 - x))
        imOut.fastSetPixel(value, (x0 - y, y0 - x))
    imOut.update()
    
def drawFillCircle(imOut, circle, value):
    """
    Draws a filled circle in 'imOut' using the tuple 'circle' containing 3
    values (center and radius (x,y,r)) using 'value' to set the pixels.
    """
    x0 = circle[0]
    y0 = circle[1]
    radius = circle[2]
    f = 1-radius
    ddF_x = 1
    ddF_y = -2*radius
    x = 0
    y = radius
    for i in range(-radius,radius+1):
        imOut.fastSetPixel(value, (x0+i, y0))
    while x<y:
        if f>=0: 
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x        
        for i in range(-x,x+1):
            imOut.fastSetPixel(value, (x0+i, y0 + y))
        for i in range(-x,x+1):
            imOut.fastSetPixel(value, (x0+i, y0 - y))
        for i in range(-y,y+1):
            imOut.fastSetPixel(value, (x0+i, y0 + x))
        for i in range(-y,y+1):
            imOut.fastSetPixel(value, (x0+i, y0 - x))    
    imOut.update()

### EXTRACT PIXEL VALUES FUNCTIONS ###

def getIntensityAlongLine(imOut, line):
    """
    Returns in a list the intensity profile along a line in 'imOut' using the
    tuple 'line' containing 4 values (starting and ending points (x1,y1,x2,y2)).
    
    This function uses the Bresenham algorithm.
    """
    profile = []
    x1,y1,x2,y2 = line
    steep = (abs(y2-y1) > abs(x2-x1))
    if steep:
        prov = x1
        x1 = y1
        y1 = prov
        prov = x2
        x2 = y2
        y2 = prov
    if x1>x2:
        prov = x1
        x1 = x2
        x2 = prov
        prov = y1
        y1 = y2
        y2 = prov
    deltax = x2-x1
    deltay = abs(y2-y1)
    error = deltax//2
    y = y1
    if y1<y2:
        ystep = 1 
    else:
        ystep = -1
    for x in range(x1,x2+1):
        if steep:
            profile.append(imOut.getPixel((y,x)))
        else:
            profile.append(imOut.getPixel((x,y)))
        error -= deltay
        if error<0:
            y += ystep
            error += deltax
    # The profile must be returned in the expected order
    x1,y1,x2,y2 = line
    if x==y1 or x==x1:
        profile.reverse()
    return profile
