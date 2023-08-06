import logging
from datetime import datetime
from pathlib import PurePosixPath

from mss import mss

from render import SCREENSHOT_DIR
from render.s3 import S3
from render.util import user_data

logger = logging.getLogger(__name__)


def capture_screenshot(client: S3):
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    ts = round(datetime.utcnow().timestamp())
    file = SCREENSHOT_DIR / f'shot-{ts}.png'
    logger.debug(f"Capturing screen {file.name}")
    with mss() as sct:
        sct.shot(mon=-1, output=str(file))

    client.upload_file(
        PurePosixPath(user_data['instance_s3_key']) / 'screens' / file.name,
        file
    )
    logger.debug(f"Screen {file.name} was uploaded")
