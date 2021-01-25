import logging
import boto3
from botocore.exceptions import ClientError, ParamValidationError
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
        Given the path to a local file, uploads to s3 using put
        Combines dataset name, version, and file suffix to create s3 key

        Parameters
        ----------
        name: name of data schema as it will appear in s3
        version: version of table as it will appear in s3
        path: local path to the data to upload
        acl: permissions

        """
        suffix = Path(path).suffix
        key = f"{name}/{version}/{name}{suffix}"
        response = self.put(path, key, acl)
        return response

    def put(self, path:str, key:str, acl:str = "public-read") -> dict:
        """
        Uploads local file to s3

        Parameters
        ----------
        path: local path to the data to upload
        key: path to dataset within s3 bucket
        acl: permissions
        """
        try:
            response = self.client.upload_file(
                path, self.bucket, key, ExtraArgs={"ACL": acl}
            )
        except ClientError as e:
            logging.error(e)
            return {}
        return response

    def exists(self, key: str):
        """
        See if a particular key exists within the s3 bucket
        """
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def ls(self, prefix:str, detail:bool = False) -> list:
        """
        List all keys within a directory. If detail, list file info.

        https://s3fs.readthedocs.io/en/latest/api.html?highlight=listdir#s3fs.core.S3FileSystem.info
        """
        response = self.client.list_objects(Bucket=self.bucket, Prefix = prefix)
        if 'Contents' in response.keys():
            contents = response['Contents']
            if detail:
                return contents
            else:
                return [content['Key'] for content in contents]
        else:
            return []

    def info(self, key:str) -> dict:
        """
        Get header info for a given file
        """
        response = self.client.head_object(
                    Bucket=self.bucket,
                    Key=key,
                )
        return response

    def cp(self, source_key:str, dest_key:str, acl: str = "public-read", info:bool = False) -> dict:
        """
        Copy a file to a new path within the same bucket

        Parameters
        ----------
        key: path within the bucket of the file to copy
        dest_ket: new path for the copy
        acl: acl for newly created file
        """
        try:
            response = self.client.copy_object(
                        Bucket=self.bucket,
                        Key=dest_key,
                        CopySource={
                            'Bucket': self.bucket,
                            'Key': source_key
                        },
                        ACL=acl,
                    )
            if info:
                return self.info(key=dest_key)
            return
        except ParamValidationError as e:
            raise ValueError(f"Copy {source_key} -> {dest_key} failed: {e}") from e

    def rm(self, *keys) -> dict:
        """
        Removes a files within the bucket
        sample usage: 
        s3.rm('path/to/file')
        s3.rm('file1', 'file2', 'file3')
        s3.rm(*['file1', 'file2', 'file3'])
        """
        objects = [{'Key':k} for k in keys]
        response = self.client.delete_objects(
                        Bucket=self.bucket,
                        Delete={
                            'Objects': objects,
                            'Quiet': False,
                        }    
                    )
        return response

    def mv(self, source_key:str, dest_key:str, acl: str = "public-read", info:bool = False):
        """
        Move a file to a new path within the same bucket.
        Calls cp then rm

        Parameters
        ----------
        source_key: path within the bucket of the file to move
        dest_ket: new path for the copy
        acl: acl for newly created file
        info: if true, get info for file in its new location
        """
        
        response = self.cp(source_key=source_key, dest_key=dest_key, acl=acl)
        response = self.rm(source_key)
        if info:
            return self.info(key=dest_key)
        return
