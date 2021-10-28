import boto3

from . import aws_access_key_id, aws_s3_bucket, aws_s3_endpoint, aws_secret_access_key


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
        self.endpoint = aws_s3_endpoint
        self.bucket = aws_s3_bucket

    def exists(self, key: str):
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def ls(self, prefix: str, detail: bool = False) -> list:
        response = self.client.list_objects(Bucket=self.bucket, Prefix=prefix)
        if "Contents" in response.keys():
            contents = response["Contents"]
            if detail:
                return contents
            else:
                return [content["Key"] for content in contents]
        else:
            return []

    def info(self, key: str) -> dict:
        """
        Get header info for a given file
        """
        response = self.client.head_object(Bucket=self.bucket, Key=key)
        # Set custom metadata keys to lowercase for compatibility with both
        # DigitalOcean and minio standards
        meta_lower = {k.lower(): v for k, v in response.get("Metadata").items()}
        response.update({"Metadata": meta_lower})
        return response

    def open(self, key: str) -> dict:
        """
        opening a file
        """
        object = self.client.get_object(Bucket=self.bucket, Key=key)
        return object
