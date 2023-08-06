import logging
import time
from argparse import ArgumentParser
from functools import partial

from render.watch.logs import collect_instance_logs
from render.watch.screen import capture_screenshot
from render.watch.window import WindowMgr

from render import LOG_DIR
from render.logger import configure_logger
from render.s3 import AWS_S3

logger = logging.getLogger(__name__)


def main(args):
    configure_logger(LOG_DIR / 'watch.log')

    s3 = AWS_S3()
    w = WindowMgr()
    functions = [
        partial(w.find_window_wildcard, args.window_name),
        w.foreground,
        w.maximaze,
        partial(capture_screenshot, s3),
        partial(collect_instance_logs, s3)
    ]
    while True:
        for func in functions:
            func()

        logger.debug(f"Waiting {args.delay} seconds")
        time.sleep(args.delay)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("window_name")
    parser.add_argument("--delay", type=int, default=60)
    main(parser.parse_args())
