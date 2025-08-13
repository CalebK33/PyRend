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

| **path** (str): The relative or absolute path to your sound file. Read below for supported file types. 
| **volume** (float): The decimal value for the volume to play the sound at. 1.0 is normal.

The `path` parameter fully supports the follow formats: .mp3, .ogg and .wav. More sound file types may work, but may not be fully supported for all functions. 

You can also create a sound object from sound data (NumPy Arrays) and a samplerate. To learn more, read the `soundfile documentation <https://python-soundfile.readthedocs.io/en/0.13.1/>`_

.. code-block:: python

  mySound = pyrend.sound.array(data, samplerate, volume=1.0)

| **data** (ndarray): The array data for the audio.
| **samplerate** (int): The sample rate for the audio.
| **volume** (float): The decimal value for the volume to play the sound at. 1.0 is normal.
