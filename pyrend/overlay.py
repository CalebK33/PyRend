"""
overlay.py
-----------
Control on screen overlays without a visible application
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFontDatabase

import ctypes
from ctypes import wintypes
import sys
import math
import os

import cv2
import threading
_videos_lock = threading.Lock()

_app = None
_overlay = None
_loaded_videos = {}
_loaded_fonts = {}

#----
#ITEM CLASSES
#----

class BaseItem:
    def __init__(self, overlay, base_pos=(0, 0), z_index=0):
        self.overlay = overlay
        self.base_pos = base_pos
        self.parent_offset = (0, 0)
        self.offset = (0, 0)
        self.x = self.base_pos[0] + self.parent_offset[0] + self.offset[0]
        self.y = self.base_pos[1] + self.parent_offset[1] + self.offset[1]
        self.abs_pos = (self.x - self.offset[0], self.y - self.offset[1])
        self.z_index = z_index
        self._visible = True
        self._deleted = False
        self._soft_deleted = False
        self.parent = None
        self.children = []
        self.rotation = 0

    @property
    def pos(self):
        ax, ay = self.get_absolute_pos()
        return (ax + self.offset[0], ay + self.offset[1])

    def get_absolute_pos(self) -> tuple:
        if self.parent:
            parent_abs = self.parent.get_absolute_pos()
            angle = self.parent.get_total_rotation()
            rad = math.radians(angle)
            ox, oy = self.parent_offset
            rox = ox * math.cos(rad) - oy * math.sin(rad)
            roy = ox * math.sin(rad) + oy * math.cos(rad)
            return (parent_abs[0] + rox, parent_abs[1] + roy)
        return self.base_pos

    def get_total_rotation(self) -> int:
        if self.parent:
            return self.rotation + self.parent.get_total_rotation()
        return self.rotation

    def hide(self):
        self._visible = False
        for child in self.children:
            child.hide()
        self.overlay.update()

    def show(self):
        self._visible = True
        for child in self.children:
            child.show()
        self.overlay.update()

    def delete(self, soft=False):
        self._soft_deleted = soft
        self._deleted = not soft
        for child in self.children:
            child.delete(soft)
        self.overlay.update()

    def become_child_of(self, parent):
        if self.parent == parent:
            return
        if self.parent:
            self.parent.children.remove(self)
        old_pos = self.pos
        self.parent = parent
        parent.children.append(self)
        self.base_pos = parent.pos
        self.parent_offset = (
            old_pos[0] - self.base_pos[0],
            old_pos[1] - self.base_pos[1]
        )

    def become_parent_of(self, child):
        child.become_child_of(self)

    def free(self, inverse=False):
        if inverse:
            for child in self.children[:]:
                child_abs = child.pos
                child.parent = None
                child.base_pos = child_abs
                self.children.remove(child)
        else:
            if self.parent:
                abs_pos = (self.pos[0] - self.offset[0], self.pos[1] - self.offset[1])
                self.parent.children.remove(self)
                self.base_pos = abs_pos
                self.parent = None
                self.parent_offset = (0, 0)

    def move(self, x, y, change=False):
        self.base_pos = (self.x + x, self.y + y) if change else (x, y)

    def move_offset(self, x, y):
        self.offset = (x, y)

    def rotate(self, degrees, change=True):
        if self.parent is None:
            self.rotation = (self.rotation + degrees) if change else degrees

    def align_center(self, x=True, y=True):
        w, h = self.width(), self.height()
        dx = -w / 2 if x else self.offset[0]
        dy = -h / 2 if y else self.offset[1]
        self.offset = (dx, dy)

    def width(self) -> int:
        if hasattr(self, "size") and self.size:
            return self.size[0] if isinstance(self.size, tuple) else self._text_width()
        return self._text_width() if hasattr(self, "text") else 0

    def height(self) -> int:
        if hasattr(self, "size") and self.size:
            return self.size[1] if isinstance(self.size, tuple) else self._text_height()
        return self._text_height() if hasattr(self, "text") else 0

    def is_mouse_hovering(self) -> bool:
        mx, my = get_mouse_pos()
        px, py = self.pos
        w, h = self.width(), self.height()
        cx, cy = px + w / 2, py + h / 2

        angle = -math.radians(self.get_total_rotation())
        dx, dy = mx - cx, my - cy
        rx = dx * math.cos(angle) - dy * math.sin(angle)
        ry = dx * math.sin(angle) + dy * math.cos(angle)

        lx, ly = rx + w / 2, ry + h / 2
        return 0 <= lx <= w and 0 <= ly <= h

    def is_held(self) -> bool:
        if not self.overlay or not self._visible:
            return False
        if not self.overlay._mouse_down:
            return False

        mx, my = self.overlay._mouse_pos
        px, py = self.pos
        w, h = self.width(), self.height()
        cx, cy = px + w / 2, py + h / 2

        angle = -math.radians(self.get_total_rotation())
        dx, dy = mx - cx, my - cy
        rx = dx * math.cos(angle) - dy * math.sin(angle)
        ry = dx * math.sin(angle) + dy * math.cos(angle)

        lx, ly = rx + w / 2, ry + h / 2
        return 0 <= lx <= w and 0 <= ly <= h

    def get_collision(self, item) -> bool:
        item1 = self
        item2 = item
        if item1._deleted or item2._deleted or not item1._visible or not item2._visible:
            return False

        x1, y1 = item1.pos
        w1, h1 = item1.width(), item1.height()

        x2, y2 = item2.pos
        w2, h2 = item2.width(), item2.height()

        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )

class _TextItem(BaseItem):
    def __init__(self, overlay, text, base_pos=(0, 0), size=48, color=(255, 255, 255), fontname="Arial", z_index=0):
        super().__init__(overlay, base_pos, z_index)
        self.text = str(text)
        self.size = int(size)
        self.color = QtGui.QColor(*color)
        self.fontname = str(fontname)

    def __repr__(self):
        return f'TextItem("{self.text}" at {self.pos})'

    def edit(self, base_pos=None, text=None, size=None, color=None, fontname=None, rotation=None):
        if base_pos is not None and self.parent is None:
            self.base_pos = (float(base_pos[0]), float(base_pos[1]))
        if rotation is not None:
            self.rotation = float(rotation)
        if text is not None:
            self.text = str(text)
        if size is not None:
            self.size = int(size)
        if color is not None:
            self.color = QtGui.QColor(*color)
        if fontname is not None:
            self.fontname = str(fontname)
        self.overlay.update()

    def _text_width(self):
        font = QtGui.QFont(self.fontname, self.size)
        metrics = QtGui.QFontMetrics(font)
        return metrics.horizontalAdvance(self.text)

    def _text_height(self):
        font = QtGui.QFont(self.fontname, self.size)
        metrics = QtGui.QFontMetrics(font)
        return metrics.height()

class _ShapeItem(BaseItem):
    def __init__(self, overlay, iscircle=False, base_pos=(0, 0), size=(100, 100), color=(255, 255, 255), opacity=1.0, radius=0, z_index=0):
        super().__init__(overlay, base_pos, z_index)
        self.iscircle = iscircle
        self.size = size
        self.color = QtGui.QColor(*color)
        self.opacity = float(opacity)
        self.radius = radius

    def __repr__(self):
        return f'ShapeItem("pos={self.pos})'

    def edit(self, base_pos=None, size=None, color=None, opacity=None, radius=None, rotation=None):
        if base_pos is not None and self.parent is None:
            self.base_pos = (float(base_pos[0]), float(base_pos[1]))
        if rotation is not None:
            self.rotation = float(rotation)
        if size is not None:
            self.size = size
        if color is not None:
            self.color = QtGui.QColor(*color)
        if opacity is not None:
            self.opacity = float(opacity)
        if radius is not None:
            self.radius = radius
        self.overlay.update()

class _ImageItem(BaseItem):
    def __init__(self, overlay, path, base_pos=(0, 0), size=None, opacity=1.0, keep_aspect_ratio=True, z_index=0):
        super().__init__(overlay, base_pos, z_index)
        self.path = path
        self.size = size
        self.opacity = float(opacity)
        self.keep_aspect_ratio = keep_aspect_ratio
        self.pixmap = QtGui.QPixmap(path)

    def __repr__(self):
        return f'ImageItem("{self.path}" at {self.pos})'

    def edit(self, path=None, base_pos=None, size=None, opacity=None, keep_aspect_ratio=None, rotation=None):
        if path is not None:
            self.path = path
            self.pixmap = QtGui.QPixmap(path)
        if base_pos is not None and self.parent is None:
            self.base_pos = (float(base_pos[0]), float(base_pos[1]))
        if rotation is not None:
            self.rotation = float(rotation)
        if size is not None:
            self.size = size
        if opacity is not None:
            self.opacity = float(opacity)
        if keep_aspect_ratio is not None:
            self.keep_aspect_ratio = keep_aspect_ratio
        self.overlay.update()

class _VideoItem(BaseItem):
    def __init__(self, overlay, video_data_or_path, base_pos=(0,0), size=None, opacity=1.0, on_end=None, on_end_args=(), z_index=0, keep_aspect_ratio=True, loop = True, smooth=False):
        super().__init__(overlay, base_pos, z_index)
        self.size = size
        self.smooth = smooth
        self.keep_aspect_ratio = keep_aspect_ratio
        self.paused = None
        self.opacity = float(opacity)
        self.on_end = on_end
        self.loop = loop
        self.on_end_args = on_end_args
        self.frame_index = 0
        self.path = video_data_or_path
        self._elapsed = QtCore.QElapsedTimer()
        self._elapsed.start()
        self.last_frame_time = 0
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._check_and_advance_frame)
        self._timer.start(1)
        self._loading = False

        if isinstance(video_data_or_path, str):
            if video_data_or_path in _loaded_videos and _loaded_videos[video_data_or_path] is not None:
                self.frames = _loaded_videos[video_data_or_path]['frames']
                self.frame_interval = _loaded_videos[video_data_or_path]['interval']
                self._done = _loaded_videos[video_data_or_path].get('done', True)
                self._loading = not self._done
            else:
                frames = []
                _loaded_videos[video_data_or_path] = {'frames': frames, 'interval': 33, 'done': False}
                self.frames = frames
                self.frame_interval = 33  
                self._loading = True
                self._done = False
                def load_and_update():
                    cap = cv2.VideoCapture(video_data_or_path)
                    if not cap.isOpened():
                        _loaded_videos[video_data_or_path] = None
                        return
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    if not fps or fps <= 1:
                        fps = 30
                    interval = int(1000 / fps)
                    _loaded_videos[video_data_or_path]['interval'] = interval
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                        h, w, _ = frame.shape
                        qimage = QtGui.QImage(frame.data, w, h, QtGui.QImage.Format_RGBA8888).copy()
                        frames.append(qimage)
                    cap.release()
                    _loaded_videos[video_data_or_path]['done'] = True
                    self._done = True
                    self._loading = False
                threading.Thread(target=load_and_update, daemon=True).start()
        else:
            self.frames = video_data_or_path[0]
            self.frame_interval = video_data_or_path[1]
            self._done = True
            self._loading = False

    def __repr__(self):
        return f'VideoItem("{self.path}" at {self.pos})'

    def _check_and_advance_frame(self):
        if getattr(self, "paused", False):
            return
        if not self.frames:
            return

        now = self._elapsed.elapsed()

        if not self.smooth:
            target_index = now // self.frame_interval
            if target_index >= len(self.frames):
                if self._loading or not self._done:
                    target_index = len(self.frames) - 1
                else:
                    self._elapsed.restart()
                    target_index %= len(self.frames)
                    if self.on_end:
                        self.on_end(*self.on_end_args)
            if target_index != self.frame_index:
                self.frame_index = int(target_index)
                self.overlay.update()

        else:
            if now - self.last_frame_time >= self.frame_interval:
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    if self._loading or not self._done:
                        self.frame_index = len(self.frames) - 1
                    else:
                        self.frame_index = 0
                        if self.on_end:
                            self.on_end(*self.on_end_args)
                self.last_frame_time = now
                self.overlay.update()

    def current_frame(self) -> int:
        if not self.frames:
            return None
        if self.frame_index >= len(self.frames):
            return None
        return self.frames[self.frame_index]
    
    def pause(self):
        self.paused = True

    def play(self):
        self.paused = False

    def seek(self, seconds):
        if not getattr(self, 'frames', None) or not hasattr(self, 'frame_interval'):
            return

        ms = int(seconds * 1000)
        idx = ms // self.frame_interval
        idx = max(0, min(idx, len(self.frames) - 1))
        self.frame_index = idx

        self._seek_offset = idx * self.frame_interval
        self._elapsed.restart()
        self.overlay.update()


    def edit(self, base_pos=None, size=None, opacity=None, rotation=None, loop=None, on_end=None, on_end_args=None):
        if base_pos is not None and self.parent is None:
            self.base_pos = (float(base_pos[0]), float(base_pos[1]))
        if size is not None:
            self.size = size
        if opacity is not None:
            self.opacity = float(opacity)
        if rotation is not None:
            self.rotation = float(rotation)
        if loop is not None:
            self.loop = loop
        if on_end is not None:
            self.on_end = on_end
        if on_end_args is not None:
            self.on_end_args = on_end_args
        self.overlay.update()

class _PointItem(BaseItem):
    def __init__(self, overlay, base_pos):
        super().__init__(overlay, base_pos)

    def __repr__(self):
        return f'PointItem("pos={self.pos})'

    def edit(self, base_pos=None, rotation=None):
        if base_pos is not None and self.parent is None:
            self.base_pos = (float(base_pos[0]), float(base_pos[1]))
        if rotation is not None:
            self.rotation = float(rotation)

#----
#OVERLEY CLASS
#----

class Overlay(QtWidgets.QWidget):
    def __init__(self, ghost=True):
        super().__init__()

        self.taskbaroverlay = False
        self._mouse_pos = (0, 0)
        self._mouse_down = False
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, ghost)

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool |
            QtCore.Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setWindowTitle("PyRend Overlay")

        module_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(module_dir, 'icon.ico')
        icon = QtGui.QIcon(icon_path)
        _app.setWindowIcon(icon)

        if self.taskbaroverlay:
            screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        else:
            screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_geometry)

        if ghost:
            self._make_clickthrough()

        self._items = []
        self.show()
        self._start_autoloop()

        hwnd = int(self.winId())
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x80000
        WS_EX_TRANSPARENT = 0x20
        WS_EX_TOPMOST = 0x00000008

        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)

        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOACTIVATE = 0x0010

        ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                          SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)

    def __repr__(self):
        return f"PyRendOverlayObject()"

    def _make_clickthrough(self):
        hwnd = int(self.winId())
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x80000
        WS_EX_TRANSPARENT = 0x20

        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)

    def write(self, text, base_pos=(0, 0), size=48, color=(255, 255, 255), font="Arial", z_index=0):
        item = _TextItem(self, text, base_pos, size, color, font, z_index)
        self._items.append(item)
        self.update()
        return item

    def shape(self, iscircle=False, base_pos=(0, 0), size=(100, 100), color=(255, 255, 255), opacity=1.0, radius=0, z_index=0):
        item = _ShapeItem(self, iscircle, base_pos, size, color, opacity, radius, z_index)
        self._items.append(item)
        self.update()
        return item

    def image(self, path, base_pos=(0, 0), size=None, opacity=1.0, keep_aspect_ratio=True, z_index=0):
        item = _ImageItem(self, path, base_pos, size, opacity, keep_aspect_ratio, z_index)
        self._items.append(item)
        self.update()
        return item

    def point(self, base_pos):
        item = _PointItem(self, base_pos)
        self._items.append(item)
        self.update()
        return item

    def video(self, video_data_or_path, *args, **kwargs):
        item = _VideoItem(self, video_data_or_path, *args, **kwargs)
        self._items.append(item)
        self.update()
        return item

    def hide(self):
        super().hide()

    def show(self):
        super().show()

    def close(self):
        self.hide()
        self.deleteLater()

    def mousePressEvent(self, event):
        self._mouse_down = True
        self._mouse_pos = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self._mouse_down = False
        self._mouse_pos = (event.x(), event.y())

    def mouseMoveEvent(self, event):
        self._mouse_pos = (event.x(), event.y())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        visibles = [i for i in self._items if hasattr(i, 'z_index')]

        for item in sorted(visibles, key=lambda x: x.z_index):
            if item._deleted or item._soft_deleted or not item._visible:
                continue

            px, py = item.pos
            cx, cy = item.get_absolute_pos() 
            angle = item.get_total_rotation()

            if isinstance(item, _TextItem):
                painter.save()
                font = QtGui.QFont(item.fontname, item.size)
                painter.setFont(font)
                painter.setPen(item.color)
                painter.translate(cx, cy)
                painter.rotate(angle)
                painter.translate(-cx, -cy)
                painter.drawText(int(px), int(py), item.text)
                painter.restore()

            elif isinstance(item, _ShapeItem):
                painter.save()
                painter.setOpacity(item.opacity)
                painter.setBrush(item.color)
                painter.setPen(QtCore.Qt.NoPen)
                painter.translate(cx, cy)
                painter.rotate(angle)
                painter.translate(-cx, -cy)
                if item.iscircle:
                    painter.drawEllipse(int(px), int(py), int(item.size[0]), int(item.size[1]))
                else:
                    path = QtGui.QPainterPath()
                    path.addRoundedRect(QtCore.QRectF(px, py, item.size[0], item.size[1]), item.radius, item.radius)
                    painter.drawPath(path)
                painter.restore()

            elif isinstance(item, _ImageItem):
                painter.save()
                painter.setOpacity(item.opacity)
                img = item.pixmap
                if item.size:
                    mode = QtCore.Qt.KeepAspectRatio if item.keep_aspect_ratio else QtCore.Qt.IgnoreAspectRatio
                    img = img.scaled(item.size[0], item.size[1], mode, QtCore.Qt.SmoothTransformation)
                painter.translate(cx, cy)
                painter.rotate(angle)
                painter.translate(-cx, -cy)
                painter.drawPixmap(int(px), int(py), img)
                painter.restore()

            elif isinstance(item, _VideoItem):
                frame = item.current_frame()
                if frame:
                    painter.save()
                    painter.setOpacity(item.opacity)
                    if item.size:
                        mode = QtCore.Qt.KeepAspectRatio if item.keep_aspect_ratio else QtCore.Qt.IgnoreAspectRatio
                        frame = frame.scaled(item.size[0], item.size[1], mode, QtCore.Qt.SmoothTransformation)
                    painter.translate(cx, cy)
                    painter.rotate(angle)
                    painter.translate(-cx, -cy)
                    painter.drawImage(int(px), int(py), frame)
                    painter.restore()

            elif isinstance(item, _PointItem):
                pass

    def _start_autoloop(self, interval=16):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self._safe_update_call)
        timer.start(interval)

    def _safe_update_call(self):
        if hasattr(self, "update_loop") and callable(self.update_loop):
            self.update_loop()
        self.update()

    def screen_width(self) -> int:
        return self.geometry().width()

    def screen_height(self) -> int:
        return self.geometry().height()

    def set_overlay_taskbar(self, enable=True):
        self.taskbaroverlay = enable

#----
#CALCULATION FUNCTIONS
#----

def _background_load_video(path):
    if path in _loaded_videos:
        return
    frames = []
    with _videos_lock:
        _loaded_videos[path] = {'frames': frames, 'interval': 33, 'done': False}
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        _loaded_videos[path] = None
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 1:
        fps = 30
    interval = int(1000 / fps)
    with _videos_lock:
        _loaded_videos[path]['interval'] = interval
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        h, w, _ = frame.shape
        qimage = QtGui.QImage(frame.data, w, h, QtGui.QImage.Format_RGBA8888).copy()
        frames.append(qimage)
    cap.release()
    with _videos_lock:
        _loaded_videos[path]['done'] = True

def _ensure_overlay(ghost=True) -> Overlay:
    global _app, _overlay
    if _app is None:
        _app = QtWidgets.QApplication(sys.argv)
        _app.setQuitOnLastWindowClosed(True)
        _app.setApplicationName("PyRend Overlay")
        module_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(module_dir, 'icon.ico')
        icon = QtGui.QIcon(icon_path)
        _app.setWindowIcon(icon)

        import signal
        signal.signal(signal.SIGINT, lambda *args: QtWidgets.QApplication.quit())

    if _overlay is None:
        _overlay = Overlay(ghost)
    return _overlay

def screen_size() -> tuple:
    return tuple([_overlay.screen_width(), _overlay.screen_height()])

def get_mouse_pos() -> tuple:
    pt = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

#----
#PUBLIC API
#----

def init():
    _ensure_overlay(True)

def write(text, pos=(0, 0), size=48, color=(255, 255, 255), font="Arial", z_index=0):
    return _ensure_overlay().write(text, pos, size, color, font, z_index)

def shape(iscircle=False, pos=(0, 0), size=(100, 100), color=(255, 255, 255), opacity=1.0, radius=0, z_index=0):
    return _ensure_overlay().shape(iscircle, pos, size, color, opacity, radius, z_index)

def image(path, pos=(0, 0), size=None, opacity=1.0, keep_aspect_ratio=True, z_index=0):
    return _ensure_overlay().image(path, pos, size, opacity, keep_aspect_ratio, z_index)

def video(video_data_or_path, base_pos=(0, 0), size=None, opacity=1.0, on_end=None, on_end_args=(), z_index=0, keep_aspect_ratio=True, smooth=False):
    return _ensure_overlay().video(video_data_or_path, base_pos, size, opacity, on_end, on_end_args, z_index, keep_aspect_ratio, smooth)

def load_video(path):
    if path not in _loaded_videos:
        thread = threading.Thread(target=_background_load_video, args=(path,), daemon=True)
        thread.start()
    return path

def point(base_pos):
    p = _ensure_overlay().point(base_pos)
    del p.z_index
    return p

def start(update_loop=None):
    global _app, _overlay
    _ensure_overlay()
    if update_loop:
        _overlay.update_loop = update_loop
    _app.exec_()

def close():
    global _app, _overlay
    if _overlay:
        _overlay.close()
        _overlay = None
    if _app:
        _app.quit()
        _app = None

def set_clickthrough(enable=True):
    hwnd = int(_overlay.winId())
    GWL_EXSTYLE = -20
    WS_EX_TRANSPARENT = 0x20

    style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)

    if enable:
        style |= WS_EX_TRANSPARENT
    else:
        style &= ~WS_EX_TRANSPARENT

    ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style) 

def load_font(path):
    if path in _loaded_fonts:
        return _loaded_fonts[path]
    font_id = QFontDatabase.addApplicationFont(path)
    if font_id == -1:
        raise ValueError(f"Failed to load font: {path}")
    family = QFontDatabase.applicationFontFamilies(font_id)[0]
    _loaded_fonts[path] = family
    return family
