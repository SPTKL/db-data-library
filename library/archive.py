import os

from . import (
    aws_access_key_id,
    aws_s3_bucket,
    aws_s3_endpoint,
    aws_secret_access_key,
    base_path,
    pp,
)
from .ingest import Ingestor
from .s3 import S3


class Archive:
    def __init__(self):
        self.ingestor = Ingestor()
        self.s3 = S3(
            aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket
        )

    def __call__(
        self,
        path,
        output_format,
        push: bool = False,
        clean: bool = False,
        latest: bool = False,
        *args,
        **kwargs
    ):
        # Get ingestor by format
        ingestor_of_format = getattr(self.ingestor, output_format)

        # Initiate ingestion
        output_files, version, acl = ingestor_of_format(path, *args, **kwargs)
        print(output_files)

        # Write to s3
        for _file in output_files:
            if push:
                key = _file.replace(base_path + "/", "")
                self.s3.put(_file, key, acl)
            if push and latest:
                self.s3.put(_file, key.replace(version, "latest"), acl)
            if clean:
                os.remove(_file)
