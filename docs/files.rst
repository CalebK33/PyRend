Files
=====

Overview
--------

The PyRend files submodule allows the ability to run files of various types, manipulate open windows and take screenshots. Its main features lies in the window manipulation, with the ability to resize windows, restore windows, minimise, maximise, close and much more. 

Managing files
-------------

You can run files using PyRend with:

.. code-block:: python

  pyrend.files.run(path)

**path** (str): The relative or absolute path to the file to be ran. The file will be instantly run in a subproccess, without stopping the main script. The file types you can run are: .exe, .bat, .py, .sh and .jar. Attempting to run any other unsupported file type will result in the error "`PyRend error: Unsupported file type .{extension}`".

You can also download a file from the internet using:

.. code-block:: python

  pyrend.files.download(link)

The link can be anywhere on the internet, and be any file type. For example, you could download the PyRend favicon from ``'https://pyrend.readthedocs.io/en/latest/_static/favicon.png'``! It will download into the same folder as the script running. 

Windows
============

Functions
---------

There are a few useful functions for accessing windows in PyRend. The first few allow you to get the title or win32 window object from open windows. 

.. code-block:: python

  pyrend.files.activeWindow(title=False) -> Win32Window or str

Will return the window that is currently on top/active. If `title` parameter is False like it is by default, it will return a Win32Window object, which is useful for creating window classes or managing in other ways. If True, will return the title of the window as a string, for example; ``'Downloads - File Explorer'``, ``Command Prompt`` or ``'Outer Wilds'``.

You can get a list of all open windows titles using:

.. code-block:: python

  pyrend.files.getWindowTitles() -> list

This will give a list of all open windows. Note that the list will return some empty strings belonging to windows that are processes and not visible, so you will need to account for that. There also will be two non-visible windows most of the time: "Windows Input Experience" and "Program Manager" (Only tested on Windows 11, likely differs on windows 10). 

You can also use the a similar function for getting a list of all windows in Win32Window format:

.. code-block:: python

  pyrend.files.getWindows() -> list

You can create a PyRend window class to allow manipulation over windows. You can make this using:

.. code-block:: python

  myWindow = pyrend.files.window(window)

For the window parameter, you can pass either a string with the full title of the window, or a Win32Window object (likely obtained from the previous functions)

Class
-----

Creating a PyRend window class using the ``window()`` function above allows you to manipulate windows and get specific details from them. 

Attributes
~~~~~~~~~~

When a window object is created, it has a `window` and `title` attribute built in. The window is the Win32Window object and the title is a string with its title. As of PyRend 0.1.47, the title is a property, so `will` update if it changes (eg. You go to a different browser tab).

**Example usage:**

.. code-block:: python

  import pyrend
  
  myWindow = pyrend.files.window(pyrend.files.activeWindow())
  print(f"You are currently looking at: {myWindow.title}!")

Output:

.. code-block:: bash

  You are currently looking at: main.py - Untitled (Workspace) - Visual Studio Code!

You can also use the property ``isMaximised`` to tell if the window is maximised. Yes, you are being forced to spell it the non-American way.

.. code-block:: python

  myWindow.isMaximised -> bool

Will return True or False whether the window is maximised or not. You can also use ``width`` and ``height`` attributes to check its size. 

.. code-block:: python

  myWindow.width -> int
  myWindow.height -> int

Will return its width or height in pixels. 

Using these attributes, you can do things like this:

.. code-block:: python

  import pyrend

  myWindow = pyrend.files.window(pyrend.files.activeWindow())
  status = "maximised" if myWindow.isMaximised else "not maximised"
  print(f"{myWindow.title} is {status} and is {myWindow.widtpixels wide!")

Output:

.. code-block:: bash

  Spotify Free is not maximised and is 845 pixels wide!

Management
~~~~~~~~~~

You can close a window using:

.. code-block:: python

  myWindow.close()

You can minimise or maximise a window using:

.. code-block:: python

  myWindow.minimize()
  myWindow.maximize()

And you can restore a window using:

.. code-block:: python

  myWindow.restore()

You can also resize windows:

.. code-block:: python

  myWindow.resize(x, y)

**x** and **y** are integers of how many pixels wide and tall to resize the window to. You can move a window to a certain position using:

.. code-block:: python

  myWindow.move(x, y)

| This will move (teleport) a window to the x and y coordinates specified. This also uses pixels. For both moving and resizing, you can use ``pyrend.r2p()``. To read about pixel vs relative coordinates, view `here <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_.
| Moving a window will move it instantly with no animation. 

Examples
--------

Managing windows in PyRend has a lot of possibilities, especially in combination with the other submodules. Add keybinds to controlling windows with the input submodule, add sound effects with the sound submodule or manipulate windows in combination with the overlay submodule. Below are some examples of things you can do with mostly just the files submodule, with minimal other submodule usage. 

This script allows you to use the arrow keys to resize the window active when the script is run:

.. code-block:: python

  import pyrend
  pyrend.init()
  
  window = pyrend.files.window(pyrend.files.activeWindow())
  window.restore()  # Get the active window and set it up
  window.move(0, 0)
  window.resize(pyrend.overlay.screen_size()[0], pyrend.overlay.screen_size()[1])
  
  def update():
      # Quit shortcut
      if pyrend.input.is_key_down('ALT') and pyrend.input.is_key_down('Q'):
          pyrend.close()
  
      if pyrend.input.is_key_down('LEFT'):   # If keys pressed, change window size
          window.resize(window.width - 10, window.height)
      if pyrend.input.is_key_down('RIGHT'):
          window.resize(window.width + 10, window.height)
      if pyrend.input.is_key_down('UP'):
          window.resize(window.width, window.height - 10)
      if pyrend.input.is_key_down('DOWN'):
          window.resize(window.width, window.height + 10)
  
  pyrend.start(update)

Note that these are basic scripts for proof of concept and aren't optimised or bug free.

This script adds a hovering effect to non-maximised windows:

.. code-block:: python

  import math
  import time
  import random
  import pyrend
  import win32gui
  
  pyrend.init()
  
  # Store base positions + random phase for each window
  window_data = {}
  start_time = time.time()
  
  def update():
      global window_data, start_time
  
      # Quit shortcut
      if pyrend.input.is_key_down('ALT') and pyrend.input.is_key_down('Q'):
          pyrend.close()
  
      t = time.time() - start_time
  
      for w in pyrend.files.getWindows():
          window = pyrend.files.window(w)
  
          if window.isMaximised:
              continue  # skip maximized windows
  
          hwnd = window.window._hWnd
  
          if hwnd not in window_data:     # Calculate how to move the window
              rect = win32gui.GetWindowRect(hwnd)
              base_x, base_y = rect[0], rect[1]
              phase = random.uniform(0, math.pi * 2)   
              speed = random.uniform(1.6, 2.1)         
              window_data[hwnd] = (base_x, base_y, phase, speed)
  
          base_x, base_y, phase, speed = window_data[hwnd]
  
          # Gentle vertical oscillation with random phase + speed
          offset = int(5 * math.sin(t * speed + phase))
          window.move(base_x, base_y + offset)

  pyrend.start(update)


Screenshots
===========
