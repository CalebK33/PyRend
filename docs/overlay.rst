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

PyRend overlay objects are created by assigning them to variables, which allows you to modify them later. For example, the code below creates a `ShapeItem` and assigns it to `myShape` (Ignoring parameters for now).

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
        opacity=1.0,
        radius=0,
        z_index=0
    )

| **iscircle** (bool): Whether the shape is elliptical (`True`) or rectangular (`False`).  
| **pos** (tuple): The (`x, y`) position of the top-left corner of the shape, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): The (`width, height`) of the shape, in pixels.  
| **color** (tuple): The RGB color of the shape, e.g. (`255, 0, 0`) for red. See: `RGB vs hex codes <https://pyrend.readthedocs.io/en/latest/index.html#hex-vs-rgb-codes>`_ 
| **opacity** (float): Opacity of the shape from 0.0 (`fully transparent`) to 1.0 (`fully opaque`). 
| **radius** (int): Corner radius (in pixels) for rectangular shapes. Ignored if iscircle=True. 
| **z_index** (int): Determines draw order. Items with a higher z_index appear above those with lower values.  

Text
----

.. code-block:: python

    myText = pyrend.overlay.write(
        text,
        pos=(0, 0),
        size=(48),
        color=(255, 255, 255),
        font="Arial",
        z_index=0
    )

| **text** (str): The text to be written onto the overlay
| **pos** (tuple): The (`x, y`) position of the top-left corner of the text, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): The (`width, height`) of the text, in pixels.  
| **color** (tuple): The RGB color of the text, e.g. (`255, 0, 0`) for red. See: `RGB vs hex codes <https://pyrend.readthedocs.io/en/latest/index.html#hex-vs-rgb-codes>`_ 
| **font** (str): The font to write in. See: Custom Fonts (below)
| **z_index** (int): Determines draw order. Items with a higher z_index appear above those with lower values.  

Custom Fonts
~~~~~~~~~~~~

PyRend allows the addition of custom fonts via TrueType Font files (.ttf). You can load them with the function:

.. code-block:: python

    myFont = pyrend.overlay.load_font(path)

**path** (str): The absoloute or relative path to a true type font file.

**Example**

Creating and using a custom font:

.. code-block:: python

    import pyrend

    myFont = pyrend.overlay.load_font("assets/font.ttf")
    myText = pyrend.overlay.write("This text uses a custom font", font=myFont)

    def update():
        pass

    pyrend.start(update)

Images
-----

.. code-block:: python

    myImage = pyrend.overlay.image(
        path,
        pos=(0, 0),
        size=(100, 100),
        opacity=1.0,
        keep_aspect_ratio=True,
        z_index=0
    )

| **path** (str): Path to the image. Read below for more info.
| **pos** (tuple): The (`x, y`) position of the top-left corner of the image, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): The (`width, height`) of the image, in pixels.  
| **opacity** (float): Opacity of the shape from 0.0 (`fully transparent`) to 1.0 (`fully opaque`). 
| **keep_aspect_ratio** (bool): If true, will automatically resize to remain aspect ratio. Read below for more info.
| **z_index** (int): Determines draw order. Items with a higher z_index appear above those with lower values.  

PyRend images can be in the format of JPEG, PNG, WEBP, GIF (Animation not supported) or SVG. More images types may work but aren't fully supported The **path** parameter can be either a relative or absoloute path, and must include the file extension. 
The **keep_aspect_ratio** parameter determines whether to automatically resize the image to remain the file's aspect ratio. It will take the size tuple and modify it to stay the same aspect ratio, preventing the image from coming out squashed or stretched. 

Points
------

PyRend uses points as invisible items that can store just a location and rotation. They are not rendered onto the screen, making them useful for storing a position, adding multiple joints or hitboxes to existing items, and are nessasairy for creating specific roation points. (See custom rotation points)

.. code-block:: python

    myPoint = pyrend.overlay.point(base_pos)

**base_pos** (tuple): The  (`x, y`) position to be stored with the point, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 

Videos
------

Videos are one of the more complex features of PyRend, although they aren't fully supported. When a video is created, it will immediately play (presuming the loop has been started). When the video ends, by default it will loop iteself, but also call a function that you can specify in the parameters. Therefore you could set a function to stop the video when it finishs. Videos also have a few unique methods. 

.. warning::

    Videos are not fully supported in PyRend. Videos can lag significantly and cause immense strain on CPU. 

    It is also not currently possible to sync audio to video. 

Videos can be either pre-loaded or played immediately. Pre-loading a video will be less intense on the CPU, so you should use it when you don't need to play a video immediately. You can pre-load a video like this:

.. code-block:: python

    videoPreload = pyrend.overlay.load_video(path)

**path** (str): Absoloute or relative path to a .mp4, .mov or .webm video file to be loaded under that variable.

That video will be loaded and can be later used to create a video item. You can create one like this:

.. code-block:: python

    myVideo = pyrend.overlay.video(
        video_data_or_path
        base_pos=(0, 0)
        size=None
        opacity=1.0
        on_end=None
        on_end_args=None
        z_index=0
        keep_aspect_ratio=True
        smooth=False
    )

| **video_data_or_path** (str/data): Can be either a string path to a video or a pre-loaded video.
| **base_pos** (tuple): The  (`x, y`) position of the top-left corecer of the video, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): | **size** (tuple): The (`width, height`) of the video, in pixels. If left blank will use video size.
| **opacity** (float): Opacity of the video from 0.0 (`fully transparent`) to 1.0 (`fully opaque`). Can increase lag.
| **on_end** (function): Function to be called when the video ends.
| **on_end_args** (any): Arguments to be passed to the on_end function. (Slightly buggy)
| **z_index** (int): Determines draw order. Items with a higher z_index appear above those with lower values.  
| **keep_aspect_ratio** (bool): If true, will automatically resize to remain aspect ratio, no matter what width/height is specified.
| **smooth** (bool): Whether to slow the video down to attempt to smooth lag. 

Video methods
~~~~~~~~~~~~~

.. code-block:: python

    myVideo.seek(seconds)

Skip to a certain time length into the video. `seconds` must be an integer. Using 0 will restart the video.

.. code-block:: python

    myVideo.pause()

Pauses the video until played.

.. code-block:: python

    myVideo.play(seconds)

Resumes a paused video.

Example
~~~~~~~

This script creates a video that immidiately plays and closes when finished. 

.. code-block:: python

    import pyrend

    def finished():
        pyrend.close()
    
    myVideo = pyrend.overlay.video("clip.mp4", (300, 200), (500, 300), on_end=finished)
    
    def update():
        pass
    
    pyrend.start(update)

.. note::

    You can use the VideoItem's proptery `frames` to get a list of all loaded frames in the video or `frame_index` to get the current frame.

    Example: `print(f"The video is on frame {myVideo.frame_index}")`

Demonstration
-------------

This script uses multiple of the items shown in this section to draw a square image to the screen, and add a rounded border and custom font title to it. Note that the things you can do with PyRend greatly expands with the ability to modify items, documented in the next section. 

.. code-block:: python

    import pyrend

    border = pyrend.overlay.shape(False, (70, 70), (430, 430), (255, 100, 0), radius=10)
    image = pyrend.overlay.image("image.png", (100, 100), (370, 370), keep_aspect_ratio=False)
    font = pyrend.overlay.load_font("font.ttf")
    title = pyrend.overlay.write("Image", (120, 440), 30, font=font)
    
    def my_update_loop():
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()
    
    pyrend.start(my_update_loop)


Modifying Items
===============

The possiblities of PyRend greatly expand when you can modify items during the loop. This means you can create games, interactable interfaces or other dynamic effects. 

Editing
-------

Editing an item is the easiest way to modify it. `edit()` is a method on all items that allows you to change the properties. As different items have some different properties, the edit method changes slightly between item types. This is an example of the edit method on a ShapeItem:

.. code-block:: python

    myShape.edit(
        base_pos=None,
        size=None,
        color=None,
        opacity=None,
        radius=None,
        rotation=None,
    )

Visibility
~~~~~~~~~~

Position and Offset
-------------------

Heirachy
--------

Rotating
--------

Custom rotation points
~~~~~~~~~~~~~~~~~~~~~~

Other
=====

Properties
----------

Mouse
-----
