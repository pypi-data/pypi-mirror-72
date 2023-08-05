# Description

This is a framework based on pygame that allows an easier process for making games. This is so much more than a tool kit.
Tested in pygame2 not in pygame1.

# Geometry objects

Geometry components added:
* point
* segment
* vector
* line
* halfline

But also:
* circle
* rectangle
* square
* polygon
* triangle
* bezier curve
* trajectory

# Physics/Maths objects

* force
* motion
* body
* polynomial
* perlin noise


# Game objects

* entity
* anatomy
* widget
* menu
* manager

# More technical physics objects

* material
* material form
* material circle
* material formcollider

# Installation

```bash
pip install pygame-context
```

# Draw a 
```python
import pygame_geometry as pgg
from pgg.abstract import *
from pgg.context import Context
from pgg import colors as cl

context = Context("title") # create a context similar to a pygame surface

p1 = Point(2,2)
p2 = Point(3,2, color=cl.BLUE)
r = Rectangle(50, 50, 100, 200)

# main game loop
while context.open:
    # clear the window
    context.clear()
    # check quit event (empty pygame event buffer by doing so)
    context.check() 

    # update objects
    p1.rotate()
    r.move(1, 0)

    # show objects
    p1.show(context)
    p2.show(context)
    r.show(context)

    # flip the screen
    context.flip()
```


```python

```

# Description


# Controls

* Space: Switch to next mode.
* Enter: Go back to the center.
* Up/Down/Right/Left Arrow: Move arround.
* Right/Left Shift: Zoom in or out.
* Quit/Escape: Quit.
* Z: Cancel last sample.
* R: Remove all samples.
* S: Save the fourier-coefficients.

# Enjoy!