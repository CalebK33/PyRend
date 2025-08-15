Input
=====

Overview
--------

The input submodule of PyRend allows the control over windows keybindings, mouse input, listening for global keypresses and some other window functions. The input submodule is very useful in combination with the overlay, as you can manage keybinds for games or GUIs, manipulate the mouse and more. 

**Features:**

- Detect keypresses
- Manipulate key presses (force press keys) using ctypes
- Write text using strings
- Execute keyboard commands
- Manipulate and manage the mouse
- Alter current application and lock workstation

Keyboard
========

Listeners
---------

You can detect if a key is down using ``is_key_down``. This will return `True` if the key is currently down. Note that if put in a loop, will return `True` **every** frame it is down for, so you will have to account for that.

.. code-block:: python

  pyrend.input.is_key_down(key) -> bool

For the **key** parameter, you will need to supply one of the PyRend key codes in string format. For the most part, this is a number, symbol or upper case letter (eg. ``'A'``, ``'3'``, ``'='``) or it's name (eg. ``'SPACE'``, ``'LEFT'``, ``'F1'``, ``'NUMPAD0'``). Some keys also have multiple key codes, eg. for the tilde key you can use ``'TILDE'`` or ``'~'``. The full table of all PyRend key codes can be viewed at the end of this documentation, `here <#Key-Codes>`_.

Control
-------

Other
=====

Mouse
-----

Windows
-------

Key codes
=========
