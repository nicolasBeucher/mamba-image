"""
This module provides palette definition and functions to build specific 
palettes.
"""

###############################################################################
#  Color palettes
#  Three color palettes are defined: rainbow, inverted_rainbow and patchwork

rainbow = (0,0,0)
for _i in range(51): #red to yellow
    rainbow = rainbow + (255,_i*5,0)
for _i in range(51): #yellow to green
    rainbow = rainbow + (255-_i*5,255,0)
for _i in range(51): #green to indigo
    rainbow = rainbow + (0,255,_i*5)
for _i in range(51): #indigo to blue
    rainbow = rainbow + (0,255-_i*5,255)
for _i in range(51): #blue to purple
    rainbow = rainbow + (_i*5,0,255)
    
inverted_rainbow = (0,0,0)
for _i in range(51): #purple to blue
    inverted_rainbow = inverted_rainbow + (255-_i*5,0,255)
for _i in range(51): #blue to indigo
    inverted_rainbow = inverted_rainbow + (0,_i*5,255)
for _i in range(51): #indigo to green
    inverted_rainbow = inverted_rainbow + (0,255,255-_i*5)
for _i in range(51): #green to yellow
    inverted_rainbow = inverted_rainbow + (_i*5,255,0)
for _i in range(51): #yellow to red
    inverted_rainbow = inverted_rainbow + (255,255-_i*5,0)

patchwork = ()
_blue_val = (0, 146, 36, 219, 109, 182, 73, 255)
_green_val = (0, 85, 170, 255)
_red_val = (0, 73, 182, 109, 219, 36, 146, 255)
for _i in range (8):
    for _j in range(4):
        for _k in range(8):
            patchwork = patchwork + (_red_val[_k], _green_val[_j], _blue_val[_i])

################################################################################
# Palette functions
################################################################################

def tagOneColorPalette(value, color):
    """
    Creates a palette that tags a specific 'value' inside an image with a given 
    'color', a tuple (red, green, blue), while the rest of the image stays in 
    greyscale.
    """
    pal = ()
    if value<0 or value>255:
        raise ValueError("value must be inside range [0,255] : %d" % (value))
    for i in range(value):
        pal = pal + (i,i,i)
    pal = pal + tuple(color)
    for i in range(value+1,256):
        pal = pal + (i,i,i)
    return pal
    
def changeColorPalette(palette, value, color):
    """
    Modifies the given 'palette' so that the given 'value' is tagged using
    the new color 'color',  a tuple (red, green, blue). The rest of the
    palette is unmodified. Returns the created palette.
    """
    pal = list(palette)
    for i in range(3):
        pal[value*3+i] = color[i]
    return tuple(pal)
