# Demos included in the mamba shell

demo1 = """
Hello and welcome to the Mamba demo !

This demo will show you some of the functionalities of Mamba.
To enjoy it, make sure im1 and im2 displays are visible.
The next lines will ensure this :

>>>im1.show()
>>>im2.show()
>>>im1.unfreeze()
>>>im2.unfreeze()

Ok, now first we will load an image into im1:
>>>im1.load("%s")

You can always get information on images, such as their size or depth:
>>>im1.getSize()
>>>im1.getDepth()

Mamba comes with a preintegrated color palette that you can apply to your
display by pressing the letter P in the window.

Performing any operation is done by calling the appropriate function.
For example, to perform an erosion of im1:
>>>erode(im1, im2)

Of course, the erode function has many parametrable arguments such as:
 - size
 - structuring element
 - ... 
Here is another example:
>>>erode(im1, im2, 10, se=DIAMOND)

To get a complete view of the possibilities of the function
(and of other ones) refer to the python API reference document.
You can also ask help directly: help(erode)

One important point is that you can always use the same 
image as input and output in any operation 
(with the exception of multidepth operations) such as:
>>>erode(im1, im1)

Mamba offers a display that can be disabled and enabled easily.
For example to hide a display:
>>>im1.hide()

If you want it back:
>>>im1.show()

The display is quite convenient when trying ideas, debugging or showing results.
However it has its drawbacks such as its impact on speed.
Here is a small example of the effect of display on speed:

At first with display ON
>>>erode(im1, im2, 100)

Now with the display OFF
>>>im2.hide()
>>>erode(im1, im2, 100)
>>>im2.show()

Obviously the second time was faster.
So don't hesitate to disable the display when you perform long computations
(this can be done by simply reducing the window).
You can always re-enable it after.

The display offers dynamic control such as zoom, palette enabling, etc...
Try zooming by using your mouse wheel.

The display can be enlarged or reduced to fit your screen
and you can always move the image inside it 
by moving the mouse while holding left button pressed (or using the scrollbars).

To obtain the complete possibilities of the display, refer to the user manual.

This concludes our short tour of Mamba. We hope it has helped you.
For more information: www.mamba-image.org
"""
