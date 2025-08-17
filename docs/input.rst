Input
=====

Overview
--------

The input submodule of PyRend allows the control over windows keybindings, mouse input, listening for global keypresses and some other window functions. The input submodule is very useful in combination with the overlay, as you can manage keybinds for games or GUIs, manipulate the mouse and more. No functions require administrator access/run with administrator.

**Features:**

- Detect keypresses
- Manipulate key presses (force press keys) using ctypes
- Write text using strings
- Execute keyboard commands
- Manipulate and manage the mouse
- Alter current application and lock workstation
- Run without windows permissions/administrator

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

There are many functions in PyRend that allow you to manipulate the windows keyboard. The most basic of these is ``press()``. This will press a key for one frame, which will could a single character or press a single key.

.. code-block:: python

  pyrend.input.press("SPACE")

This will press the space key once. Note that this will press a single key, so will not account for uppercase letters or similar keys which require the shift key to be down. You will need to do this yourself, or use the ``write()`` function.

.. note::

  The parameter for ``press()`` and other following functions requires a PyRend key code. For most keys, this is a string with the key (uppercase) to be used, such as     ``'A'`` or ``'='``. To read the full list of all PyRend keycodes, view the table `here <#Key-Codes>`_.

To hold a key down for longer, you can use:

.. code-block:: python

  pyrend.input.hold('SHIFT')

It will stay down until released with:

.. code-block:: python

  pyrend.input.release('SHIFT')

However, it will also release if the user presses that key and releases it manually. 

To manipulat the keyboard into writing words, you can use:

.. code-block:: python

  pyrend.input.write("This will be typed!")

This will use the keyboard to write text to the screen, and it `will` account for the shift key (capital letters or symbols like '!'). Note that this can have unexpected results if the user is holding down keybind buttons such as control, alt or the windows key. To reduce the chance of this causing issues, you could ``release()`` those keys before writing.

You can also force the keyboard to execute command keybinds using:

.. code-block:: python

  pyrend.input.command(
    key,
    control = True,
    shift = False,
    windows = False,
    alt = False
  )

| **key** (str): The PyRend key code to use for the command. View `all key codes table <#Key-Codes>`_.
| **control** (bool): Whether to press the control key for the command. True by default.
| **shift** (bool): Whether to press the shift key for the command. False by default.
| **windows** (bool): Whether to press the windows key for the command. False by default.
| **alt** (bool): Whether to press the alt key for the command. False by default.

For example, this will execute ``CONTROL`` + ``ALT`` + ``TAB``:

.. code-block:: python

  pyrend.input.command('TAB', alt=True)

Note that some commands will be blocked by windows and cannot be executed, such as ``CONTROL`` + ``ALT`` + ``DEL``.

Other
=====

Mouse
-----

The input submodule also has some tools relating to the mouse cursor. 

.. code-block:: python

  pyrend.input.hide_cursor()

And...

.. code-block:: python

  pyrend.input.show_cursor()

Pretty self explanatory, hides and shows the cursor. 

You can also teleport the cursor to a specific location:

.. code-block:: python

  pyrend.input.move_mouse(x, y)

Specify an x and y position, in pixels, to move the cursor to. You can pyrend.r2p here, see `pixel vs relative coordinates. <https://pyrend.readthedocs.io/en/latest/index.html#pixel-vs-relative-coordinates>`_.

If you want to obtain the current position of the mouse, you can use the ``get_mouse_pos()`` function in the overlay submodule, documented `here <https://pyrend.readthedocs.io/en/latest/overlay.html#mouse>`_.

Windows
-------

The input submodule also has some minimal functions relating to managing windows/applications. For more application control, read about the `files submodule <https://pyrend.readthedocs.io/en/latest/files.html>`_.

.. code-block:: python

  pyrend.input.close_foreground()

Closes the current foreground (currently on top) window. This does not close the hidden overlay application. This function is easier, but not as reliable as ways you can do this in the files submodule.

.. code-block:: python

  pyrend.input.minimize_windows()

Minimises all windows. Again, this is less reliable than what you can do with the files submodule, but is a much easier and simpler function.

.. code-block:: python

  pyrend.input.lock()

Locks the computer.

Don't get any ideas.

Yes, you could.

No, it doesn't require administrative access.

Key codes
=========

.. list-table:: PyRend Key Codes
   :header-rows: 1
   :widths: 30 40 30

   * - Key Name
     - Description
     - VK Hex Code
   * - ``'LBUTTON'``, ``'RBUTTON'``, ``'MBUTTON'``
     - Left, Right, and Middle Mouse Buttons
     - 0x01, 0x02, 0x04
   * - ``'BACK'``, ``'TAB'``, ``'ENTER'``
     - Backspace, Tab, Enter/Return
     - 0x08, 0x09, 0x0D
   * - ``'SHIFT'``, ``'CTRL'``, ``'CONTROL'``, ``'ALT'``, ``'PAUSE'``, ``'CAPSLOCK'``
     - Modifier Keys and Lock Keys
     - 0x10, 0x11, 0x11, 0x12, 0x13, 0x14
   * - ``'ESC'``, ``'SPACE'``, ``'DELETE'``, ``' '`` 
     - Escape, Spacebar, Delete
     - 0x1B, 0x20, 0x2E, 0x20
   * - ``'PAGEUP'``, ``'PAGEDOWN'``, ``'END'``, ``'HOME'``, ``'LEFT'``, ``'UP'``, ``'RIGHT'``, ``'DOWN'``
     - Navigation Keys
     - 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28
   * - ``'A'`` – ``'Z'``
     - Alphabet Keys
     - 0x41–0x5A
   * - ``'0'`` – ``'9'``
     - Number Keys
     - 0x30–0x39
   * - ``'NUMPAD0'`` – ``'NUMPAD9'``
     - Numeric Keypad Keys
     - 0x60–0x69
   * - ``'F1'`` – ``'F12'``
     - Function Keys
     - 0x70–0x7B
   * - ``'PLUS'``, ``'='``
     - Plus / Equals Key
     - 0xBB
   * - ``'MINUS'``, ``'-'``
     - Minus / Hyphen Key
     - 0xBD
   * - ``'COMMA'``, ``','``
     - Comma Key
     - 0xBC
   * - ``'PERIOD'``, ``'.'``
     - Period Key
     - 0xBE
   * - ``'SLASH'``, ``'/'``
     - Forward Slash Key
     - 0xBF
   * - ``'TILDE'``, ``'~'``
     - Tilde / Backtick Key
     - 0xC0
   * - ``'OPENBRACKET'``, ``'['``
     - Left Bracket Key
     - 0xDB
   * - ``'BACKSLASH'``
     - Backslash Key
     - 0xDC
   * - ``'CLOSEBRACKET'``, ``']'``
     - Right Bracket Key
     - 0xDD
   * - ``'QUOTE'``, ``"'"``
     - Quote Key
     - 0xDE
   * - ``'SEMICOLON'``, ``';'``
     - Semicolon Key
     - 0xBA
   * - ``'VOLUME_MUTE'``, ``'VOLUME_DOWN'``, ``'VOLUME_UP'``, ``'MEDIA_NEXT'``, ``'MEDIA_PREV'``, ``'MEDIA_STOP'``, ``'MEDIA_PLAY_PAUSE'``
     - Media Control Keys
     - 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3
   * - ``'LWIN'``, ``'RWIN'``, ``'APPS'``
     - Windows & Menu Keys
     - 0x5B, 0x5C, 0x5D
   * - ``'BROWSER_BACK'``, ``'BROWSER_FORWARD'``, ``'BROWSER_REFRESH'``, ``'BROWSER_STOP'``, ``'BROWSER_SEARCH'``, ``'BROWSER_FAVORITES'``, ``'BROWSER_HOME'``
     - Browser Keys
     - 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC


