import json
from functools import cached_property

from . import aws_access_key_id, aws_s3_bucket, aws_s3_endpoint, aws_secret_access_key
from .s3 import S3


class Dataset:
    def __init__(self, name: str):
        self.s3 = S3(
            aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket
        )
        self.name = name

    @cached_property
    def list_versions(self) -> list:
        prefix = f"datasets/{self.name}/"
        response = self.s3.client.list_objects(
            Bucket=self.s3.bucket, Prefix=prefix, Delimiter="/"
        )
        return [x["Prefix"].split("/")[2] for x in response["CommonPrefixes"]]

    def get_config_by_version(self, version: str) -> str:
        key = f"datasets/{self.name}/{version}/config.json"
        object = self.s3.open(key)
        return json.loads(object["Body"].read())

    @property
    def latest_version(self) -> str:
        config = self.get_config_by_version("latest")
        return config["dataset"]["version"]

    def list_files_by_version(self, version: str) -> list:
        prefix = f"datasets/{self.name}/{version}/"
        files = self.s3.ls(prefix)
        return files

    def create_download_url(self, key) -> str:
        return f"{self.s3.endpoint}/{self.s3.bucket}/{key}"
