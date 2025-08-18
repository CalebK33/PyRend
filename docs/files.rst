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

Will return the window that is currently on top/active. If `title` parameter is False like it is by default, it will return a Win32Window object, which is useful for creating window classes or managing in other ways. If True, will return the title of the window as a string, for example; ``'Downloads - File Explorer'``, ``Command Prompt`` ``'Outer Wilds'``.

You can get a list of all open windows titles using:

.. code-block:: python

  pyrend.files.getWindowTitles() -> list

This will give a list of all open windows. Note that some of them will likely be empty processes, so you may have to account for that. You can also use the a similar function for getting a list of all windows in Win32Window format.

.. code-block:: python

  pyrend.files.getWindows() -> list

Class
-----

Attributes
~~~~~~~~~~

Management
~~~~~~~~~~

Screenshots
===========
