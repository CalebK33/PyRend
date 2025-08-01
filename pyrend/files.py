"""
files.py
-----------
Control proccesses, resize or alter windows and manage files
"""

import subprocess
import requests
import sys
import threading
import pygetwindow as pgw
from urllib.parse import urlparse
from PIL import Image
import win32gui
import os
import mss

class Window():
    def __init__(self, window):
        self.window = window
        self.title = window.title

    @property
    def isMaximised(self):
        return self.window.isMaximised
    @property
    def width(self):
        return self.window.width
    @property
    def height(self):
        return self.window.height

    def close(self):
        self.window.close()
    def minimize(self):
        self.window.minimize()
    def maximize(self):
        self.window.maximise()
    def restore(self):
        self.window.restore()
    def resize(self, w, h):
        hwnd = self.window._hWnd  
        rect = win32gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        win32gui.MoveWindow(hwnd, x, y, w, h, True)
    def move(self, x, y):
        self.window.moveTo(x, y)

class Screenshot:
    def __init__(self, monitor_index=1):
        self.monitor_index = monitor_index
        self._retake()

    def _retake(self):
        with mss.mss() as sct:
            shot = sct.grab(sct.monitors[self.monitor_index])
        self.raw = shot.rgb
        self.image = Image.frombytes('RGB', shot.size, self.raw)

    def retake(self):
        self._retake()

    def write(self, path):
        self.image.save(path)

    def show(self):
        self.image.show()

    def resize(self, w, h):
        hwnd = self.window._hWnd
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            x, y = rect[:2]
            win32gui.MoveWindow(hwnd, x, y, w, h, True)
        else:
            print(f"PyRend Error: Cannot resize — invalid window handle.")

    def get_bytes(self):
        return self.raw

def _runfile(path):
    ext = path.lower().split('.')[-1]
    
    if ext == "exe":
        subprocess.run([path])
    elif ext == "py":
        subprocess.run([sys.executable, path])
    elif ext == "bat":
        subprocess.run(["cmd.exe", "/c", path])
    elif ext == "sh":
        subprocess.run(["bash", path])
    elif ext == "jar":
        subprocess.run(["java", "-jar", path])
    else:
        print(f"PyRend Error: Unsupported file type .{ext}")

def run(path):
    threading.Thread(target=_runfile, args=(path,)).start()

def window(window):
    if isinstance(window, str):
        matches = pgw.getWindowsWithTitle(window)
        if matches:
            return Window(matches[0])
        else:
            print(f"PyRend Error: Window '{window}' not found.")
            return None
    else:
        return Window(window)

def activeWindow(title=False):
    if title:
        return pgw.getActiveWindowTitle()
    else:
        return pgw.getActiveWindow()
    
def getWindows():
    return pgw.getAllWindows()

def getWindowTitles():
    return pgw.getAllTitles()

def grab_screen():
    return Screenshot(monitor_index=1)

def download(link):
    url = link  
    local_filename = os.path.basename(urlparse(link).path)

    try:
        response = requests.get(url, stream=True)  
        response.raise_for_status()  

        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):  
                f.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")