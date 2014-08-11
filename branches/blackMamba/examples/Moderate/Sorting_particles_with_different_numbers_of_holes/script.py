# exampleM15.py
# IN gruyere.png
# OUT sorted_particles.png

## TITLE #######################################################################
# Sorting particles with different numbers of holes

## DESCRIPTION #################################################################
# This example uses different morphological operators (geodesic reconstruction,
# SKIZ) to separate particles with no hole (simply connected particles) from
# particles with one hole then with more than one hole. More sophisticated
# procedures exist to sort any particle according to its number of holes. But
# these procedures are out of the scope of this example. 

## SCRIPT ######################################################################
# Importing the mamba modules
from mamba import *
from mambaDisplay.extra import *
    
# Reading the initial image 
imIn = imageMb('gruyere.png')
imIn.convert(1)
imWrk1 = imageMb(imIn)
imWrk2 = imageMb(imIn)
imWrk3 = imageMb(imIn)

# Particles without holes are sorted. Holes are extracted and they are used
# (after an elementary dilation) as markers for building particles which 
# contain at least one hole.
closeHoles(imIn, imWrk1)
diff(imWrk1, imIn, imWrk1)
dilate(imWrk1, imWrk1)
build(imIn, imWrk1)
# Now, imWrk1 contains only particles with hole(s)

# Separating now particles with a single hole from particles with more
# than one hole.
negate(imWrk1, imWrk2)
fastSKIZ(imWrk2, imWrk2)
negate(imWrk2, imWrk2)
# Particles with several holes are marked by multiple points in the SKIZ.
multiplePoints(imWrk2, imWrk2)
build(imWrk1, imWrk2)

# The results can be seen by the superposer.
diff(imIn, imWrk1, imWrk3)
logic(imWrk2, imWrk3, imWrk3, "sup")
superpose(imWrk1, imWrk3)

