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

.. note::

    The PyRend overlay does not show on the taskbar and will be classified under something like ``Console Windows Host`` in the task manager. This is normally shown        whether PyRend is running or not, meaning there is no way to tell the overlay is open.

    However, if you package a PyRend script into an exe file using PyInstaller (or any alternative), the PyRend overlay will appear in the task manager under the name      and icon of that executable.

Items
-----

To draw elements onto the overlay in PyRend, you first need to create items. These items are Python objects that store properties defining how and where something appears on the screen. PyRend provides six types of overlay items: ShapeItem, TextItem, ImageItem, VideoItem, PointItem, and a base class BaseItem, which serves as the foundation for all others.
This section of the documentation will guide you through how to create and use each item type, as well as explain shared methods and other overlay-related functionality.

Creating items
==============

PyRend overlay objects are created by assigning them to variables, which allows you to modify them later. For example, the code below creates a ``ShapeItem`` and assigns it to `myShape` (Ignoring parameters for now).

.. code-block:: python

  myShape = pyrend.overlay.shape(...)

With that said, we can begin to create items using the following functions.

Shapes
------

Shapes in PyRend can be rectangular or elliptical. You can create them with ``pyrend.overlay.shape`` with default parameters like so:

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
        opacity=1,
        z_index=0
    )

| **text** (str): The text to be written onto the overlay
| **pos** (tuple): The (`x, y`) position of the top-left corner of the text, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 
| **size** (tuple): The (`width, height`) of the text, in pixels.  
| **color** (tuple): The RGB color of the text, e.g. (`255, 0, 0`) for red. See: `RGB vs hex codes <https://pyrend.readthedocs.io/en/latest/index.html#hex-vs-rgb-codes>`_ 
| **font** (str): The font to write in. See: Custom Fonts (below)
| **opacity** (float): Opacity of the shape from 0.0 (`fully transparent`) to 1.0 (`fully opaque`). 
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
| **opacity** (float): Opacity of the shape from 0.0 (`fully transparent`) to 1.0 (`fully opaque`). Can cause more lag.
| **keep_aspect_ratio** (bool): If true, will automatically resize to remain aspect ratio. Read below for more info.
| **z_index** (int): Determines draw order. Items with a higher z_index appear above those with lower values.  

PyRend images can be in the format of JPEG, PNG, WEBP, GIF (Animation not supported) or SVG. More images types may work but aren't fully supported The **path** parameter can be either a relative or absoloute path, and must include the file extension. 
The **keep_aspect_ratio** parameter determines whether to automatically resize the image to remain the file's aspect ratio. It will take the size tuple and modify it to stay the same aspect ratio, preventing the image from coming out squashed or stretched. 

Points
------

PyRend uses points as invisible items that can store just a location and rotation. They are not rendered onto the screen, making them useful for storing a position, adding multiple joints or hitboxes to existing items, and are nessasairy for creating specific roation points. (See custom rotation points)

.. code-block:: python

    myPoint = pyrend.overlay.point(base_pos)

**base_pos** (tuple): The (`x, y`) position to be stored with the point, in pixels. See: `Pixel vs relative coordinates <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_ 

Debug Mode
~~~~~~~~~~

By enabling debug mode, all points will apear on top of everything as small red dots. This can make it easier to debug errors or visualise things. You can enable debug mode using:

.. code-block:: python

    pyrend.overlay.enable_debug(enable=True)

**enable** (bool): Whether to turn debug mode on or off.

Debug mode also enables the logging of some useful video information, such as displaying when a video has started loading asyncronously and when all frames finish loading. 

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
| **on_end** (function): Function to be called when the video ends/loops.
| **on_end_args** (any): Arguments to be passed to the on_end function. (Slightly buggy)
| **z_index** (int): Determines draw order. Items with a higher z_index appear above those with lower values.  
| **keep_aspect_ratio** (bool): If true, will automatically resize to remain aspect ratio, no matter what width/height is specified.
| **smooth** (bool): Whether to slow the video down to attempt to smooth lag. 

Video methods
~~~~~~~~~~~~~

.. code-block:: python

    myVideo.seek(seconds)

Skip to a certain time length into the video. ``seconds`` must be an integer. Using 0 will restart the video.

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

    You can use the VideoItem's proptery ``frames`` to get a list of all loaded frames in the video or ``frame_index`` to get the current frame.

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

Editing an item is the easiest way to modify it. ``edit()`` is a method on all items that allows you to change the properties. As different items have some different properties, the edit method changes slightly between item types. This is an example of the edit method on a ShapeItem:

.. code-block:: python

    myShape.edit(
        base_pos=None,
        size=None,
        color=None,
        opacity=None,
        radius=None,
        rotation=None,
    )

When you edit, you can specify any properties you would like to change. This documentation will not include the unique edit methods for every item, but it should be pretty self explanatory. To put it simply, this would be how you change the colour of a shape:

.. code-block:: python

    myShape.edit(color=(0, 255, 0))

Therefore you could also put things in your update function to change them dynamically. Therefore you could make something like this script which immidiately fades out an image when the script is run:

.. code-block:: python

    import pyrend
    
    image = pyrend.overlay.image("image.png", (100, 100), (500, 500))
    
    def my_update_loop():        # The update loop is called 60 times a second
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()
        if image.opacity > 0:
            image.edit(opacity=image.opacity - 0.01)    # Opacity is a decimal value, therefore descreasing at 
                                                        # 0.01pf at 60fps will take 1.6 seconds to dissapear.
        else:                                           
            pyrend.close()    # Finish the program when the image has vanished
    
    pyrend.start(my_update_loop)

Or this script which will create a circle in a random loction on the screen every time the space key is pressed. See: Detecting Keypresses

.. code-block:: python

    import pyrend
    import random    # Use random to create circles in random positions
    
    circles = []        # Store a list of all existing circles
    spacedown = False    
    
    def my_update_loop():
        global spacedown  
    
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()
    
        if pyrend.input.is_key_down("SPACE") and not spacedown:     # Only execute once after space is pressed
            spacedown = True
            circle = pyrend.overlay.shape(        # Create a new circle at a random position
                True,
                (random.randint(0, 1950), random.randint(0, 1020)),
                (150, 150)
            )
            circles.append(circle)
        elif not pyrend.input.is_key_down("SPACE"):    # Detect if the space key has already been down for a frame
            spacedown = False
    
    pyrend.start(my_update_loop)

.. note::

    Technically you can also manually change the properties of an item simply by doing:

    ``myItem.opacity += 0.2`` 

    However, it is only reccomended to use this for things like opacity, colour or size. Since rotation and position are cached to save memory, you **must** only           change these with ``edit()``, ``move()`` or ``rotate()`` 

You can also move an item using:

.. code-block:: python

    myItem.move(x, y, change=False)

| **x** and **y**: The pixel position to move the item to.
| **change** (bool): Whether to instantly move the item to the specified coordinates (`False`) or to alter its current position by the values specified (`True`)

You can also alter the offset of an item using the similar method ``move_offset()``, which works in the exact same way but for the items offset. To learn what an items offset is, see `Position and Offset <#position-and-offset>`_.

Visibility
----------

You can choose whether a PyRend object will be visible using the `hide()` or `show()` methods. 

.. note::

    Hidden items will still have collision, and can be altered while hidden. Hiding an item will only skip it from being drawn onto the screen. 

Usage:

.. code-block:: 

    myItem.hide() # Make the item invisible 
    myItem.show() # Make the item visible again

You can also delete an item using:

.. code-block:: 

    myItem.delete(soft=False)

The **soft** parameter is False by default and defines whether the item will be soft or hard deleted. Soft deleted items are still stored in memory but not drawn/processed. This means they are technically recoverable, and your script will be able to handle referencing it after deletion. Hard deletion immediatly erases the item from memory. Hard deleting an item makes it unable to be recovered completely. It is highly reccomended to use hard deletion for deletion of objects in mass, most likely items created in iteration (eg. particles, game enemies).  

.. note::

    Deleting a parent also deletes all of its children. To avoid this, use the ``free()`` method (inverted) on the Item prior to deletion.

Position and Offset
===============================

How position, offset, absolute position and base position work in PyRend is one of the more complex aspects of PyRend to understand.

**offset** is a tuple property that remains at ``(0, 0)`` until changed using the ``move_offset(x, y)`` method. It adjusts the *visual position* of an item without modifying its base coordinates. An item's offset is taken into account when drawn, so it allows changing where it appears visually **without altering its logical or hierarchical location**.

Offset **is** taken into account when detecting collisions, calculating `pos`, and responding to mouse hover or interaction events.

**base_pos** is a tuple that defines the *original or intended position* of the item in screen or world space. It is the starting point of the item, ignoring any visual adjustments (like offset). For items without a parent, `base_pos` represents their core anchor point. For child items, `base_pos` is set to the *position of the parent* at the time the child relationship is formed.

**parent_offset** is the relative distance between the item's `base_pos` and the current position of its parent. It's automatically calculated when an item becomes a child of another using ``become_child_of()``. This offset is then transformed (rotated if needed) and added to the parent's absolute position.

**absolute position** (as returned by ``get_absolute_pos()``) is the calculated position of the item based on its base position, parent hierarchy, and rotation — but **not** including the visual offset.

**pos** is a read-only property that returns the final visual position of the item. It combines:
- the `absolute position` of the item
- plus the current `offset`

This is the coordinate used when drawing the item on screen, checking collisions, and tracking mouse interaction.

**original_pos** is a snapshot style attribute storing the original position when the item was created. Avoid modifying it and generally shouldn't be used much.

Summary 
-------

.. list-table:: Summary
   :header-rows: 1
   :widths: 20 50 30

   * - Property
     - Meaning
     - How to Modify
   * - ``base_pos``
     - Original anchor position; not affected by offset
     - Set via constructor or ``move()``
   * - ``offset``
     - Visual adjustment; affects drawing and logic
     - Use ``move_offset(x, y)``
   * - ``parent_offset``
     - Relative positional offset set when parenting
     - Automatically via ``become_child_of()``
   * - ``get_absolute_pos()``
     - Computed from ``base_pos``, parents, and rotation
     - Read-only (computed dynamically)
   * - ``pos``
     - Final visual position (absolute + offset)
     - Read-only (computed dynamically)
   * - ``original_pos``
     - Cached absolute position snapshot (at creation). Not updated.
     - Avoid modifying, but `can` be modified manually
   * - ``rotation``
     - Rotation in degrees (cumulative via parents)
     - Use ``rotate(degrees)`` or set directly


Tip: Always use ``pos`` and ``get_absolute_pos()`` for dynamic logic like collision, drawing, or movement logic.

You can also use ``offset`` to align an item to the center of its position. You can easily do this with the build in method:

.. code-block:: python

    Item.align_center(x=True, y=True)

This will set it's offset to half of its width and height, essentially centering it on the screen. You can specify whether just just center it on the x or y plane by setting the variables you want to align to True, which they both are by default. Note that when aligned to the center, all previous offset will be cleared. If you want previous offset to be saved after alignment, you will have to store it in a variable **before** alignment and apply it afterwards.

Heirachy
--------

PyRend has a heirachy that uses children and parents. Children will mimic the parents rotation and position, taking into account parent offset. Children and parents can be assigned in one of two ways:

.. code-block:: python

    Item1.become_child_of(Item2)
    # Or...
    Item2.become_parent_of(Item1)

**Parent offset** is a property (`parent_offset`) that is set when you assign a parent to an item. It will store it's position relative to it's parent and it's absoloute position will take this into account every frame. When an item is a child, it cannot be moved as normal, you will only be able to change it's offset, or it's parent offset depending on if you want to move it visually or physically. Note that you can only assign one parent to an object, and trying to set a new parent will replace it's old parent.

To remove a parent or children, you can use ``free()``:

.. code-block:: python

    Item1.free(inverse=False)

**inverse** (bool): Whether to inverse the effects of the ``free()`` method. When False, the item will become free from any parents, and when False, will free all of it's children. 

Rotating
--------

Items can also be rotated using either ``edit()`` or `rotate`. Items rotate around the top left of the item, regardless of offset. Therefore if you were to center an item, it would appear to be rotating around its center. Items can be rotated like this:

.. code-block:: python

    myItem.rotate(degrees, change=True)

| **degrees** (int): Integer of degrees to rotate the item.
| **change** (bool): True by default, determintes whether to add the specified degrees to it's current rotation (`True`) or set its current rotation to the degrees specified (`False`)

Custom rotation points
~~~~~~~~~~~~~~~~~~~~~~

Since rotation is based around parent rotation if in a heirachy, this can be taken advantage of to create custom rotation points using `PointItems <#points>`_. You can set the PointItem as a parent of a shape and rotate it to have a custom rotation point. It's rotation point will then be essentially set to it's parent offset (See: `Hierachy <#heirachy>`_). This results in children being able to orbit parents. 

This script will create a rectangle with a custom rotation point just left of it's center, and spins it to demonstrate:

.. code-block:: python

    import pyrend

    myShape = pyrend.overlay.shape(False, (300, 300), (500, 200), (255, 0, 0))
    myRotationPoint = pyrend.overlay.point((425, 400))
    myShape.become_child_of(myRotationPoint)
    
    def my_update_loop():
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()
        
        myRotationPoint.rotate(1)
    
    pyrend.start(my_update_loop)

Or alternatively, define the roation point as a propery of the ShapeItem (IDE Autocorrect won't support):

.. code-block:: python

    import pyrend
    
    myShape = pyrend.overlay.shape(False, (300, 300), (500, 200), (255, 0, 0))
    myShape.rotationPoint = pyrend.overlay.point((425, 400))
    myShape.become_child_of(myShape.rotationPoint)
    
    def my_update_loop():
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()
        
        myShape.rotationPoint.rotate(1)
    
    pyrend.start(my_update_loop)

Other
=====

Properties
----------

You can return the width and height of an item using:

.. code-block:: python

    w = Item.width() -> int
    h = Item.height() -> int

You can return the width or height of the screen using the ``screen_size`` method:

.. code-block:: python

    w, h = pyrend.overlay.screen_size() -> tuple

Both variables in the tuple will be integers. 

Collision
~~~~~~~~~

You can detect a collisions between two objects using:

.. code-block:: python

    Item1.get_collision(Item2) -> bool

This will detect if any point of Item1 intersects with Item2. Collision does **not** take into account rotation. Collision detection for ellipses or text will use a full square hitbox, rather than what is visible. 

.. note::

    Points calculate collision in the say way the mouse hover function does. This means it `does` account for rotation and is very reliable. This method of collision       detection will automatically be used whenever you use the get collision method either from or using a PointItem.

Mouse
-----

The PyRend overlay has a range of features relating to managing the mouse and interacting with items, however the possibilities of user input expands significantly using the `input submodule <https://pyrend.readthedocs.io/en/latest/input.html>`_.  The following are mouse related features in the overlay submodule.

.. code-block:: python

    pyrend.overlay.get_mouse_pos() -> tuple

Returns a tuple with two integers, x and y, with the current position of the mouse. 
You can detect if the mouse is hovering over an object using ``is_held()``

.. code-block:: python

    Item.is_mouse_hovering() -> bool

This will return `True` if the mouse is currently touching the item, accounting for rotation. You can combine this with using ``input.is_key_down`` to detect if the mouse is also clicking, to then axecute an action. This could even be used for things such as drag and drop mechanics.

Using this, we could adapt the circle creation script from earlier to allow deleting certain circles. Now, you can press space to create a circle in a random position, and click it to remove it. Note that this code is not optimised.

.. code-block:: python

    import pyrend
    import random    # Use random to create circles in random positions
    
    circles = []        # Store a list of all existing circles
    spacedown = False         
    
    
    def my_update_loop():
        global spacedown
    
        if pyrend.input.is_key_down("LBUTTON"): # Detect if mouse is clicked
            for c in circles:
                if c.is_mouse_hovering():  # Detect if the mouse is hovering for each circle
                    c.delete()   # Delete the circle
    
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()
    
        if pyrend.input.is_key_down("SPACE") and not spacedown:     # Only execute once after space is pressed
            spacedown = True
            circle = pyrend.overlay.shape(        # Create a new circle at a random position
                True,
                (random.randint(0, 1950), random.randint(0, 1020)),
                (150, 150)
            )
            circles.append(circle)
        elif not pyrend.input.is_key_down("SPACE"):    # Detect if the space key has already been down for a frame
            spacedown = False
    
    pyrend.start(my_update_loop)

If you want to learn more about keypresses, read the `input submodule <https://pyrend.readthedocs.io/en/latest/input.html>`_.

By default, PyRend overlays are clickthrough, meaning they are ghost-like in the sense that the mouse can click straight through it to whatever application is behind. You can change this with:

.. code-block:: python

    pyrend.overlay.set_clickthrough(enabled=False)

Now by setting this with `False`, the overlay will **not** be clickthrough, and you will no longer be able to click behind where an item is. You will still be able to click where there is no items. To get around this, you could create an invisible (0.0 opacity) ShapeItem covering the entire screen. Partially or even fully transparent items still detect clicks and cannot be clicked through if clickthrough is disabled.  
