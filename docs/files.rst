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

This will give a list of all open windows. Note that some of them will likely be empty processes, so you may have to account for that. You can also use the a similar function for getting a list of all windows in Win32Window format.

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

When a window object is created, it has a `window` and `title` attribute built in. The window is the Win32Window object and the title is a string with its title. Note that as of PyRend 0.1.47, the title is a property, so `will` update if it changes (eg. You go to a different browser tab).

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
  print(f"{myWindow.title} is {status} and is {myWindow.width} pixels wide!")

Output:

.. code-block:: bash

  Spotify Free is not maximised and is 845 pixels wide!

Management
~~~~~~~~~~

Screenshots
===========
