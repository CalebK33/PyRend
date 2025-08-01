# PyRend

**PyRend** is a Python library for rendering invisible overlays on top of the desktop. It allows you to draw shapes, images, video, and text over any running application, including windowed or borderless windowed games, without showing a visible window or stealing focus.

It also includes support for playing and recording audio, handling video playback, and capturing/controlling keyboard input. PyRend is designed for scenarios where you want full control over what is drawn on screen, without creating a traditional GUI application, plus many more features.

---

## Features

- Draw shapes (rectangles, circles, lines) and text over the screen
- Render images and video into the overlay
- Invisible overlay window that is always on top and does not appear in the taskbar or alt-tab list
- Keyboard input handling (e.g., listen for keypresses globally)
- Control keyboard and mouse input via simple functions
- Play and record sound
- Works in borderless windowed mode across most applications

---

## Installation

```bash
pip install pyrend
