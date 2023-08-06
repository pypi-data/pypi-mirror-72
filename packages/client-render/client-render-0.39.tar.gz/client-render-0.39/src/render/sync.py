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
import win32com.client

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
        self.handle = None
        self.shell = win32com.client.Dispatch("WScript.Shell")

    def find_window(self, class_name, window_name=None):
        self.handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self.handle = hwnd

    def find_window_wildcard(self, wildcard):
        self.handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def foreground(self):
        if self.handle is not None:
            win32gui.SetForegroundWindow(self.handle)

    def maximaze(self):
        if self.handle is not None:
            self.shell.SendKeys('%')
            win32gui.ShowWindow(self.handle, win32con.SW_MAXIMIZE)


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

        sleep(5)  # check each 5 seconds


if __name__ == '__main__':
    main(sys.argv[1])
