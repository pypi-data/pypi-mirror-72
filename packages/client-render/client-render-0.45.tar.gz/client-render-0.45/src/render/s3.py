from pathlib import PurePath, Path

import boto3
from boto3.s3.transfer import TransferConfig, MB

from render.util import user_data


class S3:
    DEFAULT_CONTENT_TYPE = 'application/binary'
    EXT_TO_CONTENT_TYPE = {
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.txt': 'text/plain',
        '.log': 'text/plain',
    }

    def __init__(self, bucket, *args, **kwargs):
        self.bucket = bucket
        self.client = boto3.client('s3', *args, **kwargs)

    def upload_file(self, path: PurePath, filename: Path):
        key = str(path)
        config = TransferConfig(
            multipart_threshold=25 * MB,
            multipart_chunksize=25 * MB,
        )

        self.client.upload_file(
            Filename=str(filename),
            Bucket=self.bucket,
            Key=key,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': self.EXT_TO_CONTENT_TYPE.get(
                    path.suffix,
                    self.DEFAULT_CONTENT_TYPE
                )
            },
            Config=config,
        )

    def download_file(self, path: PurePath, dest: Path):
        dest.parent.mkdir(exist_ok=True)
        self.client.download_file(self.bucket, str(path), str(dest))


class AWS_S3(S3):
    def __init__(self):
        super().__init__(
            user_data['aws_bucket'],
            aws_access_key_id=user_data['aws_access_key_id'],
            aws_secret_access_key=user_data['aws_secret_access_key'],
            endpoint_url=user_data['aws_endpoint'],
        )
