import re

import win32com.client
import win32con
import win32gui


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
