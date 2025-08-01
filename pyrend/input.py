"""
input.py
-----------
Manage keyboard and mouse input and run keybinds or macros.
"""

import ctypes
from ctypes import wintypes

#----
#WINTYPES BINDINGS
#----

user32 = ctypes.WinDLL('user32')
shell32 = ctypes.WinDLL('shell32')

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008
MAPVK_VK_TO_VSC = 0

HWND = wintypes.HWND
UINT = wintypes.UINT
BOOL = wintypes.BOOL
LPARAM = wintypes.LPARAM
ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [
            ("mi", MOUSEINPUT),
            ("ki", KEYBDINPUT),
            ("hi", HARDWAREINPUT)
        ]
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_input", _INPUT)
    ]

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (UINT, LPINPUT, ctypes.c_int)

#----
#KEY CODE BINDINGS
#----

VK_HEX_CODES = {
    'LBUTTON': 0x01,
    'RBUTTON': 0x02,
    'MBUTTON': 0x04,
    
    'BACK': 0x08,
    'TAB': 0x09,
    'ENTER': 0x0D,
    'SHIFT': 0x10,
    'CTRL': 0x11, 'CONTROL': 0x11,
    'ALT': 0x12,
    'PAUSE': 0x13,
    'CAPSLOCK': 0x14,
    'ESC': 0x1B,
    'SPACE': 0x20, ' ': 0x20,
    'DELETE': 0x2E,
    
    'PAGEUP': 0x21,
    'PAGEDOWN': 0x22,
    'END': 0x23,
    'HOME': 0x24,
    'LEFT': 0x25,
    'UP': 0x26,
    'RIGHT': 0x27,
    'DOWN': 0x28,
    
    'A': 0x41,
    'B': 0x42,
    'C': 0x43,
    'D': 0x44,
    'E': 0x45,
    'F': 0x46,
    'G': 0x47,
    'H': 0x48,
    'I': 0x49,
    'J': 0x4A,
    'K': 0x4B,
    'L': 0x4C,
    'M': 0x4D,
    'N': 0x4E,
    'O': 0x4F,
    'P': 0x50,
    'Q': 0x51,
    'R': 0x52,
    'S': 0x53,
    'T': 0x54,
    'U': 0x55,
    'V': 0x56,
    'W': 0x57,
    'X': 0x58,
    'Y': 0x59,
    'Z': 0x5A,
    
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    
    'NUMPAD0': 0x60,
    'NUMPAD1': 0x61,
    'NUMPAD2': 0x62,
    'NUMPAD3': 0x63,
    'NUMPAD4': 0x64,
    'NUMPAD5': 0x65,
    'NUMPAD6': 0x66,
    'NUMPAD7': 0x67,
    'NUMPAD8': 0x68,
    'NUMPAD9': 0x69,
    
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    
    'PLUS': 0xBB, '=': 0xBB,
    'MINUS': 0xBD, '-': 0xBD,
    'COMMA': 0xBC, ',': 0xBC,
    'PERIOD': 0xBE, '.': 0xBE,
    'SLASH': 0xBF, '/': 0xBF,
    'TILDE': 0xC0, '~': 0xC0,
    'OPENBRACKET': 0xDB, '[': 0xDB,
    'BACKSLASH': 0xDC,
    'CLOSEBRACKET': 0xDD, ']': 0xDD,
    'QUOTE': 0xDE, "'": 0xDE,
    'SEMICOLON': 0xBA, ';': 0xBA,

    'VOLUME_MUTE': 0xAD,
    'VOLUME_DOWN': 0xAE,
    'VOLUME_UP': 0xAF,
    'MEDIA_NEXT': 0xB0,
    'MEDIA_PREV': 0xB1,
    'MEDIA_STOP': 0xB2,
    'MEDIA_PLAY_PAUSE': 0xB3,
    
    'LWIN': 0x5B,
    'RWIN': 0x5C,
    'APPS': 0x5D,
    
    'BROWSER_BACK': 0xA6,
    'BROWSER_FORWARD': 0xA7,
    'BROWSER_REFRESH': 0xA8,
    'BROWSER_STOP': 0xA9,
    'BROWSER_SEARCH': 0xAA,
    'BROWSER_FAVORITES': 0xAB,
    'BROWSER_HOME': 0xAC,
}

SHIFT_REPLACEMENTS = {
    ":": ";",
    "?": "/",
    '"': "'",
    "<": ",",
    ">": ".",
    "{": "[",
    "}": "]",
    "+": "=",
    "_": "-",
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "~": "`"
}

#----
#API FUNCTIONS
#----

# Mouse actions

def hide_cursor():
    while user32.ShowCursor(False) >= 0: pass

def show_cursor():
    while user32.ShowCursor(True) < 0: pass

def move_mouse(x, y):
    user32.SetCursorPos(x, y)

def click(): 
    user32.mouse_event(0x0002, 0, 0, 0, 0)  
    user32.mouse_event(0x0004, 0, 0, 0, 0)

# Key actions

def press(key):
    hold(key)
    release(key)

def hold(key):
    key_code = VK_HEX_CODES[key.upper()] if isinstance(key, str) else key
    kb_input = KEYBDINPUT(
        wVk=key_code,
        dwFlags=0,  
        dwExtraInfo=0
    )
    x = INPUT(type=INPUT_KEYBOARD, ki=kb_input)
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def release(key):
    key_code = VK_HEX_CODES[key.upper()] if isinstance(key, str) else key
    kb_input = KEYBDINPUT(
        wVk=key_code,
        dwFlags=KEYEVENTF_KEYUP,  # Key up flag
        dwExtraInfo=0
    )
    x = INPUT(type=INPUT_KEYBOARD, ki=kb_input)
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def write(text):
    for l in text:
        if l.isalpha():
            if l.upper() == l:
                hold('SHIFT')
                press(l.upper())
                release('SHIFT')
            else:
                press(l.upper())
        elif not l in SHIFT_REPLACEMENTS:
            press(l)
        else:
            hold('SHIFT')
            press(SHIFT_REPLACEMENTS.get(l))
            release('SHIFT')
    release('SHIFT')

def command(key, control=True, shift=False, windows=False, alt=False):
    if control: hold('CTRL')
    if shift: hold('SHIFT')
    if windows: hold('LWIN')
    if alt: hold('ALT')
    press(key)
    if control: release('CTRL')
    if shift: release('SHIFT')
    if windows: release('LWIN')
    if alt: release('ALT')

def is_key_down(key):
    key_code = VK_HEX_CODES[key.upper()] if isinstance(key, str) else key
    return ctypes.windll.user32.GetAsyncKeyState(key_code) & 0x8000 != 0

# Window management

def lock():
    try:
        success = ctypes.windll.user32.LockWorkStation()
        if not success:
            raise ctypes.WinError()
        return True
    except Exception as e:
        print(f"Lock failed: {e}")
        return False

def minimize_windows():
    user32.keybd_event(0x5B, 0, 0, 0) 
    user32.keybd_event(0x44, 0, 0, 0) 
    user32.keybd_event(0x44, 0, 2, 0) 
    user32.keybd_event(0x5B, 0, 2, 0) 

def close_foreground():
    user32.keybd_event(0x12, 0, 0, 0)  
    user32.keybd_event(0x73, 0, 0, 0)  
    user32.keybd_event(0x73, 0, 2, 0)  
    user32.keybd_event(0x12, 0, 2, 0) 
