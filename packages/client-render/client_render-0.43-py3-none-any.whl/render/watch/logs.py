import glob
import itertools
import logging
import os
from pathlib import PurePosixPath

from render import RENDER_DIR
from render.s3 import S3
from render.util import user_data

logger = logging.getLogger(__name__)


def collect_instance_logs(client: S3):
    logger.debug("Collecting log files...")
    for file in itertools.chain(
            # additional logs could be appended here
            glob.glob(str(RENDER_DIR / '*.log'), recursive=True),
    ):
        logger.debug(f"Found log {file}")
        client.upload_file(
            PurePosixPath(user_data['instance_s3_key']) / 'logs' / os.path.basename(
                file),
            file
        )
