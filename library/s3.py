import logging
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from .progressbar import ProgressPercentage
from . import pp

class S3:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_s3_endpoint: str,
        aws_s3_bucket: str,
    ):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=aws_s3_endpoint,
        )
        self.bucket = aws_s3_bucket

    def upload_file(self, name: str, version: str, path: str, acl: str = "public-read"):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        """
        suffix = Path(path).suffix
        key = f"{name}/{version}/{name}{suffix}"
        try:
            response = self.client.upload_file(
                path,
                self.bucket,
                key,
                ExtraArgs={"ACL": acl}
            )
        except ClientError as e:
            logging.error(e)
            return {}
        return response

    def exists(self, key:str):
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def ls(self, prefix:str, detail:bool = False) -> list:
        response = self.client.list_objects(Bucket=self.bucket, Prefix = prefix)
        contents = response['Contents']
        if detail:
            return contents
        else:
            return [content['Key'] for content in contents]

    # https://s3fs.readthedocs.io/en/latest/api.html?highlight=listdir#s3fs.core.S3FileSystem.info