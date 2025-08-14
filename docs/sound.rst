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

.. code-block:: python

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

Recording
=========

The PyRend sound submodule allows you to record audio input from the mic. To do this, you need to create a Recording object.

.. code-block:: python

  myRecording = pyrend.sound.recording(time, callback=None, args=())

| **time** (float): Number of seconds to record audio for.
| **callback** (func): Function to call when the object has finished recording.
| **args** (tuple): Arguments to give to function command when object finishes recording.  

When a recording object has finished recording, it will automatically transform into a sound object. This means you could immediately play it, pitch change it, or write it to a file. Due to this change in object, it could lead to tricky scenarios where your script will crash trying to execute a not yet, or no longer existing method. You could get around this by using pythons `try` statement, or by using the built in `isinstance <https://docs.python.org/3/library/functions.html#isinstance>`_ function like this:

.. code-block:: python

  myRecording = pyrend.sound.recording(3, callback=None, args=())
  myRecording.start()

  while True:
    if isinstance(myRecording, pyrend.sound.Sound):
      print("Recording finished!")

This will be used in a proper loop later in the example.

Methods
-------

Creating a recording will not immediately start it. To start recording audio input, use:

.. code-block:: python

  myRecording.start()

This will start the recording for the duration specified on creation. When playing it does not pause your script/loop. While running you can use:

.. code-block:: python

  myRecording.pause()

...To pause the recording. Then you can use:

.. code-block:: 

  myRecording.resume()

...To resume it. 

Usage
-----

The following script creates a five second recording, starts it and waits until it's finished and plays when the space key is pressed. To read about key presses, take a look at the `input submodule <https://pyrend.readthedocs.io/en/latest/input.html>`_

.. code-block:: python

  import pyrend
  
  myRecording = pyrend.sound.recording(5, callback=None, args=()) 
  myRecording.start()         # Create and start a five second recording
  
  while not isinstance(myRecording, pyrend.sound.Sound):
      pass        # Wait until it has finished
  
  space_pressed = False    # Create global variables to check if keys are pressed
  bracket_pressed = False
  
  def update():
      global alt_q_pressed, space_pressed, bracket_pressed    # Get global variables
  
      if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
          pyrend.close()      # Safety quit keybind
  
      if pyrend.input.is_key_down("SPACE"):
          if not space_pressed: 
              if myRecording.playing:
                  myRecording.stop()  # If space is pressed, stop or play the recording
              else:
                  myRecording.play()
              space_pressed = True    # Set global variable to True to avoid repetitive execution
      else:
          space_pressed = False  
  
      if pyrend.input.is_key_down("["):
          if not bracket_pressed:  
              myRecording.write("sound.wav")  # If left bracket is pressed, write the audio to file.
              bracket_pressed = True
      else:
          bracket_pressed = False  
  
  pyrend.start(update)    # Start the update loop


A lot of this code is clutter as the ``is_key_down`` method will execute every frame. Obviously we do not want the space key to pause or play the audio every frame, so we need to account for this.  

Examples
========

Below are some scripts that combine everything documented in this documentation page.

The following script plays some music, and when the space key is pressed, gently fades it out to a stop:

.. code-block:: python

  import pyrend

  music = pyrend.sound.createsound('music/track1.ogg')
  music.play()    # Create and start music
  playing = True
  
  def update():
      global playing
  
      # Safety quit
      if pyrend.input.is_key_down("ALT") and pyrend.input.is_key_down("Q"):
          pyrend.close()
  
      # Pause trigger
      if playing and pyrend.input.is_key_down("SPACE"):
          playing = False
  
      # Fade out
      if not playing:
          if music.volume > 0:
              music.volume = max(0, music.volume - 0.01)
          else:
              music.stop()

  pyrend.start(update)

This script records five seconds of audio input, then shifts its pitch up three steps and saves it to a file:

.. code-block:: python

  
