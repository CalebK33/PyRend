Welcome to PyRends's Documentation
======================================

.. toctree::
   :caption: Navigation
   :maxdepth: 2
   :hidden:

   overlay
   sound
   files
   input

Overview
--------

PyRend is a multipurpose Python library designed for easy control and management windows devices. PyRend's main utility is it's ability to draw invisible overlays onto the screen without a visible application. This overlay is dynamic and can be easily altered live, and is visible on top of all bordered or borderless windowed applications. The PyRend overlay comes with various settings such as specifying click through, and simple functions make it easy to draw shapes, images, text or even videos to the overlay. 


PyRend also comes with a multitude of other features that simplify advanced modules such as ctypes to utelize global keypresses, play or record sound, control and resize open applications and more.


You can view PyRend's PyPi page with version history `here. <https://pypi.org/project/pyrend>`_

You can view PyRend's source code `here. <https://github.com/CalebK33/PyRend>`_

Features
--------
- Invisible graphical overlays
   - Simple to use API for drawing shapes and text through objects
   - Image and video support
   - Click detection
   - Dynamic interface
- Playing sound and recording audio input
   - Play sound from ogg, mp3 or wav
   - Record audio input from user microphone
   - Pitch shift audio and volume
- Manage keyboard and mouse input
   - Detect global keypresses
   - Simulate user input to press keys
   - Detect and manipulate mouse movement and clicks
- Manipulate open applications and files
   - Resize, maximize, minimize or move open windows
   - Run applications in background threads
   - Capture and save screenshots
   - Download URLs
   - Return open applications as manipulatable objects

Getting Started
===============

This section explains how to install and begin using PyRend. 

Installation
------------

Use pip to install PyRend:

.. code-block:: bash

    pip install pyrend

To check PyRend was successfully installed, run:

.. code-block:: bash

   pip show pyrend

If it shows PyRend is installed, you have successfully installed PyRend and can begin... PyRending...?

.. note::
   PyRends dependencies are: librosa, moviepy, mss, numpy, opencv-python, Pillow, pygetwindow, PyQt5, requests, sounddevice, soundfile

PyRend Basics & Update Loop
---------------------------

The core features of PyRend are its overlay and update loop. PyRend's update loop allows the program and overlay to continually until closed. The most simple way to start this is with:

.. code-block:: python

   pyrend.start()

This will start the loop inside of PyRend and the program will continue to run. It can only be closed by quitting the terminal. How to fix this? Add a function as the parameter for pyrend.start() This will set that function as the update function to be called every loop (So 60 times a second at 60fps). Setting an update loop, though not nessasairy, is *highly* reccomended for all PyRend programs. using this, a basic starter program should look like this:

.. code-block:: python

   import pyrend

   def myUpdateLoop():
      pass

   pyrend.start(myUpdateLoop)

This is a lot better as now you can put anything in the update loop, however the program can still only be ended from quitting the terminal, as the PyRend overlay does not show up as an application, in the taskbar or as a window. You can close the PyRend application using:

.. code-block:: python

   pyrend.close()

This will stop the update loop, delete the overlay and continue the program from whereever **pyrend.start()** was called, which usually results in the program finishing. Something I would highly reccomend is to make a keybind to close the overlay, using:

.. code-block:: python

   pyrend.input.is_key_down(key) -> bool

This is using PyRends input module, which will be explained in more deatil later in the documentation. Describing it simply, pass the function a key in strong form, and it will return True or False dependind on whether the key is held down. Using this we can finish our basic PyRend skeleton by adding a way to quit the program:

.. code-block:: python

   import pyrend

   def myUpdateLoop():
      if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
         pyrend.close()

   pyrend.start(myUpdateLoop)

Obviously you can bind any keys you want, in that scenario I used `Alt + Q`. 

And there you go, you have a working skeleton PyRend script!  
