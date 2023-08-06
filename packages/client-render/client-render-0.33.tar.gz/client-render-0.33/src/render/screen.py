import logging
import sys
from time import sleep

import pyscreenshot as ImageGrab
import wx
from mss import mss

from render import RENDER_DIR

logger = logging.getLogger(__name__)


def capture_screenshots(tick):
    logger.debug("Screenshots configuring...")
    path = RENDER_DIR / 'screens'
    path.mkdir(exist_ok=True)
    with mss() as sct:
        sct.shot(mon=-1, output=str(path / f'mss-{tick}.png'))

    grab_filename = path / f'grab-screen-{tick}.png'

    im = ImageGrab.grab()
    im.save(str(grab_filename))

    wx_filename = path / f'wx-screen-{tick}.png'
    wx.App()  # Need to create an App instance before doing anything
    screen = wx.ScreenDC()
    size = screen.GetSize()
    bmp = wx.EmptyBitmap(size[0], size[1])
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
    del mem  # Release bitmap
    bmp.SaveFile(str(wx_filename), wx.BITMAP_TYPE_PNG)

    # with Display(size=(100, 60)) as disp:  # start Xvfb display
    #     # display is available
    #     with EasyProcess(["xmessage", "hello"]):  # start xmessage
    #         sleep(1)  # wait for diplaying window
    #         img = ImageGrab.grab()
    # img.save("xmessage.png")


def main():
    delay = int(sys.argv[1])
    tick = 0
    while True:
        capture_screenshots(tick)
        sleep(delay)
        tick += 1


if __name__ == '__main__':
    main()
