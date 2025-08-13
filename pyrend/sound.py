"""
sound.py
-----------
Play sound and record audio from microphone input
"""

import os
import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
import atexit
from moviepy import VideoFileClip

class Recording:
    def __init__(self, time, callback=None, args=(), kwargs=None):
        self.time = time
        self.fs = 44100
        self.callback = callback
        self.callback_args = args
        self.callback_kwargs = kwargs or {}
        
        self._total_frames = int(self.time * self.fs)
        self._frames_recorded = 0
        
        self._buffer = []
        self._lock = threading.Lock()
        
        self._paused = True
        self.finished = threading.Event()
        
        self._stream = sd.InputStream(
            samplerate=self.fs,
            channels=2,
            callback=self._audio_callback
        )
    
    def __repr__(self):
        return f"<Recording time={self.time}s recorded={self._frames_recorded/self.fs:.2f}s>"
    
    def _audio_callback(self, indata, frames, time_info, status):
        if self._paused:
            return
        
        with self._lock:
            frames_to_take = min(frames, self._total_frames - self._frames_recorded)
            if frames_to_take > 0:
                self._buffer.append(indata[:frames_to_take].copy())
                self._frames_recorded += frames_to_take
            
            if self._frames_recorded >= self._total_frames:
                self._stream.stop()
                self._finalize()
    
    def _finalize(self):
        data = np.concatenate(self._buffer, axis=0)
        samplerate = self.fs
        
        self.finished.set()
        
        self.__class__ = Sound
        self.__init__(data=data, samplerate=samplerate)
        
        if self.callback:
            try:
                self.callback(self, *self.callback_args, **self.callback_kwargs)
            except Exception as e:
                print(f"[Callback Error] {e}")
    
    def start(self):
        if self._stream.active:
            self._paused = False
        else:
            self._paused = False
            self._stream.start()
    
    def pause(self):
        self._paused = True
    
    def resume(self):
        if not self._stream.active:
            self._stream.start()
        self._paused = False

class Sound:
    def __init__(self, path=None, volume=1.0, data=None, samplerate=None):
        self.volume = volume
        self.stream = None
        self.thread = None
        self.playing = False
        self.rawpath = path
        self.path = path
        self.current_pitch = 0
        self.original_data = None
        self.original_samplerate = None
        self._pitch_lock = threading.Lock()
        self._current_data = None
        self._next_data = None
        self._pending_pitch = None
        self._current_index = 0
        self._temp_files = []
        self._should_cleanup = True

        if path:
            ext = os.path.splitext(path)[1].lower()
            if ext == ".mp4":
                clip = VideoFileClip(path)
                temp_wav = path + "_temp.wav"
                self.path = temp_wav
                clip.audio.write_audiofile(temp_wav, logger=None)
                clip.close()
                self._temp_files.append(temp_wav)
                path = temp_wav

            self.data, self.samplerate = sf.read(path)
            self.original_data = self.data.copy()
            self.original_samplerate = self.samplerate
            self._current_data = self.original_data

            atexit.register(self._cleanup)

        elif data is not None and samplerate is not None:
            self.data = data
            self.samplerate = samplerate
            self.original_data = self.data.copy()
            self.original_samplerate = self.samplerate
            self._current_data = self.original_data
        else:
            raise AttributeError("Please give either a path or data to a sound object")

    def __repr__(self):
        return f'PyRendSoundObject(path="{self.path}")'

    def _cleanup(self):
        if not self._should_cleanup:
            return
            
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self._temp_files = []

    def _apply_pitch_shift(self, n_steps):
        try:
            if self.original_data.ndim == 1:
                shifted = librosa.effects.pitch_shift(
                    y=self.original_data,
                    sr=self.original_samplerate,
                    n_steps=n_steps
                )
            else:
                left = librosa.effects.pitch_shift(
                    y=self.original_data[:,0],
                    sr=self.original_samplerate,
                    n_steps=n_steps
                )
                right = librosa.effects.pitch_shift(
                    y=self.original_data[:,1],
                    sr=self.original_samplerate,
                    n_steps=n_steps
                )
                shifted = np.column_stack((left, right))
            
            with self._pitch_lock:
                self._next_data = shifted
                self._pending_pitch = n_steps
        except Exception:
            pass

    def set_pitch(self, pitch=0):
        if pitch == self.current_pitch:
            return
            
        threading.Thread(target=self._apply_pitch_shift, args=(pitch,), daemon=True).start()

    def _playback(self, volume=None):
        vol = volume if volume is not None else self.volume
        self.playing = True

        def callback(outdata, frames, time, status):
            if status:
                return

            with self._pitch_lock:
                if self._next_data is not None and self._pending_pitch is not None:
                    current_pos = self._current_index / len(self._current_data)
                    self._current_data = self._next_data
                    self._current_index = int(current_pos * len(self._current_data))
                    self.current_pitch = self._pending_pitch
                    self._next_data = None
                    self._pending_pitch = None

                remaining = len(self._current_data) - self._current_index
                if remaining <= 0:
                    outdata[:] = 0
                    self.playing = False
                    raise sd.CallbackStop()

                frames_available = min(frames, remaining)
                chunk = self._current_data[self._current_index:self._current_index+frames_available] * vol
                outdata[:frames_available] = chunk
                if frames_available < frames:
                    outdata[frames_available:] = 0
                
                self._current_index += frames_available

        self._current_index = 0
        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=1 if self._current_data.ndim == 1 else self._current_data.shape[1],
            callback=callback
        )
        self.stream.start()

        while self.playing and self.stream.active:
            sd.sleep(100)

        if self.stream:
            self.stream.close()
        self.playing = False

    def play(self, volume=None):
        if self.playing:
            self.stop()
        self.thread = threading.Thread(target=self._playback, args=(volume,), daemon=True)
        self.thread.start()

    def stop(self):
        self.playing = False
        if self.stream:
            self.stream.abort()
        if self.thread:
            self.thread.join()

    def get_playback_time(self) -> float:
        if not self.playing:
            return 0
        return self._current_index / self.samplerate
    
    def seek(self, seconds=0):
        new_index = int(seconds * self.samplerate)
        new_index = max(0, min(new_index, len(self._current_data) - 1))  # clamp
        with self._pitch_lock:
            self._current_index = new_index

    def wait(self):
        if self.thread:
            self.thread.join()

    def write(self, path="sound.wav"):
        sf.write(path, self.data, self.samplerate)

    def set_volume(self, volume):
        self.volume = volume

    def __del__(self):
        self._cleanup()

def createsound(path, volume=1.0) -> Sound:
    return Sound(path, volume)

def array(data, samplerate, volume=1.0) -> Sound:
    return Sound(volume=volume, data=data, samplerate=samplerate)

def recording(time, callback=None, args=(), kwargs=None) -> Recording:
    return Recording(time, callback=callback, args=args, kwargs=kwargs)
