"""
Drawing 3D operators.

This module defines functions to draw inside Mamba 3D images. Drawing functions
include lines, cubes, ... The module also provides functions to extract
pixel information.
"""

# Contributors : Nicolas BEUCHER

import mamba3D as m3D
import mamba

### DRAW FUNCTIONS ###

def drawLine3D(imOut, line, value):
    """
    Draws a line in 'imOut' using the tuple 'line' containing 4 values (starting
    and ending points (x1,y1,z1,x2,y2,z2)) using 'value' to set the pixels.
    
    This function uses the Bresenham algorithm. It works with image3DMb
    instances.
    """
    x1,y1,z1,x2,y2,z2 = line
    pixel = [0,0,0]

    pixel[0] = x1
    pixel[1] = y1
    pixel[2] = z1
    dx = x2-x1
    dy = y2-y1
    dz = z2-z1
    x_inc = (dx<0) and -1 or 1
    l = abs(dx)
    y_inc = (dy<0) and -1 or 1
    m = abs(dy)
    z_inc = (dz<0) and -1 or 1
    n = abs(dz)
    dx2 = l<<1
    dy2 = m<<1
    dz2 = n<<1

    if l>=m and l>=n :
        err_1 = dy2-l
        err_2 = dz2-l
        for i in range(l):
            imOut[pixel[2]].fastSetPixel(value, pixel[0:2])
            if err_1>0:
                pixel[1] += y_inc
                err_1 -= dx2
            if err_2>0:
                imOut[pixel[2]].update()
                pixel[2] += z_inc
                err_2 -= dx2
            err_1 += dy2
            err_2 += dz2
            pixel[0] += x_inc

    elif m>=l and m>=n:
        err_1 = dx2-m;
        err_2 = dz2-m;
        for i in range(m):
            imOut[pixel[2]].fastSetPixel(value, pixel[0:2])
            if err_1>0:
                pixel[0] += x_inc
                err_1 -= dy2
            if err_2>0:
                imOut[pixel[2]].update()
                pixel[2] += z_inc
                err_2 -= dy2
            err_1 += dx2
            err_2 += dz2
            pixel[1] += y_inc

    else:
        err_1 = dy2-n;
        err_2 = dx2-n;
        for i in range(n):
            imOut[pixel[2]].fastSetPixel(value, pixel[0:2])
            if err_1>0:
                pixel[1] += y_inc
                err_1 -= dz2
            if err_2>0:
                pixel[0] += x_inc
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            imOut[pixel[2]].update()
            pixel[2] += z_inc
            
    imOut[pixel[2]].fastSetPixel(value, pixel[0:2])
    imOut[pixel[2]].update()

def drawCube(imOut, cube, value):
    """
    Draws a cube in 'imOut' using the tuple 'cube' containing 4 values 
    (nearest upper left to farest down right corners (x1,y1,z1,x2,y2,z2))
    using 'value' to set the pixels.
    """
    x1,y1,z1,x2,y2,z2 = cube
    if x1>x2:
        prov = x1
        x1 = x2
        x2 = prov
    if y1>y2:
        prov = y1
        y1 = y2
        y2 = prov
    if z1>z2:
        prov = z1
        z1 = z2
        z2 = prov
    for z in range(z1,z2+1):
        for y in range(y1,y2+1):
            for x in range(x1,x2+1): 
                imOut[z].fastSetPixel(value, (x,y))
        imOut[z].update()

### EXTRACT PIXEL VALUES FUNCTIONS ###

def getIntensityAlongLine3D(imOut, line):
    """
    Returns in a list the intensity profile along a line in 'imOut' using the
    tuple 'line' containing 6 values (starting and ending points (x1,y1,z1,x2,y2,z2)).
    
    This function uses the Bresenham algorithm. It works with image3DMb
    instances.
    """
    profile = []
    x1,y1,z1,x2,y2,z2 = line
    pixel = [0,0,0]

    pixel[0] = x1
    pixel[1] = y1
    pixel[2] = z1
    dx = x2-x1
    dy = y2-y1
    dz = z2-z1
    x_inc = (dx<0) and -1 or 1
    l = abs(dx)
    y_inc = (dy<0) and -1 or 1
    m = abs(dy)
    z_inc = (dz<0) and -1 or 1
    n = abs(dz)
    dx2 = l<<1
    dy2 = m<<1
    dz2 = n<<1

    if l>=m and l>=n :
        err_1 = dy2-l
        err_2 = dz2-l
        for i in range(l):
            profile.append(imOut[pixel[2]].getPixel(pixel[0:2]))
            if err_1>0:
                pixel[1] += y_inc
                err_1 -= dx2
            if err_2>0:
                pixel[2] += z_inc
                err_2 -= dx2
            err_1 += dy2
            err_2 += dz2
            pixel[0] += x_inc

    elif m>=l and m>=n:
        err_1 = dx2-m;
        err_2 = dz2-m;
        for i in range(m):
            profile.append(imOut[pixel[2]].getPixel(pixel[0:2]))
            if err_1>0:
                pixel[0] += x_inc
                err_1 -= dy2
            if err_2>0:
                imOut[pixel[2]].update()
                pixel[2] += z_inc
                err_2 -= dy2
            err_1 += dx2
            err_2 += dz2
            pixel[1] += y_inc

    else:
        err_1 = dy2-n;
        err_2 = dx2-n;
        for i in range(n):
            profile.append(imOut[pixel[2]].getPixel(pixel[0:2]))
            if err_1>0:
                pixel[1] += y_inc
                err_1 -= dz2
            if err_2>0:
                pixel[0] += x_inc
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            imOut[pixel[2]].update()
            pixel[2] += z_inc
    
    profile.append(imOut[pixel[2]].getPixel(pixel[0:2]))
    return profile
