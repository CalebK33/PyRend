Files
=====

Overview
--------

The PyRend files submodule allows the ability to run files of various types, manipulate open windows and take screenshots. Its main features lies in the window manipulation, with the ability to resize windows, restore windows, minimise, maximise, close and much more. 

Running files
-------------

You can run files using PyRend with:

.. code-block:: python

  pyrend.files.run(path)

**path** (str): The relative or absolute path to the file to be ran. The file will be instantly run in a subproccess, without stopping the main script. The file types you can run are: .exe, .bat, .py, .sh and .jar. Attempting to run any other unsupported file type will result in the error "`PyRend error: Unsupported file type .{extension}`".

Applications
============



Window class
============

Attributes
----------

Management
----------

Screenshots
===========
