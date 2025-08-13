Sound
=====

Overview
--------

The PyRend sound submodule allows you to play, modify, record and write sound. It uses two main object types, ``Sound()`` and ```Recording()``. 

Sound Objects
-------------

Sound objects are general objects containing everything in PyRend related to sound. They can be created with the ``createsound()`` function.

.. code-block:: python

  mySound = pyrend.sound.createsound(path, volume=1.0)

| **path** ()
