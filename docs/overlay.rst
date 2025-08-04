Overlay
=======

Overview
--------

The overlay submodule for PyRend is the largest and most powerful component of the PyRend as it allows control over an invisible overlay on the screen with each creation of shape, text, image or video objects. 

Features
--------

- Easily draw images, shapes or text to the screen
- Render videos to the overlay
- Rotate or move items 
- Manage opacity and paint order
- Create position or rotation points
- Assign children and parents to create a hierachy
- Detect collisions and mouse clicks

Introduction
============

This submodule documentation assumes you already know how to create and understand a basic PyRend loop, presumably with a keybind to quit:

.. code-block:: python

    import pyrend

    def my_update_loop():
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()

    pyrend.start(my_update_loop)

Items
-----

To draw elements onto the overlay in PyRend, you first need to create items. These items are Python objects that store properties defining how and where something appears on the screen. PyRend provides six types of overlay items: ShapeItem, TextItem, ImageItem, VideoItem, PointItem, and a base class BaseItem, which serves as the foundation for all others.
This section of the documentation will guide you through how to create and use each item type, as well as explain shared methods and other overlay-related functionality.

Creating items
==============

General
-------

PyRend overlay objects are created by assigning them to variables, which allows you to modify them later. For example, the code below creates a `ShapeItem` and assigns it to `myShape` (Ignoring parameters for now)

.. code-block:: python

  myShape = pyrend.overlay.shape(...)

With that said, we can begin to create items using the following functions.

Shapes
------

Shapes in PyRend can be rectangular or elliptical. You can create them with `pyrend.overlay.shape` with default parameters like so:

.. code-block:: python

    myShape = pyrend.overlay.shape(
        iscircle=False,
        pos=(0, 0),
        size=(100, 100),
        color=(255, 255, 255),
        opacity = 1.0,
        radius = 0,
        z_index = 0
    )

| **iscircle** (bool): Whether the shape is elliptical (`True`) or rectangular (`False`).  
| **pos** (tuple): The (`x, y`) position of the top-left corner of the shape, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): The (`width, height`) of the shape, in pixels.  
| **color** (tuple): The RGB color of the shape, e.g. (`255, 0, 0`) for red. See: `RGB vs hex codes <https://pyrend.readthedocs.io/en/latest/index.html#hex-vs-rgb-codes>`_ 
| **opacity** (float): Opacity of the shape from 0.0 (fully transparent) to 1.0 (`fully opaque`). 
| **radius** (int): Corner radius (in pixels) for rectangular shapes. Ignored if iscircle=True. 
| **z_index** (int): Determines draw order. Shapes with a higher z_index appear above those with lower values.  

Text
----

.. code-block:: python

    myText = pyrend.overlay.write(
        text,
        pos = (0, 0),
        size = (48),
        color = (255, 255, 255),
        font = "Arial",
        z_index = 0
    )

| **text** (str): The text to be written onto the overlay
| **pos** (tuple): The (`x, y`) position of the top-left corner of the shape, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): The (`width, height`) of the shape, in pixels.  
| **color** (tuple): The RGB color of the shape, e.g. (`255, 0, 0`) for red. See: `RGB vs hex codes <https://pyrend.readthedocs.io/en/latest/index.html#hex-vs-rgb-codes>`_ 
| **font** (str): The font to write in. See: Defining custom fonts
| **z_index** (int): Determines draw order. Shapes with a higher z_index appear above those with lower values.  
