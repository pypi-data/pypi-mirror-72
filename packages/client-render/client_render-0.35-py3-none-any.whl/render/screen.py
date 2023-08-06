import logging
import sys
from time import sleep

from mss import mss

from render import RENDER_DIR

logger = logging.getLogger(__name__)


def capture_screenshots(tick):
    logger.debug("Screenshots configuring...")
    path = RENDER_DIR / 'screens'
    path.mkdir(exist_ok=True)
    with mss() as sct:
        sct.shot(mon=-1, output=str(path / f'mss-{tick}.png'))


def main():
    delay = int(sys.argv[1])
    tick = 0
    while True:
        capture_screenshots(tick)
        sleep(delay)
        tick += 1


if __name__ == '__main__':
    main()
