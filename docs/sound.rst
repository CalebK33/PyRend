Sound
=====

Overview
--------

The PyRend sound submodule allows you to play, modify, record and write sound. It uses two main object types, ``Sound()`` and ```Recording()``. 

This submodule documentation assumes you have read the `introduction <https://pyrend.readthedocs.io/en/latest/index.html>`_ and understand how to create a basic PyRend loop.

Sound Objects
=============

Sound objects are general objects containing everything in PyRend related to sound. They can be created with the ``createsound()`` function.

.. code-block:: python

  mySound = pyrend.sound.createsound(path, volume=1.0)

| **path** (str): The relative or absolute path to your sound file. Read below for supported file types. 
| **volume** (float): The decimal value for the volume to play the sound at. 1.0 is normal.

The `path` parameter fully supports the follow formats: .mp3, .ogg .wav, and .mp4. More sound file types may work, but may not be fully supported for all functions. 

That's right; you can extract audio from an mp4 file to turn into a Sound object.

You can also create a sound object from sound data (NumPy Arrays) and a samplerate. To learn more, read the `soundfile documentation <https://python-soundfile.readthedocs.io/en/>`_

.. code-block:: python

  mySound = pyrend.sound.array(data, samplerate, volume=1.0)

| **data** (ndarray): The array data for the audio.
| **samplerate** (int): The sample rate for the audio.
| **volume** (float): The decimal value for the volume to play the sound at. 1.0 is normal.

Playback
--------

Sound playback can be controlled through a few simple functions. 

.. code-block:: python

  mySound.play(volume=None)

| **volume** (float): Set a temporary volume for the specific playback. 

Plays the sound. The sound is played in a seperate thread meaning it does not interrupt your script.  

.. code-block:: python

  mySound.stop()

Stops all playback of that sound. 

.. code-block:: python

  mySound.wait()

Pauses the script on that function to wait until it has finished playback, if currently playing.

.. code-block:: python

  mySound.get_playback_time() -> float

Returns a float of the current time (seconds) that the sound is into playback, if it is playing.

.. code-block:: python

  mySound.seek(seconds)

Skip to a certain amount of seconds in the video. As of PyRend 0.1.45, it can be used before playback has started to set a point to start at. 

You can combine ``get_playback_time()`` with ``seek()`` and a stored time, to make a rough pause and resume feature. 

Example
~~~~~~~

..code-block:: python

  import pyrend
  
  mySound = pyrend.sound.createsound('sound.mp3', 1.0)    # Create the sound object
  mySound.seek(1)     # Start the playback a second in
  mySound.play()      # Play the sound
  
  def update():
      if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
          pyrend.close()
  
      if pyrend.input.is_key_down("Space"):   # If space is pressed, stop playback
          mySound.stop()
  
  pyrend.start(update)

Audio manipulation
------------------

Though PyRend doesn't support as much audio manipulation as some other libraries, it does have the ability to shift pitch:

.. code-block:: python

  mySound.set_pitch(pitch=0)

**pitch** (float): The number of steps to shift the pitch by. A positive number makes it higher and a negative makes it lower. 

Shifting a sounds pitch takes a while, however it will not pause your script or stop you from playing it when working. While shifting pitch, you can still call ``play()``, however it will still play in normal pitch. When the pitch shift is finished, it will switch audio playback to the pitch shifted version, but resume playback from the same point. 

.. warning:: 

  Pitch shifting large audio files can be intensive on the CPU, so use carefully. 

.. code-block:: python

  mySound.set_volume(volume)

Sets the volume to the specified. You can also just change the `volume` attribute directly to have the same effect.

You can also save a sound object to a .wav file using ``write()``

.. code-block:: python

  mySound.write(path="sound.wav")

**path** (str): The path to save the audio file under. This `must` end in .wav. 

.. note::

  Writing a sound object to a file saves its pitch.
