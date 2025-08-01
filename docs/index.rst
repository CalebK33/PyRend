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

.. contents::
   :local:
   :depth: 2

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

This section explains how to get started with PyRend.

Installation
------------

Use pip to install PyRend:

.. code-block:: bash

    pip install pyrend

