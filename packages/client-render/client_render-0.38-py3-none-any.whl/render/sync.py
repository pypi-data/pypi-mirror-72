import hashlib
import logging
import os
import re
import sys
import time
from pathlib import Path
from time import sleep

import win32gui
import win32con

from render import RENDER_DIR

logger = logging.getLogger(__name__)

EXTENSIONS = [
    'cxr',
    'exr',
    'fxr',
    'log',
    'png',
    'jpg',
    'jpeg',
    'jpe',
    'bmp',
    'hdr',
    'pic',
]


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        self._handle = None

    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def foreground(self):
        if self._handle:
            win32gui.SetForegroundWindow(self._handle)

    def maximaze(self):
        if self._handle:
            win32gui.ShowWindow(self._handle, win32con.SW_MAXIMIZE)


def sha256(filename):
    hash_ = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_.update(byte_block)
        return hash_.hexdigest()


def iterate_files():
    for root, dir, files in os.walk(RENDER_DIR):
        for file in files:
            *_, ext = file.rsplit('.', maxsplit=1)
            if ext in EXTENSIONS:
                yield Path(root) / file


def check_files():
    # for file in iterate_files():
    #     hex = sha256(file)
    pass


def main(window):
    # while True:
    #     check_files()
    #     time.sleep(60 * delay)

    w = WindowMgr()
    while True:
        w.find_window_wildcard(window)
        w.foreground()
        w.maximaze()

        sleep(10)  # check each 10 seconds


if __name__ == '__main__':
    main(sys.argv[1])
