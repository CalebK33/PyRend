Overview
========

PyRend is a multipurpose Python library designed for easy control and management of Windows devices. Its main utility is its ability to draw invisible overlays onto the screen without a visible application window. These overlays are dynamic, can be altered live, and appear on top of all bordered or borderless windowed applications.

The PyRend overlay includes various settings such as click-through functionality, and simple functions make it easy to draw shapes, images, text, or even videos to the screen.

PyRend also includes a range of features that simplify advanced modules like `ctypes` to:

- Detect global keypresses
- Play or record sound
- Control and resize open applications
- Perform system-level tasks such as taking screenshots or managing files

You can view PyRend’s PyPI page with version history `here <https://pypi.org/project/pyrend>`_.

You can view PyRend’s source code `here <https://github.com/CalebK33/PyRend>`_.

Features
--------

- :doc:`Invisible graphical overlays<overlay>`
   - Easy-to-use API for drawing shapes, images, and text
   - Image and video support
   - Click detection
   - Dynamic, real-time interface updates

- :doc:`Audio playback and recording<sound>`
   - Play audio from OGG, MP3, or WAV
   - Record audio from the user’s microphone
   - Pitch shifting and volume control

- :doc:`Keyboard and mouse input management<input>`
   - Detect global keypresses
   - Simulate user input (keyboard and mouse)
   - Detect and manipulate mouse movement and clicks

- :doc:`Window and file manipulation<files>`
   - Resize, maximize, minimize, or move open windows
   - Run applications in background threads
   - Capture and save screenshots
   - Download files from URLs
   - Return open applications as manipulatable objects

Getting Started
===============

This section explains how to install and begin using PyRend.

Installation
------------

Install PyRend using pip:

.. code-block:: bash

    pip install pyrend

To confirm PyRend was installed successfully:

.. code-block:: bash

    pip show pyrend

If the command returns PyRend’s details, the installation was successful.

.. note::
   PyRend's dependencies include: librosa, moviepy, mss, numpy, opencv-python, Pillow, pygetwindow, PyQt5, requests, sounddevice, and soundfile.

PyRend Basics & Update Loop
---------------------------

The core of PyRend is its overlay system and update loop. This loop allows the overlay and program to run continuously until manually closed.

To start the loop:

.. code-block:: python

    pyrend.start()

This begins the internal PyRend loop, and the program will continue running. However, at this point, it can only be closed by quitting the terminal.

To improve this, you can pass a function into `pyrend.start()`. This function will be called every frame (typically 60 times per second). Using an update loop is *highly* recommended in most PyRend programs.

Example:

.. code-block:: python

    import pyrend

    def my_update_loop():
        pass

    pyrend.start(my_update_loop)

This gives you control over what happens each frame. However, the program can still only be ended by closing the terminal, since PyRend does not create a visible application window or taskbar icon.

To close PyRend programmatically:

.. code-block:: python

    pyrend.close()

This stops the update loop, deletes the overlay, and resumes execution after the `pyrend.start()` call—usually causing the program to exit.

A useful approach is binding a key or key combination to exit the program. PyRend provides an input module to check global keypresses:

.. code-block:: python

    pyrend.input.is_key_down(key) -> bool

This function takes a key name (as a string) and returns `True` if the key is currently held down. For example:

.. code-block:: python

    import pyrend

    def my_update_loop():
        if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
            pyrend.close()

    pyrend.start(my_update_loop)

In this example, pressing **Alt + Q** will exit the program. You can bind any key combination you prefer.

.. warning::
   Sometimes calling certain overlay functions first will cause the error:
   
   **AttributeError: 'NoneType' object has no attribute...**

   This issue is caused by trying to access the overlay object before it is created. To fix this, call *pyrend.init()* at the top of your script

With that, you now have a complete skeleton for a functional PyRend script! Now you can begin to draw items onto the screen. To learn how to manage the overlay and create items, view the :doc:`overlay documentation.<overlay>` 

Otherwise, continue on this page to check out the other module level functions, or view the :doc:`sound<sound>`, :doc:`input<input>` or :doc:`files<files>` submodule documentation.

Base Module Functions
=====================
Pixel vs Relative Coordinates
-----------------------------

.. code-block:: python

   pyrend.rel_to_pixel(x, y) -> tuple
   pyrend.r2p(x, y)

Both of the above functions do the same thing, r2p is just a shorthand version of rel_to_pixel. These functions convert relative coordinates to pixel coordinates. 

**Relative coordinates** hold values from -1 to 1, from the left to right or bottom to top of the screen. This makes it easy to center things as (0, 0) is always the center, no matter the screen size. 

**Pixel coordinates** start at (0, 0) in the top left and measure the pixels across the screen. All PyRend functions that use screen coordinates use pixel coordinates, making the functions for converting relative coordinates to pixels extremely useful. 

The functions also have reverse calculations:

.. code-block:: python

   pyrend.pixel_to_rel(x, y)
   pyrend.p2r(x, y)

All of these functions accept two paramters, x and y. If you feed both it will return a tuple, but if you only give one parameter a single integer/float will be returned. For example:

.. code-block:: python

   print(pyrend.r2p(0.3, -0.2))
   print(pyrend.r2p(0.4))

Outputs:

.. code-block:: python

   (1247, 618)    -> tuple
   1343           -> int
   
Hex vs RGB codes
----------------

All functions that involve colour in PyRend use RGB codes, rather than hex codes. You can use *pyrend.hex()* to convert colour hex codes to RGB tuples:

.. code-block:: python

   rgb = pyrend.hex("#3AF204")
   print(rgb)

Output:

.. code-block:: text

   (58, 242, 4)


