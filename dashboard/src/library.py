from functools import cached_property

from . import aws_access_key_id, aws_s3_bucket, aws_s3_endpoint, aws_secret_access_key
from .s3 import S3


class Library:
    def __init__(self):
        self.s3 = S3(
            aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket
        )

    @cached_property
    def datasets(self) -> list:
        prefix = "datasets/"
        response = self.s3.client.list_objects(
            Bucket=self.s3.bucket, Prefix=prefix, Delimiter="/"
        )
        return [x["Prefix"].split("/")[1] for x in response["CommonPrefixes"]]
