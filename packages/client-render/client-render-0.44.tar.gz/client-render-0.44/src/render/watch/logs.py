import glob
import itertools
import logging
import os
from pathlib import PurePosixPath, Path

from render import RENDER_DIR, LOG_DIR
from render.s3 import S3
from render.util import user_data

logger = logging.getLogger(__name__)


def collect_instance_logs(client: S3):
    logger.debug("Collecting log files...")
    for path in itertools.chain(
            # additional logs could be appended here
            glob.glob(str(RENDER_DIR / '**' / '*.log')),
    ):
        file = Path(path)
        logger.debug(f"Found log {file}")
        try:
            file.relative_to(LOG_DIR)
        except ValueError:
            filename = f"{file.parent.name}/{file.name}"
        else:
            filename = file.name

        client.upload_file(
            PurePosixPath(user_data['instance_s3_key']) / 'logs' / filename,
            file
        )
